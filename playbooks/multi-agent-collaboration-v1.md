# Multi-Agent Collaboration Playbook

星型 + 臨時網狀架構 (Hub & Spoke + Temporary Mesh) 完整操作手冊

---

## 概述

本 playbook 定義了多 Agent 協作的標準流程，適用於：
- 複雜專案需要多人協作
- 需要任務分工與質量把關
- 追求可重複、可優化的協作模式

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

## Phase 3: 每週優化

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

## 常見坑與解決

| 坑 | 解決方案 |
|----|----------|
| Agent 各自為政，沒有匯報 | 強制每個 task 結束時返回標準格式 |
| 依賴關係漏掉 | 用 dispatching-parallel-agents 自動識別 |
| 重複勞動 | 統一 memory 寫入，避免信息孤島 |
| 卡住沒人支援 | 設定 30 分鐘升級機制 |

---

## 總結

> 一句話：每天早會用 dispatching-parallel-agents 分配任務，中間用 sessions_send 協調依賴，晚上寫入 memory。

---

## 版本資訊

| 版本 | 日期 | 備註 |
|------|------|------|
| v1.0 | 2026-03-17 | 初始版本 |
