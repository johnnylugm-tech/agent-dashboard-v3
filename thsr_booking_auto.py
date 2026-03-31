#!/usr/bin/env python3
"""
高鐵訂票輔助工具（自動化版本）
功能：
- 自動填入訂票資訊
- 自動查詢可用班次
- 自動選擇班次
- 驗證碼需要手動輸入
"""

import json
import os
import time
import sys
from datetime import datetime, timedelta

# 站點對應
STATIONS = {
    "南港": "Nangang", "台北": "Taipei", "板橋": "Banqiao",
    "桃園": "Taoyuan", "新竹": "Hsinchu", "苗栗": "Miaoli",
    "台中": "Taichung", "彰化": "Changhua", "雲林": "Yunlin",
    "嘉義": "Chiayi", "台南": "Tainan", "左營": "Zuoying"
}

STATION_IDS = {
    "南港": "0990", "台北": "1000", "板橋": "1010",
    "桃園": "1020", "新竹": "1030", "苗栗": "1040",
    "台中": "1050", "彰化": "1060", "雲林": "1065",
    "嘉義": "1070", "台南": "1080", "左營": "1090"
}

BOOKING_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"
TIMETABLE_FILE = "data/thsr_timetable_v2.json"


def load_timetable():
    """載入時刻表數據"""
    if os.path.exists(TIMETABLE_FILE):
        with open(TIMETABLE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def find_trains(from_station, to_station, date=None, time_period="all"):
    """
    從時刻表數據中找到符合條件的班次
    """
    data = load_timetable()
    if not data:
        return []
    
    # 決定方向
    from_idx = list(STATIONS.keys()).index(from_station)
    to_idx = list(STATIONS.keys()).index(to_station)
    
    if to_idx > from_idx:
        direction = "southbound"
    else:
        direction = "northbound"
    
    timetable = data.get(direction, {})
    all_trains = []
    
    for period in ["morning", "afternoon", "evening"]:
        if time_period != "all" and period != time_period:
            continue
        for train in timetable.get(period, []):
            all_trains.append({
                "train_no": train.get("train_no"),
                "departure": train.get("times", [None]*12)[0] if train.get("times") else None,
                "period": period
            })
    
    # 按發車時間排序
    all_trains.sort(key=lambda x: x["departure"] or "99:99")
    return all_trains[:10]  # 返回前10班


def auto_book(from_station, to_station, date=None, time="09:00", 
              passengers=1, train_no=None, headless=False):
    """
    全自動訂票流程
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 需要安裝 Playwright: pip install playwright")
        return False
    
    print(f"\n🚀 開始自動訂票...")
    print(f"📍 {from_station} → {to_station}")
    print(f"📅 {date or '今天'} | ⏰ {time} | 👤 {passengers} 人")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. 開啟訂票頁面
        print("\n[1/6] 開啟訂票頁面...")
        page.goto(BOOKING_URL)
        page.wait_for_load_state("networkidle")
        
        # 同意 cookie
        try:
            page.click('button:has-text("我同意")', timeout=2000)
        except:
            pass
        print("✅ 頁面已開啟")
        
        # 2. 填入訂票資訊
        print("\n[2/6] 填入訂票資訊...")
        
        # 出發站
        page.click('select >> nth=0')
        page.wait_for_timeout(300)
        page.select_option('select >> nth=0', index=list(STATIONS.keys()).index(from_station) + 1)
        
        # 到達站
        page.click('select >> nth=1')
        page.wait_for_timeout(300)
        page.select_option('select >> nth=1', index=list(STATIONS.keys()).index(to_station) + 1)
        
        # 日期和時間
        if date:
            # 清除並輸入日期
            page.fill('input[placeholder*="日期"], input[id*="date"]', date)
        
        # 出發時段
        hour = int(time.split(":")[0])
        if hour < 12:
            period = "00:00"
        elif hour < 18:
            period = "12:00"
        else:
            period = "18:00"
        
        page.select_option('select >> nth=3', period)
        
        # 乘客數
        page.select_option('select >> nth=4', str(passengers))
        
        print(f"✅ 已填入: {from_station} → {to_station}, {date}, {time}")
        
        # 3. 開始查詢
        print("\n[3/6] 點擊查詢...")
        page.click('button:has-text("開始查詢")')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # 4. 選擇班次
        print("\n[4/6] 選擇班次...")
        
        # 嘗試找到符合的班次
        if train_no:
            # 指定車次
            try:
                # 點擊包含車次編號的按鈕
                page.click(f'button:has-text("{train_no}"), td:has-text("{train_no}")', timeout=5000)
                print(f"✅ 已選擇車次: {train_no}")
            except:
                # 選擇第一班
                page.click('button >> nth=5', timeout=5000)
                print("⚠️ 指定車次不存在，選擇第一班")
        else:
            # 選擇第一班
            try:
                page.click('button >> nth=5', timeout=5000)
                print("✅ 已選擇第一班")
            except:
                print("⚠️ 無法自動選擇班次，請手動選擇")
        
        page.wait_for_timeout(1000)
        
        # 5. 輸入驗證碼（暫停等待手動輸入）
        print("\n[5/6] 輸入驗證碼...")
        print("⚠️ 請在瀏覽器中手動輸入驗證碼")
        print("⏳ 等待 60 秒...")
        
        # 等待用戶輸入驗證碼
        page.wait_for_timeout(60000)
        
        # 6. 確認訂票
        print("\n[6/6] 確認訂票...")
        try:
            page.click('button:has-text("確認"), button:has-text("送出")', timeout=3000)
            print("✅ 訂票已送出！")
        except:
            print("⚠️ 無法自動確認，請手動點擊確認")
        
        print("\n" + "="*50)
        print("🎉 訂票流程完成！")
        print("="*50)
        
        # 保持瀏覽器開啟
        input("\n按 Enter 關閉瀏覽器...")
        
        browser.close()
        return True


def interactive_book():
    """互動式訂票"""
    print("\n" + "="*50)
    print("🚄 高鐵訂票輔助工具（互動版）")
    print("="*50)
    
    # 選擇站點
    print("\n可用站點:")
    for i, s in enumerate(STATIONS.keys(), 1):
        print(f"  {i}. {s}")
    
    while True:
        try:
            from_idx = int(input("\n出發站編號: ")) - 1
            from_station = list(STATIONS.keys())[from_idx]
            break
        except:
            print("輸入錯誤，請重新輸入")
    
    while True:
        try:
            to_idx = int(input("到達站編號: ")) - 1
            to_station = list(STATIONS.keys())[to_idx]
            break
        except:
            print("輸入錯誤，請重新輸入")
    
    # 日期
    date_input = input("出發日期 (直接 Enter = 今天): ").strip()
    date = date_input if date_input else None
    
    # 時間
    time = input("出發時間 (預設 09:00): ").strip() or "09:00"
    
    # 乘客數
    passengers = int(input("乘客數 (預設 1): ").strip() or "1")
    
    # 車次（可選）
    train_no = input("指定車次 (直接 Enter = 自動選擇第一班): ").strip() or None
    
    # 顯示可用班次
    print("\n📋 查詢可用班次...")
    trains = find_trains(from_station, to_station, date, "all")
    print(f"找到 {len(trains)} 班:")
    for i, t in enumerate(trains[:5], 1):
        print(f"  {i}. 車次 {t['train_no']} | {t['departure']} | {t['period']}")
    
    # 執行訂票
    auto_book(from_station, to_station, date, time, passengers, train_no)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="高鐵訂票輔助工具")
    parser.add_argument("-f", "--from", dest="from_station", help="出發站")
    parser.add_argument("-t", "--to", dest="to_station", help="到達站")
    parser.add_argument("-d", "--date", default=None, help="日期 (YYYY/MM/DD)")
    parser.add_argument("--time", default="09:00", help="時間 (HH:MM)")
    parser.add_argument("-p", "--passengers", type=int, default=1, help="乘客數")
    parser.add_argument("--train", dest="train_no", help="指定車次")
    parser.add_argument("--interactive", "-i", action="store_true", help="互動模式")
    parser.add_argument("--headless", action="store_true", help="無頭模式（不開瀏覽器）")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_book()
    elif args.from_station and args.to_station:
        auto_book(
            from_station=args.from_station,
            to_station=args.to_station,
            date=args.date,
            time=args.time,
            passengers=args.passengers,
            train_no=args.train_no,
            headless=args.headless
        )
    else:
        print("使用方法:")
        print("  python3 thsr_booking_auto.py -f 新竹 -t 彰化")
        print("  python3 thsr_booking_auto.py -i  # 互動模式")
        print("\n範例:")
        print("  python3 thsr_booking_auto.py -f 台北 -t 左營 -d 2026/03/25 --time 14:00 -p 2")
