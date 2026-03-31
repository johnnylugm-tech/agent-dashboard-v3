"""
錯誤分類器 - 使用 methodology-v2 ErrorClassifier
"""
from enum import Enum
from typing import Optional
import sys
sys.path.insert(0, '/workspace/methodology-v2')

try:
    from error_classifier import ErrorClassifier, ErrorLevel
    USE_FRAMEWORK = True
except ImportError:
    USE_FRAMEWORK = False
    ErrorLevel = None


class HSRErrorLevel(Enum):
    """高鐵訂票系統錯誤等級"""
    L1_RECOVERABLE = "L1"  # 可自動修復
    L2_USER_ACTION = "L2"  # 需用戶操作
    L3ManualIntervention = "L3"  # 需手動介入
    L4_CRITICAL = "L4"  # 嚴重錯誤


class HSRError(Exception):
    """高鐵訂票系統錯誤基類"""
    
    def __init__(self, message: str, level: HSRErrorLevel, code: str):
        self.message = message
        self.level = level
        self.code = code
        super().__init__(message)
    
    def to_dict(self) -> dict:
        return {
            "error": self.message,
            "level": self.level.value if self.level else "UNKNOWN",
            "code": self.code,
        }


# 錯誤碼定義
class ErrorCode:
    # 網路錯誤 (L1)
    NETWORK_TIMEOUT = "E1001"
    NETWORK_CONNECTION = "E1002"
    
    # 認證錯誤 (L2)
    SESSION_EXPIRED = "E2001"
    CAPTCHA_FAILED = "E2002"
    CAPTCHA_EMPTY = "E2003"
    
    # 訂票錯誤 (L3)
    SEAT_FULL = "E3001"
    TICKET_LIMIT = "E3002"
    INVALID_ID = "E3003"
    PAYMENT_FAILED = "E3004"
    
    # 系統錯誤 (L4)
    API_CHANGED = "E4001"
    MAINTENANCE = "E4002"


def classify_error(error: Exception) -> dict:
    """錯誤分類 - 整合 methodology-v2"""
    
    error_mapping = {
        ErrorCode.NETWORK_TIMEOUT: (HSRErrorLevel.L1_RECOVERABLE, "網路超時，可重試"),
        ErrorCode.NETWORK_CONNECTION: (HSRErrorLevel.L1_RECOVERABLE, "連線錯誤，可重試"),
        ErrorCode.SESSION_EXPIRED: (HSRErrorLevel.L2_USER_ACTION, "Session 過期，需重新登入"),
        ErrorCode.CAPTCHA_FAILED: (HSRErrorLevel.L2_USER_ACTION, "驗證碼錯誤，需人工識別"),
        ErrorCode.CAPTCHA_EMPTY: (HSRErrorLevel.L2_USER_ACTION, "驗證碼為空"),
        ErrorCode.SEAT_FULL: (HSRErrorLevel.L2_USER_ACTION, "座位已滿"),
        ErrorCode.TICKET_LIMIT: (HSRErrorLevel.L3ManualIntervention, "超出票數限制"),
        ErrorCode.INVALID_ID: (HSRErrorLevel.L3ManualIntervention, "身份證號格式錯誤"),
        ErrorCode.PAYMENT_FAILED: (HSRErrorLevel.L3ManualIntervention, "付款失敗"),
        ErrorCode.API_CHANGED: (HSRErrorLevel.L4_CRITICAL, "API 已變更，需更新程式"),
        ErrorCode.MAINTENANCE: (HSRErrorLevel.L4_CRITICAL, "系統維護中"),
    }
    
    # 如果有 methodology-v2 框架，使用其分類
    if USE_FRAMEWORK and ErrorLevel:
        framework_result = ErrorClassifier.classify(str(error))
        return {
            "original": error,
            "framework_level": framework_result.level.value if hasattr(framework_result, 'level') else None,
            **error_mapping.get(error.__class__.__name__, (HSRErrorLevel.L1_RECOVERABLE, "未知錯誤"))
        }
    
    return error_mapping.get(
        error.__class__.__name__, 
        (HSRErrorLevel.L1_RECOVERABLE, "未知錯誤")
    )
