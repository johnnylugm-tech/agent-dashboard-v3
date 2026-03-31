# 🔄 Multi-Agent Collaboration Toolkit

> 讓每個人都能輕鬆實現多 Agent 協作

---

## 概述

Multi-Agent Collaboration Toolkit 提供一套完整的工具和方法論，幫助開發者快速建立、管理和監控多個 AI Agent 的協作系統。

---

## 核心組件

| 組件 | 功能 | 狀態 |
|------|------|:----:|
| **Task Dispatcher** | 任務分配與排程 | ✅ |
| **Communication Hub** | Agent 間訊息傳遞 | ✅ |
| **State Manager** | 共享狀態管理 | ✅ |
| **Quality Gate** | 品質把關 | ✅ |
| **Monitor Dashboard** | 監控儀表板 | ✅ |

---

## 快速開始

### 1. 安裝

```bash
pip install multi-agent-toolkit
```

### 2. 基本使用

```python
from multi_agent import Agent, Crew, Task

# 建立 Agent
researcher = Agent(role="Researcher", goal="Research AI trends")
coder = Agent(role="Coder", goal="Write code")

# 建立任務
research_task = Task(description="Research LLM trends", agent=researcher)
code_task = Task(description="Implement feature", agent=coder)

# 建立 Crew
crew = Crew(agents=[researcher, coder], tasks=[research_task, code_task])

# 執行
result = crew.kickoff()
```

---

## 方法論

### 錯誤分類 (L1-L4)

| 等級 | 類型 | 處理 |
|------|------|------|
| L1 | 輸入錯誤 | 立即返回 |
| L2 | 工具錯誤 | 重試 3 次 |
| L3 | 執行錯誤 | 降級處理 |
| L4 | 系統錯誤 | 熔斷/警報 |

### 協作模式

```
1. 規劃 (Planning)
   └─> 任務拆分

2. 執行 (Execution)
   └─> Agent 處理

3. 協調 (Coordination)
   └─> 訊息傳遞

4. 品質 (Quality)
   └─> 結果驗證
```

---

## 監控

```python
from monitor import Monitor

monitor = Monitor()

# 追蹤
monitor.track(agent_id="agent-001", task="coding", cost=0.5)

# 獲取狀態
status = monitor.get_status()
print(f"Health: {status['health_score']}")
```

---

## API Reference

### Agent

```python
Agent(
    role: str,           # 角色名稱
    goal: str,           # 目標
    backstory: str,      # 背景故事
    llm: BaseLLM,        # 使用的 LLM
    tools: List[Tool]    # 工具列表
)
```

### Task

```python
Task(
    description: str,    # 任務描述
    agent: Agent,        # 負責的 Agent
    expected_output: str # 預期輸出
)
```

### Crew

```python
Crew(
    agents: List[Agent],
    tasks: List[Task],
    process: str,       # "sequential" | "parallel"
    manager: Manager     # 可選的 manager
)
```

---

## 示例專案

### 示例 1: 簡單串聯

```python
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research, write, edit],
    process="sequential"
)
```

### 示例 2: 並行處理

```python
crew = Crew(
    agents=[coder1, coder2, tester],
    tasks=[task1, task2, test_task],
    process="parallel"
)
```

### 示例 3:階層式

```python
manager = Manager(agents=[researcher, coder])

crew = Crew(
    agents=[manager, researcher, coder],
    tasks=[main_task],
    process="hierarchical"
)
```

---

## 整合

### 與 LangChain 整合

```python
from langchain.llms import OpenAI
from multi_agent import Agent

agent = Agent(
    role="Expert",
    llm=OpenAI(model="gpt-4")
)
```

### 與 OpenClaw 整合

```python
from openclaw import sessions_spawn

# 建立子 Agent
session = sessions_spawn(
    task="幫我完成這個任務",
    agentId="developer"
)
```

---

## 監控與警報

### 健康評分

```
100 - 任務全部成功
75  - 小問題
50  - 需要關注
25  - 嚴重問題
0   - 系統故障
```

### 警報級別

| 級別 | 觸發條件 |
|------|----------|
| 🔴 Critical | 健康 < 25 |
| 🟡 Warning | 健康 < 50 |
| 🔵 Info | 健康 < 75 |

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| v1.0.0 | 2026-03 | 初始發布 |

---

*用 AI 技術改變世界，讓每個人生活更便利、更幸福*
