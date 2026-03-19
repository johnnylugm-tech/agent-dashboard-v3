#!/usr/bin/env python3
"""
執行路徑視覺化 - Agent Monitor v3

功能：
- 樹狀圖生成
- 時間軸生成
- Mermaid 導出
- 執行差異對比
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

from storage import storage


@dataclass
class TraceStep:
    """追蹤步驟"""
    id: int
    trace_id: str
    parent_id: Optional[int]
    step_type: str
    name: str
    input_data: Dict
    output_data: Dict
    tokens: int
    cost: float
    duration_ms: int
    status: str
    started_at: str
    completed_at: Optional[str]
    children: List['TraceStep'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class TraceVisualizer:
    """執行路徑視覺化"""
    
    def __init__(self):
        self.storage = storage
    
    def generate_tree(self, trace_id: str) -> Dict:
        """生成樹狀結構"""
        # 獲取所有步驟
        cursor = self.storage.conn.cursor()
        cursor.execute("""
            SELECT * FROM traces WHERE trace_id = ? ORDER BY started_at
        """, (trace_id,))
        
        rows = cursor.fetchall()
        if not rows:
            return {"error": "Trace not found"}
        
        # 轉換為對象
        steps = []
        for row in rows:
            steps.append(TraceStep(
                id=row["id"],
                trace_id=row["trace_id"],
                parent_id=row["parent_id"],
                step_type=row["step_type"],
                name=row["name"],
                input_data=json.loads(row["input_data"]) if row["input_data"] else {},
                output_data=json.loads(row["output_data"]) if row["output_data"] else {},
                tokens=row["tokens"],
                cost=row["cost"],
                duration_ms=row["duration_ms"],
                status=row["status"],
                started_at=row["started_at"],
                completed_at=row["completed_at"]
            ))
        
        # 構建樹
        step_map = {s.id: s for s in steps}
        root = None
        
        for step in steps:
            if step.parent_id is None:
                root = step
            else:
                parent = step_map.get(step.parent_id)
                if parent:
                    parent.children.append(step)
        
        if root is None:
            return {"error": "Root step not found"}
        
        return self._tree_to_dict(root)
    
    def _tree_to_dict(self, step: TraceStep) -> Dict:
        """轉換樹為字典"""
        return {
            "id": step.id,
            "name": step.name,
            "type": step.step_type,
            "status": step.status,
            "tokens": step.tokens,
            "cost": step.cost,
            "duration_ms": step.duration_ms,
            "started_at": step.started_at,
            "completed_at": step.completed_at,
            "input": step.input_data,
            "output": step.output_data,
            "children": [self._tree_to_dict(c) for c in step.children]
        }
    
    def generate_timeline(self, trace_id: str) -> Dict:
        """生成時間軸"""
        cursor = self.storage.conn.cursor()
        cursor.execute("""
            SELECT * FROM traces WHERE trace_id = ? ORDER BY started_at
        """, (trace_id,))
        
        rows = cursor.fetchall()
        if not rows:
            return {"error": "Trace not found"}
        
        events = []
        for row in rows:
            events.append({
                "id": row["id"],
                "name": row["name"],
                "type": row["step_type"],
                "status": row["status"],
                "start": row["started_at"],
                "end": row["completed_at"],
                "duration_ms": row["duration_ms"],
                "tokens": row["tokens"],
                "cost": row["cost"]
            })
        
        # 計算總時間
        start_time = events[0]["start"] if events else None
        end_time = events[-1]["end"] if events else None
        
        return {
            "trace_id": trace_id,
            "start_time": start_time,
            "end_time": end_time,
            "total_duration_ms": sum(e["duration_ms"] for e in events),
            "total_tokens": sum(e["tokens"] for e in events),
            "total_cost": sum(e["cost"] for e in events),
            "events": events
        }
    
    def to_mermaid(self, trace_id: str) -> str:
        """轉換為 Mermaid 圖"""
        tree = self.generate_tree(trace_id)
        
        if "error" in tree:
            return f"Error: {tree['error']}"
        
        lines = ["```mermaid", "graph TD"]
        
        def add_nodes(step: Dict, parent_id: str = None):
            node_id = f"step{step['id']}"
            label = f"{step['name']}\n({step['type']})"
            status = step.get("status", "running")
            
            # 樣式
            if status == "failed":
                style = f"style {node_id} fill:#f87171,stroke:#ef4444"
            elif status == "completed":
                style = f"style {node_id} fill:#86efac,stroke:#22c55e"
            else:
                style = f"style {node_id} fill:#fde047,stroke:#eab308"
            
            lines.append(f"    {node_id}[\"{label}\"]")
            lines.append(f"    {style}")
            
            # 連線
            if parent_id:
                lines.append(f"    {parent_id} --> {node_id}")
            
            # 子節點
            for child in step.get("children", []):
                add_nodes(child, node_id)
        
        add_nodes(tree)
        
        lines.append("```")
        
        return "\n".join(lines)
    
    def to_ascii_tree(self, trace_id: str) -> str:
        """轉換為 ASCII 樹"""
        tree = self.generate_tree(trace_id)
        
        if "error" in tree:
            return f"Error: {tree['error']}"
        
        lines = [f"📊 Trace: {trace_id}"]
        
        def print_tree(step: Dict, prefix: str = "", is_last: bool = True):
            connector = "└── " if is_last else "├── "
            
            status_icon = {
                "completed": "✅",
                "failed": "❌",
                "running": "⏳"
            }.get(step.get("status", ""), "❓")
            
            duration = step.get("duration_ms", 0)
            tokens = step.get("tokens", 0)
            
            line = f"{prefix}{connector}{status_icon} {step['name']} ({step['type']}) - {duration}ms, {tokens}tokens"
            lines.append(line)
            
            children = step.get("children", [])
            for i, child in enumerate(children):
                new_prefix = prefix + ("    " if is_last else "│   ")
                print_tree(child, new_prefix, i == len(children) - 1)
        
        print_tree(tree)
        
        # 統計
        total_duration = tree.get("duration_ms", 0)
        total_tokens = tree.get("tokens", 0)
        total_cost = tree.get("cost", 0)
        
        lines.append("")
        lines.append(f"📈 Total: {total_duration}ms, {total_tokens}tokens, ${total_cost:.4f}")
        
        return "\n".join(lines)
    
    def compare(self, trace_id_1: str, trace_id_2: str) -> Dict:
        """對比兩個執行"""
        tree1 = self.generate_tree(trace_id_1)
        tree2 = self.generate_tree(trace_id_2)
        
        if "error" in tree1:
            return {"error": f"Trace 1: {tree1['error']}"}
        if "error" in tree2:
            return {"error": f"Trace 2: {tree2['error']}"}
        
        def extract_stats(tree: Dict) -> Dict:
            def sum_tree(step: Dict) -> Dict:
                stats = {
                    "duration": step.get("duration_ms", 0),
                    "tokens": step.get("tokens", 0),
                    "cost": step.get("cost", 0),
                    "steps": 1
                }
                
                for child in step.get("children", []):
                    child_stats = sum_tree(child)
                    for k in stats:
                        stats[k] += child_stats[k]
                
                return stats
            
            return sum_tree(tree)
        
        stats1 = extract_stats(tree1)
        stats2 = extract_stats(tree2)
        
        return {
            "trace_1": {
                "id": trace_id_1,
                **stats1
            },
            "trace_2": {
                "id": trace_id_2,
                **stats2
            },
            "diff": {
                "duration_ms": stats2["duration_ms"] - stats1["duration_ms"],
                "tokens": stats2["tokens"] - stats1["tokens"],
                "cost": stats2["cost"] - stats1["cost"],
                "steps": stats2["steps"] - stats1["steps"]
            }
        }


# ============== 快捷函數 ==============

def get_tree(trace_id: str) -> Dict:
    """獲取樹狀圖"""
    return TraceVisualizer().generate_tree(trace_id)


def get_timeline(trace_id: str) -> Dict:
    """獲取時間軸"""
    return TraceVisualizer().generate_timeline(trace_id)


def to_mermaid(trace_id: str) -> str:
    """轉換為 Mermaid"""
    return TraceVisualizer().to_mermaid(trace_id)


def to_ascii(trace_id: str) -> str:
    """轉換為 ASCII"""
    return TraceVisualizer().to_ascii_tree(trace_id)


# ============== 主程式 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("🌳 Trace Visualizer Test")
    print("=" * 50)
    
    viz = TraceVisualizer()
    
    # 測試樹
    print("\n🌲 Tree View:")
    tree = viz.generate_tree("trace-001")
    print(f"  {json.dumps(tree, indent=2)[:500]}...")
    
    # ASCII
    print("\n📝 ASCII Tree:")
    print(viz.to_ascii("trace-001"))
    
    # Mermaid
    print("\n📊 Mermaid:")
    print(viz.to_mermaid("trace-001"))
    
    print("\n✅ Visualizer test complete!")
