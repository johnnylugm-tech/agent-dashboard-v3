#!/usr/bin/env python3
"""
高鐵時刻表 API 服務
"""

import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "thsr_timetable_v2.json")
DATA = None


def load_data():
    global DATA
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            DATA = json.load(f)
    return DATA


@app.route('/api/status', methods=['GET'])
def status():
    """服務狀態"""
    load_data()
    if not DATA:
        return jsonify({"error": "無資料，請先執行下載"}), 404
    
    north = DATA.get('northbound', {})
    south = DATA.get('southbound', {})
    
    return jsonify({
        "status": "ok",
        "update_time": DATA.get("update_time"),
        "northbound": {
            "morning": len(north.get("morning", [])),
            "afternoon": len(north.get("afternoon", [])),
            "evening": len(north.get("evening", []))
        },
        "southbound": {
            "morning": len(south.get("morning", [])),
            "afternoon": len(south.get("afternoon", [])),
            "evening": len(south.get("evening", []))
        },
        "stations": len(DATA.get("fares", {}))
    })


@app.route('/api/stations', methods=['GET'])
def stations():
    """站點列表"""
    load_data()
    if not DATA:
        return jsonify({"error": "無資料"}), 404
    
    return jsonify({
        "stations": DATA.get("stations", [])
    })


@app.route('/api/fare', methods=['GET'])
def fare():
    """票價查詢"""
    load_data()
    if not DATA:
        return jsonify({"error": "無資料"}), 404
    
    origin = request.args.get('from', '')
    destination = request.args.get('to', '')
    
    if not origin or not destination:
        return jsonify({"error": "請提供 from 和 to 參數"}), 400
    
    fares = DATA.get('fares', {})
    
    # 精確匹配
    if origin in fares and destination in fares[origin]:
        return jsonify({
            "from": origin,
            "to": destination,
            "price": fares[origin][destination]
        })
    
    # 模糊匹配
    for station in fares:
        if station in origin or origin in station:
            if destination in fares[station]:
                return jsonify({
                    "from": station,
                    "to": destination,
                    "price": fares[station][destination]
                })
        if station in destination or destination in station:
            if origin in fares[station]:
                return jsonify({
                    "from": origin,
                    "to": station,
                    "price": fares[station][origin]
                })
    
    return jsonify({"error": f"查無 {origin} → {destination} 票價"}), 404


@app.route('/api/timetable', methods=['GET'])
def timetable():
    """時刻表查詢"""
    load_data()
    if not DATA:
        return jsonify({"error": "無資料"}), 404
    
    direction = request.args.get('direction', 'southbound')
    period = request.args.get('period', 'all')  # morning/afternoon/evening/all
    
    if direction not in ['northbound', 'southbound']:
        return jsonify({"error": "direction 必須是 northbound 或 southbound"}), 400
    
    timetable = DATA.get(direction, {})
    
    if period == 'all':
        return jsonify(timetable)
    elif period in timetable:
        return jsonify({period: timetable[period]})
    else:
        return jsonify({"error": "period 必須是 morning/afternoon/evening"}), 400


@app.route('/api/search', methods=['GET'])
def search():
    """綜合搜尋（票價 + 時刻）"""
    load_data()
    if not DATA:
        return jsonify({"error": "無資料"}), 404
    
    origin = request.args.get('from', '')
    destination = request.args.get('to', '')
    
    if not origin or not destination:
        return jsonify({"error": "請提供 from 和 to 參數"}), 400
    
    # 票價
    fares = DATA.get('fares', {})
    price = None
    for station in fares:
        if station in origin or origin in station:
            if destination in fares[station]:
                price = fares[station][destination]
                break
    
    # 建議時段（找直達車）
    direction = 'southbound'  # 預設南下
    timetable = DATA.get(direction, {})
    
    return jsonify({
        "from": origin,
        "to": destination,
        "price": price,
        "available_periods": list(timetable.keys()) if timetable else []
    })


@app.route('/', methods=['GET'])
def index():
    """首頁"""
    return jsonify({
        "name": "高鐵時刻表 API",
        "version": "1.0",
        "endpoints": [
            "/api/status - 服務狀態",
            "/api/stations - 站點列表",
            "/api/fare?from=台北&to=左營 - 票價查詢",
            "/api/timetable?direction=southbound&period=morning - 時刻表",
            "/api/search?from=台北&to=左營 - 綜合搜尋"
        ]
    })


if __name__ == "__main__":
    print("🚀 高鐵時刻表 API 啟動中...")
    print("📍 http://localhost:5000")
    load_data()
    if DATA:
        print(f"✅ 資料已載入: {DATA.get('update_time')}")
    else:
        print("⚠️ 無資料，請先執行 python3 thsr_downloader_v2.py")
    app.run(host='0.0.0.0', port=5000, debug=True)
