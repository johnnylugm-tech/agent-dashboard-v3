---
name: jarvis-ui
description: "Jarvis風格的儀表板 (OpenClaw Studio)，即時監控 OpenClaw agents，包含Agent管理、對話記錄、系統監控"
---

# Jarvis UI / OpenClaw Studio

已安裝 OpenClaw Studio - Jarvis 風格的 Web 儀表板。

## ✅ 安裝狀態

| 項目 | 狀態 |
|------|------|
| **位置** | ~/jarvis-ui |
| **執行中** | ✅ http://localhost:3000 |
| **依賴** | 已完成 npm install |
| **設定** | 已配置 .env.local |

## 功能

- **Three.js 互動球體** - 可視化 Agent 狀態
- **即時聊天** - 透過 Gateway WebSocket 傳遞訊息
- **音訊視覺化** - 光譜、環形、波形顯示
- **系統監控** - 模型使用量、Token 統計
- **文字轉語音 (TTS)** - Edge TTS 或 macOS say

## 安裝需求

1. **Node.js 20+**
2. **Python edge-tts** (可選，跨平台 TTS)
3. **ffmpeg** (可選，特定音訊工作流程)
4. **pm2** (推薦，生產環境部署)

## 安裝步驟

```bash
# 1. 建立目錄
mkdir -p ~/jarvis-ui && cd ~/jarvis-ui

# 2. 安裝
npm install openclaw/jarvis-ui

# 或從源碼安裝
git clone https://github.com/openclaw/jarvis-ui.git
cd jarvis-ui
npm install

# 3. 設定
cp config.json config.local.json
# 編輯 config.local.json 自訂設定

# 4. 啟動
npm start

# 或使用 pm2
pm2 start ecosystem.config.js
```

## 設定檔 (config.local.json)

```json
{
  "gateway": {
    "url": "http://localhost:18789",
    "token": "YOUR_GATEWAY_TOKEN"
  },
  "server": {
    "port": 3456,
    "host": "0.0.0.0"
  },
  "tts": {
    "provider": "say",  // 或 "edge-tts"
    "voice": "Samantha"
  },
  "ui": {
    "theme": "dark",
    "orbColor": "#00ffff"
  }
}
```

## 獲取 Gateway Token

```bash
cat ~/.openclaw/openclaw.json | grep token
```

## 訪問 HUD

- 本地：http://localhost:3456
- 、行動版支援 (PWA)

## 功能說明

### Agent 狀態球
- 顏色變化反映 Agent 狀態
- 大小/脈動表示負載

### 即時聊天
- 訊息即時傳遞
- 支援語音回覆

### 系統監控
- Token 使用量
- 回應時間
- 模型資訊

## 安全考量

- **不要**將 UI 暴露到公開網際網路
- 若需遠端訪問，在 openclaw.json 中謹慎設定
- 定期檢查存取日誌

## 常見問題

**Q: 如何讓其他裝置訪問？**
A: 更新 ~/.openclaw/openclaw.json 的 controlUi 設定，重啟 Gateway

**Q: TTS 選項？**
A: Edge TTS (跨平台，需 Python + edge-tts) 或 macOS say (離線)

**Q: 支援行動版？**
A: 是 PWA，可新增到主畫面

## 啟動後檢查

```bash
# 查看 logs
pm2 logs jarvis-ui

# 查看狀態
pm2 status

# 重啟
pm2 restart jarvis-ui
```
