#!/usr/bin/env python3
"""
高鐵訂票輔助工具（完整自動化版本 v2）
使用 JavaScript 選擇器，更穩定
"""

import json
import os
import time
import sys
from playwright.sync_api import sync_playwright

BOOKING_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"
TIMETABLE_FILE = "data/thsr_timetable_v2.json"


def auto_book_simple(from_station="新竹", to_station="彰化", date=None, time="09:00", passengers=1):
    """
    簡化版自動訂票 - 使用更穩定的方式
    """
    print(f"\n🚀 開始自動訂票...")
    print(f"📍 {from_station} → {to_station}")
    print(f"📅 {date or '今天'} | ⏰ {time} | 👤 {passengers} 人")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 1. 開啟訂票頁面
        print("\n[1/5] 開啟訂票頁面...")
        page.goto(BOOKING_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # 同意 cookie
        try:
            page.click('button:has-text("我同意")', timeout=3000)
        except:
            pass
        print("✅ 頁面已開啟")
        
        # 2. 填入訂票資訊（使用 JavaScript）
        print("\n[2/5] 填入訂票資訊...")
        
        # 站點對應數字
        station_map = {
            "南港": 1, "台北": 2, "板橋": 3, "桃園": 4, "新竹": 5,
            "苗栗": 6, "台中": 7, "彰化": 8, "雲林": 9, "嘉義": 10,
            "台南": 11, "左營": 12
        }
        
        from_idx = station_map.get(from_station, 1)
        to_idx = station_map.get(to_station, 8)
        
        # 使用 JavaScript 直接設定值
        page.evaluate(f"""
            // 設定出發站
            const originSelect = document.querySelector('select[name*="origin"], select[id*="origin"]');
            if (originSelect) {{
                originSelect.selectedIndex = {from_idx};
                originSelect.dispatchEvent(new Event('change'));
            }}
            
            // 設定到達站
            const destSelect = document.querySelector('select[name*="dest"], select[id*="dest"], select[name*="to"], select[id*="to"]');
            if (destSelect) {{
                destSelect.selectedIndex = {to_idx};
                destSelect.dispatchEvent(new Event('change'));
            }}
        """)
        
        page.wait_for_timeout(1000)
        print(f"✅ 已填入站點")
        
        # 3. 開始查詢
        print("\n[3/5] 點擊查詢...")
        try:
            page.click('button:has-text("開始查詢")', timeout=10000)
            page.wait_for_timeout(3000)
            print("✅ 已查詢")
        except Exception as e:
            print(f"⚠️ 查詢失敗: {e}")
        
        # 4. 選擇班次
        print("\n[4/5] 選擇班次...")
        
        # 嘗試點擊第一個班次
        try:
            # 找到班次表格，點擊第一個可用選項
            page.click('td button, .train-item button, tr button', timeout=5000)
            print("✅ 已選擇班次")
        except:
            # 嘗試另一種方式
            try:
                page.evaluate("""
                    const buttons = document.querySelectorAll('button');
                    for (const btn of buttons) {
                        if (btn.textContent.includes('選擇') || btn.textContent.includes('Select')) {
                            btn.click();
                            break;
                        }
                    }
                """)
                print("✅ 已選擇班次")
            except:
                print("⚠️ 請手動選擇班次")
        
        # 5. 驗證碼
        print("\n[5/5] 驗證碼處理...")
        print("⚠️ 請在瀏覽器中輸入驗證碼並確認")
        
        print("\n" + "="*50)
        print("📋 訂票流程進行中...")
        print("   請在瀏覽器中完成以下步驟：")
        print("   1. 輸入驗證碼")
        print("   2. 選擇座位（可略過）")
        print("   3. 點擊確認訂票")
        print("="*50)
        
        # 保持瀏覽器開啟，讓用戶完成後續操作
        input("\n按 Enter 關閉瀏覽器...")
        
        browser.close()
        print("👋 已關閉")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="高鐵自動訂票")
    parser.add_argument("-f", "--from", dest="from_station", default="新竹", help="出發站")
    parser.add_argument("-t", "--to", dest="to_station", default="彰化", help="到達站")
    parser.add_argument("-d", "--date", default=None, help="日期")
    parser.add_argument("--time", default="09:00", help="時間")
    parser.add_argument("-p", "--passengers", type=int, default=1, help="乘客數")
    
    args = parser.parse_args()
    
    auto_book_simple(
        from_station=args.from_station,
        to_station=args.to_station,
        date=args.date,
        time=args.time,
        passengers=args.passengers
    )
