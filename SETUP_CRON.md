# Heartbeat Cron 設置指南

## 方法 1: macOS Launchd（推薦）

### 1. 複製 plist 到 LaunchAgents 目錄
```bash
mkdir -p ~/Library/LaunchAgents
cp scripts/com.ai.musk.heartbeat.plist ~/Library/LaunchAgents/
```

### 2. 載入服務
```bash
launchctl load ~/Library/LaunchAgents/com.ai.musk.heartbeat.plist
```

### 3. 啟動服務
```bash
launchctl start ai.musk.heartbeat
```

### 4. 檢查狀態
```bash
launchctl list | grep musk
```

### 5. 查看日誌
```bash
tail -f logs/heartbeat.log
```

---

## 方法 2: 手動執行

### 每次 Heartbeat 手動觸發
```bash
# 執行追蹤器
python3 scripts/heartbeat_tracker.py

# 更新儀表板數據
python3 scripts/generate_dashboard_data.py
```

---

## 訪問儀表板

### 本地訪問
```bash
# 用 Python 啟動簡易伺服器
cd /Users/johnny/.openclaw/workspace-musk
python3 -m http.server 8080
```

然後訪問: http://localhost:8080/dashboard.html

### 或者直接打開
```bash
open /Users/johnny/.openclaw/workspace-musk/dashboard.html
```

---

## 自動化流程圖

```
┌─────────────────────────────────────────────┐
│           Launchd (每 60 分鐘)              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│     scripts/heartbeat_tracker.py            │
│     - 解析 HEARTBEAT.md                     │
│     - 計算進度                              │
│     - 檢查警報                              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│     scripts/generate_dashboard_data.py      │
│     - 生成 dashboard_data.json              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│           dashboard.html                    │
│     - 視覺化展示                            │
│     - 自動刷新                             │
└─────────────────────────────────────────────┘
```

---

## 當前狀態

| 項目 | 狀態 |
|------|------|
| Heartbeat 腳本 | ✅ 已創建 |
| Launchd plist | ✅ 已創建 |
| 儀表板 HTML | ✅ 已創建 |
| 數據生成器 | ✅ 已創建 |
| Launchd 載入 | ❌ 待執行 |
