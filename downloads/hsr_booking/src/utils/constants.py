"""
常數定義
"""

# HTTP Headers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]

# 請求延遲（秒）
REQUEST_DELAY_MIN = 0.5
REQUEST_DELAY_MAX = 2.0

# 重試次數
MAX_RETRIES = 3

# 逾時（秒）
REQUEST_TIMEOUT = 30
