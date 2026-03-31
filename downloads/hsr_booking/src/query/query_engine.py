"""
高鐵班次查詢引擎
使用 TDX API 獲取班次資訊
"""
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from dataclasses import dataclass

from ..config import HSR_STATIONS, EARLY_BIRD_DISCOUNT


@dataclass
class TrainSchedule:
    """班次資訊"""
    train_no: str
    departure_station: str
    arrival_station: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    early_bird_discount: Optional[int] = None
    available_seats: int = 0


class QueryEngine:
    """查詢引擎"""
    
    def __init__(self, TDX_API_KEY: str = ""):
        self.TDX_API_KEY = TDX_API_KEY
        self.base_url = "https://ptx.transportdata.tw/MOTC/v2"
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.TDX_API_KEY:
            headers["Authorization"] = f"Bearer {self.TDX_API_KEY}"
        return headers
    
    def calculate_presale_date(self, travel_date: datetime) -> datetime:
        """
        計算預售開放日期
        一般日：乘車日前 29 天（含當日）凌晨 00:00
        週末延長：週五/週六可預訂至四週後之週日
        """
        # 判斷是否為週末
        weekday = travel_date.weekday()  # 0=週一, 5=週六, 6=週日
        
        if weekday == 4:  # 週五
            # 可預訂至四週後的週日
            days_ahead = 28
        elif weekday == 5:  # 週六
            # 可預訂至四週後的週日
            days_ahead = 27
        else:
            days_ahead = 29
        
        presale_date = travel_date - timedelta(days=days_ahead)
        return presale_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def is_presale_open(self, travel_date: datetime) -> bool:
        """檢查是否開放預售"""
        presale_date = self.calculate_presale_date(travel_date)
        now = datetime.now()
        return now >= presale_date
    
    def get_payment_deadline(self, booking_date: datetime, travel_date: datetime) -> datetime:
        """
        計算付款期限
        - 發車日 > 訂位日 + 3天：訂位日起 3 日內
        - 發車日 <= 訂位日 + 3天：乘車日前 1 日
        - 當日班次 (>1小時)：發車前 30 分鐘
        - 當日班次 (<1小時)：立即付款
        """
        days_diff = (travel_date - booking_date).days
        
        if days_diff > 3:
            # 3天前訂票，3天內付款
            return booking_date + timedelta(days=3)
        elif days_diff > 0:
            # 3天內訂票，乘車日前1天
            return travel_date - timedelta(days=1)
        else:
            # 當日訂票
            return travel_date - timedelta(minutes=30)
    
    async def query_trains(
        self,
        origin: str,
        destination: str,
        date: datetime,
        early_bird_filter: Optional[int] = None,
    ) -> List[TrainSchedule]:
        """
        查詢班次
        這是模擬實現，實際需要對接 TDX API 或高鐵私有 API
        """
        # 驗證站點
        if origin not in HSR_STATIONS:
            raise ValueError(f"Invalid origin station: {origin}")
        if destination not in HSR_STATIONS:
            raise ValueError(f"Invalid destination station: {destination}")
        
        # 模擬班次數據（實際應調用 API）
        mock_trains = [
            TrainSchedule(
                train_no="001",
                departure_station=origin,
                arrival_station=destination,
                departure_time="06:00",
                arrival_time="07:30",
                duration_minutes=90,
                early_bird_discount=35,
                available_seats=80,
            ),
            TrainSchedule(
                train_no="005",
                departure_station=origin,
                arrival_station=destination,
                departure_time="08:00",
                arrival_time="09:30",
                duration_minutes=90,
                early_bird_discount=20,
                available_seats=50,
            ),
            TrainSchedule(
                train_no="101",
                departure_station=origin,
                arrival_station=destination,
                departure_time="10:00",
                arrival_time="11:30",
                duration_minutes=90,
                early_bird_discount=None,
                available_seats=100,
            ),
        ]
        
        # 早鳥折扣過濾
        if early_bird_filter:
            mock_trains = [
                t for t in mock_trains 
                if t.early_bird_discount == early_bird_filter
            ]
        
        return mock_trains
    
    def filter_by_time(
        self, 
        trains: List[TrainSchedule], 
        start_time: str = "00:00",
        end_time: str = "23:59"
    ) -> List[TrainSchedule]:
        """按時段過濾"""
        return [
            t for t in trains 
            if start_time <= t.departure_time <= end_time
        ]
    
    def filter_by_train_no(
        self, 
        trains: List[TrainSchedule], 
        train_nos: List[str]
    ) -> List[TrainSchedule]:
        """按車次編號過濾"""
        return [t for t in trains if t.train_no in train_nos]
