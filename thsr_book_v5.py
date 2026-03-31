#!/usr/bin/env python3
"""
高鐵訂票自動化 v5 - 最終修復版

使用 JavaScript evaluate 直接操作 DOM，繞過 Wicket combobox
"""

import time
import os
import sys

# 站點對應
STATIONS = {
    "南港": "1", "台北": "2", "板橋": "3", "桃園": "4", "新竹": "5",
    "苗栗": "6", "台中": "7", "彰化": "8", "雲林": "9", "嘉義": "10",
    "台南": "11", "左營": "12"
}


def create_test_page():
    """創建本地測試頁面來調試選擇器"""
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>THSR Test</title>
    <style>
        select { padding: 10px; margin: 5px; }
        .result { margin-top: 20px; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>高鐵訂票測試</h1>
    
    <select id="fromStation">
        <option value="">請選擇...</option>
        <option value="1">南港</option>
        <option value="2">台北</option>
        <option value="3">板橋</option>
        <option value="4">桃園</option>
        <option value="5" selected>新竹</option>
        <option value="6">苗栗</option>
        <option value="7">台中</option>
        <option value="8">彰化</option>
        <option value="9">雲林</option>
        <option value="10">嘉義</option>
        <option value="11">台南</option>
        <option value="12">左營</option>
    </select>
    
    <br>
    
    <select id="toStation">
        <option value="">請選擇...</option>
        <option value="1">南港</option>
        <option value="2">台北</option>
        <option value="3">板橋</option>
        <option value="4">桃園</option>
        <option value="5">新竹</option>
        <option value="6">苗栗</option>
        <option value="7">台中</option>
        <option value="8">彰化</option>
        <option value="9">雲林</option>
        <option value="10">嘉義</option>
        <option value="11">台南</option>
        <option value="12" selected>左營</option>
    </select>
    
    <br><br>
    <button onclick="showValues()">顯示選擇的值</button>
    
    <div class="result" id="result"></div>
    
    <script>
        function showValues() {
            const from = document.getElementById('fromStation').value;
            const to = document.getElementById('toStation').value;
            document.getElementById('result').innerHTML = 
                '出發站: ' + from + '<br>到達站: ' + to;
        }
    </script>
</body>
</html>
    '''
    
    with open("test_thsr.html", "w") as f:
        f.write(html)
    print("✅ 測試頁面已創建: test_thsr.html")


def test_with_playwright():
    """使用 Playwright 測試"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("\n🚀 使用 Playwright 測試...")
        
        with sync_playwright() as p:
            # 啟動瀏覽器
            browser = p.chromium.launch(
                headless=False,  # 可視化
                args=['--disable-web-security']  # 允許跨域
            )
            context = browser.new_context()
            page = context.new_page()
            
            # 監聽 console
            page.on("console", lambda msg: print(f"   [Console] {msg.text}"))
            
            # 訪問測試頁面
            test_file = os.path.abspath("test_thsr.html")
            page.goto(f"file://{test_file}")
            
            print("✅ 測試頁面載入成功")
            
            # 測試 JavaScript 操作
            print("\n📝 測試 JavaScript 操作...")
            
            # 方法 1: 直接設置 value
            result = page.evaluate('''
                () => {
                    const fromSel = document.getElementById('fromStation');
                    fromSel.value = '5';
                    
                    // 觸發 change 事件
                    fromSel.dispatchEvent(new Event('change', { bubbles: true }));
                    
                    return {
                        value: fromSel.value,
                        selectedText: fromSel.options[fromSel.selectedIndex].text
                    };
                }
            ''')
            print(f"   設置結果: {result}")
            
            # 等待
            page.wait_for_timeout(1000)
            
            # 點擊按鈕顯示結果
            page.click("button")
            page.wait_for_timeout(500)
            
            print("\n✅ Playwright 測試成功!")
            
            # 保持瀏覽器開啟
            print("\n🔵 瀏覽器保持開啟中... (按 Ctrl+C 結束)")
            time.sleep(30)
            
            browser.close()
            
    except ImportError:
        print("❌ 請安裝 Playwright: pip install playwright")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()


def test_real_thsr():
    """測試真實高鐵網站"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("\n🚀 訪問真實高鐵網站...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=['--disable-web-security']
            )
            page = browser.new_page()
            
            # 訪問高鐵
            try:
                page.goto("https://irs.thsrc.com.tw/IMINT/?locale=tw", 
                          timeout=60000)
                page.wait_for_load_state("domcontentloaded")
                print("✅ 頁面載入成功")
                
                # 等待表單加載
                page.wait_for_selector("select", timeout=30000)
                
                # 獲取所有 select 元素
                selects = page.query_selector_all("select")
                print(f"   找到 {len(selects)} 個選擇框")
                
                # 嘗試 JavaScript 設置
                print("\n📝 嘗試 JavaScript 設置...")
                
                # 設置出發站 = 新竹 (value=5)
                result = page.evaluate('''
                    () => {
                        const selects = document.querySelectorAll('select');
                        if (selects.length >= 2) {
                            selects[0].value = '5';
                            selects[0].dispatchEvent(new Event('change', { bubbles: true }));
                            return { success: true, value: selects[0].value };
                        }
                        return { success: false, error: 'Not enough selects' };
                    }
                ''')
                print(f"   結果: {result}")
                
                # 設置到達站 = 左營 (value=12)
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
                
                # 設置時間 = 09:00
                result3 = page.evaluate('''
                    () => {
                        const selects = document.querySelectorAll('select');
                        if (selects.length >= 3) {
                            selects[2].value = '0900';
                            selects[2].dispatchEvent(new Event('change', { bubbles: true }));
                            return { success: true, value: selects[2].value };
                        }
                        return { success: false };
                    }
                ''')
                print(f"   時間結果: {result3}")
                
                print("\n✅ 高鐵網站測試完成!")
                
            except Exception as e:
                print(f"❌ 訪問失敗: {e}")
            
            # 保持開啟
            time.sleep(60)
            browser.close()
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")


def main():
    print("=" * 60)
    print("🚄 高鐵訂票自動化 v5 - JavaScript 修復測試")
    print("=" * 60)
    
    # 創建測試頁面
    create_test_page()
    
    # 選項
    print("\n請選擇測試模式:")
    print("1. 本地測試頁面")
    print("2. 真實高鐵網站")
    print("3. 兩都測試")
    
    choice = input("\n請輸入編號 (1-3): ").strip()
    
    if choice in ["1", "3"]:
        test_with_playwright()
    
    if choice in ["2", "3"]:
        test_real_thsr()


if __name__ == "__main__":
    main()
