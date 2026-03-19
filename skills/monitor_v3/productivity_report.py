#!/usr/bin/env python3
"""
Team Productivity Report - 團隊產能報告

生成團隊產能報告：任務完成數/成功率/成本效率
"""

from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict


class ProductivityReporter:
    """團隊產能報告生成器"""
    
    def __init__(self, journey_tracker=None, cost_tracker=None, 
                 alert_manager=None):
        """
        初始化
        
        Args:
            journey_tracker: JourneyTracker 實例
            cost_tracker: CostTracker 實例
            alert_manager: AlertManager 實例
        """
        self.journey = journey_tracker
        self.cost = cost_tracker
        self.alerts = alert_manager
    
    def generate_report(self, period: str = "monthly") -> Dict:
        """
        生成產能報告
        
        Args:
            period: daily, weekly, monthly
            
        Returns:
            報告字典
        """
        report = {
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "summary": self._get_summary(period),
            "metrics": self._get_metrics(period),
            "agents": self._get_agent_metrics(period),
            "trends": self._get_trends(period),
            "recommendations": self._get_recommendations(period)
        }
        
        return report
    
    def _get_summary(self, period: str) -> Dict:
        """獲取摘要"""
        # 任務數據
        total_tasks = 100  # 模擬數據
        completed_tasks = 85
        failed_tasks = 15
        
        # 成本數據
        total_cost = 500.0
        
        # 計算指標
        success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        cost_per_task = total_cost / total_tasks if total_tasks > 0 else 0
        avg_task_duration = 120  # 秒
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": round(success_rate, 1),
            "total_cost": round(total_cost, 2),
            "cost_per_task": round(cost_per_task, 2),
            "avg_task_duration_seconds": avg_task_duration
        }
    
    def _get_metrics(self, period: str) -> Dict:
        """獲取詳細指標"""
        return {
            "completion": {
                "on_time": 75,
                "delayed": 20,
                "timeout": 5,
                "on_time_rate": "75%"
            },
            "quality": {
                "re_work_required": 10,
                "re_work_rate": "10%",
                "escalations": 5
            },
            "efficiency": {
                "avg_turns_per_task": 5.2,
                "avg_retries": 1.3,
                "cache_hit_rate": "35%"
            }
        }
    
    def _get_agent_metrics(self, period: str) -> List[Dict]:
        """獲取各 Agent 指標"""
        # 模擬數據
        agents = [
            {
                "agent_id": "agent-001",
                "name": "Code Generator",
                "tasks": 50,
                "success_rate": 90.0,
                "avg_duration": 100,
                "cost": 150.0,
                "efficiency_score": 85
            },
            {
                "agent_id": "agent-002",
                "name": "Reviewer",
                "tasks": 30,
                "success_rate": 95.0,
                "avg_duration": 60,
                "cost": 80.0,
                "efficiency_score": 92
            },
            {
                "agent_id": "agent-003",
                "name": "Researcher",
                "tasks": 20,
                "success_rate": 80.0,
                "avg_duration": 180,
                "cost": 270.0,
                "efficiency_score": 70
            }
        ]
        
        return sorted(agents, key=lambda x: x["efficiency_score"], reverse=True)
    
    def _get_trends(self, period: str) -> Dict:
        """獲取趨勢"""
        days = 30 if period == "monthly" else 7
        
        return {
            "success_rate_trend": "+5%",  # 本期 vs 上期
            "cost_trend": "-10%",
            "efficiency_trend": "+15%",
            "daily_breakdown": [
                {"day": f"Day {i}", "tasks": 10 + i, "success_rate": 80 + i * 0.5}
                for i in range(1, days + 1)
            ]
        }
    
    def _get_recommendations(self, period: str) -> List[str]:
        """獲取建議"""
        recommendations = []
        
        # 基於數據生成建議
        summary = self._get_summary(period)
        
        if summary["success_rate"] < 80:
            recommendations.append("⚠️ 成功率偏低，建議檢查 Agent 配置")
        
        if summary["cost_per_task"] > 10:
            recommendations.append("💰 單位成本偏高，考慮優化提示詞或使用更便宜的模型")
        
        recommendations.append("📈 整體趨勢良好，維持當前配置")
        
        return recommendations
    
    def generate_text_report(self, period: str = "monthly") -> str:
        """生成文字報告"""
        report = self.generate_report(period)
        
        lines = [
            f"\n{'='*60}",
            f"📊 Team Productivity Report - {period.upper()}",
            f"{'='*60}",
            "",
            "📋 Summary",
            "-" * 40,
            f"  Total Tasks:    {report['summary']['total_tasks']}",
            f"  Completed:       {report['summary']['completed_tasks']}",
            f"  Failed:          {report['summary']['failed_tasks']}",
            f"  Success Rate:    {report['summary']['success_rate']}%",
            f"  Total Cost:      ${report['summary']['total_cost']}",
            f"  Cost/Task:      ${report['summary']['cost_per_task']}",
            "",
            "🤖 Agent Performance",
            "-" * 40,
        ]
        
        for agent in report["agents"]:
            lines.append(f"\n  {agent['name']} ({agent['agent_id']})")
            lines.append(f"    Tasks: {agent['tasks']}, Success: {agent['success_rate']}%")
            lines.append(f"    Cost: ${agent['cost']}, Efficiency: {agent['efficiency_score']}")
        
        lines.extend([
            "",
            "💡 Recommendations",
            "-" * 40,
        ])
        
        for rec in report["recommendations"]:
            lines.append(f"  {rec}")
        
        lines.append(f"\n{'='*60}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(lines)


# 使用範例
if __name__ == "__main__":
    reporter = ProductivityReporter()
    
    # 生成報告
    report = reporter.generate_report("monthly")
    
    # 打印文字報告
    print(reporter.generate_text_report("monthly"))
