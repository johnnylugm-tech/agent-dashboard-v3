# 高鐵時刻表 API 部署指南

## 本地部署

### 方式1: 直接運行
```bash
cd ~/.openclaw/workspace-musk
python3 thsr_api_prod.py
```

### 方式2: Gunicorn (推薦生產環境)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 thsr_api_prod:app
```

---

## 雲端部署

### Render.com (免費)

1. **上傳 GitHub**
```bash
# 初始化 git
git init
git add .
git commit -m "THSR API v1"
```

2. **建立 Repo**
```bash
# 推送到 GitHub
git remote add origin https://github.com/YOUR_USERNAME/thsr-api.git
git push -u origin main
```

3. **Render 部署**
- 登入 render.com
- New → Web Service
- 選擇 GitHub repo
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn thsr_api_prod:app`

### Railway

```bash
# 安裝 railway
npm install -g @railway/cli

# 登入並部署
railway login
railway init
railway deploy
```

### Fly.io

```bash
# 安裝
brew install flyctl

# 登入並部署
flyctl auth login
flyctl launch
flyctl deploy
```

---

## 快速部署（臨時）

### ngrok
```bash
# 安裝
brew install ngrok

# 啟動 API + 隧道
ngrok http 5000
```

---

## 當前狀態

| 項目 | 狀態 |
|------|------|
| API 代碼 | ✅ thsr_api_prod.py |
| 依賴 | ✅ requirements.txt |
| 本地運行 | ✅ port 5001 |
| 雲端部署 | ❌ 待設定 |

---

## 下一步

1. **本地測試**: `python3 thsr_api_prod.py`
2. **選擇部署平台**
3. **設定環境變數**

要選擇哪個部署方式？
