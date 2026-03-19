#!/usr/bin/env python3
"""
SQLite 存儲層 - Agent Monitor v3

功能：
- SQLite 持久化存儲
- 日誌索引與搜尋
- 自動建表遷移
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import threading


@dataclass
class LogEntry:
    """日誌條目"""
    id: Optional[int] = None
    timestamp: str = None
    level: str = "info"
    message: str = ""
    agent_id: str = None
    session_id: str = None
    trace_id: str = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class TraceEntry:
    """追蹤條目"""
    id: Optional[int] = None
    trace_id: str = None
    session_id: str = None
    agent_id: str = None
    parent_id: str = None
    step_type: str = "llm"  # llm, tool, reasoning
    name: str = None
    input_data: Dict = None
    output_data: Dict = None
    tokens: int = 0
    cost: float = 0.0
    duration_ms: int = 0
    status: str = "running"  # running, completed, failed
    started_at: str = None
    completed_at: str = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AlertRecord:
    """警報記錄"""
    id: Optional[int] = None
    timestamp: str = None
    level: str = "warning"
    title: str = ""
    message: str = ""
    agent_id: str = None
    session_id: str = None
    metric_name: str = None
    metric_value: float = None
    threshold: float = None
    status: str = "triggered"  # triggered, acknowledged, resolved
    acknowledged_at: str = None
    acknowledged_by: str = None
    resolved_at: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class Storage:
    """SQLite 存儲引擎"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path: str = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_path: str = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self.db_path = db_path or os.getenv(
            "MONITOR_DB_PATH", 
            "./data/monitor.db"
        )
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._initialized = True
        
        self._migrate()
    
    def _migrate(self):
        """建表遷移"""
        cursor = self.conn.cursor()
        
        # Logs 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                agent_id TEXT,
                session_id TEXT,
                trace_id TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 建立索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON logs(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_level ON logs(level)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_agent ON logs(agent_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_logs_session ON logs(session_id)
        """)
        
        # Traces 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS traces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trace_id TEXT NOT NULL,
                session_id TEXT,
                agent_id TEXT,
                parent_id TEXT,
                step_type TEXT,
                name TEXT,
                input_data TEXT,
                output_data TEXT,
                tokens INTEGER DEFAULT 0,
                cost REAL DEFAULT 0.0,
                duration_ms INTEGER DEFAULT 0,
                status TEXT DEFAULT 'running',
                started_at TEXT,
                completed_at TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_traces_trace ON traces(trace_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_traces_session ON traces(session_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_traces_agent ON traces(agent_id)
        """)
        
        # Alerts 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT,
                agent_id TEXT,
                session_id TEXT,
                metric_name TEXT,
                metric_value REAL,
                threshold REAL,
                status TEXT DEFAULT 'triggered',
                acknowledged_at TEXT,
                acknowledged_by TEXT,
                resolved_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sessions 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id TEXT,
                agent_id TEXT,
                status TEXT DEFAULT 'active',
                started_at TEXT,
                ended_at TEXT,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Metrics 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                tags TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_metrics_agent ON metrics(agent_id)
        """)
        
        self.conn.commit()
    
    # ============== Logs ==============
    
    def insert_log(self, log: LogEntry) -> int:
        """插入日誌"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO logs (timestamp, level, message, agent_id, session_id, trace_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            log.timestamp,
            log.level,
            log.message,
            log.agent_id,
            log.session_id,
            log.trace_id,
            json.dumps(log.metadata)
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def search_logs(
        self,
        query: str = None,
        level: List[str] = None,
        agent_id: str = None,
        session_id: str = None,
        trace_id: str = None,
        start_time: str = None,
        end_time: str = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """搜尋日誌"""
        cursor = self.conn.cursor()
        
        sql = "SELECT * FROM logs WHERE 1=1"
        params = []
        
        if query:
            sql += " AND message LIKE ?"
            params.append(f"%{query}%")
        
        if level:
            sql += f" AND level IN ({','.join(['?']*len(level))})"
            params.extend(level)
        
        if agent_id:
            sql += " AND agent_id = ?"
            params.append(agent_id)
        
        if session_id:
            sql += " AND session_id = ?"
            params.append(session_id)
        
        if trace_id:
            sql += " AND trace_id = ?"
            params.append(trace_id)
        
        if start_time:
            sql += " AND timestamp >= ?"
            params.append(start_time)
        
        if end_time:
            sql += " AND timestamp <= ?"
            params.append(end_time)
        
        sql += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "timestamp": row["timestamp"],
                "level": row["level"],
                "message": row["message"],
                "agent_id": row["agent_id"],
                "session_id": row["session_id"],
                "trace_id": row["trace_id"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else {}
            })
        
        return results
    
    def count_logs(
        self,
        query: str = None,
        level: List[str] = None,
        agent_id: str = None,
        session_id: str = None
    ) -> int:
        """統計日誌數量"""
        cursor = self.conn.cursor()
        
        sql = "SELECT COUNT(*) as count FROM logs WHERE 1=1"
        params = []
        
        if query:
            sql += " AND message LIKE ?"
            params.append(f"%{query}%")
        
        if level:
            sql += f" AND level IN ({','.join(['?']*len(level))})"
            params.extend(level)
        
        if agent_id:
            sql += " AND agent_id = ?"
            params.append(agent_id)
        
        if session_id:
            sql += " AND session_id = ?"
            params.append(session_id)
        
        cursor.execute(sql, params)
        return cursor.fetchone()["count"]
    
    def aggregate_logs(self, field: str = "level") -> Dict:
        """聚合日誌"""
        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT {field}, COUNT(*) as count 
            FROM logs 
            GROUP BY {field}
        """)
        
        results = {}
        for row in cursor.fetchall():
            results[row[field]] = row["count"]
        
        return results
    
    # ============== Traces ==============
    
    def insert_trace(self, trace: TraceEntry) -> int:
        """插入追蹤"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO traces (
                trace_id, session_id, agent_id, parent_id, step_type, name,
                input_data, output_data, tokens, cost, duration_ms, status,
                started_at, completed_at, metadata
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trace.trace_id,
            trace.session_id,
            trace.agent_id,
            trace.parent_id,
            trace.step_type,
            trace.name,
            json.dumps(trace.input_data) if trace.input_data else None,
            json.dumps(trace.output_data) if trace.output_data else None,
            trace.tokens,
            trace.cost,
            trace.duration_ms,
            trace.status,
            trace.started_at,
            trace.completed_at,
            json.dumps(trace.metadata) if trace.metadata else None
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_trace_tree(self, trace_id: str) -> Dict:
        """獲取追蹤樹"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM traces WHERE trace_id = ? ORDER BY started_at
        """, (trace_id,))
        
        steps = []
        for row in cursor.fetchall():
            steps.append({
                "id": row["id"],
                "trace_id": row["trace_id"],
                "parent_id": row["parent_id"],
                "step_type": row["step_type"],
                "name": row["name"],
                "input_data": json.loads(row["input_data"]) if row["input_data"] else {},
                "output_data": json.loads(row["output_data"]) if row["output_data"] else {},
                "tokens": row["tokens"],
                "cost": row["cost"],
                "duration_ms": row["duration_ms"],
                "status": row["status"],
                "started_at": row["started_at"],
                "completed_at": row["completed_at"]
            })
        
        # 構建樹結構
        return self._build_tree(steps)
    
    def _build_tree(self, steps: List[Dict]) -> Dict:
        """構建樹結構"""
        step_map = {s["id"]: {**s, "children": []} for s in steps}
        root = None
        
        for step in steps:
            if step["parent_id"] is None:
                root = step_map[step["id"]]
            else:
                parent = step_map.get(step["parent_id"])
                if parent:
                    parent["children"].append(step_map[step["id"]])
        
        return root or {"error": "No trace found"}
    
    # ============== Alerts ==============
    
    def insert_alert(self, alert: AlertRecord) -> int:
        """插入警報"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (
                timestamp, level, title, message, agent_id, session_id,
                metric_name, metric_value, threshold, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert.timestamp,
            alert.level,
            alert.title,
            alert.message,
            alert.agent_id,
            alert.session_id,
            alert.metric_name,
            alert.metric_value,
            alert.threshold,
            alert.status
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_alerts(
        self,
        status: str = None,
        level: str = None,
        agent_id: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """獲取警報"""
        cursor = self.conn.cursor()
        
        sql = "SELECT * FROM alerts WHERE 1=1"
        params = []
        
        if status:
            sql += " AND status = ?"
            params.append(status)
        
        if level:
            sql += " AND level = ?"
            params.append(level)
        
        if agent_id:
            sql += " AND agent_id = ?"
            params.append(agent_id)
        
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        
        results = []
        for row in cursor.fetchall():
            results.append(dict(row))
        
        return results
    
    # ============== Sessions ==============
    
    def create_session(
        self,
        session_id: str,
        user_id: str = None,
        agent_id: str = None
    ) -> int:
        """創建會話"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (session_id, user_id, agent_id, status, started_at)
            VALUES (?, ?, ?, 'active', ?)
        """, (session_id, user_id, agent_id, datetime.now().isoformat()))
        self.conn.commit()
        return cursor.lastrowid
    
    def close_session(self, session_id: str):
        """關閉會話"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sessions 
            SET status = 'completed', ended_at = ?
            WHERE session_id = ?
        """, (datetime.now().isoformat(), session_id))
        self.conn.commit()
    
    # ============== Metrics ==============
    
    def insert_metric(
        self,
        agent_id: str,
        metric_name: str,
        value: float,
        tags: Dict = None
    ):
        """插入指標"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO metrics (timestamp, agent_id, metric_name, value, tags)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            agent_id,
            metric_name,
            value,
            json.dumps(tags) if tags else None
        ))
        self.conn.commit()
    
    def get_metrics(
        self,
        agent_id: str = None,
        metric_name: str = None,
        start_time: str = None,
        end_time: str = None,
        limit: int = 1000
    ) -> List[Dict]:
        """獲取指標"""
        cursor = self.conn.cursor()
        
        sql = "SELECT * FROM metrics WHERE 1=1"
        params = []
        
        if agent_id:
            sql += " AND agent_id = ?"
            params.append(agent_id)
        
        if metric_name:
            sql += " AND metric_name = ?"
            params.append(metric_name)
        
        if start_time:
            sql += " AND timestamp >= ?"
            params.append(start_time)
        
        if end_time:
            sql += " AND timestamp <= ?"
            params.append(end_time)
        
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "timestamp": row["timestamp"],
                "agent_id": row["agent_id"],
                "metric_name": row["metric_name"],
                "value": row["value"],
                "tags": json.loads(row["tags"]) if row["tags"] else {}
            })
        
        return results
    
    def close(self):
        """關閉連接"""
        self.conn.close()


