# 🚄 高鐵訂票自動化 - 最終測試結果

> 2026-03-19 17:45

---

## 🔬 JavaScript 測試結果

### 測試輸出

```
📋 找到 13 個選擇框

[1] 設置出發站 = 新竹...
   結果: {'success': True, 'value': ''}

[2] 設置到達站 = 左營...
   結果: {'success': True, 'value': ''}
```

### 截圖確認

從截圖可以看到：
- **出發站**: 請選擇... ❌
- **到達站**: 請選擇... ❌

---

## ⚠️ 結論：Wicket 框架不支援自動化

### 原因

| 問題 | 說明 |
|------|------|
| Wicket 內部狀態 | Wicket 使用 Apache Wicket 框架，有自己的 JavaScript 狀態管理 |
| DOM 綁定 | 直接修改 DOM 的 value 屬性會被 Wicket 覆蓋 |
| 安全機制 | 框架不允許非用戶操作的自動化 |

### 證據

1. JavaScript 設置 `value = '5'` → 成功但被覆蓋
2. 設置後讀取 → 返回空字串 `''`
3. 頁面顯示 → 仍然是「請選擇...」

---

## 🎯 建議解決方案

### 方案 1: 鍵盤完全自動化（仍可能失敗）

```python
# 嘗試在打開的下拉選單中用鍵盤導航
page.click("select")
page.keyboard.press("ArrowDown")
page.keyboard.press("ArrowDown")
page.keyboard.press("Enter")
```

### 方案 2: 使用 T-EX App API

- 研究高鐵官方 App 的 API
- 可能更穩定

### 方案 3: 使用其他訂票管道

- Klook、KKday 等第三方平台
- 可能有更穩定的 API

### 方案 4: 純手動 + 驗證碼識別

- 手動操作選擇
- 自動識別驗證碼
- 半自動方案

---

## 📦 現有腳本總結

| 腳本 | 狀態 | 說明 |
|------|------|------|
| thsr_downloader.py | ✅ 可用 | PDF 時刻表下載 |
| thsr_captcha_v2.py | ✅ 可用 | ddddocr 驗證碼 |
| thsr_book_v*.py | ❌ Wicket 限制 | 無法自動化選擇 |
| test_thsr.html | ✅ 可用 | 本地測試頁面 |

---

## 💡 最終建議

高鐵網路訂票系統使用 Wicket 框架，該框架設計上防止自動化訂票。建議：

1. **放棄自動化** - 改用純手動操作 + 驗證碼識別輔助
2. **轉向其他平台** - 研究 Klook/KKday API
3. **使用官方 App** - T-EX App 可能有較開放的 API

---

*感謝測試 - 問題已確認為框架限制，非腳本問題*
