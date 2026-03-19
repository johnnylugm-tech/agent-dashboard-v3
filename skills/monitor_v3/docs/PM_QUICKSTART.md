# Agent Monitor - PM 快速入門指南

> 這是給專案經理的快速上手指南

---

## PM 的一天

| 時間 | 情境 | 使用功能 |
|------|------|----------|
| 早上 9:00 | 健康檢查 | Morning Report |
| 上午 10:00 | 進度確認 | Journey Tracker |
| 中午 12:00 | 異常處理 | Alert + Root Cause |
| 下午 3:00 | 成本檢視 | Cost Tracker |
| 下午 5:00 | 進度彙報 | Report |

---

## 快速開始

### 1. 晨間健康檢查

```python
from monitor.morning_report import MorningReportGenerator

generator = MorningReportGenerator(
    health_tracker=health,
    cost_tracker=cost,
    alert_manager=alerts
)

# 生成今日報告
print(generator.generate())
```

輸出：
```
============================================================
🌅 Morning Report - 2026-03-19
============================================================

📊 總覽
----------------------------------------
  健康評分: 85/100
  昨日成本: $12.50
  昨日警報: 2 次

📈 趨勢 (7天)
----------------------------------------
  2026-03-13: $10.00
  2026-03-14: $12.00
  ...

⚠️ 異常警報
----------------------------------------
  ✅ 無重大異常
```

---

### 2. 成本檢視

```python
from monitor.cost_tracker import CostTracker

tracker = CostTracker()

# 查看成本
daily = tracker.get_all_agents_cost("daily")
print(f"今日成本: ${daily['total_cost']}")

# 查看趨勢
trend = tracker.get_cost_trend(days=7)
print(trend)
```

---

### 3. 成本預測

```python
from monitor.cost_predictor import CostPredictor

predictor = CostPredictor(tracker)

# 預測未來 7 天
prediction = predictor.predict_daily(7)
print(f"本月預測: ${prediction['monthly_estimate']}")
print(f"趨勢: {prediction['trend']}")
```

---

### 4. 警報設置

```python
from monitor.alerts_v2 import AlertManager

manager = AlertManager()

# 添加自定義規則
manager.add_rule(
    name="high_cost",
    condition=lambda m: m.get("cost", 0) > 10.0,
    level="warning",
    title="HighCost",
    message="成本超過 $10"
)
```

---

### 5. 團隊產能報告

```python
from monitor_v3.productivity_report import ProductivityReporter

reporter = ProductivityReporter(
    journey_tracker=journey,
    cost_tracker=cost,
    alert_manager=alerts
)

# 生成月報
print(reporter.generate_text_report("monthly"))
```

---

## 版本選擇

| 情境 | 推薦版本 | 功能 |
|------|----------|------|
| 個人開發者 | v2 輕量版 | 健康、成本、警報 |
| 小團隊 (2-5人) | v2 輕量版 | + journey 追蹤 |
| 中團隊 (5-20人) | v3 完整版 | + RBAC + 日誌 |
| 大團隊 | v3 完整版 | + 進階分析 |

---

## 常見問題

### Q: 如何設置每日報告自動發送？

```python
import schedule
import time

def send_morning_report():
    generator = MorningReportGenerator(...)
    generator.send_to_slack("YOUR_WEBHOOK_URL")

# 每天早上 9 點發送
schedule.every().day.at("09:00").do(send_morning_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Q: 如何追蹤特定 Agent？

```python
# 查看單一 Agent 成本
agent_cost = tracker.get_agent_cost("agent-001", "daily")

# 查看 Agent journey
journey = journey_tracker.get_journey("agent-001")
```

### Q: 成本超支時如何警報？

```python
manager.add_rule(
    name="daily_budget",
    condition=lambda m: m.get("daily_cost", 0) > 20.0,
    level="critical",
    title="BudgetExceeded",
    message="每日成本超過 $20"
)
```

---

## 快捷指令

```bash
# v2 輕量版
python -m monitor.health                  # 健康檢查
python -m monitor.cost_tracker --daily      # 每日成本
python -m monitor.alerts --history         # 警報歷史

# v3 完整版
python -m monitor_v3.rbac list            # 列出用戶
python -m monitor_v3.log_search --query error  # 搜尋日誌
```

---

## 聯繫支持

- GitHub: https://github.com/johnnylugm-tech/agent-monitor-v2
- Issues: https://github.com/johnnylugm-tech/agent-monitor-v2/issues

---

*Generated: 2026-03-19*
