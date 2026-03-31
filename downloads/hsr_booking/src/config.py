# 高鐵站代碼配置
# Taiwan HSR Station Codes

HSR_STATIONS = {
    "Nangang": {"code": "1000", "name": "南港"},
    "Taipei": {"code": "1001", "name": "台北"},
    "Banqiao": {"code": "1002", "name": "板橋"},
    "Taoyuan": {"code": "1003", "name": "桃園"},
    "Hsinchu": {"code": "1005", "name": "新竹"},
    "Taichung": {"code": "1006", "name": "台中"},
    "Changhua": {"code": "1007", "name": "彰化"},
    "Yunlin": {"code": "1008", "name": "雲林"},
    "Chiayi": {"code": "1009", "name": "嘉義"},
    "Tainan": {"code": "1010", "name": "台南"},
    "Zuoying": {"code": "1070", "name": "左營"},
}

# Reverse lookup
STATION_BY_CODE = {v["code"]: k for k, v in HSR_STATIONS.items()}

# Ticket types
TICKET_TYPES = {
    "adult": {"code": "1", "name": "全票"},
    "child": {"code": "2", "name": "孩童票"},
    "senior": {"code": "3", "name": "敬老票"},
    "disabled": {"code": "4", "name": "愛心票"},
    "student": {"code": "5", "name": "大學生"},
}

# Early bird discount types
EARLY_BIRD_DISCOUNT = {
    35: {"code": "35", "name": "早鳥 35%"},
    20: {"code": "20", "name": "早鳥 20%"},
    10: {"code": "10", "name": "早鳥 10%"},
}
