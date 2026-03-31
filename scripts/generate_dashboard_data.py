#!/usr/bin/env python3
"""
Heartbeat 儀表板數據生成器
生成 JSON 數據供 dashboard.html 使用
"""

import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/johnny/.openclaw/workspace-musk")
DASHBOARD_DATA_FILE = WORKSPACE / "dashboard_data.json"


def generate_dashboard_data():
    """生成儀表板所需的數據"""
    
    data = {
        "timestamp": datetime.now().isoformat(),
        
        # 年度目標
        "annual_goals": {
            "資訊領先": {"current": 10, "target": 52, "unit": "篇"},
            "翻譯能力": {"current": 0, "target": 12, "unit": "篇"},
            "實戰經驗": {"current": 5, "target": 20, "unit": "個"},
            "落地應用": {"current": 0, "target": 1, "unit": "個"}
        },
        
        # 每週任務
        "weekly_tasks": {
            "已完成": 3,
            "進行中": 2,
            "待處理": 5
        },
        
        # 阻塞項目
        "blockers": [
            {"icon": "⚠️", "text": "GitHub 尚未初始化", "owner": "self"},
            {"icon": "⏸️", "text": "等待 Johnny 回饋（投影片/影片審核）", "owner": "Johnny"},
            {"icon": "⏳", "text": "TDX API 審核中（已改用 PDF 方案）", "owner": "self"}
        ],
        
        # 待辦清單
        "todos": [
            {"text": "GitHub Repo 初始化 + push", "status": "pending", "owner": "self"},
            {"text": "高鐵 v1 時刻表功能優化", "status": "pending", "owner": "self"},
            {"text": "投影片/影片根據回饋調整", "status": "pending", "owner": "self"},
            {"text": "Heartbeat 演化 + 自動化", "status": "done", "owner": "self"}
        ],
        
        # 趨勢數據
        "trend_data": {
            "labels": ["W1", "W2", "W3", "W4"],
            "values": [3, 5, 3, 0]
        },
        
        # 工具測試
        "tools_data": {
            "labels": ["AI Chat", "Agent", "Dev", "Tools", "Other"],
            "tested": [2, 1, 1, 1, 0],
            "target": [5, 5, 5, 5, 0]
        }
    }
    
    # 寫入 JSON
    with open(DASHBOARD_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 儀表板數據已更新: {DASHBOARD_DATA_FILE}")
    return data


if __name__ == "__main__":
    generate_dashboard_data()
