#!/usr/bin/env python3
"""
Agent Hierarchy - Agent 階層追蹤

追蹤父子 Agent 關係和執行樹
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AgentStatus(Enum):
    """Agent 狀態"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentNode:
    """Agent 節點"""
    agent_id: str
    name: str
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    status: AgentStatus = AgentStatus.PENDING
    started_at: datetime = None
    completed_at: datetime = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    metadata: Dict = field(default_factory=dict)


class AgentHierarchy:
    """Agent 階層管理器"""
    
    def __init__(self):
        """初始化"""
        self.agents: Dict[str, AgentNode] = {}
        self.root_agents: List[str] = []
    
    def create_agent(self, agent_id: str, name: str, 
                   parent_id: str = None, metadata: Dict = None) -> AgentNode:
        """
        建立 Agent
        
        Args:
            agent_id: Agent ID
            name: 名稱
            parent_id: 父 Agent ID
            metadata: 額外數據
            
        Returns:
            建立的 Agent 節點
        """
        agent = AgentNode(
            agent_id=agent_id,
            name=name,
            parent_id=parent_id,
            status=AgentStatus.PENDING,
            metadata=metadata or {},
            started_at=datetime.now()
        )
        
        self.agents[agent_id] = agent
        
        # 更新父 Agent 的 children
        if parent_id:
            if parent_id in self.agents:
                self.agents[parent_id].children.append(agent_id)
        else:
            # 根 Agent
            self.root_agents.append(agent_id)
        
        return agent
    
    def start_agent(self, agent_id: str):
        """啟動 Agent"""
        if agent_id in self.agents:
            self.agents[agent_id].status = AgentStatus.RUNNING
            self.agents[agent_id].started_at = datetime.now()
    
    def complete_agent(self, agent_id: str, cost: float = 0,
                    input_tokens: int = 0, output_tokens: int = 0):
        """完成 Agent"""
        if agent_id in self.agents:
            self.agents[agent_id].status = AgentStatus.COMPLETED
            self.agents[agent_id].completed_at = datetime.now()
            self.agents[agent_id].cost = cost
            self.agents[agent_id].input_tokens = input_tokens
            self.agents[agent_id].output_tokens = output_tokens
    
    def fail_agent(self, agent_id: str, error: str = None):
        """Agent 失敗"""
        if agent_id in self.agents:
            self.agents[agent_id].status = AgentStatus.FAILED
            self.agents[agent_id].completed_at = datetime.now()
            if error:
                self.agents[agent_id].metadata["error"] = error
    
    def get_tree(self, root_id: str = None) -> Dict:
        """
        獲取 Agent 樹
        
        Args:
            root_id: 根 Agent ID (可選)
            
        Returns:
            樹結構字典
        """
        if root_id:
            roots = [root_id]
        else:
            roots = self.root_agents
        
        def build_tree(agent_id: str) -> Dict:
            agent = self.agents.get(agent_id)
            if not agent:
                return {}
            
            return {
                "agent_id": agent.agent_id,
                "name": agent.name,
                "status": agent.status.value,
                "duration": self._get_duration(agent),
                "cost": agent.cost,
                "children": [build_tree(child_id) for child_id in agent.children]
            }
        
        return [build_tree(root) for root in roots]
    
    def get_stats(self, agent_id: str) -> Dict:
        """獲取 Agent 統計"""
        agent = self.agents.get(agent_id)
        if not agent:
            return {}
        
        # 遞迴計算子 Agent
        total_cost = agent.cost
        total_input = agent.input_tokens
        total_output = agent.output_tokens
        child_count = len(agent.children)
        
        def calculate_stats(aid: str):
            nonlocal total_cost, total_input, total_output, child_count
            a = self.agents.get(aid)
            if a:
                total_cost += a.cost
                total_input += a.input_tokens
                total_output += a.output_tokens
                child_count += len(a.children)
                for child in a.children:
                    calculate_stats(child)
        
        for child in agent.children:
            calculate_stats(child)
        
        return {
            "agent_id": agent_id,
            "name": agent.name,
            "status": agent.status.value,
            "total_cost": total_cost,
            "total_tokens": total_input + total_output,
            "total_children": child_count,
            "depth": self._get_depth(agent_id)
        }
    
    def _get_duration(self, agent: AgentNode) -> float:
        """計算執行時長（秒）"""
        if not agent.started_at:
            return 0
        end = agent.completed_at or datetime.now()
        return (end - agent.started_at).total_seconds()
    
    def _get_depth(self, agent_id: str) -> int:
        """獲取深度"""
        agent = self.agents.get(agent_id)
        if not agent or not agent.parent_id:
            return 0
        return 1 + self._get_depth(agent.parent_id)
    
    def render_tree(self, root_id: str = None, max_depth: int = 3) -> str:
        """
        渲染樹（文字版）
        
        Args:
            root_id: 根 Agent ID
            max_depth: 最大深度
            
        Returns:
            樹狀圖字串
        """
        tree = self.get_tree(root_id)
        
        lines = []
        
        def render_node(node: Dict, indent: int = 0):
            if indent > max_depth:
                return
            
            prefix = "  " * indent
            
            status_icon = {
                "pending": "⏳",
                "running": "🔄",
                "completed": "✅",
                "failed": "❌"
            }.get(node.get("status", ""), "❓")
            
            lines.append(
                f"{prefix}{status_icon} {node.get('name')} ({node.get('agent_id')}) "
                f"- ${node.get('cost', 0):.2f}"
            )
            
            for child in node.get("children", []):
                render_node(child, indent + 1)
        
        for root in tree:
            render_node(root)
        
        return "\n".join(lines)


# 使用範例
if __name__ == "__main__":
    hierarchy = AgentHierarchy()
    
    # 建立根 Agent
    hierarchy.create_agent("agent-001", "Main Agent")
    hierarchy.start_agent("agent-001")
    
    # 建立子 Agent
    hierarchy.create_agent("agent-002", "Code Generator", parent_id="agent-001")
    hierarchy.create_agent("agent-003", "Code Reviewer", parent_id="agent-001")
    hierarchy.create_agent("agent-004", "Tester", parent_id="agent-002")
    
    hierarchy.start_agent("agent-002")
    hierarchy.start_agent("agent-003")
    hierarchy.start_agent("agent-004")
    
    # 完成
    hierarchy.complete_agent("agent-004", cost=0.5, input_tokens=100, output_tokens=50)
    hierarchy.complete_agent("agent-002", cost=1.0, input_tokens=200, output_tokens=100)
    hierarchy.complete_agent("agent-003", cost=0.8, input_tokens=150, output_tokens=80)
    hierarchy.complete_agent("agent-001", cost=2.5, input_tokens=500, output_tokens=300)
    
    # 渲染樹
    print("=== Agent Hierarchy ===")
    print(hierarchy.render_tree())
    
    print("\n=== Stats for agent-001 ===")
    stats = hierarchy.get_stats("agent-001")
    for k, v in stats.items():
        print(f"  {k}: {v}")
