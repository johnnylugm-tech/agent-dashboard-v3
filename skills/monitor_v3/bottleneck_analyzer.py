#!/usr/bin/env python3
"""
Bottleneck Analyzer - 瓶頸診斷

分析 Agent 執行中的瓶頸問題
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict


@dataclass
class Bottleneck:
    """瓶頸問題"""
    type: str           # bottleneck 類型
    severity: str       # critical, warning, info
    description: str   # 描述
    location: str      # 位置（agent/task）
    impact: str        # 影響
    suggestion: str    # 建議


class BottleneckAnalyzer:
    """瓶頸分析器"""
    
    def __init__(self, journey_tracker=None, cost_tracker=None):
        """
        初始化分析器
        
        Args:
            journey_tracker: JourneyTracker 實例
            cost_tracker: CostTracker 實例
        """
        self.journey_tracker = journey_tracker
        self.cost_tracker = cost_tracker
    
    def analyze_agent(self, agent_id: str, duration_minutes: int = 30) -> Dict:
        """
        分析 Agent 瓶頸
        
        Args:
            agent_id: Agent ID
            duration_minutes: 分析時長（分鐘）
            
        Returns:
            瓶頸分析結果
        """
        bottlenecks = []
        
        # 1. 延遲分析
        latency_issues = self._analyze_latency(agent_id, duration_minutes)
        bottlenecks.extend(latency_issues)
        
        # 2. 成本分析
        cost_issues = self._analyze_cost(agent_id, duration_minutes)
        bottlenecks.extend(cost_issues)
        
        # 3. 錯誤分析
        error_issues = self._analyze_errors(agent_id, duration_minutes)
        bottlenecks.extend(error_issues)
        
        # 4. 資源分析
        resource_issues = self._analyze_resources(agent_id, duration_minutes)
        bottlenecks.extend(resource_issues)
        
        return {
            "agent_id": agent_id,
            "analyzed_at": datetime.now().isoformat(),
            "duration_minutes": duration_minutes,
            "bottlenecks": [self._bottleneck_to_dict(b) for b in bottlenecks],
            "summary": {
                "total": len(bottlenecks),
                "critical": len([b for b in bottlenecks if b.severity == "critical"]),
                "warning": len([b for b in bottlenecks if b.severity == "warning"]),
                "info": len([b for b in bottlenecks if b.severity == "info"])
            }
        }
    
    def _analyze_latency(self, agent_id: str, duration_minutes: int) -> List[Bottleneck]:
        """分析延遲瓶頸"""
        issues = []
        
        # 假設有 latency 數據
        # 實際實現需要從 journey_tracker 獲取
        avg_latency = 5000  # 假設平均 5 秒
        
        if avg_latency > 10000:
            issues.append(Bottleneck(
                type="latency",
                severity="critical",
                description=f"平均延遲 {avg_latency/1000:.1f}s 過高",
                location=agent_id,
                impact="用戶體驗差",
                suggestion="考慮使用更快的模型或增加快取"
            ))
        elif avg_latency > 5000:
            issues.append(Bottleneck(
                type="latency",
                severity="warning",
                description=f"平均延遲 {avg_latency/1000:.1f}s 偏高",
                location=agent_id,
                impact="可能影響用戶體驗",
                suggestion="優化提示詞或減少輸出長度"
            ))
        
        return issues
    
    def _analyze_cost(self, agent_id: str, duration_minutes: int) -> List[Bottleneck]:
        """分析成本瓶頸"""
        issues = []
        
        if not self.cost_tracker:
            return issues
        
        # 獲取成本數據
        cost_data = self.cost_tracker.get_agent_cost(agent_id, "daily")
        daily_cost = cost_data.get("total_cost", 0)
        
        if daily_cost > 50:
            issues.append(Bottleneck(
                type="cost",
                severity="critical",
                description=f"日成本 ${daily_cost:.2f} 過高",
                location=agent_id,
                impact="預算超支風險",
                suggestion="切換到更便宜的模型或優化請求"
            ))
        elif daily_cost > 20:
            issues.append(Bottleneck(
                type="cost",
                severity="warning",
                description=f"日成本 ${daily_cost:.2f} 偏高",
                location=agent_id,
                impact="成本可控但需關注",
                suggestion="考慮使用低成本模型處理簡單任務"
            ))
        
        return issues
    
    def _analyze_errors(self, agent_id: str, duration_minutes: int) -> List[Bottleneck]:
        """分析錯誤瓶頸"""
        issues = []
        
        # 假設有錯誤率數據
        error_rate = 0.15  # 15%
        
        if error_rate > 0.2:
            issues.append(Bottleneck(
                type="error_rate",
                severity="critical",
                description=f"錯誤率 {error_rate*100:.1f}% 過高",
                location=agent_id,
                impact="任務失敗率高",
                suggestion="檢查 API 穩定性或模型選擇"
            ))
        elif error_rate > 0.1:
            issues.append(Bottleneck(
                type="error_rate",
                severity="warning",
                description=f"錯誤率 {error_rate*100:.1f}% 偏高",
                location=agent_id,
                impact="部分任務失敗",
                suggestion="增加錯誤處理和重試機制"
            ))
        
        return issues
    
    def _analyze_resources(self, agent_id: str, duration_minutes: int) -> List[Bottleneck]:
        """分析資源瓶頸"""
        issues = []
        
        # 假設有資源數據
        cpu_usage = 85  # 85%
        
        if cpu_usage > 90:
            issues.append(Bottleneck(
                type="cpu",
                severity="critical",
                description=f"CPU 使用率 {cpu_usage}% 過高",
                location=agent_id,
                impact="處理速度下降",
                suggestion="優化計算密集型任務"
            ))
        
        return issues
    
    def _bottleneck_to_dict(self, bottleneck: Bottleneck) -> Dict:
        """轉換為字典"""
        return {
            "type": bottleneck.type,
            "severity": bottleneck.severity,
            "description": bottleneck.description,
            "location": bottleneck.location,
            "impact": bottleneck.impact,
            "suggestion": bottleneck.suggestion
        }
    
    def get_heatmap_data(self, agent_id: str = None) -> Dict:
        """
        獲取熱點圖數據
        
        Args:
            agent_id: 可選的 Agent ID
            
        Returns:
            熱點圖數據
        """
        # 模擬熱點數據
        return {
            "agents": ["agent-001", "agent-002", "agent-003"],
            "metrics": ["latency", "cost", "errors", "cpu"],
            "data": [
                [50, 30, 20, 10],  # agent-001
                [80, 60, 40, 30],  # agent-002
                [30, 20, 10, 5],   # agent-003
            ]
        }


# 使用範例
if __name__ == "__main__":
    analyzer = BottleneckAnalyzer()
    
    result = analyzer.analyze_agent("agent-001", 30)
    
    print(f"\n=== Bottleneck Analysis: {result['agent_id']} ===")
    print(f"Duration: {result['duration_minutes']} minutes")
    print(f"\nSummary: {result['summary']}")
    
    print("\nBottlenecks:")
    for b in result['bottlenecks']:
        print(f"  [{b['severity'].upper()}] {b['description']}")
        print(f"    → {b['suggestion']}")
