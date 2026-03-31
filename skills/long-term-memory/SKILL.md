---
name: long-term-memory
description: "創建本地持久化資料庫，從對話中完整記錄所有歷史、偏好、習慣、需求、性格、常用指令，永不丟失，自動增量學習"
---

# Long-Term Memory System

建立本地持久化資料庫，完整記錄對話歷史、偏好、習慣、需求、性格、常用指令。

## 存儲結構

```
~/.openclaw/workspace/memory/longterm/
├── database.jsonl    # 完整對話記錄
├── profiles/        # 用戶画像
│   └── boss.json    # 老闆的個人資料
├── preferences/     # 偏好設定
│   └── boss.json
├── habits/          # 習慣
│   └── boss.json
├── personality/     # 性格分析
│   └── boss.json
├── commands/        # 常用指令
│   └── boss.json
└── summaries/       # 摘要
    └── boss.json
```

## 記錄時機

| 觸發條件 | 記錄內容 |
|----------|----------|
| 每次對話結束 | 完整對話歷史 |
| 用戶明確表達偏好 | 偏好設定 |
| 重複行為 >=3 次 | 習慣 |
| 用戶性格表現 | 性格分析 |
| 用戶使用指令 | 常用指令 |
| 每 50 條對話 | 濃縮摘要 |

## 數據格式

### 對話記錄 (database.jsonl)
```json
{"timestamp":"2026-03-02T12:30:00Z","role":"user","content":"今天新聞"}
{"timestamp":"2026-03-02T12:30:05Z","role":"assistant","content":"今日新聞摘要..."}
```

### 用戶画像 (profiles/boss.json)
```json
{
  "name": "老闆",
  "identity": "科技愛好者、工程師",
  "first_seen": "2026-02-24",
  "total_conversations": 150,
  "topics_of_interest": ["科技", "AI", "新聞", "備份"]
}
```

### 偏好 (preferences/boss.json)
```json
{
  "language": "中文",
  "communication_style": "輕鬆幽默",
  "preferred_info_format": "條列式",
  "interests": ["3C", "動畫", "科技新聞"]
}
```

### 習慣 (habits/boss.json)
```json
{
  "daily_news_check": {"time": "09:00-11:00", "frequency": "daily"},
  "backup_routine": {"time": "03:00", "frequency": "daily"},
  "morning_checkin": {"time": "09:00"}
}
```

### 性格 (personality/boss.json)
```json
{
  "tone": "開朗幽默",
  "values": ["效率", "學習", "安全"],
  "communication": "直接明確",
  "preferences": ["條列式", "簡潔"]
}
```

### 常用指令 (commands/boss.json)
```json
{
  "recent_commands": [
    {"cmd": "新聞摘要", "count": 20},
    {"cmd": "備份", "count": 5},
    {"cmd": "安裝skill", "count": 3}
  ]
}
```

## 自動記錄流程

1. **對話結束時** → 寫入 database.jsonl
2. **檢測偏好** → 更新 preferences/boss.json
3. **檢測習慣** → 更新 habits/boss.json（需重複 3 次確認）
4. **分析性格** → 更新 personality/boss.json
5. **濃縮摘要** → 每 50 條對話生成 summary

## 查詢語法

```
!memory search <query>    # 搜尋對話歷史
!memory profile           # 查看用戶画像
!memory preferences       # 查看偏好
!memory habits           # 查看習慣
!memory summary          # 查看摘要
!memory stats            # 統計資訊
```

## 實現命令

### 初始化資料庫
```bash
mkdir -p ~/.openclaw/workspace/memory/longterm/{profiles,preferences,habits,personality,commands,summaries}
touch ~/.openclaw/workspace/memory/longterm/database.jsonl
```

### 記錄對話
```bash
echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","role":"user","content":"'$USER_MSG'"}' >> ~/.openclaw/workspace/memory/longterm/database.jsonl
```

### 搜尋
```bash
grep -i "關鍵詞" ~/.openclaw/workspace/memory/longterm/database.jsonl
```

## 與現有系統整合

- **現有 MEMORY.md** → 保留，作為高層次總結
- **longterm/** → 詳細記錄支撐
- **ontology/** → 結構化知識圖譜

## 安全考量

- 所有數據存於本地 ~/.openclaw/workspace/memory/
- 不上傳雲端
- 可設定敏感詞過濾
- 定期清理可選擇性刪除

## 觸發關鍵字

- "記住"
- "我的偏好"
- "我習慣"
- "我通常"
- "不要忘記"
- "之後查"
- "!memory"
