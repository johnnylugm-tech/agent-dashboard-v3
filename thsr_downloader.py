#!/usr/bin/env python3
"""
高鐵時刻表解析器
從 PDF 解析時刻表數據並輸出為 JSON
"""

import requests
import json
import os
import re
from datetime import datetime

# 設定
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "data")
TIMETABLE_URL = "https://www.thsrc.com.tw/Attachment/Download?pageID=a3b630bb-1066-4352-a1ef-58c7b4e8ef7c&id=b5e78f70-fa6d-4f75-8f31-a13387d7ea88"
PDF_FILENAME = "thsr_timetable.pdf"
JSON_FILENAME = "thsr_timetable.json"

# 站點順序（南下）
STATIONS_SOUTH = ["南港", "台北", "板橋", "桃園", "新竹", "苗栗", "台中", "彰化", "雲林", "嘉義", "台南", "左營"]
# 站點順序（北上）
STATIONS_NORTH = ["左營", "台南", "嘉義", "雲林", "彰化", "台中", "苗栗", "新竹", "桃園", "板橋", "台北", "南港"]

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_timetable():
    """下載高鐵時刻表 PDF"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print("📥 正在下載高鐵時刻表...")
    response = requests.get(TIMETABLE_URL, headers=headers, timeout=30, verify=False)
    
    if response.status_code == 200:
        pdf_path = os.path.join(DOWNLOAD_DIR, PDF_FILENAME)
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"✅ 已下載: {pdf_path}")
        return pdf_path
    else:
        print(f"❌ 下載失敗: {response.status_code}")
        return None


def parse_northbound(text):
    """解析北上時刻表"""
    trains = []
    lines = text.split('\n')
    
    # 找到時刻表開始的位置
    in_table = False
    for line in lines:
        if '時刻表 / 北上' in line:
            in_table = True
            continue
        if '時刻表 / 南下' in line:
            break
        if not in_table:
            continue
            
        # 匹配車次格式: 數字 + 日期標記 + 時間
        # 例如: 502 06:05 06:24 06:37...
        # 或: 1504 ● ● ● ● ● 06:30 06:49...
        
        # 簡單解析：找類似 "502 06:05" 這樣的行
        parts = line.split()
        if len(parts) >= 3:
            try:
                train_no = parts[0]
                # 確認是數字
                if train_no.isdigit() or (train_no.startswith('0') and train_no[1:].isdigit()):
                    # 找時間（格式為 HH:MM）
                    times = []
                    for p in parts[1:]:
                        if re.match(r'\d{2}:\d{2}', p):
                            times.append(p)
                        elif p == '─':
                            times.append(None)  # 不停靠
                    
                    if times:
                        trains.append({
                            "train_no": train_no,
                            "times": times,
                            "direction": "northbound"
                        })
            except:
                continue
    
    return trains


def parse_southbound(text):
    """解析南下時刻表"""
    trains = []
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
        if len(parts) >= 3:
            try:
                train_no = parts[0]
                if train_no.isdigit() or (train_no.startswith('0') and train_no[1:].isdigit()):
                    times = []
                    for p in parts[1:]:
                        if re.match(r'\d{2}:\d{2}', p):
                            times.append(p)
                        elif p == '─':
                            times.append(None)
                    
                    if times:
                        trains.append({
                            "train_no": train_no,
                            "times": times,
                            "direction": "southbound"
                        })
            except:
                continue
    
    return trains


def parse_fare(text):
    """解析票價表"""
    fares = {}
    lines = text.split('\n')
    
    # 找票價數據
    for i, line in enumerate(lines):
        if '標準車廂' in line and '對號座' in line:
            # 接下来几行是票价数据
            for j in range(i+1, min(i+15, len(lines))):
                fare_line = lines[j]
                # 匹配格式: 站名 價格 價格 ...
                parts = fare_line.split()
                if len(parts) >= 3:
                    # 检查是否是站名行
                    for station in STATIONS_SOUTH:
                        if station in fare_line:
                            # 这是一个票价行
                            fares[station] = {}
                            # 解析价格
                            prices = re.findall(r'[\d,]+', fare_line)
                            if prices:
                                idx = 0
                                for s in STATIONS_SOUTH:
                                    if s != station and idx < len(prices):
                                        price = prices[idx].replace(',', '')
                                        if price.isdigit():
                                            fares[station][s] = int(price)
                                        idx += 1
                            break
    
    return fares


def parse_timetable(pdf_path):
    """解析 PDF 時刻表"""
    import pdfplumber
    
    print("📄 正在解析 PDF...")
    
    northbound_trains = []
    southbound_trains = []
    fares = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            
            if page_num == 1:
                # 解析北上
                northbound_trains = parse_northbound(text)
                print(f"  解析北上: {len(northbound_trains)} 班")
            elif page_num == 2:
                # 解析南下
                southbound_trains = parse_southbound(text)
                print(f"  解析南下: {len(southbound_trains)} 班")
                # 解析票價
                fares = parse_fare(text)
                print(f"  解析票價: {len(fares)} 站")
    
    # 整理輸出
    timetable_data = {
        "update_time": datetime.now().isoformat(),
        "source": "https://www.thsrc.com.tw/ArticleContent/a3b630bb-1066-4352-a1ef-58c7b4e8ef7c",
        "northbound": northbound_trains,
        "southbound": southbound_trains,
        "fares": fares,
        "stations": {
            "southbound": STATIONS_SOUTH,
            "northbound": STATIONS_NORTH
        }
    }
    
    # 儲存 JSON
    json_path = os.path.join(DOWNLOAD_DIR, JSON_FILENAME)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(timetable_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已儲存: {json_path}")
    return timetable_data


def main():
    """主流程"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 1. 下載 PDF
    pdf_path = download_timetable()
    if not pdf_path:
        return
    
    # 2. 解析 PDF
    data = parse_timetable(pdf_path)
    if data:
        total = len(data.get('northbound', [])) + len(data.get('southbound', []))
        print(f"📊 共擷取 {total} 班車 + 票價資料")


if __name__ == "__main__":
    main()
