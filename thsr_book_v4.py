#!/usr/bin/env python3
"""
高鐵訂票自動化 v4 - 使用 Browser CDP 连接

直接连接到已打开的浏览器会话
"""

import time
import subprocess
import os

# 站點對應
STATIONS = {
    "南港": "1", "台北": "2", "板橋": "3", "桃園": "4", "新竹": "5",
    "苗栗": "6", "台中": "7", "彰化": "8", "雲林": "9", "嘉義": "10",
    "台南": "11", "左營": "12"
}


def get_browser_target():
    """获取已打开的浏览器标签页"""
    try:
        result = subprocess.run(
            ["openclaw", "browser", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # 解析输出获取 tab ID
        # 这里需要根据实际输出格式调整
        return None
    except:
        return None


def execute_on_page(tab_id, script):
    """在指定标签页执行 JavaScript"""
    # 使用 browser action 执行
    pass


def manual_step_by_step():
    """
    分步手动操作指南
    配合已打开的浏览器
    """
    print("""
╔══════════════════════════════════════════════════════════╗
║          🚄 高鐵訂票自動化 - 操作指南                    ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  瀏覽器已打開高鐵訂票頁面，請按以下步驟操作：            ║
║                                                          ║
║  [1] 點擊「出發站」下拉選單                             ║
║      → 選擇：新竹                                        ║
║                                                          ║
║  [2] 點擊「到達站」下拉選單                              ║
║      → 選擇：左營                                        ║
║                                                          ║
║  [3] 點擊「出發日期」輸入框                              ║
║      → 輸入：2026/04/15                                 ║
║                                                          ║
║  [4] 點擊「出發時間」下拉選單                            ║
║      → 選擇：09:00                                      ║
║                                                          ║
║  [5] 輸入驗證碼（圖片中的文字）                          ║
║                                                          ║
║  [6] 點擊「開始查詢」                                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)


def create_automated_script():
    """创建自动化脚本（供用户在本地运行）"""
    
    script = '''#!/usr/bin/env python3
"""
高鐵訂票自動化 - 自動版
需要在本地終端運行
"""

import time
from playwright.sync_api import sync_playwright

STATIONS = {
    "南港": "1", "台北": "2", "板橋": "3", "桃園": "4", "新竹": "5",
    "苗栗": "6", "台中": "7", "彰化": "8", "雲林": "9", "嘉義": "10",
    "台南": "11", "左營": "12"
}

def book(from_station, to_station, date, time_hour):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 訪問頁面
        page.goto("https://irs.thsrc.com.tw/IMINT/?locale=tw", timeout=120000)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        
        # 點擊同意
        try:
            page.click("button:has-text('我同意')", timeout=2000)
        except:
            pass
        
        # 等待頁面加載完成
        page.wait_for_selector("select", timeout=30000)
        
        # 找到所有 select 元素
        selects = page.query_selector_all("select")
        print(f"找到 {len(selects)} 個選擇框")
        
        # 填寫表單
        # select[0] = 出發站
        # select[1] = 到達站  
        # select[2] = 出發時間
        # select[3] = 票數
        
        from_idx = STATIONS.get(from_station, "5")
        to_idx = STATIONS.get(to_station, "12")
        
        # 點擊並選擇
        page.click("select:nth-of-type(1)")
        time.sleep(0.5)
        page.select_option("select:nth-of-type(1)", from_idx)
        
        page.click("select:nth-of-type(2)")
        time.sleep(0.5)
        page.select_option("select:nth-of-type(2)", to_idx)
        
        # 選擇時間
        page.click("select:nth-of-type(3)")
        time.sleep(0.5)
        page.select_option("select:nth-of-type(3)", time_hour)
        
        # 等待用戶輸入驗證碼
        print("\\n請輸入驗證碼...")
        time.sleep(30)
        
        # 點擊查詢
        page.click("button:has-text('開始查詢')")
        
        # 等待結果
        page.wait_for_timeout(5000)
        
        # 獲取結果
        print("\\n查詢結果：")
        try:
            table = page.query_selector("table")
            if table:
                rows = table.query_selector_all("tr")
                for row in rows[:6]:
                    cols = row.query_selector_all("td")
                    if len(cols) >= 4:
                        print(f"  {cols[0].inner_text()} | {cols[1].inner_text()} -> {cols[2].inner_text()}")
        except:
            pass
        
        print("\\n完成！瀏覽器保持開啟...")
        time.sleep(60)
        browser.close()

if __name__ == "__main__":
    book("新竹", "左營", "2026/04/15", "09:00")
'''
    
    with open("/Users/johnny/.openclaw/workspace-musk/thsr_auto.py", "w") as f:
        f.write(script)
    
    print("✅ 自動化腳本已創建: thsr_auto.py")


if __name__ == "__main__":
    print("=" * 60)
    print("🚄 高鐵訂票自動化 v4")
    print("=" * 60)
    
    # 顯示手動操作指南
    manual_step_by_step()
    
    # 創建自動化腳本
    create_automated_script()
    
    print("""
📝 下一步：
1. 按照上面的指南在瀏覽器中手動操作
2. 或運行：python3 thsr_auto.py（需要在有網絡的環境）
""")
