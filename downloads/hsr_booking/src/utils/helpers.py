"""
輔助工具函數
"""
import json
from pathlib import Path
from typing import Dict, Any


def validate_config(config: Dict[str, Any]) -> bool:
    """驗證配置檔"""
    required = ["user", "route", "ticket"]
    for key in required:
        if key not in config:
            return False
    return True


def load_config(config_path: str) -> Dict[str, Any]:
    """載入配置檔"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        if path.suffix == '.json':
            return json.load(f)
        elif path.suffix == '.toml':
            import toml
            return toml.load(f)
    raise ValueError(f"Unsupported config format: {path.suffix}")
