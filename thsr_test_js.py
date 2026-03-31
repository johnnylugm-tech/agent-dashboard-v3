#!/usr/bin/env python3
"""
高鐵訂票自動化 v5 - 直接執行版

直接測試 JavaScript 操作真實高鐵網站
"""

import time

def test_thsr():
    """測試高鐵網站"""
    from playwright.sync_api import sync_playwright
    
    print("🚀 啟動瀏覽器...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-web-security']
        )
        page = browser.new_page()
        
        print("📥 訪問高鐵網站...")
        
        try:
            page.goto("https://irs.thsrc.com.tw/IMINT/?locale=tw", timeout=60000)
            page.wait_for_load_state("domcontentloaded")
            print("✅ 頁面載入成功")
            
            # 等待表單
            page.wait_for_selector("select", timeout=30000)
            time.sleep(2)
            
            # 獲取選擇框數量
            selects = page.query_selector_all("select")
            print(f"📋 找到 {len(selects)} 個選擇框")
            
            # JavaScript 設置出發站
            print("\n[1] 設置出發站 = 新竹...")
            result = page.evaluate('''
                () => {
                    const selects = document.querySelectorAll('select');
                    if (selects.length >= 1) {
                        selects[0].value = '5';
                        selects[0].dispatchEvent(new Event('change', { bubbles: true }));
                        return { success: true, value: selects[0].value };
                    }
                    return { success: false };
                }
            ''')
            print(f"   結果: {result}")
            time.sleep(0.5)
            
            # JavaScript 設置到達站
            print("[2] 設置到達站 = 左營...")
            result2 = page.evaluate('''
                () => {
                    const selects = document.querySelectorAll('select');
                    if (selects.length >= 2) {
                        selects[1].value = '12';
                        selects[1].dispatchEvent(new Event('change', { bubbles: true }));
                        return { success: true, value: selects[1].value };
                    }
                    return { success: false };
                }
            ''')
            print(f"   結果: {result2}")
            time.sleep(0.5)
            
            # 獲取頁面截圖確認
            page.screenshot(path="thsr_after_js.png")
            print("📸 截圖已保存: thsr_after_js.png")
            
            print("\n✅ JavaScript 操作測試完成!")
            print("請查看截圖確認選擇是否成功")
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        # 保持瀏覽器
        print("\n🔵 瀏覽器保持開啟中... (60秒後自動關閉)")
        time.sleep(60)
        
        browser.close()


if __name__ == "__main__":
    print("=" * 50)
    print("🚄 高鐵訂票 v5 - JS 直接測試")
    print("=" * 50)
    
    try:
        test_thsr()
    except Exception as e:
        print(f"❌ 執行錯誤: {e}")
        import traceback
        traceback.print_exc()
