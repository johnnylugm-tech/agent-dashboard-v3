# 📖 安裝教學

> 5 分鐘快速上手 AI Agent 開發工具箱

---

## 前置需求

| 需求 | 版本 | 說明 |
|------|------|------|
| Python | 3.8+ | [下載](https://www.python.org/) |
| pip | 20.0+ | Python 內建 |

---

## 安裝步驟

### 1. 安裝 Model Router

```bash
pip install model-router
```

### 2. 安裝 Agent Quality Guard

```bash
pip install agent-quality-guard
```

### 3. 驗證安裝

```bash
# 檢查版本
model-router --version
agent-quality-guard --version
```

---

## 快速範例

### 範例 1：自動選模型

```bash
model-router --task "幫我寫一個 Python 排序函數"
```

**輸出**：
```
✅ 已選擇模型：GPT-4o
💰 預估成本：$0.02
📝 任務類型：CODE_GENERATION
```

### 範例 2：低預算模式

```bash
model-router --task "翻譯這段文章" --budget low
```

**輸出**：
```
✅ 已選擇模型：Gemini 2.0 Flash
💰 預估成本：$0.001
📝 任務類型：TRANSLATION
```

### 範例 3：程式碼品質檢測

```bash
agent-quality-guard --file your_code.py
```

**輸出**：
```
📊 品質分數：95 (A)
🔒 安全性：100%
⚡ 效能：92%
```

---

## 配置文件

### 建立配置檔

建立 `~/.model-router/config.yaml`：

```yaml
# Model Router 配置
router:
  default_budget: medium
  preferred_providers:
    - openai
    - anthropic
  
# 成本限制
cost_limit:
  daily: 10
  monthly: 100
```

---

## 常见問題

### Q: 需要 API Key 嗎？

A: 是的，使用各 provider 前需要設定 API Key：

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Q: 支援哪些模型？

A: 目前支援 17+ 模型：

| Provider | 模型 |
|----------|------|
| OpenAI | GPT-4o, GPT-4o-mini |
| Anthropic | Claude Opus, Claude Sonnet |
| Google | Gemini 3.1 Pro, Gemini 2.0 Flash |
| DeepSeek | DeepSeek V4, V3 |
| MiniMax | Kimi K2.5, K1.5 |

---

## 下一步

- [架構說明](architecture.md) - 了解技術架構
- [整合教學](integration.md) - 與現有專案整合
- [版本比較](comparison.md) - 了解版本差異

---

*安裝有問題？請開 GitHub Issue*