# ============== 便捷函數 ==============

storage = Storage()


def log(
    message: str,
    level: str = "info",
    agent_id: str = None,
    session_id: str = None,
    trace_id: str = None,
    **metadata
):
    """快捷日誌記錄"""
    entry = LogEntry(
        message=message,
        level=level,
        agent_id=agent_id,
        session_id=session_id,
        trace_id=trace_id,
        metadata=metadata
    )
    return storage.insert_log(entry)


def search_logs(**kwargs):
    """快捷日誌搜尋"""
    return storage.search_logs(**kwargs)


def trace(
    trace_id: str,
    step_type: str = "llm",
    name: str = None,
    agent_id: str = None,
    session_id: str = None,
    parent_id: str = None,
    **data
) -> int:
    """快捷追蹤記錄"""
    entry = TraceEntry(
        trace_id=trace_id,
        step_type=step_type,
        name=name,
        agent_id=agent_id,
        session_id=session_id,
        parent_id=parent_id,
        input_data=data.get("input"),
        output_data=data.get("output"),
        tokens=data.get("tokens", 0),
        cost=data.get("cost", 0.0),
        duration_ms=data.get("duration_ms", 0),
        status=data.get("status", "running")
    )
    return storage.insert_trace(entry)


# ============== 主程式 ==============

if __name__ == "__main__":
    # 測試
    print("=" * 50)
    print("🗄️ Agent Monitor Storage Test")
    print("=" * 50)
    
    # 插入日誌
    log("System started", level="info", agent_id="musk")
    log("High error rate detected", level="warning", agent_id="dev-agent")
    log("API request failed", level="error", agent_id="api-gateway", session_id="sess-001")
    
    # 搜尋
    print("\n📥 All logs:")
    for row in storage.search_logs(limit=10):
        print(f"  [{row['level']}] {row['message']}")
    
    print("\n🔍 Search 'error':")
    for row in storage.search_logs(query="error"):
        print(f"  [{row['level']}] {row['message']}")
    
    print("\n📊 Aggregate by level:")
    for level, count in storage.aggregate_logs("level").items():
        print(f"  {level}: {count}")
    
    # 插入追蹤
    trace("trace-001", "llm", "generate", agent_id="musk", session_id="sess-001")
    trace("trace-001", "tool", "search", agent_id="musk", session_id="sess-001", parent_id="1")
    
    # 獲取樹
    print("\n🌳 Trace tree:")
    tree = storage.get_trace_tree("trace-001")
    print(f"  {tree}")
    
    print("\n✅ Storage test complete!")
