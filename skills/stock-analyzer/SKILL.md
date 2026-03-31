---
name: stock-analyzer
description: "股票分析工具：根據股票代碼分析當前交易量、市場情況並給出投資策略。當：用戶給出股票名稱或代碼要求分析。NOT for：加密貨幣、虛擬貨幣，建議買賣（只能提供資訊和分析）。"
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["curl"]
    timeout: 300
---

# Stock Analyzer Skill

股票深度分析工具，結合當前交易量與市場情況給出策略建議。

## 執行建議

- **建議 Timeout**：300 秒（5 分鐘）
- **選擇權數據需要較多搜尋時間**，建議預留足夠時間

## When to Use

✅ **USE this skill when:**

- 用戶給出股票代碼要求分析（如「NVDA」、「AAPL」）
- 用戶要求股票策略建議
- 用戶查詢股票交易量

## When NOT to Use

❌ **DON'T use this skill when:**

- 加密貨幣分析 → 使用加密貨幣專門工具
- 虛擬貨幣 → 不提供分析
- 要求具體買賣建議 → 只能提供資訊和分析
- 短線當日交易 → 不提供當日沖銷建議
- 選擇權複雜策略 → 建議諮詢專業人士

## Analysis Process

### Step 1: 獲取基本數據
使用 stock-market-pro skill：
```bash
cd ~/.openclaw/workspace/skills/stock-market-pro && uv run --script scripts/yf.py price {SYMBOL}
```

### Step 2: 搜尋市場 Context
使用 tavily 或 web_search 搜尋相關新聞

### Step 3: 結構化輸出

## Output Format

### 1️⃣ 當前數據
| 項目 | 數據 | 來源 | 狀態 |
|------|------|------|------|
| 股價 | $XXX | Yahoo Finance | ✅ 已確認 |
| 交易量 | XXM | Yahoo Finance | ✅ 已確認 |
| 市值 | $X.XXT | Bloomberg | ✅ 已確認 |

### 2️⃣ 市場 Context
- 大盤趨勢
- 法人動向
- 產業趨勢

### 3️⃣ 財報數據（如有）
| 項目 | 數據 | 市場預期 |
|------|------|----------|
| 營收 | $XXB | $XXB ✅擊敗 |

### 4️⃣ 選擇權/期貨分析
| 項目 | 數據 | 說明 |
|------|------|------|
| IV (隱含波動率) | XX% | 高/中/低 |
| IV Rank | XX | 0-100 位置 |
| PCR | X.XX | >1 偏空，<1 偏多 |
| 最大痛點 | $XXX | 網站：options.maxpain.com |
| 支撐/壓力區 | $XXX / $XXX | 選擇權布局集中區 |

**選擇權策略建議（僅供參考）**：
| 策略 | 適用情境 | 說明 |
|------|----------|------|
| Covered Call | 溫和上漲 | 持有股票前提下賣出-call |
|  Protective Put | 避險需求 | 持有股票前提下買入-put |
|  Bull Call Spread | 温和看多 | 買入低價call + 賣出高價call |
|  Iron Condor | 區間震盪 | 賣出兩側選擇權收權利金 |

### 5️⃣ 策略建議
| 維度 | 分析 |
|------|------|
| 基本面 | 強/中/弱 |
| 技術面 | 支撐/壓力 |
| 交易量 | 放量/縮量 |
| 風險 | 高/中/低 |

### 5️⃣ 結論
| 策略 | 建議 |
|------|------|
| 短線 | 買/賣/觀望 |
| 長線 | 買/賣/觀望 |
| 選擇權 | 適合策略（如有）|

## 選擇權數據來源

- **IV 查詢**：Yahoo Finance Options頁面
- **PCR**：put/call ratio 
- **最大痛點**：options.maxpain.com
- **選擇權鏈**：券商APP或網站

## 狀態標示

| 標示 | 意義 |
|------|------|
| ✅ 已確認 | 來自可靠來源，可信度高 |
| ⚠️ 推測 | 搜尋結果有限，可能有誤差 |
| 🔗 連結 | 可直接點擊驗證 |

## Important Principles

1. **正確性 > 速度** — 不確定的資訊直接說「不知道」
2. **標註狀態** — 每個數據都要標註來源和狀態
3. **只提供分析** — 不給具體買賣建議
4. **提醒風險** — 最後一定要提醒「投資有風險，請自行評估」

## 安全提醒

- 此工具僅提供資訊和分析，不構成投資建議
- 使用前請務必了解相關風險
- 數據來源為 Yahoo Finance，請自行驗證
