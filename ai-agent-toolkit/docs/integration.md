# 🔗 整合教學

> 將工具箱整合到你的專案中

---

## 1. 與 Python 專案整合

### 安裝依賴

```bash
pip install model-router agent-quality-guard
```

### 基本使用

```python
from model_router import Router
from agent_quality_guard import Analyzer

# 初始化 Router
router = Router(budget="medium")

# 路由任務
result = router.route("幫我寫一個 Python 函數")
print(f"使用模型: {result['model']}")
print(f"預估成本: {result['cost']}")

# 檢測程式碼品質
analyzer = Analyzer()
score = analyzer.analyze(result['code'])
print(f"品質分數: {score}")
```

---

## 2. 與 LangChain 整合

### 安裝

```bash
pip install langchain model-router
```

### 範例

```python
from langchain.llms import OpenAI
from model_router import Router

# 使用 Model Router 選擇模型
router = Router()
model_info = router.route("翻譯這段文字")

# 初始化 LangChain
llm = OpenAI(
    model=model_info['model'],
    temperature=0.7
)

# 使用
result = llm("翻譯: Hello world")
```

---

## 3. 與 CrewAI 整合

### 安裝

```bash
pip install crewai model-router
```

### 範例

```python
from crewai import Agent, Task, Crew
from model_router import Router

# 使用 Model Router 選擇模型
router = Router(budget="low")

# 建立 Agent
researcher = Agent(
    role='Researcher',
    goal='Find information about AI',
    llm=router.get_llm()  # 自動選擇模型
)

# 建立 Task
task = Task(
    description='Research AI trends',
    agent=researcher
)

# 執行
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

---

## 4. 與 Git Hook 整合

### 安裝 Hook

```bash
agent-quality-guard hook install
```

### 自動檢測

```bash
# 每次 git commit 會自動檢測
git commit -m "新增功能"
# → 自動執行品質檢測
```

---

## 5. 與 CI/CD 整合

### GitHub Actions

```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: pip install agent-quality-guard
      
      - name: Run quality check
        run: agent-quality-guard --path ./src --json > quality-report.json
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: quality-report
          path: quality-report.json
```

---

## 6. 與監控系統整合

### Prometheus 指標

```python
from prometheus_client import Counter, Histogram

# 追蹤 Router 使用
router_calls = Counter('router_calls', 'Total router calls')
cost_spent = Histogram('cost_spent', 'Cost spent in USD')

# 使用 Router
router = Router()
result = router.route(task)

# 記錄指標
router_calls.inc()
cost_spent.observe(result['cost'])
```

---

## 7. 環境變數配置

### 必要變數

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic  
export ANTHROPIC_API_KEY="sk-ant-..."

# Google
export GOOGLE_API_KEY="..."

# DeepSeek
export DEEPSEEK_API_KEY="..."
```

### 可選變數

```bash
# 預算限制
export MODEL_ROUTER_DAILY_LIMIT=10
export MODEL_ROUTER_MONTHLY_LIMIT=100

# 日誌
export LOG_LEVEL=INFO
```

---

## 8. 完整範例

```python
"""
AI Agent 應用完整範例
"""
from model_router import Router
from agent_quality_guard import Analyzer
from agent_monitor import Monitor

class AIAgent:
    def __init__(self, budget="medium"):
        self.router = Router(budget=budget)
        self.analyzer = Analyzer()
        self.monitor = Monitor()
    
    def execute(self, task):
        # 1. 選擇模型
        model_info = self.router.route(task)
        
        # 2. 執行任務
        result = self.call_llm(model_info, task)
        
        # 3. 品質檢測
        quality = self.analyzer.analyze(result['code'])
        
        # 4. 監控記錄
        self.monitor.record({
            'task': task,
            'model': model_info['model'],
            'cost': result['cost'],
            'quality': quality
        })
        
        return {
            'result': result,
            'quality': quality
        }

# 使用
agent = AIAgent(budget="low")
response = agent.execute("寫一個排序函數")
```

---

## 下一步

- [版本比較](comparison.md) - 了解版本差異
- [安裝教學](getting-started.md) - 回顧安裝

---

*整合有問題？請開 GitHub Issue*
