"""
高鐵訂位執行模組
處理訂票邏輯與參數驗證
"""
import asyncio
import random
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass

from ..config import TICKET_TYPES
from ..errors import HSRError, ErrorCode, HSRErrorLevel


@dataclass
class Passenger:
    """乘客資訊"""
    id_number: str  # ROC 身份證字號
    name: Optional[str] = None
    ticket_type: str = "adult"  # adult/child/senior/disabled/student


@dataclass
class BookingRequest:
    """訂位請求"""
    departure_station: str
    arrival_station: str
    train_no: str
    travel_date: datetime
    passengers: List[Passenger]
    round_trip: bool = False
    return_date: Optional[datetime] = None


class BookingExecutor:
    """訂位執行器"""
    
    def __init__(self):
        self.session = None
        self.csrf_token: Optional[str] = None
        self.cookies: Dict = {}
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    @staticmethod
    def validate_id_number(id_number: str) -> bool:
        """驗證 ROC 身份證字號格式"""
        if len(id_number) != 10:
            return False
        
        area_codes = {
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14,
            'F': 15, 'G': 16, 'H': 17, 'I': 34, 'J': 18,
            'K': 19, 'L': 20, 'M': 21, 'N': 22, 'O': 35,
            'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27,
            'U': 28, 'V': 29, 'W': 32, 'X': 30, 'Y': 31,
            'Z': 33
        }
        
        first_char = id_number[0].upper()
        if first_char not in area_codes:
            return False
        
        if not id_number[1:].isdigit():
            return False
        
        return True
    
    @staticmethod
    def validate_ticket_quantity(quantity: int, round_trip: bool = False) -> bool:
        """驗證票數限制"""
        if round_trip:
            return quantity <= 5
        return quantity <= 10
    
    def validate_booking_request(self, request: BookingRequest) -> List[str]:
        """驗證訂位請求"""
        errors = []
        
        if not self.validate_ticket_quantity(len(request.passengers), request.round_trip):
            errors.append("票數超過限制（單程最多10張，去回程各5張）")
        
        for i, passenger in enumerate(request.passengers):
            if not self.validate_id_number(passenger.id_number):
                errors.append(f"乘客{i+1}的身份證號格式錯誤")
            
            if passenger.ticket_type in ["senior", "disabled"]:
                if len(passenger.id_number) != 10:
                    errors.append(f"乘客{i+1}敬老/愛心票需提供有效身份證號")
        
        return errors
    
    async def init_session(self):
        """初始化 Session"""
        self.session = {"user_agent": "Mozilla/5.0", "initialized": True}
    
    async def refresh_captcha(self) -> bytes:
        """獲取驗證碼圖片"""
        await asyncio.sleep(0.1)
        return b"CAPTCHA_IMAGE_BYTES"
    
    async def book_train(self, request: BookingRequest) -> Dict:
        """執行訂位"""
        errors = self.validate_booking_request(request)
        if errors:
            raise HSRError("; ".join(errors), HSRErrorLevel.L3ManualIntervention, ErrorCode.INVALID_ID)
        
        # 隨機延遲 (Jitter) - 防灌爆伺服器
        delay = random.uniform(0.5, 2.0)
        await asyncio.sleep(delay)
        
        return {
            "status": "success",
            "booking_no": f"BR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "train_no": request.train_no,
            "passengers": len(request.passengers),
            "total_amount": len(request.passengers) * 1500,
        }
    
    async def check_booking_status(self, booking_no: str) -> Dict:
        """檢查訂單狀態"""
        return {
            "booking_no": booking_no,
            "status": "pending_payment",
            "payment_deadline": datetime.now().isoformat(),
        }
    
    async def close(self):
        """關閉 Session"""
        self.session = None
