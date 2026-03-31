#!/usr/bin/env python3
"""
高鐵訂票輔助工具（完整自動化版本）
包含驗證碼自動辨識
"""

import json
import os
import time
import sys
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

# 引入驗證碼模組
sys.path.insert(0, os.path.dirname(__file__))
from thsr_captcha import solve_captcha_ocr, manual_captcha, recognize_captcha, HAS_OCR

# 站點對應
STATIONS = {
    "南港": "Nangang", "台北": "Taipei", "板橋": "Banqiao",
    "桃園": "Taoyuan", "新竹": "Hsinchu", "苗栗": "Miaoli",
    "台中": "Taichung", "彰化": "Changhua", "雲林": "Yunlin",
    "嘉義": "Chiayi", "台南": "Tainan", "左營": "Zuoying"
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
    """找到符合條件的班次"""
    data = load_timetable()
    if not data:
        return []
    
    from_idx = list(STATIONS.keys()).index(from_station)
    to_idx = list(STATIONS.keys()).index(to_station)
    direction = "southbound" if to_idx > from_idx else "northbound"
    
    timetable = data.get(direction, {})
    all_trains = []
    
    for period in ["morning", "afternoon", "evening"]:
        if time_period != "all" and period != time_period:
            continue
        for train in timetable.get(period, []):
            times = train.get("times", [])
            all_trains.append({
                "train_no": train.get("train_no"),
                "departure": times[0] if times else None,
                "period": period
            })
    
    all_trains.sort(key=lambda x: x["departure"] or "99:99")
    return all_trains[:10]


def fill_form_and_search(page, from_station, to_station, date, time, passengers):
    """填寫表單並查詢"""
    # 出發站
    page.click('select >> nth=0')
    page.wait_for_timeout(300)
    page.select_option('select >> nth=0', index=list(STATIONS.keys()).index(from_station) + 1)
    
    # 到達站
    page.click('select >> nth=1')
    page.wait_for_timeout(300)
    page.select_option('select >> nth=1', index=list(STATIONS.keys()).index(to_station) + 1)
    
    # 日期
    if date:
        page.fill('input[placeholder*="日期"], input[id*="date"], input[name*="date"]', date)
    
    # 時段
    hour = int(time.split(":")[0])
    if hour < 12:
        period = "00:00"
    elif hour < 18:
        period = "12:00"
    else:
        period = "18:00"
    
    try:
        page.select_option('select >> nth=3', period)
    except:
        pass
    
    # 乘客數
    try:
        page.select_option('select >> nth=4', str(passengers))
    except:
        pass
    
    # 點擊查詢
    page.click('button:has-text("開始查詢")')
    page.wait_for_load_state("domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)


def solve_captcha_with_retry(page, max_attempts=3):
    """
    嘗試自動解決驗證碼
    """
    print("\n🔐 嘗試自動辨識驗證碼...")
    
    # 嘗試 OCR
    if HAS_OCR:
        for attempt in range(max_attempts):
            try:
                # 取得驗證碼圖片元素
                captcha_img = page.query_selector('img')
                
                if captcha_img:
                    # 截圖
                    screenshot = captcha_img.screenshot()
                    
                    # 辨識
                    result = recognize_captcha(screenshot)
                    
                    if result and len(result) >= 3:
                        # 填入驗證碼
                        try:
                            page.fill('input[id*="captcha"], input[name*="captcha"], input[type="text"]', result)
                            print(f"   ✅ 已填入驗證碼: {result}")
                            return True
                        except:
                            pass
                            
            except Exception as e:
                print(f"   ⚠️ 嘗試 {attempt + 1} 失敗: {e}")
            
            # 重新產生驗證碼
            try:
                page.click('button:has-text("重新產生"), button:has-text("重新整理")')
                page.wait_for_timeout(1000)
            except:
                pass
    
    # OCR 失敗，切換到手動
    print("🔐 OCR 辨識失敗，請手動輸入...")
    return manual_captcha(page, timeout=90)


def auto_book_full(from_station, to_station, date=None, time="09:00", 
                   passengers=1, train_no=None, auto_captcha=True):
    """
    完整自動化訂票
    """
    print(f"\n🚀 開始自動訂票...")
    print(f"📍 {from_station} → {to_station}")
    print(f"📅 {date or '今天'} | ⏰ {time} | 👤 {passengers} 人")
    
    if train_no:
        print(f"🚂 指定車次: {train_no}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 1. 開啟訂票頁面
        print("\n[1/6] 開啟訂票頁面...")
        page.goto(BOOKING_URL, timeout=60000)
        page.wait_for_load_state("domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)  # 等待頁面穩定
        
        # 同意 cookie
        try:
            page.click('button:has-text("我同意")', timeout=2000)
        except:
            pass
        print("✅ 頁面已開啟")
        
        # 2. 填入訂票資訊
        print("\n[2/6] 填入訂票資訊...")
        fill_form_and_search(page, from_station, to_station, date, time, passengers)
        print("✅ 已填入並查詢")
        
        # 3. 選擇班次
        print("\n[3/6] 選擇班次...")
        try:
            if train_no:
                # 嘗試找到指定車次
                page.click(f'td:has-text("{train_no}"), button:has-text("{train_no}")', timeout=3000)
                print(f"✅ 已選擇車次: {train_no}")
            else:
                # 選擇第一班
                page.click('button >> nth=5', timeout=3000)
                print("✅ 已選擇第一班")
        except Exception as e:
            print(f"⚠️ 自動選班失敗: {e}")
            print("   請手動選擇班次")
            input("   按 Enter 繼續...")
        
        page.wait_for_timeout(1000)
        
        # 4. 輸入驗證碼
        print("\n[4/6] 處理驗證碼...")
        
        if auto_captcha:
            captcha_success = solve_captcha_with_retry(page, max_attempts=2)
            
            if not captcha_success:
                print("⚠️ 驗證碼需要手動輸入")
        else:
            manual_captcha(page, timeout=90)
        
        # 等待用戶確認
        print("\n[5/6] 請確認訂票資訊...")
        input("   確認無誤後按 Enter 繼續...")
        
        # 5. 確認訂票
        print("\n[6/6] 確認訂票...")
        try:
            page.click('button:has-text("確認"), button:has-text("送出")', timeout=3000)
            print("✅ 訂票已送出！")
            
            # 等待結果
            page.wait_for_timeout(3000)
            
            # 檢查結果
            try:
                success_msg = page.query_selector('text/div:has-text("完成"), text/div:has-text("成功")')
                if success_msg:
                    print("\n🎉 訂票成功！")
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ 自動確認失敗: {e}")
        
        print("\n" + "="*50)
        print("📋 訂票流程完成，請檢查訂單結果")
        print("="*50)
        
        # 保持瀏覽器開啟
        input("\n按 Enter 關閉瀏覽器...")
        
        browser.close()
        return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="高鐵自動訂票工具")
    parser.add_argument("-f", "--from", dest="from_station", required=True, help="出發站")
    parser.add_argument("-t", "--to", dest="to_station", required=True, help="到達站")
    parser.add_argument("-d", "--date", default=None, help="日期 (YYYY/MM/DD)")
    parser.add_argument("--time", default="09:00", help="時間 (HH:MM)")
    parser.add_argument("-p", "--passengers", type=int, default=1, help="乘客數")
    parser.add_argument("--train", dest="train_no", help="指定車次")
    parser.add_argument("--no-captcha", action="store_true", help="跳過自動驗證碼")
    
    args = parser.parse_args()
    
    auto_book_full(
        from_station=args.from_station,
        to_station=args.to_station,
        date=args.date,
        time=args.time,
        passengers=args.passengers,
        train_no=args.train_no,
        auto_captcha=not args.no_captcha
    )
