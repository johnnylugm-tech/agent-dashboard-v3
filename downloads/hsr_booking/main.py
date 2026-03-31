#!/usr/bin/env python3
"""
台灣高鐵自動化訂票系統
僅供學習與個人研究使用
"""
import asyncio
import argparse
from datetime import datetime, timedelta

from src.query.query_engine import QueryEngine
from src.booking.booking_executor import BookingExecutor, BookingRequest, Passenger
from src.captcha.captcha_solver import CaptchaSolver
from src.config import HSR_STATIONS


async def search_trains(origin: str, destination: str, date_str: str):
    """查詢班次"""
    print(f"🔍 查詢 {origin} → {destination}，日期：{date_str}")
    
    async with QueryEngine() as engine:
        travel_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # 檢查預售是否開放
        if not engine.is_presale_open(travel_date):
            presale_date = engine.calculate_presale_date(travel_date)
            print(f"⚠️ 預售尚未開放，開放日期：{presale_date.strftime('%Y-%m-%d')}")
            return
        
        trains = await engine.query_trains(origin, destination, travel_date)
        
        print(f"\n找到 {len(trains)} 個班次：")
        for train in trains:
            discount = f" (早鳥 {train.early_bird_discount}%)" if train.early_bird_discount else ""
            print(f"  🚄 {train.train_no} | {train.departure_time}→{train.arrival_time} | {train.duration_minutes}分鐘{discount}")


async def book_ticket(origin: str, destination: str, train_no: str, id_number: str):
    """訂票"""
    print(f"🎫 訂購 {train_no}，身份證：{id_number[:3]}***")
    
    async with BookingExecutor() as executor:
        await executor.init_session()
        
        # 建立訂位請求
        request = BookingRequest(
            departure_station=origin,
            arrival_station=destination,
            train_no=train_no,
            travel_date=datetime.now() + timedelta(days=7),
            passengers=[Passenger(id_number=id_number, ticket_type="adult")]
        )
        
        # 驗證請求
        errors = executor.validate_booking_request(request)
        if errors:
            print(f"❌ 驗證失敗：{errors}")
            return
        
        # 訂票
        result = await executor.book_train(request)
        
        print(f"✅ 訂票成功！")
        print(f"   訂單編號：{result['booking_no']}")
        print(f"   車次：{result['train_no']}")
        print(f"   金額：${result['total_amount']}")


def main():
    parser = argparse.ArgumentParser(description="高鐵訂票系統 - 僅供學習使用")
    parser.add_argument("action", choices=["search", "book"], help="執行動作")
    parser.add_argument("--from", dest="origin", default="Taipei", help="起點站")
    parser.add_argument("--to", dest="destination", default="Zuoying", help="目的地")
    parser.add_argument("--date", default=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), help="日期")
    parser.add_argument("--train", dest="train_no", help="車次編號")
    parser.add_argument("--id", dest="id_number", help="身份證字號")
    
    args = parser.parse_args()
    
    if args.action == "search":
        asyncio.run(search_trains(args.origin, args.destination, args.date))
    elif args.action == "book":
        if not args.train_no or not args.id_number:
            print("❌ 訂票需要 --train 和 --id 參數")
            return
        asyncio.run(book_ticket(args.origin, args.destination, args.train_no, args.id_number))


if __name__ == "__main__":
    main()
