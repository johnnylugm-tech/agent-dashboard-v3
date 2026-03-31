---
name: persistent-agent
description: "增強 Agent 持久化能力：跨會話記憶傳遞、任務狀態追蹤、主動進度回報、長期目標推進"
---

# Persistent Agent Skill

增強 Agent 的持久化運作能力，確保任務跨會話持續推進。

## 現有持久化機制

OpenClaw 本身已具備持久化架構：

| 組件 | 功能 |
|------|------|
| **Gateway** | 訊息路由與會話管理 |
| **Memory** | 對話歷史自動壓縮儲存 |
| **Skills** | 擴展能力持久化 |
| **Cron** | 定時任務跨會話執行 |
| **Heartbeat** | 主動檢查與狀態監控 |

## 新增持久化能力

### 1. 任務狀態追蹤

```
~/.openclaw/workspace/memory/tasks/
├── active.json      # 進行中任務
├── pending.json     # 待處理任務
├── completed.json  # 已完成任務
└── failed.json     # 失敗任務
```

### 2. 跨會話任務傳遞

每當對話結束，若有未完成任務：
- 自動寫入 `active.json`
- 下次會話自動載入並繼續

### 3. 主動進度回報

- 完成關鍵步驟主動通知
- 定時匯報任務進度
- 阻塞時及時預警

### 4. 長期目標推進

```json
// goals/boss.json
{
  "active_goals": [
    {
      "id": "goal_001",
      "title": "建立完整知識庫",
      "milestones": [
        {"id": "m1", "title": "安裝長期記憶", "status": "done"},
        {"id": "m2", "title": "建立 Ontology", "status": "in_progress"},
        {"id": "m3", "title": "整合外部資料", "status": "pending"}
      ],
      "created": "2026-03-02"
    }
  ]
}
```

## 運作流程

### 接收任務
1. 解析任務目標與里程碑
2. 寫入 `goals/boss.json`
3. 建立檢查點

### 執行任務
1. 每步驟完成更新狀態
2. 記錄關鍵決策
3. 主動摘要進度

### 任務完成/失敗
1. 寫入 `completed.json` 或 `failed.json`
2. 提取教訓到 `LEARNINGS.md`
3. 通知用戶

## 觸發條件

| 觸發 | 動作 |
|------|------|
| 用戶說「繼續上次任務」 | 載入 `active.json` |
| 用戶說「我的目標是...」 | 建立新 goal |
| 用戶說「進度怎樣」 | 匯報所有 goals |
| 長時間無回應 | 主動提醒任務狀態 |

## 查詢指令

```
!tasks active      # 查看進行中任務
!tasks pending    # 查看待處理
!tasks completed  # 查看已完成
!goals            # 查看長期目標
!status           # 完整狀態報告
```

## 與現有系統整合

- **Cron** → 定時檢查任務進度
- **Memory** → 對話歷史支撐
- **Long-term-memory** → 詳細記錄
- **Ontology** → 結構化目標圖譜

## 安全考量

- 所有數據存於本地
- 敏感任務可標記加密
- 定時清理已完成任務

---

## 知識庫建構

### 自動建構 (每日 23:00)

系統自動執行：
1. 分析當日對話
2. 提取偏好/禁忌/目標
3. 更新知識模型

### 手動觸發

```bash
# 立即執行知識提取
python3 ~/.openclaw/scripts/extract_preferences.py

# 產生摘要
bash ~/.openclaw/scripts/knowledge_builder.sh
```

### 查詢知識模型

```bash
# 查看當前偏好
cat ~/.openclaw/workspace/memory/longterm/preferences/boss.json

# 查看完整知識模型
cat ~/.openclaw/workspace/memory/longterm/knowledge_model.json

# 查看今日摘要
ls ~/.openclaw/workspace/memory/daily_summary_*.md
```

### 知識更新觸發

| 觸發 | 動作 |
|------|------|
| 用戶明確說「記住我的偏好」 | 更新 preferences |
| 用戶修正你 | 記錄到 taboos |
| 用戶設定目標 | 記錄到 goals |
| 每天 23:00 | 自動全量建構 |


---

## 自動優化響應系統

### 核心功能

| 功能 | 說明 |
|------|------|
| **風格分析** | 學習用戶說話方式 |
| **需求預測** | 主動預測下一步 |
| **質量優化** | 持續改進回應 |
| **主動出擊** | 預先準備答案 |

### 數據流

```
對話 → database.jsonl → 優化引擎 → response_rules.json → 回應調整
                              ↓
                       knowledge_model.json
```

### 執行命令

```bash
# 手動執行優化
python3 ~/.openclaw/scripts/optimize_responses.py

# 查看當前規則
cat ~/.openclaw/workspace/memory/optimization/response_rules.json
```

### 優化維度

- 訊息長度偏好
- 格式偏好 (條列/表格/純文字)
- 語言風格
- 指令模式
- 提問習慣
- 回應速度優化

### 主動預測

根據歷史模式，主動猜測用戶可能需要的操作：
- 常見指令捷徑
- 相關功能建議
- 下一步提醒
