# 🚄 高鐵訂票系統 V2

## 專案目標
開發完整的高鐵訂票自動化系統

---

## 版本規劃

| 版本 | 功能 | 狀態 |
|------|------|------|
| **V1** | 時刻表下載 + 解析 | ✅ 完成 |
| **V2** | 班次查詢 + 訂票功能 | 🔄 開發中 |
| **V3** | JavaScript 注入方式 | 🆕 完成 |

---

## V1 功能

- [x] PDF 時刻表下載
- [x] JSON 解析輸出
- [x] 票價資料

---

## V2/V3 開發進度

### 技術方案

| 方案 | 說明 | 狀態 |
|------|------|------|
| Playwright 自動化 | 傳統點擊方式 | ⚠️ Wicket 框架問題 |
| JavaScript 注入 | 直接操作 DOM | ✅ 更穩定 |
| ddddocr 識別 | 驗證碼識別 | ✅ 可用 |

### 關鍵發現

1. **Wicket 框架**：高鐵使用 Wicket 框架，選擇器經常變化
2. **解決方案**：使用 JavaScript 直接操作 DOM
3. **驗證碼**：ddddocr 可正常識別

---

## 現有檔案

| 檔案 | 功能 |
|------|------|
| `thsr_downloader.py` | PDF 時刻表下載 |
| `thsr_captcha_v2.py` | ddddocr 驗證碼 |
| `thsr_book_v3.py` | 最新訂票腳本 |

---

## 使用方式

```bash
python3 thsr_book_v3.py
```

---

## 技術細節

### 站點對應

```python
STATIONS = {
    "南港": "1", "台北": "2", "板橋": "3", "桃園": "4", "新竹": "5",
    "苗栗": "6", "台中": "7", "彰化": "8", "雲林": "9", "嘉義": "10",
    "台南": "11", "左營": "12"
}
```

### JavaScript 注入

```javascript
// 直接設置 select 值
const selects = document.querySelectorAll('select');
selects[0].value = '5';  // 新竹
selects[1].value = '12'; // 左營
```

---

*更新：2026-03-19*
