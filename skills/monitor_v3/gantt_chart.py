#!/usr/bin/env python3
"""
Gantt Chart Generator - Gantt 圖生成器

生成任務執行的 Gantt 圖（文字版）
"""

from typing import Dict, List
from datetime import datetime, timedelta


class GanttGenerator:
    """Gantt 圖生成器"""
    
    def __init__(self, journey_tracker=None):
        """
        初始化
        
        Args:
            journey_tracker: JourneyTracker 實例
        """
        self.journey = journey_tracker
    
    def generate(self, agent_id: str = None, hours: int = 24) -> str:
        """
        生成 Gantt 圖
        
        Args:
            agent_id: 可選的 Agent ID
            hours: 顯示過去幾小時
            
        Returns:
            Gantt 圖字串
        """
        # 模擬數據（實際從 journey_tracker 獲取）
        tasks = self._get_tasks(agent_id, hours)
        
        if not tasks:
            return "No tasks in this period"
        
        # 計算時間範圍
        now = datetime.now()
        start = now - timedelta(hours=hours)
        
        lines = [
            f"\n{'='*80}",
            f"Gantt Chart - Last {hours} hours",
            f"{'='*80}\n",
            "Time       | " + " | ".join([f"Task {i+1}" for i in range(min(5, len(tasks)))]) + " |",
            "-" * 80
        ]
        
        # 每小時一行
        for h in range(hours):
            hour_time = start + timedelta(hours=h)
            time_str = hour_time.strftime("%H:00")
            
            row = [time_str]
            
            for task in tasks[:5]:  # 最多顯示 5 個任務
                # 檢查這個小時是否有任務執行
                task_start = task.get("start", now - timedelta(hours=1))
                task_end = task.get("end", now)
                
                if task_start <= hour_time < task_end:
                    # 根據狀態顯示
                    status = task.get("status", "running")
                    if status == "completed":
                        row.append("█")
                    elif status == "running":
                        row.append("▓")
                    elif status == "failed":
                        row.append("✗")
                    else:
                        row.append("░")
                else:
                    row.append(" ")
            
            lines.append(" | ".join([f"{r:10s}" for r in row]) + " |")
        
        # 圖例
        lines.extend([
            "",
            "Legend: █ Completed | ▓ Running | ✗ Failed | ░ Waiting",
            f"{'='*80}"
        ])
        
        return "\n".join(lines)
    
    def _get_tasks(self, agent_id: str, hours: int) -> List[Dict]:
        """獲取任務數據"""
        # 模擬數據
        now = datetime.now()
        
        tasks = [
            {
                "task_id": "task-001",
                "name": "Code Generation",
                "start": now - timedelta(hours=5),
                "end": now - timedelta(hours=3),
                "status": "completed",
                "agent": "agent-001"
            },
            {
                "task_id": "task-002",
                "name": "Code Review",
                "start": now - timedelta(hours=3),
                "end": now - timedelta(hours=2),
                "status": "completed",
                "agent": "agent-002"
            },
            {
                "task_id": "task-003",
                "name": "Testing",
                "start": now - timedelta(hours=2),
                "end": now - timedelta(hours=1),
                "status": "completed",
                "agent": "agent-001"
            },
            {
                "task_id": "task-004",
                "name": "Deployment",
                "start": now - timedelta(hours=1),
                "end": now,
                "status": "running",
                "agent": "agent-003"
            }
        ]
        
        if agent_id:
            tasks = [t for t in tasks if t.get("agent") == agent_id]
        
        return tasks
    
    def get_timeline(self, task_id: str) -> Dict:
        """獲取任務時間線"""
        # 模擬
        return {
            "task_id": task_id,
            "stages": [
                {"name": "Init", "duration": 5, "status": "completed"},
                {"name": "Execute", "duration": 30, "status": "completed"},
                {"name": "Review", "duration": 10, "status": "completed"},
                {"name": "Complete", "duration": 2, "status": "completed"}
            ],
            "parallel_tasks": [
                {"name": "API Call 1", "start": 5, "duration": 10},
                {"name": "API Call 2", "start": 5, "duration": 15}
            ]
        }


# 使用範例
if __name__ == "__main__":
    generator = GanttGenerator()
    
    print(generator.generate(hours=6))
