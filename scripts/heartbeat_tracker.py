#!/usr/bin/env python3
"""
Heartbeat 自動化追蹤系統
自動計算進度、觸發報告、記錄日誌
"""

import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/johnny/.openclaw/workspace-musk")
HEARTBEAT_FILE = WORKSPACE / "HEARTBEAT.md"
DAILY_LOG_DIR = WORKSPACE / "memory" / "daily"

# 確保目錄存在
DAILY_LOG_DIR.mkdir(parents=True, exist_ok=True)


def parse_heartbeat():
    """解析 HEARTBEAT.md 提取關鍵指標"""
    if not HEARTBEAT_FILE.exists():
        return None
    
    content = HEARTBEAT_FILE.read_text()
    
    # 解析年度目標
    metrics = {}
    lines = content.split('\n')
    in_metrics = False
    
    for i, line in enumerate(lines):
        if '年度目標' in line:
            in_metrics = True
            continue
        if in_metrics and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4 and parts[1] and parts[1] != '維度':
                metric = parts[1]
                progress = parts[3]
                metrics[metric] = progress
    
    return metrics


def calculate_weekly_progress():
    """計算每週進度"""
    # 讀取 HEARTBEAT
    content = HEARTBEAT_FILE.read_text()
    
    # 解析 W3 目標
    weekly_tasks = []
    lines = content.split('\n')
    in_w3 = False
    
    for line in lines:
        if 'W3' in line and '03/18' in line:
            in_w3 = True
            continue
        if in_w3 and line.startswith('## '):
            break
        if in_w3 and '- [x]' in line:
            weekly_tasks.append((line.strip(), 'done'))
        elif in_w3 and '- [ ]' in line:
            weekly_tasks.append((line.strip(), 'pending'))
    
    return weekly_tasks


def generate_report():
    """生成進度報告"""
    metrics = parse_heartbeat()
    weekly = calculate_weekly_progress()
    
    report = f"""# Heartbeat 報告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 年度指標

| 維度 | 進度 |
|------|------|
"""
    for k, v in (metrics or {}).items():
        report += f"| {k} | {v} |\n"
    
    report += """
## 本週任務

"""
    for task, status in weekly:
        emoji = '✅' if status == 'done' else '⏳'
        task_name = task.replace('- [x]', '').replace('- [ ]', '').strip()
        report += f"- {emoji} {task_name}\n"
    
    # 寫入日誌
    log_file = DAILY_LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"
    log_file.write_text(report)
    
    return report


def check_alerts():
    """檢查是否需要警報"""
    alerts = []
    
    # 檢查 blocker
    content = HEARTBEAT_FILE.read_text()
    if 'GitHub 初始化' in content and '❌' in content:
        alerts.append("⚠️ GitHub 尚未初始化")
    
    if '高鐵' in content and '待 Johnny' in content:
        alerts.append("⏸️ 等待 Johnny 回饋")
    
    return alerts


def main():
    """主流程"""
    print(f"🫀 Heartbeat - {datetime.now().isoformat()}")
    
    # 1. 解析指標
    metrics = parse_heartbeat()
    print(f"📊 指標: {metrics}")
    
    # 2. 計算每週進度
    weekly = calculate_weekly_progress()
    done = sum(1 for _, s in weekly if s == 'done')
    total = len(weekly)
    print(f"📈 每週進度: {done}/{total}")
    
    # 3. 檢查警報
    alerts = check_alerts()
    if alerts:
        print("⚠️ 警報:")
        for a in alerts:
            print(f"  - {a}")
    
    # 4. 生成報告
    report = generate_report()
    print(f"✅ 報告已生成")
    
    return {
        "metrics": metrics,
        "weekly_progress": f"{done}/{total}",
        "alerts": alerts
    }


if __name__ == "__main__":
    main()
