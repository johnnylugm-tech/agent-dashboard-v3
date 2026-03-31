# 🚄 高鐵訂票自動化 - 研究報告

> 研究時間：2026-03-19

---

## 📊 現有資源

### 開源方案

| 項目 | 語言 | 狀態 | 特色 |
|------|------|------|------|
| THSR-Ticket | Python | 正常運行 | CLI 訂票、成人票 |
| thsrc_captcha | Python/Keras | 可用 | CNN 驗證碼識別 |
| TRA-Ticket-Booker | Python/Selenium | 已過時 | 臺鐵訂票 |

### 技術難點

| 難點 | 說明 | 解決方案 |
|------|------|----------|
| Wicket 框架 | 動態 ID，選擇器不穩定 | XPath/Fixed selector |
| 驗證碼 | OCR 識別困難 | ddddocr / CNN |
| 登入會員 | 需要 TGo 會員 | 可選 |
| 早鳥票 | 搶票競爭激烈 | 提前監測 |

---

## 🔧 技術架構

### 方案 A：基於現有開源優化

```
1. Clone THSR-Ticket
2. 整合我們的時刻表數據
3. 改進驗證碼識別
4. 添加監控功能
```

### 方案 B：從頭開發（推薦）

```
┌─────────────────┐
│   時刻表 API     │ ← 我們現有 (PDF 解析)
├─────────────────┤
│   班次查詢       │ ← requests + parsing
├─────────────────┤
│   驗證碼識別     │ ← ddddocr / CNN
├─────────────────┤
│   訂票流程       │ ← Playwright / Selenium
├─────────────────┤
│   監控告警       │ ← Agent Monitor 整合
└─────────────────┘
```

---

## 📈 執行規劃

### Phase 1：基礎功能

- [x] 時刻表下載
- [x] 票價數據
- [ ] 班次查詢（網頁爬蟲）
- [ ] 驗證碼識別

### Phase 2：訂票功能

- [ ] 自動填表
- [ ] 登入會員
- [ ] 提交訂單

### Phase 3：企業級

- [ ] 錯誤處理
- [ ] 重試機制
- [ ] 監控整合

---

## 🎯 關鍵技術

### 1. 驗證碼識別

```python
# 使用 ddddocr
import ddddocr

ocr = ddddocr.DdddOcr()
with open('captcha.jpg', 'rb') as f:
    result = ocr.classification(f.read())
print(result)
```

### 2. Wicket 選擇器

```python
# 不要用動態 ID
# 使用 XPath 或固定屬性
page.locator('xpath=//select[@id="BookingS1Form_ddlTicket"]').select_option('1')

# 或使用文本
page.locator('select:has-text("新竹")').first.select_option('5')
```

### 3. 搶票時機

| 類型 | 開放時間 | 難度 |
|------|----------|------|
| 一般票 | 開放日前 28 天 | 中 |
| 早鳥票 | 開放日前 28 天 | 高 |
| 剩餘票 | 每天 06:00 | 低 |

---

## 📦 現有檔案

| 檔案 | 功能 |
|------|------|
| `thsr_downloader.py` | PDF 時刻表下載 |
| `thsr_api.py` | API 服務 |
| `thsr_captcha.py` | 驗證碼識別 |
| `thsr_book.py` | Playwright 訂票 |

---

## 🔜 下一步

1. 安裝 ddddocr
2. 測試現有 thsr_book.py
3. 修復選擇器問題
4. 整合監控

---

*更新：2026-03-19*
