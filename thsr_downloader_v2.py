#!/usr/bin/env python3
"""
高鐵時刻表優化版
1. 票價雙向
2. 分離早晚班
3. API 服務
"""

import requests
import json
import os
import re
from datetime import datetime
from flask import Flask, jsonify, request

# 設定
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "data")
TIMETABLE_URL = "https://www.thsrc.com.tw/Attachment/Download?pageID=a3b630bb-1066-4352-a1ef-58c7b4e8ef7c&id=b5e78f70-fa6d-4f75-8f31-a13387d7ea88"
PDF_FILENAME = "thsr_timetable.pdf"
JSON_FILENAME = "thsr_timetable.json"

# 站點順序（完整）
STATIONS = ["南港", "台北", "板橋", "桃園", "新竹", "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "左營"]

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_timetable():
    """下載高鐵時刻表 PDF"""
    headers = {"User-Agent": "Mozilla/5.0"}
    print("📥 下載時刻表...")
    response = requests.get(TIMETABLE_URL, headers=headers, timeout=30, verify=False)
    
    if response.status_code == 200:
        pdf_path = os.path.join(DOWNLOAD_DIR, PDF_FILENAME)
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"✅ 已下載: {pdf_path}")
        return pdf_path
    return None


def parse_fare_table(text):
    """解析完整票價表（雙向）"""
    fares = {station: {} for station in STATIONS}
    
    lines = text.split('\n')
    current_station = None
    
    for line in lines:
        # 找站名
        for station in STATIONS:
            if station in line and '南港' not in line:  # 避免標題干擾
                current_station = station
                break
        
        if current_station:
            # 找價格數字
            prices = re.findall(r'(\d{1,3}(?:,\d{3})*)', line)
            if prices:
                # 對應站名
                target_idx = 0
                for station in STATIONS:
                    if station != current_station and target_idx < len(prices):
                        price = prices[target_idx].replace(',', '')
                        if price.isdigit():
                            fares[current_station][station] = int(price)
                            fares[station][current_station] = int(price)  # 雙向
                        target_idx += 1
    
    return fares


def parse_northbound(text):
    """解析北上時刻表 - 分離早/晚班"""
    morning = []  # 06:00-12:00
    afternoon = [] # 12:00-18:00
    evening = []  # 18:00-24:00
    
    lines = text.split('\n')
    in_table = False
    
    for line in lines:
        if '時刻表 / 北上' in line:
            in_table = True
            continue
        if '時刻表 / 南下' in line or '一般票價表' in line:
            break
        if not in_table:
            continue
            
        parts = line.split()
        if len(parts) >= 2:
            try:
                train_no = parts[0]
                if train_no.isdigit() or (train_no.startswith("0") and len(train_no) <= 4):
                    times = []
                    for p in parts[1:]:
                        if re.match(r'\d{2}:\d{2}', p):
                            times.append(p)
                        elif p == '─':
                            times.append(None)
                    
                    if times and times[0]:
                        hour = int(times[0].split(':')[0])
                        
                        train_data = {
                            "train_no": train_no,
                            "times": times,
                            "direction": "northbound"
                        }
                        
                        if hour < 12:
                            morning.append(train_data)
                        elif hour < 18:
                            afternoon.append(train_data)
                        else:
                            evening.append(train_data)
            except:
                continue
    
    return {"morning": morning, "afternoon": afternoon, "evening": evening}


def parse_southbound(text):
    """解析南下時刻表 - 分離早/晚班"""
    morning = []
    afternoon = []
    evening = []
    
    lines = text.split('\n')
    in_table = False
    
    for line in lines:
        if '時刻表 / 南下' in line:
            in_table = True
            continue
        if '一般票價表' in line:
            break
        if not in_table:
            continue
            
        parts = line.split()
        if len(parts) >= 2:
            try:
                train_no = parts[0]
                if train_no.isdigit() or (train_no.startswith("0") and len(train_no) <= 4):
                    times = []
                    for p in parts[1:]:
                        if re.match(r'\d{2}:\d{2}', p):
                            times.append(p)
                        elif p == '─':
                            times.append(None)
                    
                    if times and times[0]:
                        hour = int(times[0].split(':')[0])
                        
                        train_data = {
                            "train_no": train_no,
                            "times": times,
                            "direction": "southbound"
                        }
                        
                        if hour < 12:
                            morning.append(train_data)
                        elif hour < 18:
                            afternoon.append(train_data)
                        else:
                            evening.append(train_data)
            except:
                continue
    
    return {"morning": morning, "afternoon": afternoon, "evening": evening}


