# Multi-Agent Collaboration Playbook v2.0

星型 + 臨時網狀架構 (Hub & Spoke + Temporary Mesh) + 企業級規範

---

## v2.0 新增內容

| 模組 | 內容 |
|------|------|
| 設計模式 | ReAct、Chain of Thought、Reflection |
| 錯誤處理 | L1-L4 分類、熔斷機制、自我修復 |
| 監控 | 指標體系、警報規則 |
| 測試 | 單元/整合/E2E、效能、安全 |

---

## 概述

本 playbook 定義了多 Agent 協作的標準流程，適用於：
- 複雜專案需要多人協作
- 需要任務分工與質量把關
- 追求可重複、可優化的協作模式
- 企業級品質要求

---

## Phase 1: 初始化（項目啟動 - 執行一次）

### Step 1: 定義 Agent 角色矩陣

**任務：**
- [ ] 列出團隊成員對應的 Agent 角色
- [ ] 定義每個 Agent 的能力範圍
- [ ] 設定匯報關係

**產出：**

# Agent Role Matrix

| Agent ID | 角色 | 能力範圍 | 匯報給 |
|----------|------|----------|--------|
| @pm-agent | Project Manager | 任務拆分、進度追蹤 | - |
| @dev-agent-1 | Frontend Dev | React/Vue/UI開發 | @pm-agent |
| @dev-agent-2 | Backend Dev | API/數據庫/架構 | @pm-agent |
| @research-agent | Tech Research | 調研、技術選型 | @pm-agent |
| @review-agent | QA/Review | 測試、審查 | @pm-agent |

---

### Step 2: 建立通訊協議

**任務：**
- [ ] 統一任務描述格式
- [ ] 定義狀態碼
- [ ] 設定升級機制

**產出：**

## 通訊協議

### 任務格式
```
[FROM] → [TO] : [任務描述] @[優先級P0-P3]
```

### 狀態碼
| 狀態 | 意義 |
|------|------|
| ✅ 完成 | 任務已完成 |
| ⏳ 進行中 | 正在執行 |
| ❌ 阻塞 | 需升級處理 |
| 🔄 需要協助 | 需要其他 Agent 支援 |

### 升級條件
- 阻塞 > 30分鐘
- 需求不明確
- 發現重大風險
- 信心度 < 0.7

---

## Phase 2: 日常協作（每天循環）

### Step 3: 每日站會 → 任務分配

**任務：**
- [ ] PM Agent 收集各 Agent 昨日進度
- [ ] 確認今日任務清單
- [ ] 識別並行任務 vs 依賴任務
- [ ] 分配任務給各 Agent

**使用的 Skill：**
- `dispatching-parallel-agents` — 識別哪些任務可以並行

---

### Step 4: 並行執行

**任務：**
- [ ] 獨立的 Agent 開始執行
- [ ] 定期匯報進度
- [ ] 記錄 blocker

**使用的 Skill：**
- `sessions_spawn` — 為每個任務啟動獨立 Agent session
- `subagent-driven-development` — 管理子 Agent

---

### Step 5: 依賴任務協調（臨時網狀）

**任務：**
- [ ] 追蹤依賴關係
- [ ] 當 Agent A 完成 → 觸發 Agent B
- [ ] 處理跨 Agent 的數據傳遞

**使用的 Skill：**
- `sessions_send` — 跨 session 發送訊息
- `subagents(action=list)` — 查看所有 active agents

---

### Step 6: 質量把關

**任務：**
- [ ] 代碼提交後自動觸發 Review
- [ ] Review Agent 進行檢查
- [ ] 通過 → 合併；不通過 → 打回

**使用的 Skill：**
- `requesting-code-review` — 觸發審查流程
- `verification-before-completion` — 交付前驗證

---

### Step 7: 每日彙總

**任務：**
- [ ] 收集各 Agent 今日完成情況
- [ ] 識別 blocker 和風險
- [ ] 記錄 decisions（日誌）

**使用的 Skill：**
- `subagents(action=list)` — 查看所有 agents 狀態
- 寫入 `memory/YYYY-MM-DD.md`

---

## Phase 3: 設計模式（企業級）

### 3.1 基礎設計模式

#### ReAct Pattern（推理 + 行動）

```
輸入 → 推理 → 行動 → 觀察 → 輸出
 ↑__________________↓
```

**適用場景**：需要多步推理的複雜任務

**實現原則**：
- 每個循環包含：Thought → Action → Observation
- 最大循環次數：5-10次
- 失敗則重試或上報

---

#### Chain of Thought（思維鏈）

```
問題 → 分解 → 子問題1 → 子問題2 → 子問題3 → 整合 → 答案
```

**適用場景**：數學、邏輯、複雜決策

**實現原則**：
- 強制輸出思考過程
- 每步必須可追溯
- 保留中間結論

---

#### Reflection Pattern（自我反思）

