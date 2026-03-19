#!/usr/bin/env python3
"""
Resource Monitor - 資源監控

監控系統資源使用情況：CPU、記憶體、磁盤、網絡
"""

import psutil
import time
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResourceSnapshot:
    """資源快照"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_percent: float
    network_sent_mb: float
    network_recv_mb: float


class ResourceMonitor:
    """資源監控器"""
    
    def __init__(self):
        """初始化監控器"""
        self.snapshots: List[ResourceSnapshot] = []
        self._last_net_io = psutil.net_io_counters()
    
    def capture(self) -> ResourceSnapshot:
        """
        捕獲當前資源使用情況
        
        Returns:
            資源快照
        """
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Memory
        memory = psutil.virtual_memory()
        
        # Disk
        disk = psutil.disk_usage('/')
        
        # Network
        net_io = psutil.net_io_counters()
        sent_mb = (net_io.bytes_sent - self._last_net_io.bytes_sent) / 1024 / 1024
        recv_mb = (net_io.bytes_recv - self._last_net_io.bytes_recv) / 1024 / 1024
        self._last_net_io = net_io
        
        snapshot = ResourceSnapshot(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / 1024 / 1024,
            disk_percent=disk.percent,
            network_sent_mb=sent_mb,
            network_recv_mb=recv_mb
        )
        
        self.snapshots.append(snapshot)
        
        # 只保留最近 1000 個快照
        if len(self.snapshots) > 1000:
            self.snapshots = self.snapshots[-1000:]
        
        return snapshot
    
    def get_current(self) -> Dict:
        """
        獲取當前資源狀態
        
        Returns:
            資源狀態字典
        """
        snapshot = self.capture()
        
        return {
            "timestamp": snapshot.timestamp.isoformat(),
            "cpu": {
                "percent": snapshot.cpu_percent,
                "status": self._get_status(snapshot.cpu_percent, 80, 90)
            },
            "memory": {
                "percent": snapshot.memory_percent,
                "used_mb": snapshot.memory_used_mb,
                "status": self._get_status(snapshot.memory_percent, 80, 90)
            },
            "disk": {
                "percent": snapshot.disk_percent,
                "status": self._get_status(snapshot.disk_percent, 85, 95)
            },
            "network": {
                "sent_mb": snapshot.network_sent_mb,
                "recv_mb": snapshot.network_recv_mb
            }
        }
    
    def _get_status(self, value: float, warning: float, critical: float) -> str:
        """獲取狀態"""
        if value >= critical:
            return "critical"
        elif value >= warning:
            return "warning"
        return "healthy"
    
    def get_summary(self, minutes: int = 5) -> Dict:
        """
        獲取資源使用摘要
        
        Args:
            minutes: 最近幾分鐘
            
        Returns:
            摘要數據
        """
        cutoff = datetime.now().timestamp() - (minutes * 60)
        recent = [s for s in self.snapshots if s.timestamp.timestamp() > cutoff]
        
        if not recent:
            return {"message": "No data"}
        
        return {
            "period_minutes": minutes,
            "cpu": {
                "avg": sum(s.cpu_percent for s in recent) / len(recent),
                "max": max(s.cpu_percent for s in recent),
                "min": min(s.cpu_percent for s in recent)
            },
            "memory": {
                "avg": sum(s.memory_percent for s in recent) / len(recent),
                "max": max(s.memory_percent for s in recent),
                "min": min(s.memory_percent for s in recent)
            }
        }
    
    def check_thresholds(self, cpu_warning: float = 80, cpu_critical: float = 90,
                       memory_warning: float = 80, memory_critical: float = 90) -> List[Dict]:
        """
        檢查資源閾值
        
        Args:
            cpu_warning: CPU 警告閾值
            cpu_critical: CPU 嚴重閾值
            memory_warning: 記憶體警告閾值
            memory_critical: 記憶體嚴重閾值
            
        Returns:
            警報列表
        """
        current = self.capture()
        alerts = []
        
        # CPU
        if current.cpu_percent >= cpu_critical:
            alerts.append({
                "type": "cpu",
                "level": "critical",
                "message": f"CPU 使用率 {current.cpu_percent:.1f}% 超過臨界值 {cpu_critical}%"
            })
        elif current.cpu_percent >= cpu_warning:
            alerts.append({
                "type": "cpu",
                "level": "warning",
                "message": f"CPU 使用率 {current.cpu_percent:.1f}% 超過警告值 {cpu_warning}%"
            })
        
        # Memory
        if current.memory_percent >= memory_critical:
            alerts.append({
                "type": "memory",
                "level": "critical",
                "message": f"記憶體使用率 {current.memory_percent:.1f}% 超過臨界值 {memory_critical}%"
            })
        elif current.memory_percent >= memory_warning:
            alerts.append({
                "type": "memory",
                "level": "warning",
                "message": f"記憶體使用率 {current.memory_percent:.1f}% 超過警告值 {memory_warning}%"
            })
        
        return alerts


# 使用範例
if __name__ == "__main__":
    monitor = ResourceMonitor()
    
    print("=== Current Resources ===")
    current = monitor.get_current()
    print(f"CPU: {current['cpu']['percent']:.1f}% ({current['cpu']['status']})")
    print(f"Memory: {current['memory']['percent']:.1f}% ({current['memory']['status']})")
    print(f"Disk: {current['disk']['percent']:.1f}%")
    
    print("\n=== Summary (Last 5 min) ===")
    summary = monitor.get_summary(5)
    print(f"CPU Avg: {summary['cpu']['avg']:.1f}%")
    print(f"Memory Avg: {summary['memory']['avg']:.1f}%")
    
    print("\n=== Threshold Check ===")
    alerts = monitor.check_thresholds()
    for alert in alerts:
        print(f"[{alert['level'].upper()}] {alert['message']}")
