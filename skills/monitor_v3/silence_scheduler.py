#!/usr/bin/env python3
"""
靜音時段管理 - Agent Monitor v3

功能：
- 設定靜音時段
- 週期性靜音
- 自動到期
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

import storage


class SilenceLevel(Enum):
    """靜音級別"""
    ALL = "all"
    ALERTS = "alerts"
    NOTIFICATIONS = "notifications"


@dataclass
class SilenceWindow:
    """靜音時段"""
    id: Optional[int] = None
    start_time: str = None
    end_time: str = None
    level: str = "all"
    reason: str = None
    created_by: str = None
    created_at: str = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now().isoformat()
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def is_active(self) -> bool:
        """是否在靜音時段內"""
        now = datetime.now()
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time) if self.end_time else None
        
        if end is None:
            return now >= start
        
        return start <= now <= end
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "level": self.level,
            "reason": self.reason,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "is_active": self.is_active()
        }


class SilenceScheduler:
    """靜音時段管理器"""
    
    def __init__(self):
        self.storage = storage
        self._windows: List[SilenceWindow] = []
        self._load()
    
    def _load(self):
        """從文件加載"""
        try:
            with open("./data/silence.json", "r") as f:
                data = json.load(f)
                for item in data:
                    self._windows.append(SilenceWindow(**item))
        except FileNotFoundError:
            pass
    
    def _save(self):
        """保存到文件"""
        import os
        os.makedirs("./data", exist_ok=True)
        
        with open("./data/silence.json", "w") as f:
            data = [w.to_dict() for w in self._windows]
            json.dump(data, f, indent=2)
    
    def add_window(
        self,
        start: datetime,
        end: datetime,
        level: str = "all",
        reason: str = None,
        created_by: str = "system"
    ) -> int:
        """新增靜音時段"""
        window = SilenceWindow(
            start_time=start.isoformat(),
            end_time=end.isoformat(),
            level=level,
            reason=reason,
            created_by=created_by
        )
        self._windows.append(window)
        self._save()
        return len(self._windows) - 1
    
    def add_recurring(
        self,
        day_of_week: int,  # 0=Monday, 6=Sunday
        start_hour: int,
        end_hour: int,
        level: str = "all",
        reason: str = None
    ) -> int:
        """新增週期性靜音（每週）"""
        now = datetime.now()
        
        # 計算下次觸發時間
        days_ahead = day_of_week - now.weekday()
        if days_ahead < 0:
            days_ahead += 7
        
        next_start = now + timedelta(days=days_ahead)
        next_start = next_start.replace(
            hour=start_hour, 
            minute=0, 
            second=0, 
            microsecond=0
        )
        
        next_end = next_start.replace(hour=end_hour)
        
        return self.add_window(
            next_start, 
            next_end, 
            level, 
            f"{reason} (每週)"
        )
    
    def remove_window(self, window_id: int) -> bool:
        """移除靜音時段"""
        if 0 <= window_id < len(self._windows):
            self._windows.pop(window_id)
            self._save()
            return True
        return False
    
    def get_windows(
        self,
        active_only: bool = False,
        future_only: bool = False
    ) -> List[Dict]:
        """獲取靜音時段"""
        now = datetime.now()
        results = []
        
        for i, window in enumerate(self._windows):
            if future_only and window.is_active():
                continue
            
            if active_only and not window.is_active():
                continue
            
            result = window.to_dict()
            result["id"] = i
            results.append(result)
        
        return results
    
    def is_silenced(self, level: str = "all") -> bool:
        """檢查是否在靜音時段"""
        for window in self._windows:
            if window.is_active():
                if window.level == "all" or window.level == level:
                    return True
        return False
    
    def get_next_silence(self, level: str = "all") -> Optional[Dict]:
        """獲取下次靜音時間"""
        now = datetime.now()
        upcoming = []
        
        for window in self._windows:
            start = datetime.fromisoformat(window.start_time)
            if start > now:
                if window.level == "all" or window.level == level:
                    upcoming.append({
                        "start": window.start_time,
                        "end": window.end_time,
                        "reason": window.reason
                    })
        
        return upcoming[0] if upcoming else None
    
    def clear_expired(self):
        """清除已過期的靜音時段"""
        now = datetime.now()
        original_count = len(self._windows)
        
        self._windows = [
            w for w in self._windows 
            if w.end_time is None or datetime.fromisoformat(w.end_time) > now
        ]
        
        if len(self._windows) != original_count:
            self._save()


# ============== 快捷函數 ==============

scheduler = SilenceScheduler()


def is_silenced(level: str = "all") -> bool:
    """快捷檢查"""
    return scheduler.is_silenced(level)


def add_silence(
    start_hour: int,
    end_hour: int,
    reason: str = None
):
    """快捷新增靜音（今天）"""
    now = datetime.now()
    start = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)
    
    return scheduler.add_window(start, end, reason=reason)


# ============== 主程式 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("🔇 Silence Scheduler Test")
    print("=" * 50)
    
    # 新增靜音時段
    now = datetime.now()
    end = now + timedelta(hours=2)
    
    scheduler.add_window(now, end, reason="系統維護")
    
    print("\n📥 All windows:")
    for w in scheduler.get_windows():
        print(f"  {w}")
    
    print(f"\n🔇 Is silenced: {scheduler.is_silenced()}")
    
    print("\n⏰ Next silence:")
    print(f"  {scheduler.get_next_silence()}")
    
    print("\n✅ Silence test complete!")
