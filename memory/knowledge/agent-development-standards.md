# AI Agent 開發規範手冊

> 設計模式與最佳實踐

---

## 一、Agent 設計模式

### 1.1 基礎模式

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

### 1.2 協作模式

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

### 1.3 企業級模式

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

## 二、代碼規範

### 2.1 命名規範

| 類型 | 規範 | 範例 |
|------|------|------|
| Agent 名稱 | 小寫 + 連字符 | `code-review-agent` |
| 方法名稱 | 駝峰式 | `analyzeCode()` |
| 常量 | 全大寫 + 底線 | `MAX_RETRIES` |
| 配置檔 | 小寫 + 連字符 | `agent-config.yaml` |

---

### 2.2 輸入輸出規範

```yaml
# 標準輸入格式
input:
 task: "任務描述"
 context: "上下文信息"
 constraints: 
 - "約束1"
 - "約束2"
 metadata:
 user_id: ""
 session_id: ""
 timestamp: ""

# 標準輸出格式
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

### 2.3 錯誤處理規範

```python
class AgentError(Exception):
 """Agent 基礎錯誤類"""
 def __init__(self, code, message, recoverable=False):
 self.code = code
 self.message = message
 self.recoverable = recoverable

# 錯誤碼定義
ERROR_CODES = {
 "INVALID_INPUT": {"code": 1001, "recoverable": False},
 "TOOL_FAILED": {"code": 1002, "recoverable": True},
 "TIMEOUT": {"code": 1003, "recoverable": True},
 "RATE_LIMIT": {"code": 1004, "recoverable": True},
 "MAX_RETRIES": {"code": 1005, "recoverable": False},
}
```

---

### 2.4 日誌規範

```python
# 結構化日誌
log = {
 "timestamp": "2026-03-17T12:00:00Z",
 "agent": "code-review-agent",
 "level": "INFO",
 "event": "task_start",
 "task_id": "task-001",
 "context": {...},
}

# 關鍵事件必須記錄
LOG_EVENTS = [
 "task_start", # 任務開始
 "task_complete", # 任務完成
 "tool_call", # 工具調用
 "tool_result", # 工具結果
 "error", # 錯誤發生
 "retry", # 重試
 "human_approval", # 人類審批
]
```

---

## 三、流程規範

### 3.1 任務執行流程

```
1. 輸入驗證
 ├── 檢查必要欄位
 ├── 驗證資料格式
 └── [失敗?] → 返回錯誤

2. 上下文準備
 ├── 載入相關上下文
 ├── 檢索相關知識
 └── [超時?] → 使用預設

3. 執行規劃
 ├── 分解任務
 ├── 排列順序
 └── 估算時間

4. 執行監控
 ├── 記錄每步結果
 ├── 檢查是否偏離
 └── [異常?] → 暫停/重試

5. 品質檢查
 ├── 輸出自審
 ├── [不通過?] → 修正
 └── [通過?] → 輸出

6. 後處理
 ├── 記錄日誌
 ├── 更新狀態
 └── 通知相關方
```

---

### 3.2 人類審批觸發條件

| 條件 | 閾值 | 動作 |
|------|------|------|
| 敏感操作 | - | 始終審批 |
| 信心度 | < 0.7 | 審批 |
| 多次重試 | > 3次 | 審批 |
| 費用估計 | > $10 | 審批 |
| 重大變更 | - | 審批 |

---

### 3.3 監控指標

| 指標 | 閾值 | 警報 |
|------|------|------|
| 執行時間 | > 5分鐘 | ⚠️ 警告 |
| 執行時間 | > 10分鐘 | 🔴 嚴重 |
| 錯誤率 | > 10% | ⚠️ 警告 |
| 錯誤率 | > 30% | 🔴 嚴重 |
| 信心度 | < 0.6 | ⚠️ 警告 |
| Token使用 | > 50000 | ⚠️ 警告 |

---

## 四、安全規範

### 4.1 數據處理

```yaml
data_classification:
 public:
 - 公開文檔
 - 範例代碼
 
 internal:
 - 內部流程
 - 會議記錄
 
 confidential:
 - 用戶數據
 - API 金鑰
 - 商業機密

handling_rules:
 confidential:
 - 不傳輸到外部
 - 不記錄日誌
 - 加密存儲
```

---

### 4.2 權限控制

```yaml
permission_model:
 role: developer
 allowed_tools:
 - read
 - write: ["workspace/*"]
 - exec: ["npm run *"]
 
 blocked:
 - delete
 - system
 - network: external

escalation:
 - tool: deploy
 requires_approval: true
 - tool: delete
 requires_approval: true
```

---

## 五、版本管理

### 5.1 Agent 版本控制

```yaml
agent_version:
 major: 1 # 架構變更
 minor: 0 # 新功能
 patch: 0 # 修復

changelog:
 - version: "1.0.0"
 date: "2026-03-17"
 changes:
 - "初始版本"
 - "支援 ReAct 模式"
 - "支援 Human-in-loop"
```

---

## 六、檢查清單

### 開發前檢查

- [ ] 任務範圍明確
- [ ] 輸入輸出格式定義
- [ ] 錯誤處理策略
- [ ] 監控需求確認
- [ ] 安全要求評估

---

### 開發中檢查

- [ ] 遵循設計模式
- [ ] 符合命名規範
- [ ] 記錄結構化日誌
- [ ] 實現錯誤處理
- [ ] 遵守安全規範

---

### 發布前檢查

- [ ] 單元測試通過
- [ ] 整合測試通過
- [ ] 文件齊全
- [ ] 配置版本記錄
- [ ] 監控儀表板設定

---

## 附錄

### A. 錯誤碼對照表

| 錯誤碼 | 說明 | 建議動作 |
|--------|------|----------|
| 1001 | 輸入無效 | 返回錯誤，不重試 |
| 1002 | 工具失敗 | 重試或更換工具 |
| 1003 | 執行超時 | 增加超時或優化 |
| 1004 | 速率限制 | 等待後重試 |
| 1005 | 超過重試 | 上報人類 |

---

### B. 常用提示模板

```yaml
templates:
 analyze:
 System (untrusted): "你是一個專業的代碼分析師..."
 user: "請分析以下代碼：{code}"
 
 review:
 System (untrusted): "你是一個資深工程師，擅長代碼審查..."
 user: "請審查以下 PR：{pr_url}"
```

---

*版本：1.0*
*建立日期：2026-03-17*
*來源：Johnny Lu*
