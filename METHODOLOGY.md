# 🎯 AI Agent 開發方法論 v2.1

> 整合 Toolkit v2 最佳實踐 + 現有方法論

---

## 一、錯誤分類 (L1-L4)

### 分類標準

| 等級 | 類型 | 處理方式 | 範例 |
|:----:|------|----------|------|
| **L1** | 輸入錯誤 | 立即返回 | 參數錯誤、格式錯誤 |
| **L2** | 工具錯誤 | 重試 3 次 | API timeout、網路錯誤 |
| **L3** | 執行錯誤 | 降級處理 | 執行失敗、逾時 |
| **L4** | 系統錯誤 | 熔斷/警報 | 記憶體不足、嚴重異常 |

---

## 二、開發流程

### 標準階段

```
需求產生 → 評估優先級 → 開發執行 → 品質檢測 → 文檔更新 → 發布版本
```

### 階段說明

| 階段 | 輸入 | 輸出 | 負責人 |
|------|------|------|--------|
| 需求 | 用戶問題 | PRD | PM |
| 優先級 | PRD | 排序清單 | 開發者 |
| 開發 | 清單 | 程式碼 | 工程師 |
| 品質 | 程式碼 | 報告 | Agent Quality Guard |
| 文檔 | 變更 | 更新的 docs/ | 工程師 |
| 發布 | 通過檢測 | Release | CI/CD |

---

## 三、版本發布檢查清單

### 發布前檢查

```bash
□ 1. 版本號更新 (version 或 __init__.py)
□ 2. CHANGELOG.md 記錄變更
□ 3. README.md 功能說明同步
□ 4. docs/ 相關文檔更新
□ 5. 測試通過 (pytest/單元測試)
□ 6. GitHub Release 建立
□ 7. (可選) ClawHub 發布
```

### 版本號規範

```
v{major}.{minor}.{patch}
- major: 重大架構變更
- minor: 新功能相容
- patch: bug 修復
```

---

## 四、文檔結構標準

### 每個專案需包含

```
專案/
├── README.md          # 快速開始 + 概述
├── CHANGELOG.md      # 版本變更記錄
├── LICENSE           # 許可證
├── docs/
│   ├── architecture.md   # 技術架構
│   ├── integration.md   # 整合教學
│   ├── api.md           # API 文檔
│   └── getting-started.md # 安裝教學
└── src/               # 程式碼
```

### 文檔維護責任

| 文檔 | 更新時機 |
|------|----------|
| README.md | 每版本 |
| CHANGELOG.md | 每版本 |
| architecture.md | 架構變更 |
| integration.md | 新整合方式 |
| api.md | API 變更 |

---

## 五、Multi-Agent 協作模式

### 角色矩陣

| 角色 | 職責 |
|------|------|
| **PM Agent** | 需求分析、任務拆分 |
| **Developer Agent** | 程式碼開發 |
| **Review Agent** | 程式碼審查 |
| **QA Agent** | 測試驗證 |
| **Docs Agent** | 文檔撰寫 |

### 通訊協議

- 每日站會 (dispatching-parallel-agents)
- 依賴協調 (sessions_send)
- 品質把關 (verification-before-completion)

---

## 六、監控與警報

### 監控指標

| 指標 | 說明 |
|------|------|
| 健康評分 | 0-100 |
| 成本 | 每日/每月 |
| 錯誤率 | L1-L4 分類 |
| 趨勢 | 日/週/月 |

### 警報分級

| 等級 | 觸發條件 |
|------|----------|
| Critical | L4 錯誤、健康 < 50 |
| Warning | L3 錯誤、成本超標 |
| Info | L2 錯誤、效能下降 |

---

## 七、持續改進

### 回顧機制

| 頻率 | 內容 |
|------|------|
| 每日 | HEARTBEAT.md 進度檢查 |
| 每週 | 目標達成率回顧 |
| 每月 | 方法論優化 |

### 反饋來源

- 用戶反饋 (GitHub Issues)
- 評測報告
- 實際使用數據

---

## 八、範本

### CHANGELOG.md 範本

```markdown
# Changelog

## [v1.0.0] - 2026-03-20

### Added
- 新功能 A
- 新功能 B

### Fixed
- 修復問題 X
- 修復問題 Y

### Changed
- 優化效能 Z

### Removed
- 移除過時功能
```

---

*版本：v2.1*
*最後更新：2026-03-20*
