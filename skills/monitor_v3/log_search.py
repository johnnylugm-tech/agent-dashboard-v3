#!/usr/bin/env python3
"""
日誌搜尋模組 - Agent Monitor v3

功能：
- 多維度日誌搜尋
- 全文檢索
- 聚合統計
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from storage import storage, LogEntry


@dataclass
class SearchQuery:
    """搜尋查詢"""
    query: str = None              # 關鍵字
    levels: List[str] = None        # 日誌級別
    agent_ids: List[str] = None     # Agent IDs
    session_ids: List[str] = None  # Session IDs
    trace_ids: List[str] = None    # Trace IDs
    start_time: str = None         # 開始時間
    end_time: str = None           # 結束時間
    limit: int = 100               # 結果限制
    offset: int = 0                # 分頁偏移


class LogSearch:
    """日誌搜尋引擎"""
    
    def __init__(self):
        self.storage = storage
    
    def search(self, sq: SearchQuery) -> Dict:
        """執行搜尋"""
        # 轉換為存儲層格式
        params = {
            "query": sq.query,
            "limit": sq.limit,
            "offset": sq.offset
        }
        
        if sq.levels:
            params["level"] = sq.levels
        
        if sq.agent_ids and len(sq.agent_ids) == 1:
            params["agent_id"] = sq.agent_ids[0]
        
        if sq.session_ids and len(sq.session_ids) == 1:
            params["session_id"] = sq.session_ids[0]
        
        if sq.trace_ids and len(sq.trace_ids) == 1:
            params["trace_id"] = sq.trace_ids[0]
        
        if sq.start_time:
            params["start_time"] = sq.start_time
        
        if sq.end_time:
            params["end_time"] = sq.end_time
        
        # 搜尋
        results = self.storage.search_logs(**params)
        
        # 統計總數
        count_params = {k: v for k, v in params.items() if k not in ["limit", "offset"]}
        total = self.storage.count_logs(**count_params) if not sq.query or sq.query in params.get("query", "") else len(results)
        
        return {
            "results": results,
            "total": total,
            "limit": sq.limit,
            "offset": sq.offset,
            "has_more": (sq.offset + sq.limit) < total
        }
    
    def aggregate(
        self,
        field: str = "level",
        query: str = None,
        agent_id: str = None,
        session_id: str = None
    ) -> Dict:
        """聚合統計"""
        params = {}
        if query:
            params["query"] = query
        if agent_id:
            params["agent_id"] = agent_id
        if session_id:
            params["session_id"] = session_id
        
        return self.storage.aggregate_logs(field)
    
    def get_time_range_stats(
        self,
        agent_id: str = None,
        interval: str = "hour"
    ) -> List[Dict]:
        """時間範圍統計"""
        # 獲取最近 24 小時數據
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        logs = self.storage.search_logs(
            agent_id=agent_id,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            limit=10000
        )
        
        # 按時間分組
        if interval == "hour":
            format_str = "%Y-%m-%d %H:00"
        elif interval == "day":
            format_str = "%Y-%m-%d"
        else:
            format_str = "%Y-%m-%d %H:00"
        
        stats = {}
        for log in logs:
            ts = datetime.fromisoformat(log["timestamp"])
            key = ts.strftime(format_str)
            
            if key not in stats:
                stats[key] = {"count": 0, "error": 0, "warning": 0, "info": 0}
            
            stats[key]["count"] += 1
            level = log["level"]
            if level in stats[key]:
                stats[key][level] += 1
        
        # 轉換為列表
        result = []
        for ts, data in sorted(stats.items()):
            result.append({
                "timestamp": ts,
                **data
            })
        
        return result
    
    def get_top_agents(self, limit: int = 10) -> List[Dict]:
        """最活跃 Agent"""
        cursor = self.storage.conn.cursor()
        cursor.execute("""
            SELECT agent_id, COUNT(*) as count 
            FROM logs 
            WHERE agent_id IS NOT NULL 
            GROUP BY agent_id 
            ORDER BY count DESC 
            LIMIT ?
        """, (limit,))
        
        return [{"agent_id": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    def get_error_context(self, log_id: int, context_lines: int = 5) -> Dict:
        """獲取錯誤上下文"""
        cursor = self.storage.conn.cursor()
        
        # 獲取當前日誌
        cursor.execute("SELECT * FROM logs WHERE id = ?", (log_id,))
        row = cursor.fetchone()
        
        if not row:
            return {"error": "Log not found"}
        
        session_id = row["session_id"]
        timestamp = row["timestamp"]
        
        # 獲取前後日誌
        cursor.execute("""
            SELECT * FROM logs 
            WHERE session_id = ? AND id != ?
            ORDER BY ABS(julianday(timestamp) - julianday(?))
            LIMIT ?
        """, (session_id, log_id, timestamp, context_lines * 2))
        
        context = []
        for r in cursor.fetchall():
            context.append({
                "id": r["id"],
                "timestamp": r["timestamp"],
                "level": r["level"],
                "message": r["message"]
            })
        
        return {
            "target": {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "level": row["level"],
                "message": row["message"]
            },
            "context": context
        }


# ============== 快捷函數 ==============

def search(
    query: str = None,
    levels: List[str] = None,
    agent_id: str = None,
    session_id: str = None,
    limit: int = 100
) -> Dict:
    """快捷搜尋"""
    sq = SearchQuery(
        query=query,
        levels=levels,
        agent_ids=[agent_id] if agent_id else None,
        session_ids=[session_id] if session_id else None,
        limit=limit
    )
    return LogSearch().search(sq)


# ============== 主程式 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("🔍 Log Search Test")
    print("=" * 50)
    
    engine = LogSearch()
    
    # 測試搜尋
    print("\n📥 Search all:")
    result = engine.search(SearchQuery(limit=5))
    print(f"  Total: {result['total']}")
    for log in result["results"]:
        print(f"  [{log['level']}] {log['message']}")
    
    # 聚合
    print("\n📊 Aggregate by level:")
    agg = engine.aggregate()
    for level, count in agg.items():
        print(f"  {level}: {count}")
    
    # Top agents
    print("\n🏆 Top Agents:")
    for item in engine.get_top_agents():
        print(f"  {item['agent_id']}: {item['count']}")
    
    # 時間範圍
    print("\n📈 Time range stats:")
    stats = engine.get_time_range_stats()
    for s in stats[:5]:
        print(f"  {s['timestamp']}: {s['count']} logs")
    
    print("\n✅ Search test complete!")
