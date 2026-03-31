#!/usr/bin/env python3
"""
高鐵時刻表 API - 生產部署版本
"""

import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 生產環境配置
DATA_FILE = os.environ.get('DATA_FILE', os.path.join(os.path.dirname(__file__), "data", "thsr_timetable_v2.json"))
DATA = None


def load_data():
    global DATA
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            DATA = json.load(f)
    return DATA


@app.route('/api/status', methods=['GET'])
def status():
    load_data()
    if not DATA:
        return jsonify({"error": "No data", "code": 404}), 404
    
    north = DATA.get('northbound', {})
    south = DATA.get('southbound', {})
    
    return jsonify({
        "status": "ok",
        "update_time": DATA.get("update_time"),
        "northbound_count": sum(len(north.get(p, [])) for p in ['morning', 'afternoon', 'evening']),
        "southbound_count": sum(len(south.get(p, [])) for p in ['morning', 'afternoon', 'evening']),
        "stations_count": len(DATA.get("fares", {}))
    })


@app.route('/api/stations', methods=['GET'])
def stations():
    load_data()
    if not DATA:
        return jsonify({"error": "No data"}), 404
    return jsonify({"stations": DATA.get("stations", [])})


@app.route('/api/fare', methods=['GET'])
def fare():
    load_data()
    if not DATA:
        return jsonify({"error": "No data"}), 404
    
    origin = request.args.get('from', '').strip()
    destination = request.args.get('to', '').strip()
    
    if not origin or not destination:
        return jsonify({"error": "Missing parameters", "usage": "/api/fare?from=台北&to=左營"}), 400
    
    fares = DATA.get('fares', {})
    
    # 精確匹配
    if origin in fares and destination in fares[origin]:
        return jsonify({
            "from": origin,
            "to": destination,
            "price": fares[origin][destination],
            "currency": "TWD"
        })
    
    # 模糊匹配
    for station in fares:
        if station == origin or origin in station:
            if destination in fares[station]:
                return jsonify({"from": station, "to": destination, "price": fares[station][destination], "currency": "TWD"})
        if station == destination or destination in station:
            if origin in fares[station]:
                return jsonify({"from": origin, "to": station, "price": fares[station][origin], "currency": "TWD"})
    
    return jsonify({"error": f"Route {origin} → {destination} not found"}), 404


@app.route('/api/timetable', methods=['GET'])
def timetable():
    load_data()
    if not DATA:
        return jsonify({"error": "No data"}), 404
    
    direction = request.args.get('direction', 'southbound')
    period = request.args.get('period', 'all')
    
    if direction not in ['northbound', 'southbound']:
        return jsonify({"error": "Invalid direction"}), 400
    
    timetable = DATA.get(direction, {})
    
    if period == 'all':
        # 返回所有時段的摘要
        return jsonify({
            "direction": direction,
            "morning_count": len(timetable.get('morning', [])),
            "afternoon_count": len(timetable.get('afternoon', [])),
            "evening_count": len(timetable.get('evening', []))
        })
    elif period in timetable:
        return jsonify({period: timetable[period]})
    else:
        return jsonify({"error": "Invalid period"}), 400


@app.route('/api/search', methods=['GET'])
def search():
    load_data()
    if not DATA:
        return jsonify({"error": "No data"}), 404
    
    origin = request.args.get('from', '').strip()
    destination = request.args.get('to', '').strip()
    
    if not origin or not destination:
        return jsonify({"error": "Missing parameters"}), 400
    
    fares = DATA.get('fares', {})
    price = None
    
    for station in fares:
        if station == origin or origin in station:
            if destination in fares[station]:
                price = fares[station][destination]
                break
        if station == destination or destination in station:
            if origin in fares[station]:
                price = fares[station][origin]
                break
    
    return jsonify({
        "from": origin,
        "to": destination,
        "price": price,
        "currency": "TWD" if price else None
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "name": "THSR Timetable API",
        "version": "1.0.0",
        "endpoints": [
            "GET / - This info",
            "GET /health - Health check",
            "GET /api/status - Service status",
            "GET /api/stations - Station list",
            "GET /api/fare?from=台北&to=左營 - Fare lookup",
            "GET /api/timetable?direction=southbound&period=morning - Timetable",
            "GET /api/search?from=台北&to=左營 - Quick search"
        ]
    })


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting THSR API on port {port}...")
    load_data()
    if DATA:
        print(f"✅ Data loaded: {DATA.get('update_time')}")
    app.run(host='0.0.0.0', port=port)
