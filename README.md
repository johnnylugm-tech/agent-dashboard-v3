# Agent Monitor v3 開發規劃

> 完整版 MVP - 補完剩餘功能

---

## 📦 v2 保留（輕量版）

```bash
# 保持現有結構
skills/monitor/
├── alerts_v2.py          # 警報
├── health_score.py       # 健康評分
├── cost_tracker.py       # 成本
├── journey_tracker.py    # 旅程追蹤
├── unified_dashboard.py  # 統一儀表板
├── monitor_hook.py       # 嵌入
├── root_cause_analysis.py # 根因分析
├── api_simple.py         # REST API
└── openclaw_connector.py # 串流
```

---

## 🎯 v3 新增功能

### 1. 日誌搜尋系統

```python
# log_search.py
class LogSearch:
    """日誌搜尋引擎"""
    
    def __init__(self, db_path: str = "./data/logs.db"):
        self.db_path = db_path
        
    def search(
        self,
        query: str = None,
        level: List[str] = None,
        agent_id: str = None,
        session_id: str = None,
        time_range: tuple = None,
        limit: int = 100
    ) -> List[LogEntry]:
        """多維度搜尋"""
        
    def index(self, log: LogEntry):
        """索引日誌"""
        
    def aggregate(self, field: str) -> Dict:
        """聚合統計"""
```

### 2. 執行路徑視覺化

```python
# trace_visualizer.py
class TraceVisualizer:
    """執行路徑視覺化"""
    
    def generate_tree(self, trace_id: str) -> Dict:
        """生成樹狀結構"""
        
    def generate_timeline(self, trace_id: str) -> Dict:
        """生成時間軸"""
        
    def export_json(self, trace_id: str) -> str:
        """導出 JSON"""
        
    def to_mermaid(self, trace_id: str) -> str:
        """轉換為 Mermaid 圖"""
```

### 3. 靜音時段

```python
# silence_scheduler.py
class SilenceScheduler:
    """靜音時段管理"""
    
    def is_silenced(self, channel: str = "all") -> bool:
        """檢查是否在靜音時段"""
        
    def add_window(
        self,
        start: datetime,
        end: datetime,
        reason: str = None
    ):
        """新增靜音時段"""
        
    def get_windows(self) -> List[Dict]:
        """獲取所有靜音時段"""
```

### 4. RBAC 基礎

```python
# rbac.py
class RBAC:
    """基礎角色權限"""
    
    ROLES = {
        "admin": ["*"],           # 所有權限
        "editor": ["read", "write", "alert"],  # 編輯
        "viewer": ["read"]         # 僅讀取
    }
    
    def check_permission(self, role: str, action: str) -> bool:
        """檢查權限"""
        
    def get_user_role(self, user_id: str) -> str:
        """獲取用戶角色"""
```

---

## 📂 v3 目錄結構

```
agent-dashboard-v3/
├── skills/monitor/          # v2 保留
│   ├── alerts_v2.py
│   ├── health_score.py
│   └── ...
│
├── skills/monitor_v3/       # v3 新增
│   ├── log_search.py       # 日誌搜尋
│   ├── trace_visualizer.py # 執行路徑視覺化
│   ├── silence_scheduler.py # 靜音時段
│   ├── rbac.py            # RBAC
│   ├── webhook.py         # Webhook
│   ├── storage.py         # SQLite 存儲
│   └── api_v3.py          # v3 API
│
├── frontend/               # React UI
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── hooks/
│   └── package.json
│
├── docker/                 # Docker 配置
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt
└── README.md
```

---

## ⏱️ 開發時程

| 週 | 功能 | 產出 |
|----|------|------|
| Week 1 | 存儲層 + 日誌搜尋 | SQLite + 搜尋 API |
| Week 2 | 執行路徑視覺化 | Tree + Timeline |
| Week 3 | 靜音時段 + RBAC | 配置 + 權限 |
| Week 4 | Webhook + API 整合 | 完整 API |
| Week 5 | React UI 基礎 | Dashboard + Traces |
| Week 6 | Docker 部署 | 可發布版本 |

---

## ✅ MVP 完整功能（v3）

| ID | 功能 | 狀態 |
|----|------|------|
| 1.1.1 | 執行路徑視覺化 | ⏳ |
| 1.1.2 | 對話歷史記錄 | ✅ |
| 1.1.3 | 工具調用日誌 | ✅ |
| 1.1.4 | 時間軸視圖 | ⏳ |
| 1.1.5 | 錯誤堆疊追蹤 | ✅ |
| 1.2.1 | Token 儀表板 | ✅ |
| 1.2.2 | 延遲追蹤 | ✅ |
| 1.2.3 | 成本計算 | ✅ |
| 1.2.4 | 成功率監控 | ✅ |
| 1.3.1 | 結構化日誌 | ✅ |
| 1.3.2 | 日誌搜尋 | ⏳ |
| 1.3.3 | 日誌匯出 | ⏳ |
| 1.4.1 | 閾值告警 | ✅ |
| 1.4.2 | 多通道通知 | ⏳ |
| 1.4.3 | 告警歷史 | ✅ |
| 1.4.4 | 靜音時段 | ⏳ |
| 1.5.1 | 依賴關係圖 | ✅ |
| 1.8.1 | RBAC | ⏳ |

---

## 🚀 啟動

開始 Week 1？
