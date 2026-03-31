# AI Agent 錯誤處理與自我修復機制

> 建立 Agent 自我修復能力

---

## 一、錯誤分類體系

### 1.1 錯誤層級

| 層級 | 類型 | 影響範圍 | 處理方式 |
|------|------|----------|----------|
| **L1** | 輸入錯誤 | 單次請求 | 立即返回 |
| **L2** | 工具錯誤 | 單次任務 | 重試 |
| **L3** | 執行錯誤 | 任務流程 | 降級/上報 |
| **L4** | 系統錯誤 | 整體系統 | 熔斷/報警 |

---

### 1.2 錯誤碼定義

```python
# 輸入錯誤 (1000-1999)
INVALID_INPUT = "E1001"      # 輸入無效
MISSING_REQUIRED = "E1002"   # 缺少必要字段
INPUT_TOO_LARGE = "E1003"   # 輸入過大
INVALID_FORMAT = "E1004"     # 格式錯誤

# 工具錯誤 (2000-2999)
TOOL_NOT_FOUND = "E2001"     # 工具不存在
TOOL_FAILED = "E2002"       # 工具執行失敗
TOOL_TIMEOUT = "E2003"      # 工具超時
TOOL_UNAVAILABLE = "E2004"   # 工具不可用

# 執行錯誤 (3000-3999)
EXECUTION_FAILED = "E3001"   # 執行失敗
MAX_RETRIES_EXCEEDED = "E3002"  # 超過重試次數
CONTEXT_OVERFLOW = "E3003"   # 上下文溢出
RESOURCE_EXHAUSTED = "E3004" # 資源耗盡

# 系統錯誤 (4000-4999)
SYSTEM_OVERLOAD = "E4001"    # 系統過載
RATE_LIMIT = "E4002"         # 速率限制
MAINTENANCE = "E4003"        # 維護中
UNKNOWN = "E9999"             # 未知錯誤
```

---

## 二、錯誤處理策略

### 2.1 輸入錯誤處理

```python
def validate_input(input_data: Dict) -> ValidationResult:
    """驗證輸入"""
    errors = []
    
    # 1. 檢查必要字段
    required_fields = ["task", "context"]
    for field in required_fields:
        if field not in input_data:
            errors.append({"field": field, "error": "Missing required field"})
    
    # 2. 檢查數據類型
    if "task" in input_data and not isinstance(input_data["task"], str):
        errors.append({"field": "task", "error": "Must be string"})
    
    # 3. 檢查輸入大小
    if "task" in input_data and len(input_data["task"]) > 100000:
        errors.append({"field": "task", "error": "Input too large"})
    
    return ValidationResult(is_valid=len(errors) == 0, errors=errors)
```

### 2.2 工具錯誤處理

```python
async def execute_with_retry(tool_name: str, params: Dict, max_retries: int = 3) -> ToolResult:
    """帶重試的工具執行"""
    retry_delays = [1, 2, 5]  # 秒
    
    for attempt in range(max_retries):
        try:
            result = await agent.execute_tool(tool_name, params)
            if result.success:
                return result
        except Exception as e:
            last_error = str(e)
        
        # 計算延遲
        if attempt < len(retry_delays) - 1:
            delay = retry_delays[attempt]
            await asyncio.sleep(delay)
    
    return ToolResult(success=False, error_code="MAX_RETRIES_EXCEEDED")
```

---

## 三、自我修復機制

### 3.1 修復策略

| 錯誤類型 | 修復策略 | 最大嘗試 |
|----------|----------|----------|
| TOOL_FAILED | 指數退避重試 | 3 |
| TOOL_TIMEOUT | 增加超時 | 2 |
| CONTEXT_OVERFLOW | 壓縮上下文 | 2 |
| RESOURCE_EXHAUSTED | 減少範圍 | 1 |
| LOW_CONFIDENCE | 請求澄清 | 1 |

### 3.2 熔斷機制

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError()
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
    
    def _on_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
```

---

## 四、監控指標

| 指標 | 閾值 | 警報 |
|------|------|------|
| 錯誤率 (5分鐘) | > 10% | ⚠️ 警告 |
| 錯誤數 (1小時) | > 100 | ⚠️ 警告 |
| 同一錯誤 | 3次 | 🔴 嚴重 |
| 熔斷打開 | - | 🔴 嚴重 |

---

## 五、實施檢查清單

### 錯誤處理
- [ ] 定義錯誤碼體系
- [ ] 實現錯誤分類
- [ ] 建立錯誤上下文
- [ ] 實現重試機制
- [ ] 實現降級策略
- [ ] 實現熔斷機制

### 自我修復
- [ ] 實現修復決策樹
- [ ] 實現修復策略
- [ ] 實現上下文壓縮
- [ ] 實現範圍縮減

### 監控
- [ ] 實現錯誤監控
- [ ] 實現警報規則
- [ ] 實現修復報告

---

*版本：1.0*
*建立日期：2026-03-17*
*來源：Johnny Lu*