def parse_timetable(pdf_path):
    """解析 PDF 時刻表"""
    import pdfplumber
    
    print("📄 解析 PDF...")
    
    northbound = {"morning": [], "afternoon": [], "evening": []}
    southbound = {"morning": [], "afternoon": [], "evening": []}
    fares = {station: {} for station in STATIONS}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            
            if page_num == 1:
                northbound = parse_northbound(text)
                print(f"  北上: 早={len(northbound['morning'])} 午={len(northbound['afternoon'])} 晚={len(northbound['evening'])}")
            elif page_num == 2:
                southbound = parse_southbound(text)
                fares = parse_fare_table(text)
                print(f"  南下: 早={len(southbound['morning'])} 午={len(southbound['afternoon'])} 晚={len(southbound['evening'])}")
    
    # 整理輸出
    data = {
        "update_time": datetime.now().isoformat(),
        "source": TIMETABLE_URL,
        "stations": STATIONS,
        "northbound": northbound,
        "southbound": southbound,
        "fares": fares
    }
    
    # 儲存 JSON
    json_path = os.path.join(DOWNLOAD_DIR, JSON_FILENAME)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已儲存: {json_path}")
    return data


# ============ API 服務 ============

app = Flask(__name__)
DATA = None


def load_data():
    """載入數據"""
    global DATA
    json_path = os.path.join(DOWNLOAD_DIR, JSON_FILENAME)
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            DATA = json.load(f)
    return DATA


@app.route('/api/fare', methods=['GET'])
def get_fare():
    """票價查詢"""
    load_data()
    origin = request.args.get('from')
    destination = request.args.get('to')
    
    if not origin or not destination:
        return jsonify({"error": "請提供 from 和 to 參數"}), 400
    
    if DATA and 'fares' in DATA:
        fares = DATA['fares']
        if origin in fares and destination in fares[origin]:
            return jsonify({
                "from": origin,
                "to": destination,
                "price": fares[origin][destination]
            })
    
    return jsonify({"error": "查無資料"}), 404


@app.route('/api/timetable', methods=['GET'])
def get_timetable():
    """時刻表查詢"""
    load_data()
    direction = request.args.get('direction', 'southbound')  # northbound/southbound
    time_period = request.args.get('period', 'all')  # morning/afternoon/evening/all
    
    if not DATA:
        return jsonify({"error": "無資料"}), 404
    
    key = direction if direction in ['northbound', 'southbound'] else 'southbound'
    timetable = DATA.get(key, {})
    
    if time_period == 'all':
        return jsonify(timetable)
    elif time_period in timetable:
        return jsonify({time_period: timetable[time_period]})
    
    return jsonify({"error": "參數錯誤"}), 404


@app.route('/api/stations', methods=['GET'])
def get_stations():
    """站點列表"""
    load_data()
    return jsonify({"stations": DATA.get('stations', STATIONS) if DATA else STATIONS})


@app.route('/api/status', methods=['GET'])
def get_status():
    """服務狀態"""
    return jsonify({
        "status": "ok",
        "update_time": DATA.get('update_time') if DATA else None,
        "northbound_count": sum(len(v) for v in DATA.get('northbound', {}).values()) if DATA else 0,
        "southbound_count": sum(len(v) for v in DATA.get('southbound', {}).values()) if DATA else 0
    })


def main():
    """主流程"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 1. 下載
    pdf_path = download_timetable()
    if not pdf_path:
        return
    
    # 2. 解析
    data = parse_timetable(pdf_path)
    
    # 3. 顯示摘要
    print(f"\n=== V1 優化完成 ===")
    print(f"北上: {sum(len(v) for v in data['northbound'].values())} 班")
    print(f"南下: {sum(len(v) for v in data['southbound'].values())} 班")
    print(f"票價: {len(data['fares'])} 站雙向")
    
    # 4. 測試 API
    print(f"\n=== API 測試 ===")
    print("票價查詢: /api/fare?from=台北&to=左營")
    print("時刻表: /api/timetable?direction=southbound&period=morning")
    print("站點: /api/stations")
    print("狀態: /api/status")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'api':
        print("🚀 啟動 API 伺服器...")
        load_data()
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        main()