```
執行 → 結果 → 自我審查 → [通過?] → 是 → 輸出
 ↓ 否
 修正 → 重新執行
```

**適用場景**：重要輸出需要品質把關

**實現原則**：
- 輸出前必須自審
- 記錄審查過程
- 失敗可修正重試

---

### 3.2 協作模式

#### Master-Slave Pattern

```
Master Agent
 ├── 分解任務
 ├── 分派子任務
 ├── 收集結果
 └── 整合輸出
 ↑
 Slave Agent 1, 2, 3...
```

**實現原則**：
- Master 負責協調
- Slave 負責執行
- 清晰定義介面

---

#### Pipeline Pattern

```
輸入 → Agent A → Agent B → Agent C → 輸出
 (預處理) (核心處理) (後處理)
```

**實現原則**：
- 每個 Agent 有明確定義
- 數據格式標準化
- 錯誤會傳遞

---

### 3.3 企業級模式

#### Human-in-the-Loop

```
Agent → 提案 → 人類審批 → [通過?] → 是 → 執行
 ↓ 否
 修正 → 重新提案
```

**實現原則**：
- 關鍵節點需要人類批准
- 定義審批觸發條件
- 記錄審批歷史

**審批觸發條件**：
| 條件 | 閾值 | 動作 |
|------|------|------|
| 敏感操作 | - | 始終審批 |
| 信心度 | < 0.7 | 審批 |
| 多次重試 | > 3次 | 審批 |
| 費用估計 | > $10 | 審批 |
| 重大變更 | - | 審批 |

---

#### Checkpoint Pattern

```
執行中 → 檢查點1 → 檢查點2 → 檢查點3 → 完成
 ↓ ↓ ↓
 [停頓?] [停頓?] [停頓?]
```

**實現原則**：
- 定義明確的檢查點
- 每點可暫停/恢復
- 支援狀態保存

---

## Phase 4: 錯誤處理與修復

### 4.1 錯誤分類體系

| 層級 | 類型 | 影響範圍 | 處理方式 |
|------|------|----------|----------|
| **L1** | 輸入錯誤 | 單次請求 | 立即返回 |
| **L2** | 工具錯誤 | 單次任務 | 重試 |
| **L3** | 執行錯誤 | 任務流程 | 降級/上報 |
| **L4** | 系統錯誤 | 整體系統 | 熔斷/報警 |

---

### 4.2 錯誤碼定義

| 錯誤碼 | 說明 | 建議動作 |
|--------|------|----------|
| E1001 | 輸入無效 | 返回錯誤，不重試 |
| E1002 | 缺少必要字段 | 返回錯誤，不重試 |
| E2001 | 工具不存在 | 返回錯誤，不重試 |
| E2002 | 工具失敗 | 重試或更換工具 |
| E2003 | 工具超時 | 增加超時或優化 |
| E3001 | 執行失敗 | 降級或上報 |
| E3002 | 超過重試次數 | 上報人類 |
| E4001 | 系統過載 | 熔斷 |
| E4002 | 速率限制 | 等待後重試 |

---

### 4.3 修復策略

| 錯誤類型 | 修復策略 | 最大嘗試 |
|----------|----------|----------|
| TOOL_FAILED | 指數退避重試 | 3 |
| TOOL_TIMEOUT | 增加超時 | 2 |
| CONTEXT_OVERFLOW | 壓縮上下文 | 2 |
| RESOURCE_EXHAUSTED | 減少範圍 | 1 |
| LOW_CONFIDENCE | 請求澄清 | 1 |

---

### 4.4 熔斷機制

```
CLOSED → 正常運行
OPEN → 熔斷中，拒絕請求
HALF_OPEN → 測試恢復
```

**實現原則**：
- 失敗次數閾值：5
- 恢復超時：60秒
- 半開狀態測試：3次

---

## Phase 5: 監控與警報

### 5.1 核心指標

#### 業務指標

| 指標名稱 | 目標 |
|----------|------|
| task_success_rate | > 95% |
| avg_task_duration | < 60s |

#### 效能指標

| 指標名稱 | 目標 |
|----------|------|
| response_time_p95 | < 5s |
| throughput | > 100/s |

#### 品質指標

| 指標名稱 | 目標 |
|----------|------|
| confidence_score | > 0.8 |
| human_intervention_rate | < 5% |
| error_rate | < 1% |

---

### 5.2 警報規則

#### 嚴重警報 (critical)

| 警報 | 條件 |
|------|------|
| AgentDown | 停止運行 > 1m |
| HighErrorRate | 錯誤率 > 20% |
| TaskTimeout | 超時 > 10/m |

#### 警告警報 (warning)

| 警報 | 條件 |
|------|------|
| HighLatency | P95 > 5s |
| LowConfidence | 平均 < 0.7 |
| HighRetryRate | 重試率 > 15% |
| QueueBuildup | 排隊 > 100 |

---

