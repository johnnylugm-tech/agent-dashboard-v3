#!/usr/bin/env python3
"""
高鐵訂票輔助工具（半自動）
用途：個人協助開啟訂票頁面並填入資料
風險：僅輔助操作，仍需手動驗證碼確認
"""

import os
import sys

# 檢查依賴
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ 需要安裝 Playwright: pip install playwright")
    sys.exit(1)

# 站點對應
STATIONS = {
    "南港": "Nangang",
    "台北": "Taipei",
    "板橋": "Banqiao",
    "桃園": "Taoyuan",
    "新竹": "Hsinchu",
    "苗栗": "Miaoli",
    "台中": "Taichung",
    "彰化": "Changhua",
    "雲林": "Yunlin",
    "嘉義": "Chiayi",
    "台南": "Tainan",
    "左營": "Zuoying"
}

BOOKING_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"


def book_ticket(from_station, to_station, date=None, time_period="all", passengers=1):
    """
    開啟訂票頁面並填入資料
    
    Args:
        from_station: 出發站 (e.g., "新竹")
        to_station: 到達站 (e.g., "彰化")
        date: 日期 (預設今天，格式: YYYY/MM/DD)
        time_period: 時段 ("morning", "afternoon", "evening", "all")
        passengers: 乘客數
    """
    print(f"🚀 開啟高鐵訂票頁面...")
    print(f"📍 {from_station} → {to_station}")
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 開啟訂票頁面
        page.goto(BOOKING_URL)
        print("✅ 頁面已開啟")
        
        # 等待頁面載入
        page.wait_for_load_state("networkidle")
        
        # 點擊同意 cookie
        try:
            page.click('button:has-text("我同意")', timeout=3000)
        except:
            pass
        
        print("📝 填入訂票資訊...")
        
        # 填入出發站
        page.click('select[id*="origin"], select[name*="origin"], .station-select >> nth=0')
        page.wait_for_timeout(500)
        
        # 選擇出發站
        station_options = {
            "南港": 1, "台北": 2, "板橋": 3, "桃園": 4, "新竹": 5,
            "苗栗": 6, "台中": 7, "彰化": 8, "雲林": 9, "嘉義": 10,
            "台南": 11, "左營": 12
        }
        
        # 使用 JavaScript 直接選擇
        page.evaluate(f"""
            document.querySelectorAll('select option').forEach((opt, i) => {{
                if (opt.text.includes('{from_station}')) {{
                    opt.parentElement.selectedIndex = i;
                    opt.parentElement.value = opt.value;
                }}
            }});
        """)
        
        # 填入到達站
        page.click('select[id*="dest"], select[name*="dest"], .station-select >> nth=1')
        page.wait_for_timeout(500)
        
        page.evaluate(f"""
            document.querySelectorAll('select option').forEach((opt, i) => {{
                if (opt.text.includes('{to_station}')) {{
                    opt.parentElement.selectedIndex = i;
                    opt.parentElement.value = opt.value;
                }}
            }});
        """)
        
        print(f"✅ 已填入: {from_station} → {to_station}")
        
        # 顯示說明
        print("\n" + "="*50)
        print("📋 請手動完成以下步驟：")
        print("="*50)
        print("1. 確認出發/到達站是否正確")
        print("2. 選擇出發日期和時間")
        print("3. 選擇票種和數量")
        print("4. 點擊「開始查詢」")
        print("5. 輸入驗證碼")
        print("6. 選擇班次並確認訂票")
        print("="*50)
        print("\n🖥️ 瀏覽器已開啟，請在頁面上操作")
        print("💡 瀏覽器會保持開啟直到你關閉")
        
        # 保持瀏覽器開啟
        input("\n按 Enter 關閉瀏覽器...")
        
        browser.close()
        print("👋 已關閉瀏覽器")


def main():
    """主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(description="高鐵訂票輔助工具")
    parser.add_argument("--from", "-f", required=True, help="出發站 (e.g., 新竹)")
    parser.add_argument("--to", "-t", required=True, help="到達站 (e.g., 彰化)")
    parser.add_argument("--date", "-d", default=None, help="出發日期 (e.g., 2026/03/20)")
    parser.add_argument("--time", default="all", help="時段 (morning/afternoon/evening/all)")
    parser.add_argument("--passengers", "-p", type=int, default=1, help="乘客數")
    
    args = parser.parse_args()
    
    # 驗證站點
    if args.from not in STATIONS:
        print(f"❌ 錯誤的出發站: {args.from}")
        print(f"可用站點: {', '.join(STATIONS.keys())}")
        return
    
    if args.to not in STATIONS:
        print(f"❌ 錯誤的到達站: {args.to}")
        print(f"可用站點: {', '.join(STATIONS.keys())}")
        return
    
    # 執行訂票
    book_ticket(
        from_station=args.from,
        to_station=args.to,
        date=args.date,
        time_period=args.time,
        passengers=args.passengers
    )


if __name__ == "__main__":
    main()
