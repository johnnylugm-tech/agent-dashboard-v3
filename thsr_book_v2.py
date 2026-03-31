#!/usr/bin/env python3
"""
高鐵訂票自動化 v2 - 使用 Browser API

基於實際頁面結構的訂票腳本
"""

import os
import time
from datetime import datetime, timedelta

# 站點映射
STATION_MAP = {
    "南港": "1", "台北": "2", "板橋": "3", "桃園": "4", "新竹": "5",
    "苗栗": "6", "台中": "7", "彰化": "8", "雲林": "9", "嘉義": "10",
    "台南": "11", "左營": "12"
}

BOOKING_URL = "https://irs.thsrc.com.tw/IMINT/?locale=tw"


def get_next_booking_date():
    """獲取下次開放訂票的日期"""
    # 高鐵開放 28 天內的訂票
    today = datetime.now()
    next_booking = today + timedelta(days=1)  # 從明天開始
    return next_booking.strftime("%Y/%m/%d")


def search_trains(from_station, to_station, date, time_range="00:00"):
    """
    搜尋班次
    使用瀏覽器自動化
    """
    from playwright.sync_api import sync_playwright
    
    print(f"\n🚄 搜尋班次: {from_station} → {to_station}")
    print(f"📅 日期: {date}")
    print(f"⏰ 時間: {time_range}")
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 訪問頁面
            print("\n[1/5] 訪問訂票網站...")
            page.goto(BOOKING_URL, timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)
            
            # 點擊同意（如果出現）
            try:
                page.click('button:has-text("我同意")', timeout=3000)
            except:
                pass
            print("✅ 頁面載入完成")
            
            # 填入出發站
            print("\n[2/5] 填入資料...")
            from_idx = STATION_MAP.get(from_station, "5")
            to_idx = STATION_MAP.get(to_station, "8")
            
            # 使用 XPath 選擇器 - 根據實際頁面結構
            # 出發站是第二個 combobox (ref=e64)
            page.locator('xpath=//div[contains(@class, "combobox")][1]').click()
            time.sleep(0.5)
            page.locator(f'xpath=//option[text()="{from_station}"]').click()
            
            # 到達站
            page.locator('xpath=//div[contains(@class, "combobox")][2]').click()
            time.sleep(0.5)
            page.locator(f'xpath=//option[text()="{to_station}"]').click()
            
            print(f"   ✅ 站點: {from_station} → {to_station}")
            
            # 填入日期 - 使用 JavaScript
            print(f"   📅 日期: {date}")
            
            # 點擊日期輸入框並填入
            date_input = page.locator('xpath=//input[@type="text" and contains(@class, "mat-input")]').first
            if date_input.count() == 0:
                # 嘗試其他選擇器
                date_input = page.locator('xpath=//input[contains(@placeholder, "日期")]').first
            
            if date_input.count() > 0:
                date_input.click()
                time.sleep(0.5)
                # 清除並輸入新日期
                date_input.fill("")
                date_input.type(date)
            
            # 選擇時間
            print(f"   ⏰ 時間: {time_range}")
            time_select = page.locator('xpath=//select[contains(@id, " departureTime") or contains(@class, "time")]').first
            if time_select.count() > 0:
                time_select.select_option(time_range.replace(":", ""))
            
            # 票數設定為 1
            print(f"   🎫 票數: 1")
            ticket_select = page.locator('xpath=//select[contains(@id, "ticket") or contains(@class, "ticket")][1]').first
            if ticket_select.count() > 0:
                ticket_select.select_option("1")
            
            # 輸入驗證碼
            print("\n[3/5] 輸入驗證碼...")
            captcha_img = page.locator('xpath=//img[contains(@src, "captcha")]').first
            
            if captcha_img.count() > 0:
                # 截圖驗證碼
                captcha_bytes = captcha_img.screenshot()
                
                # 使用 ddddocr 識別
                try:
                    import ddddocr
                    ocr = ddddocr.DdddOcr(show_ad=False)
                    captcha_code = ocr.classification(captcha_bytes)
                    print(f"   🔤 識別結果: {captcha_code}")
                    
                    # 填入驗證碼
                    captcha_input = page.locator('xpath=//input[contains(@class, "captcha")]').first
                    if captcha_input.count() > 0:
                        captcha_input.fill(captcha_code)
                except Exception as e:
                    print(f"   ⚠️ 驗證碼識別失敗: {e}")
                    print("   請手動輸入驗證碼...")
                    time.sleep(30)  # 等待手動輸入
            
            # 點擊查詢
            print("\n[4/5] 開始查詢...")
            search_btn = page.locator('xpath=//button[contains(text(), "開始查詢")]').first
            if search_btn.count() > 0:
                search_btn.click()
                page.wait_for_timeout(3000)
                print("✅ 查詢完成")
                
                # 獲取結果
                print("\n[5/5] 班次結果:")
                trains = page.locator('xpath=//table[contains(@class, "train")]//tr').all()
                
                for i, train in enumerate(trains[:5], 1):
                    try:
                        cols = train.locator('td').all()
                        if len(cols) >= 5:
                            train_num = cols[0].inner_text()
                            dep_time = cols[1].inner_text()
                            arr_time = cols[2].inner_text()
                            duration = cols[3].inner_text()
                            print(f"   {i}. {train_num} | {dep_time} → {arr_time} | {duration}")
                    except:
                        pass
            else:
                print("❌ 找不到查詢按鈕")
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # 保持瀏覽器開啟，讓用戶確認
            print("\n🔵 瀏覽器保持開啟中...")
            time.sleep(5)
            # browser.close()
    
    return True


def main():
    """主函數"""
    print("=" * 50)
    print("🚄 高鐵訂票自動化 v2")
    print("=" * 50)
    
    # 測試參數
    from_station = "新竹"
    to_station = "左營"
    date = "2026/04/15"
    time_range = "09:00"
    
    # 執行搜尋
    result = search_trains(from_station, to_station, date, time_range)
    
    if result:
        print("\n✅ 搜尋完成！")
    else:
        print("\n❌ 搜尋失敗")


if __name__ == "__main__":
    main()