### 5.3 監控日誌格式

```json
{
 "timestamp": "2026-03-17T12:00:00Z",
 "level": "INFO",
 "agent_id": "agent-001",
 "task_id": "task-001",
 "event": "task_start",
 "context": {},
 "metrics": {}
}
```

**關鍵事件**：
- task_start, task_complete
- tool_call, tool_result
- error, retry, human_approval

---

## Phase 6: 測試

### 6.1 測試金字塔

```
     E2E 測試 (少，關鍵場景)
  整合測試 (中，跨模組)
   單元測試 (多，基本功能)
```

### 6.2 測試類別

| 類別 | 範圍 | 自動化程度 |
|------|------|------------|
| 單元測試 | 單一函數/方法 | 高 |
| 整合測試 | 多模組協作 | 高 |
| E2E測試 | 完整工作流 | 中 |
| 效能測試 | 負載/響應時間 | 中 |
| 安全測試 | 漏洞/權限 | 低 |

---

### 6.3 效能指標閾值

| 指標 | 目標 | 警告閾值 | 嚴重閾值 |
|------|------|----------|----------|
| 響應時間 P95 | < 2秒 | > 3秒 | > 5秒 |
| 吞吐量 | > 100 req/s | < 80 req/s | < 50 req/s |
| 錯誤率 | < 1% | > 2% | > 5% |

---

### 6.4 安全測試

| 測試 | 內容 |
|------|------|
| Prompt Injection | 惡意輸入攔截 |
| Data Isolation | 會話數據隔離 |
| Permission Escalation | 權限提升防護 |

---

## Phase 7: 每週優化

### Step 8: 流程回顧

**任務：**
- [ ] 回顧本週協作順暢度
- [ ] 識別瓶頸
- [ ] 調整角色定義或流程

**使用的 Skill：**
- `memory_search` — 搜索過去一週的日誌
- 讀取 `MEMORY.md` 更新最佳實踐

---

## 關鍵 Skill 快速參考

| 場景 | Skill | 命令 |
|------|-------|------|
| 啟動多個子任務 | dispatching-parallel-agents | 輸入任務列表，自動識別並行 |
| 創建子 Agent | sessions_spawn | 指定 runtime="subagent" |
| 子 Agent 間通訊 | sessions_send | 跨 session 發訊息 |
| 查看所有 Agent | subagents(action=list) | 獲取狀態 |
| 代碼審查 | requesting-code-review | 觸發審查流程 |
| 交付前驗證 | verification-before-completion | 確認通過後再標記完成 |
| Debug 問題 | systematic-debugging | 結構化排查 |
| 環境隔離 | using-git-worktrees | 每個任務獨立的 git 環境 |

---

## 代碼規範摘要

### 命名規範

| 類型 | 規範 | 範例 |
|------|------|------|
| Agent 名稱 | 小寫 + 連字符 | `code-review-agent` |
| 方法名稱 | 駝峰式 | `analyzeCode()` |
| 常量 | 全大寫 + 底線 | `MAX_RETRIES` |

### 標準輸入格式

```yaml
input:
 task: "任務描述"
 context: "上下文信息"
 constraints: ["約束1", "約束2"]
 metadata:
 user_id: ""
 session_id: ""
 timestamp: ""
```

### 標準輸出格式

```yaml
output:
 result: "執行結果"
 reasoning: "推理過程"
 confidence: 0.95
 next_steps: []
 metadata:
 agent: ""
 duration_ms: 0
 tokens_used: 0
```

---

## 常見坑與解決

| 坑 | 解決方案 |
|----|----------|
| Agent 各自為政，沒有匯報 | 強制每個 task 結束時返回標準格式 |
| 依賴關係漏掉 | 用 dispatching-parallel-agents 自動識別 |
| 重複勞動 | 統一 memory 寫入，避免信息孤島 |
| 卡住沒人支援 | 設定 30 分鐘升級機制 |
| 錯誤蔓延 | L1-L4 分類，即時隔離 |
| 系統雪崩 | 熔斷機制，防止級聯失敗 |

---

## 總結

> 一句話：每天早會用 dispatching-parallel-agents 分配任務，中間用 sessions_send 協調依賴，晚上寫入 memory。遇到錯誤用 L1-L4 分類處理，透過監控儀表板追蹤品質。

---

## 版本資訊

| 版本 | 日期 | 備註 |
|------|------|------|
| v1.0 | 2026-03-17 | 初始版本 |
| v2.0 | 2026-03-17 | 整合設計模式 + 錯誤處理 + 監控 + 測試 |

---

## 參考文檔

- `memory/knowledge/agent-development-standards.md` - 設計模式與代碼規範
- `memory/knowledge/agent-self-healing.md` - 錯誤處理與自我修復
- `memory/knowledge/agent-monitoring-dashboard.md` - 監控儀表板
- `memory/knowledge/agent-testing-framework.md` - 測試框架
