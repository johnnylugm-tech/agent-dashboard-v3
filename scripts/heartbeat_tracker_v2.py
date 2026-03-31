#!/usr/bin/env python3
"""
Heartbeat 自動化追蹤系統 v2

功能：
- 自動目標追蹤
- 進度計算
- 趨勢分析
- 提醒觸發
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Goal:
    """目標"""
    id: str
    name: str
    target: int
    current: int
    unit: str
    period: str  # daily, weekly, monthly
    category: str
    priority: str  # high, medium, low
    created_at: str
    deadline: str = None
    
    @property
    def progress(self) -> float:
        return (self.current / self.target * 100) if self.target > 0 else 0
    
    @property
    def status(self) -> str:
        if self.progress >= 100:
            return "completed"
        elif self.progress >= 80:
            return "on_track"
        elif self.progress >= 50:
            return "at_risk"
        else:
            return "behind"


@dataclass
class Task:
    """任務"""
    id: str
    name: str
    goal_id: str
    status: str  # pending, in_progress, completed
    priority: str
    due_date: str = None
    completed_at: str = None
    
    
class HeartbeatTracker:
    """Heartbeat 追蹤器"""
    
    def __init__(self, config_path: str = "./data/heartbeat.json"):
        self.config_path = config_path
        self.goals: Dict[str, Goal] = {}
        self.tasks: Dict[str, Task] = {}
        self.history: List[Dict] = []
        self._load()
    
    def _load(self):
        """從文件加載"""
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                
                for g in data.get("goals", []):
                    self.goals[g["id"]] = Goal(**g)
                    
                for t in data.get("tasks", []):
                    self.tasks[t["id"]] = Task(**t)
                    
                self.history = data.get("history", [])
        except FileNotFoundError:
            pass
    
    def _save(self):
        """保存到文件"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        data = {
            "goals": [asdict(g) for g in self.goals.values()],
            "tasks": [asdict(t) for t in self.tasks.values()],
            "history": self.history
        }
        
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=2)
    
    # ============== 目標管理 ==============
    
    def add_goal(
        self,
        name: str,
        target: int,
        unit: str,
        period: str = "weekly",
        category: str = "general",
        priority: str = "medium"
    ) -> str:
        """新增目標"""
        goal_id = f"goal-{len(self.goals) + 1}"
        
        goal = Goal(
            id=goal_id,
            name=name,
            target=target,
            current=0,
            unit=unit,
            period=period,
            category=category,
            priority=priority,
            created_at=datetime.now().isoformat()
        )
        
        self.goals[goal_id] = goal
        self._save()
        return goal_id
    
    def update_progress(self, goal_id: str, current: int):
        """更新進度"""
        if goal_id in self.goals:
            self.goals[goal_id].current = current
            
            # 記錄歷史
            self.history.append({
                "timestamp": datetime.now().isoformat(),
                "goal_id": goal_id,
                "value": current,
                "progress": self.goals[goal_id].progress
            })
            
            self._save()
    
    def get_dashboard(self) -> Dict:
        """獲取儀表板數據"""
        total_goals = len(self.goals)
        completed = sum(1 for g in self.goals.values() if g.status == "completed")
        on_track = sum(1 for g in self.goals.values() if g.status == "on_track")
        at_risk = sum(1 for g in self.goals.values() if g.status == "at_risk")
        behind = sum(1 for g in self.goals.values() if g.status == "behind")
        
        # 按類別分組
        by_category = {}
        for g in self.goals.values():
            if g.category not in by_category:
                by_category[g.category] = []
            by_category[g.category].append({
                "id": g.id,
                "name": g.name,
                "progress": g.progress,
                "status": g.status
            })
        
        return {
            "summary": {
                "total": total_goals,
                "completed": completed,
                "on_track": on_track,
                "at_risk": at_risk,
                "behind": behind,
                "completion_rate": (completed / total_goals * 100) if total_goals > 0 else 0
            },
            "by_category": by_category,
            "trending": self._get_trending()
        }
    
    def _get_trending(self) -> List[Dict]:
        """獲取趨勢"""
        if not self.history:
            return []
        
        # 最近的歷史記錄
        recent = sorted(self.history, key=lambda x: x["timestamp"], reverse=True)[:20]
        
        # 按目標分組
        by_goal = {}
        for h in recent:
            gid = h["goal_id"]
            if gid not in by_goal:
                by_goal[gid] = []
            by_goal[gid].append(h)
        
        # 計算趨勢
        trending = []
        for gid, records in by_goal.items():
            if len(records) >= 2:
                latest = records[0]["progress"]
                previous = records[-1]["progress"]
                delta = latest - previous
                
                trending.append({
                    "goal_id": gid,
                    "goal_name": self.goals[gid].name,
                    "delta": delta,
                    "trend": "up" if delta > 0 else "down" if delta < 0 else "stable"
                })
        
        return trending
    
    # ============== 報告生成 ==============
    
    def generate_report(self, period: str = "weekly") -> str:
        """生成報告"""
        dashboard = self.get_dashboard()
        
        lines = [
            f"# 📊 Heartbeat 報告",
            f"",
            f"## 總覽",
            f"- 總目標: {dashboard['summary']['total']}",
            f"- 完成: {dashboard['summary']['completed']}",
            f"- 進行中: {dashboard['summary']['on_track']}",
            f"- 風險: {dashboard['summary']['at_risk']}",
            f"- 落後: {dashboard['summary']['behind']}",
            f"- 完成率: {dashboard['summary']['completion_rate']:.1f}%",
            f"",
            f"## 趨勢"
        ]
        
        for t in dashboard.get("trending", []):
            emoji = "📈" if t["trend"] == "up" else "📉" if t["trend"] == "down" else "➡️"
            lines.append(f"- {emoji} {t['goal_name']}: {t['delta']:+.1f}%")
        
        return "\n".join(lines)
    
    # ============== 提醒 ==============
    
    def check_reminders(self) -> List[Dict]:
        """檢查提醒"""
        reminders = []
        
        for goal in self.goals.values():
            # 落後提醒
            if goal.status == "behind" and goal.priority == "high":
                reminders.append({
                    "type": "goal_behind",
                    "goal_id": goal.id,
                    "message": f"⚠️ 目標落後: {goal.name} ({goal.progress:.0f}%)",
                    "priority": "high"
                })
            
            # 風險提醒
            if goal.status == "at_risk":
                reminders.append({
                    "type": "goal_at_risk",
                    "goal_id": goal.id,
                    "message": f"🔔 目標風險: {goal.name} ({goal.progress:.0f}%)",
                    "priority": "medium"
                })
            
            # 完成提醒
            if goal.status == "completed" and goal.progress >= 100:
                reminders.append({
                    "type": "goal_completed",
                    "goal_id": goal.id,
                    "message": f"🎉 目標完成: {goal.name}!",
                    "priority": "low"
                })
        
        return reminders


# ============== 主程式 ==============

if __name__ == "__main__":
    tracker = HeartbeatTracker()
    
    # 測試
    print("=" * 50)
    print("💓 Heartbeat Tracker Test")
    print("=" * 50)
    
    # 添加目標
    goal_id = tracker.add_goal(
        name="每週趨勢解讀",
        target=5,
        unit="篇",
        period="weekly",
        category="資訊領先",
        priority="high"
    )
    
    # 更新進度
    tracker.update_progress(goal_id, 3)
    
    # 儀表板
    print("\n📊 Dashboard:")
    dashboard = tracker.get_dashboard()
    print(f"  總目標: {dashboard['summary']['total']}")
    print(f"  完成率: {dashboard['summary']['completion_rate']:.1f}%")
    
    # 提醒
    print("\n🔔 Reminders:")
    for r in tracker.check_reminders():
        print(f"  {r['message']}")
    
    # 報告
    print("\n" + tracker.generate_report())
    
    print("\n✅ Tracker test complete!")
