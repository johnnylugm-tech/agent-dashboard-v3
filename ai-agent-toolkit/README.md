# 🎯 AI Agent 開發工具箱 - 整合版

> 統一的方法論 + 工具集

---

## 概述

這是整合後的 AI Agent 開發工具箱，包含：
- **方法論**：錯誤分類、任務生命週期、品質把關
- **工具**：Model Router、Agent Quality Guard、Agent Monitor
- **協作**：多 Agent 協作模式

---

## 安裝

```bash
pip install ai-agent-toolkit
```

---

## 整合的專案

| 專案 | 版本 | 狀態 |
|------|------|------|
| Agent Quality Guard | v1.0.3 | ✅ |
| Model Router | v1.0.1 | ✅ |
| Agent Monitor v2 | v2.1.0 | ✅ |
| Agent Monitor v3 | v3.2.0 | ✅ |
| methodology-v2 | v2.1.0 | ✅ |

---

## 模組

### 1. 方法論 (methodology)

```python
from ai_agent_toolkit import ErrorClassifier, Crew, Monitor

# 錯誤分類
classifier = ErrorClassifier()
level = classifier.classify(error)
# L1-L4

# Agent 協作
crew = Crew(agents, process="sequential")
result = crew.kickoff()

# 監控
monitor = Monitor()
health = monitor.get_health_score(agent_id)
```

### 2. Model Router

```python
from ai_agent_toolkit import Router

router = Router(budget="low")
result = router.route("寫一個排序函數")
print(f"使用模型: {result['model']}")
```

### 3. Agent Quality Guard

```bash
agent-quality-guard --file app.py --json
```

### 4. Agent Monitor

```python
from ai_agent_toolkit import AgentMonitor

monitor = AgentMonitor()
status = monitor.get_status()
```

---

## 方法論

### 錯誤分類 (L1-L4)

| 等級 | 類型 | 處理 |
|------|------|------|
| L1 | 輸入錯誤 | 立即返回 |
| L2 | 工具錯誤 | 重試 3 次 |
| L3 | 執行錯誤 | 降級處理 |
| L4 | 系統錯誤 | 熔斷 + 警報 |

### 開發流程

```
需求 → 優先級 → 開發 → 品質 → 文檔 → 發布
```

### 協作模式

| 模式 | 說明 |
|------|------|
| Sequential | 串聯 A→B→C |
| Parallel | 並行 |
| Hierarchical | 階層式 |

---

## 監控與警報

### 健康評分

```
100 - 全部成功
75  - 小問題
50  - 需要關注
25  - 嚴重問題
0   - 系統故障
```

### 警報

| 級別 | 條件 |
|------|------|
| 🔴 Critical | 健康 < 25 |
| 🟡 Warning | 健康 < 50 |
| 🔵 Info | 健康 < 75 |

---

## 發布檢查清單

```bash
□ 1. 版本號更新
□ 2. CHANGELOG 記錄
□ 3. README 更新
□ 4. docs/ 同步
□ 5. 測試通過
□ 6. GitHub Release
□ 7. (可選) ClawHub
```

---

## 版本

v2.1.0 - 整合版

---

*用 AI 技術改變世界*
