#!/usr/bin/env python3
"""
高鐵訂票輔助工具（優化版）
"""

import os
import time
from playwright.sync_api import sync_playwright

BOOKING_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"


def book(from_station="新竹", to_station="彰化", date=None, time_val="09:00", passengers=1):
    """自動訂票"""
    
    station_map = {
        "南港": 1, "台北": 2, "板橋": 3, "桃園": 4, "新竹": 5,
        "苗栗": 6, "台中": 7, "彰化": 8, "雲林": 9, "嘉義": 10,
        "台南": 11, "左營": 12
    }
    
    print(f"\n🚀 自動訂票: {from_station} → {to_station}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 開頁面
        print("[1/4] 開啟頁面...")
        page.goto(BOOKING_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        # 同意
        try:
            page.click('button:has-text("我同意")', timeout=2000)
        except: pass
        print("✅ 頁面開啟")
        
        # 填站點
        print("[2/4] 填入資料...")
        
        from_idx = station_map.get(from_station, 5)
        to_idx = station_map.get(to_station, 8)
        
        # 用 JavaScript 填
        page.evaluate(f"""
            // 出發站
            const selects = document.querySelectorAll('select');
            if (selects[0]) {{
                selects[0].selectedIndex = {from_idx};
                selects[0].dispatchEvent(new Event('change', {{bubbles: true}}));
            }}
            // 到達站
            if (selects[1]) {{
                selects[1].selectedIndex = {to_idx};
                selects[1].dispatchEvent(new Event('change', {{bubbles: true}}));
            }}
        """)
        
        page.wait_for_timeout(1000)
        print(f"✅ 站點: {from_station} → {to_station}")
        
        # 查詢 - 用多個選擇器嘗試
        print("[3/4] 查詢班次...")
        
        selectors = [
            'button:has-text("開始查詢")',
            'button[type="submit"]',
            '.uk-button-primary',
            'button.btn-primary'
        ]
        
        for sel in selectors:
            try:
                page.click(sel, timeout=3000)
                print(f"✅ 點擊成功: {sel}")
                break
            except: continue
        
        page.wait_for_timeout(3000)
        
        # 選擇班次
        print("[4/4] 選擇班次...")
        
        # 點擊第一個班次按鈕
        page.evaluate("""
            const cells = document.querySelectorAll('td button, td input[type="button"]');
            if (cells.length > 0) cells[0].click();
        """)
        
        page.wait_for_timeout(2000)
        
        # 結果
        print("\n" + "="*50)
        print("📋 請在瀏覽器中完成：")
        print("   1. 輸入驗證碼")
        print("   2. 選擇座位（可略過）")
        print("   3. 確認訂票")
        print("="*50)
        
        input("\n按 Enter 關閉瀏覽器...")
        browser.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--from", dest="frm", default="新竹")
    parser.add_argument("-t", "--to", default="彰化")
    parser.add_argument("-d", "--date", default=None)
    parser.add_argument("-p", "--passengers", type=int, default=1)
    args = parser.parse_args()
    
    book(args.frm, args.to, args.date, "09:00", args.passengers)
