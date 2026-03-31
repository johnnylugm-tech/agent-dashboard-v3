#!/usr/bin/env python3
"""
高鐵訂票自動化 v3 - 最終版

使用 JavaScript 注入方式繞過 Wicket 框架的選擇器問題
"""

import time
from datetime import datetime, timedelta

# 站點對應
STATIONS = {
    "南港": "1", "台北": "2", "板橋": "3", "桃園": "4", "新竹": "5",
    "苗栗": "6", "台中": "7", "彰化": "8", "雲林": "9", "嘉義": "10",
    "台南": "11", "左營": "12"
}


def book_ticket(
    from_station: str,
    to_station: str,
    date: str = None,  # 格式: 2026/04/15
    time_slot: str = "09:00",
    adults: int = 1
):
    """
    訂票主函數
    
    參數:
        from_station: 出發站 (e.g., "新竹")
        to_station: 到達站 (e.g., "左營")
        date: 出發日期 (預設為明天)
        time_slot: 出發時段 (e.g., "09:00")
        adults: 成人票數
    """
    from playwright.sync_api import sync_playwright
    
    date = date or (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")
    from_code = STATIONS.get(from_station, "5")
    to_code = STATIONS.get(to_station, "12")
    
    print(f"\n🚄 高鐵訂票: {from_station} → {to_station}")
    print(f"📅 日期: {date}")
    print(f"⏰ 時段: {time_slot}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 訪問訂票頁面
        print("\n[1] 訪問訂票頁面...")
        page.goto("https://irs.thsrc.com.tw/IMINT/?locale=tw", timeout=120000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        # 嘗試點擊同意
        try:
            page.click('button:has-text("我同意")', timeout=3000)
        except:
            pass
        print("✅ 頁面載入完成")
        
        # 使用 JavaScript 直接填寫表單
        # 這是繞過 Wicket 框架最穩定的方式
        print("\n[2] 填寫表單...")
        
        # 直接通過 JavaScript 設置選擇框的值
        js_code = f"""
        {{
            // 嘗試找到並設置出發站
            const selects = document.querySelectorAll('select');
            if (selects.length >= 2) {{
                // 出發站 (第一個 select)
                const fromSelect = selects[0];
                fromSelect.value = '{from_code}';
                fromSelect.dispatchEvent(new Event('change', {{ bubbles: true }}));
                console.log('Set from station to: {from_station}');
                
                // 到達站 (第二個 select)  
                const toSelect = selects[1];
                toSelect.value = '{to_code}';
                toSelect.dispatchEvent(new Event('change', {{ bubbles: true }}));
                console.log('Set to station to: {to_station}');
            }}
        }}
        """
        
        page.evaluate(js_code)
        time.sleep(1)
        print(f"   ✅ 站點: {from_station} → {to_station}")
        
        # 填寫日期 - 使用 JavaScript 點擊和輸入
        print(f"   📅 日期: {date}")
        
        # 嘗試點擊日期輸入框
        try:
            date_input = page.locator('input[type="text"]').first
            date_input.click()
            time.sleep(0.5)
            
            # 清除並輸入日期
            date_input.fill("")
            date_input.type(date)
        except Exception as e:
            print(f"   ⚠️ 日期輸入: {e}")
        
        # 選擇出發時段
        print(f"   ⏰ 時段: {time_slot}")
        
        # 時段選擇 - 使用 select
        time_hour = time_slot.split(":")[0]
        try:
            time_selects = page.locator('select').all()
            if len(time_selects) >= 3:
                time_selects[2].select_option(time_hour)
        except Exception as e:
            print(f"   ⚠️ 時段選擇: {e}")
        
        # 設置票數
        print(f"   🎫 票數: {adults}")
        try:
            ticket_selects = page.locator('select').all()
            if len(ticket_selects) >= 4:
                ticket_selects[3].select_option(str(adults))
        except Exception as e:
            print(f"   ⚠️ 票數設置: {e}")
        
        # 處理驗證碼
        print("\n[3] 處理驗證碼...")
        
        try:
            # 嘗試找到驗證碼圖片
            captcha_img = page.locator('img').all()
            for img in captcha_img:
                src = img.get_attribute('src')
                if src and 'captcha' in src.lower():
                    print("   ✅ 找到驗證碼圖片")
                    
                    # 截圖
                    img.screenshot(path="captcha.png")
                    
                    # 識別
                    try:
                        import ddddocr
                        ocr = ddddocr.DdddOcr(show_ad=False)
                        with open("captcha.png", "rb") as f:
                            result = ocr.classification(f.read())
                        print(f"   🔤 識別結果: {result}")
                        
                        # 填入驗證碼
                        captcha_input = page.locator('input[type="text"]').all()
                        if len(captcha_input) >= 2:
                            captcha_input[1].fill(result)
                    except Exception as e:
                        print(f"   ⚠️ 驗證碼識別失敗: {e}")
                        print("   請手動輸入驗證碼 (有 30 秒)")
                        time.sleep(30)
                    
                    break
        except Exception as e:
            print(f"   ⚠️ 驗證碼處理: {e}")
        
        # 點擊查詢
        print("\n[4] 點擊查詢...")
        try:
            search_btn = page.locator('button:has-text("開始查詢")')
            if search_btn.count() > 0:
                search_btn.first.click()
                print("   ✅ 已點擊查詢")
                
                # 等待結果
                page.wait_for_timeout(5000)
                
                # 獲取結果
                print("\n[5] 查詢結果:")
                tables = page.locator('table').all()
                if tables:
                    rows = tables[0].locator('tr').all()
                    for i, row in enumerate(rows[:6], 1):
                        cols = row.locator('td').all()
                        if len(cols) >= 5:
                            try:
                                num = cols[0].inner_text()
                                dep = cols[1].inner_text()
                                arr = cols[2].inner_text()
                                dur = cols[3].inner_text()
                                print(f"   {i}. {num} | {dep} → {arr} | {dur}")
                            except:
                                pass
                else:
                    print("   ⚠️ 未找到結果表格")
            else:
                print("   ❌ 未找到查詢按鈕")
        except Exception as e:
            print(f"   ❌ 查詢失敗: {e}")
        
        # 保持瀏覽器開啟
        print("\n🔵 瀏覽器保持開啟中...")
        time.sleep(60)
        
        browser.close()
    
    return True


def main():
    """主函數"""
    print("=" * 50)
    print("🚄 高鐵訂票自動化 v3")
    print("=" * 50)
    
    # 測試參數
    book_ticket(
        from_station="新竹",
        to_station="左營",
        date="2026/04/15",
        time_slot="09:00",
        adults=1
    )


if __name__ == "__main__":
    main()
