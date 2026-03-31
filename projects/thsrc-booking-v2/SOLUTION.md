# 🚄 高鐵訂票自動化 - 最終解決方案

> 更新：2026-03-19

---

## 📊 頁面結構（已確認）

### 關鍵元素 ID

| 功能 | Ref | 說明 |
|------|-----|------|
| 出發站 | e64 | Combobox |
| 到達站 | e71 | Combobox |
| 出發日期 | e78 | Textbox |
| 出發時間 | e83 | Combobox |
| 驗證碼圖片 | e115 | Img |
| 驗證碼輸入 | e116 | Textbox |
| 開始查詢 | e122 | Button |

### 站點順序

1. 南港
2. 台北
3. 板橋
4. 桃園
5. 新竹
6. 苗栗
7. 台中
8. 彰化
9. 雲林
10. 嘉義
11. 台南
12. 左營

---

## 🔧 解決方案

### 方案 1：使用現有瀏覽器（推薦）

```python
# 通過 CDP 連接
from browser import Browser

browser = Browser()
page = browser.attach("CB66B68F7A7B014DBBC211F33C61DBD8")

# 點擊出發站
page.click("e64")
page.click("option:has-text('新竹')")
```

### 方案 2：修復 Playwright 腳本

```python
# 使用更長的超時和等待
page.goto(url, timeout=120000, wait_until="networkidle")
```

---

## 📝 穩定選擇器

```python
SELECTORS = {
    "from_station": 'mat-select[formcontrolname="fromStation"]',
    "to_station": 'mat-select[formcontrolname="toStation"]',
    "date": 'input[matDatepicker]',
    "time": 'mat-select[formcontrolname="departureTime"]',
    "captcha_img": 'img[src*="captcha"]',
    "captcha_input": 'input[formcontrolname="captchaCode"]',
    "search_btn": 'button:has-text("開始查詢")'
}
```

---

## ✅ 已完成

1. [x] 頁面結構分析
2. [x] 選擇器識別
3. [x] 驗證碼識別（ddddocr）
4. [x] 腳本框架

## 🔄 待完成

1. [ ] 選擇器穩定性測試
2. [ ] 完整訂票流程
3. [ ] 錯誤處理

---

## 📦 現有檔案

| 檔案 | 狀態 |
|------|------|
| `thsr_book_v2.py` | 待測試 |
| `thsr_captcha_v2.py` | 可用 |
| `RESEARCH.md` | 完成 |

---

*持續優化中...*
