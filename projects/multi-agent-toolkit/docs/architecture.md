# 🏗️ Multi-Agent Collaboration Toolkit 架構

---

## 系統總覽

```
┌─────────────────────────────────────────────────────────────┐
│              Multi-Agent Collaboration Toolkit               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Planner   │  │  Executor   │  │  Monitor    │        │
│  │             │  │             │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│                          ▼                                  │
│               ┌─────────────────────┐                     │
│               │   Communication     │                     │
│               │       Hub           │                     │
│               └─────────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心模組

### 1. Planner (規劃器)

```
src/planner/
├── task_splitter.py    # 任務拆分
├── dependency_graph.py  # 依賴圖
└── scheduler.py        # 排程器
```

**職責**：
- 將複雜任務拆分為子任務
- 建立任務依賴關係
- 排定執行順序

### 2. Executor (執行器)

```
src/executor/
├── agent_pool.py       # Agent 池
├── task_router.py      # 任務路由
└── result_aggregator.py # 結果聚合
```

**職責**：
- 管理 Agent 生命週期
- 路由任務到合適的 Agent
- 聚合多個 Agent 的結果

### 3. Monitor (監控)

```
src/monitor/
├── health_score.py     # 健康評分
├── cost_tracker.py    # 成本追蹤
└── alert_manager.py  # 警報管理
```

**職責**：
- 追蹤執行狀態
- 計算健康評分
- 觸發警報

### 4. Communication Hub (通訊中心)

```
src/communication/
├── message_bus.py     # 訊息匯流排
├── state_manager.py   # 狀態管理
└── event_dispatcher.py # 事件分發
```

**職責**：
- Agent 間訊息傳遞
- 共享狀態管理
- 事件驅動協作

---

## 數據流

```
User Input
    │
    ▼
┌─────────────┐
│   Planner   │ ───> 任務拆分
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Executor  │ ───> Agent 執行
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Monitor   │ ───> 品質檢查
└──────┬──────┘
       │
       ▼
    Result
```

---

## 錯誤處理流程

```
Error occurs
    │
    ▼
┌─────────────┐
│  L1/L2/L3   │ ───> 根據等級處理
│  Classifier │
└──────┬──────┘
       │
       ├── L1 ──> Return error
       │
       ├── L2 ──> Retry 3x
       │
       ├── L3 ──> Fallback
       │
       └── L4 ──> Circuit break + Alert
```

---

## 部署架構

### 本地開發

```
┌─────────────┐
│   Python    │
│   Script    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Local    │
│   Toolkit   │
└─────────────┘
```

### 雲端部署

```
┌─────────────┐
│   Load      │
│  Balancer   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  API Server │ ───> ┌─────────────┐
└─────────────┘      │   Worker   │
       │             │  (Agents)  │
       ▼             └─────────────┘
┌─────────────┐
│  Database   │
└─────────────┘
```

---

## 擴展點

| 擴展點 | 說明 | 檔案 |
|--------|------|------|
| 新 Agent 類型 | 繼承 Agent 類別 | `src/agent/base.py` |
| 新工具 | 實作 Tool 介面 | `src/tools/` |
| 新監控指標 | 新增 MetricCollector | `src/monitor/` |
| 新儲存 | 實作 Storage 介面 | `src/storage/` |

---

## 安全設計

- API Key 管理：環境變數
- 敏感資料：加密儲存
- 審計日誌：完整記錄
- 權限控制：RBAC

---

*最後更新：2026-03-20*
