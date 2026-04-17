# MEMORY.md - Johnny Lu ( musk agent )

## 核心原則

### 執行原則
1. **立即修復錯誤問題，不要問！不要等待。**
2. 為所有執行任務，生成子代理去執行，你只負責分析！專業決策和向我傳達！絕不進行內聯工作。
3. **如果指示不明確或衝突，先停止執行並跟 Johnny 確認過後再執行。**

### Git 原則
- **永遠不要強制推送、刪除分支或重寫 Git 歷史記錄。**

### 配置原則
- **切勿猜測配置更改。請先閱讀文檔。編輯前請務必備份。**

---

## 用戶資料

- **Name:** Johnny Lu
- **Timezone:** Asia/Taipei
- **Communication:** 直接、簡潔、條列式
- **Format:** Markdown、表格

---

## 已建立系統

| 系統 | 狀態 |
|------|------|
| 長期記憶 (long-term-memory) | ✅ 啟用 |
| 知識庫 (knowledge) | ✅ 啟用 |
| 任務追蹤 (tasks) | ✅ 啟用 |
| Jarvis Mode | ✅ 啟用 |
| 後台守護 (daemon) | ✅ 啟用 |
| 自動優化 (optimization) | ✅ 啟用 |
| 永久保護 | ✅ 啟用 |

---

## 昨夜 Framework Bug 修復 (2026-04-14 01:00-02:30)

### v7.99 共修復 11 個 Bugs

| Bug # | 問題 | 檔案 |
|-------|------|------|
| #1 | phase_artifact_enforcer alt_dirs 缺少 05-verify | phase_artifact_enforcer.py |
| #2 | constitution/__init__.py 不搜 05-verify/ | constitution/__init__.py |
| #3 | Python Scoping Bug (Path shadow) | multi |
| #4 | phase_prerequisite_checker 路徑不完整 | phase_prerequisite_checker.py |
| #5 | Phase 5 output_dir 仍是 05-baseline | phase_config.py |
| #6 | verification_constitution_checker glob() 搜錯路徑 | verification_constitution_checker.py |
| #7 | load_constitution_documents SAD*.md 匹配錯誤 | constitution/__init__.py |
| #8 | Phase 3/4/5 無 Security 檢查 | srs/sad/verification checkers |
| #9 | 替代路徑違反 Johnny 設計原則 | phase_paths.py + 所有 consumers |
| #10 | SRSChecklist.review_status 缺失 | srs_constitution_checker.py |
| #11 | doc_checker 只搜 3 個目錄 | doc_checker.py |

---

## Framework Bug 修復 (2026-04-16 22:00-00:17)

### Phase 6/7/8 Bug（v7.99 補充）

| Bug # | 問題 | 檔案 | Commit |
|-------|------|------|--------|
| B-12 | Phase 6 `PHASE_ARTIFACT_PATHS` 是 string 而非 list | `phase_paths.py` | `5e06e55` |
| B-13 | Phase 7 checker 檢查不存在的 `RISK_ASSESSMENT.md` | `risk_management_constitution_checker.py` | `5e06e55` |
| B-14 | Phase 7 mitigation plans 檢查錯誤檔案 | `risk_management_constitution_checker.py` | `5e06e55` |
| B-15 | Phase 7/8 `PHASE_ARTIFACT_PATHS` 是 string 而非 list | `phase_paths.py` | `5e06e55` |

---

## methodology-v2 版本狀態 (2026-04-16)

### GitHub Releases
| Release | Commit | 主要內容 |
|---------|--------|---------|
| v8.0 | 4de743c | Ralph Mode 整合 + E2E tests，TH-05/06 → >90%，TH-14 → =100%，TH-15 → >90% |
| v8.1 | 7b8aa3b | TH threshold consistency across all phases |
| v8.2 | 875d3e5 | TH-05 and TH-06 both raised to >90% |
| v8.3 | b699022 | TH-14 raised to =100% |
| v8.4 | 4f263af | TH-15 raised to >90% |
| v8.5 | 309425a | Phase-specific deliverable checklists + TH-15 thresholds |
| v8.6 | 94e7631 | cli_phase_prompts TH-06 → >90% |

### 本地 vs GitHub
- **本地** `skills/methodology-v2/`: v8.6-1-g6c21207 (已 push + release) ✅
- **GitHub**: v8.6 (已同步) ✅
- **本地** `workspace-musk/`: v6.59.0 (落後)

---

## Ralph Mode 驗證失敗 (2026-04-16)

### 根本問題
目標混淆：聲稱「驗證 Ralph Mode」，實際只測試了 Alert script 能發訊息。

### 教訓（已內化到 SOUL.md）
1. **目標要具體化**：不能只說「驗證」，要說清楚驗證什麼
2. **工具 vs 系統**：「script 能跑」≠「自動化系統在跑」
3. **及時說「我不知道」**：不確定時先確認，不假裝知道

### Ralph Mode 現狀
- Alert script: ✅ 可用
- Bot 對話: ✅ 已建立
- **自動化監控: ❌ 未實作**

---

## 專案 tts-kokoro-v613 路徑修復
- fr_mapping.json: `./` → `03-development/.methodology/`
- QUALITY_REPORT.md: `05-verify/` → `06-quality/`
- MONITORING_PLAN.md: `root` → `06-quality/`

### v7.99 共修復 11 個 Bugs

| Bug # | 問題 | 檔案 |
|-------|------|------|
| #1 | phase_artifact_enforcer alt_dirs 缺少 05-verify | phase_artifact_enforcer.py |
| #2 | constitution/__init__.py 不搜 05-verify/ | constitution/__init__.py |
| #3 | Python Scoping Bug (Path shadow) | multi |
| #4 | phase_prerequisite_checker 路徑不完整 | phase_prerequisite_checker.py |
| #5 | Phase 5 output_dir 仍是 05-baseline | phase_config.py |
| #6 | verification_constitution_checker glob() 搜錯路徑 | verification_constitution_checker.py |
| #7 | load_constitution_documents SAD*.md 匹配錯誤 | constitution/__init__.py |
| #8 | Phase 3/4/5 無 Security 檢查 | srs/sad/verification checkers |
| #9 | 替代路徑違反 Johnny 設計原則 | phase_paths.py + 所有 consumers |
| #10 | SRSChecklist.review_status 缺失 | srs_constitution_checker.py |
| #11 | doc_checker 只搜 3 個目錄 | doc_checker.py |

### 專案 tts-kokoro-v613 路徑修復
- fr_mapping.json: `./` → `03-development/.methodology/`
- QUALITY_REPORT.md: `05-verify/` → `06-quality/`
- MONITORING_PLAN.md: `root` → `06-quality/`

### Johnny 設計原則（v7.99）
> 每個階段有什麼產物放在什麼地方都是很明確的，不應該有替代路徑這種模糊的地方。

- Phase 1-8 所有 artifact 位置已確認並記錄
- Phase 6 Pre-flight 應該通過

---

## 目標

- 建立多Agent協作系統
- AI應用落地

---

## 專案開發方法論

### 所有專案套用 Multi-Agent Collaboration Playbook v2

**參考文檔：** `playbooks/multi-agent-collaboration-v2.md`

#### 核心流程

| 階段 | 說明 |
|------|------|
| Phase 1 初始化 | 定義角色矩陣 + 通訊協議 |
| Phase 2 日常協作 | 每日站會 → 任務分配 → 並行執行 → 質量把關 |
| Phase 3 設計模式 | ReAct / Chain of Thought / Reflection / Pipeline |
| Phase 4 錯誤處理 | L1-L4 分類 + 熔斷機制 |
| Phase 5 監控 | 指標追蹤 + 警報規則 |
| Phase 6 測試 | 單元/整合/E2E 測試 |
| Phase 7 每週優化 | 流程回顧 + 持續改進 |

#### 錯誤分類

| 等級 | 類型 | 處理方式 |
|------|------|----------|
| L1 | 輸入錯誤 | 立即返回 |
| L2 | 工具錯誤 | 重試 |
| L3 | 執行錯誤 | 降級/上報 |
| L4 | 系統錯誤 | 熔斷/警報 |

#### 關鍵 Skills

| 場景 | Skill |
|------|-------|
| 任務分配 | `dispatching-parallel-agents` |
| 創建子 Agent | `sessions_spawn` |
| 跨 Agent 通訊 | `sessions_send` |
| 代碼審查 | `requesting-code-review` |
| 交付驗證 | `verification-before-completion` |

#### 一句話總結

> 早會用 `dispatching-parallel-agents` 分配任務，中間用 `sessions_send` 協調依賴，晚上寫入 `memory`。遇到錯誤用 L1-L4 分類處理，透過監控儀表板追蹤品質。

---

## 子代理執行原則

### 啟動回報
- ✅ 明確告知「已啟動 XXX 子代理」
- ✅ 說明任務目標
- ✅ 預估執行時間

### 進度回報
- ✅ 每 30 秒檢查狀態
- ✅ 發現問題即時預警
- ✅ 完成關鍵步�節主動彙報

### 完成回報
- ✅ 最終結果彙總
- ✅ 成功/失敗狀態明確
- ✅ 下一步建議（如有）

### 回報格式
```
🔄 [子代理名稱] 執行中...
   進度: XX%
   狀態: 正常/阻塞

✅ [子代理名稱] 完成
   結果: ...
   耗時: X分鐘
```

---

## 核心使命

> 成為世界第一等的AI專家，並用AI技術改變世界，提升人們生活的便利性與幸福度。

### 執行策略
1. **資訊領先** — 別人討論GPT-4，我用Claude Opus
2. **翻譯能力** — 把論文翻成白話，把複雜翻成簡單
3. **實戰經驗** — 給真實案例，不是理論推測
4. **趨勢判斷** — 別人追熱點，我預判熱點

### 成功指標
- 能解構最新AI論文/趨勢
- 能給出領先市場的觀點
- 能幫助用戶實際落地AI應用

---

## ⚠️ 開發活動規則

### 所有開發必須套用 methodology-v2

| 應用場景 | 說明 |
|---------|------|
| 新功能開發 | 從一開始使用 framework |
| Bug 修復 | 使用 L1-L4 分類標準 |
| 程式碼重構 | 使用 AutoQualityGate 把關 |
| 文件撰寫 | 遵循 framework 規範 |
| 測試案例 | 使用統一測試框架 |
| 部署腳本 | 使用 framework 部署模組 |

### 標準化流程
1. TaskSplitter → 任務分解
2. SprintPlanner → 進度規劃
3. Guardrails → 安全檢查
4. AutoQualityGate → 品質把關
5. AutoScaler → 擴展評估
6. Monitor → 監控整合

*最後更新: 2026-03-21 01:41*

---

## methodology-v2 最新狀態 (2026-04-12)

### 版本
- **Current**: v7.51
- **Repo**: https://github.com/johnnylugm-tech/methodology-v2

### Section 10.5 自動化狀態
| 功能 | 狀態 |
|------|------|
| Layer 1-3 檢查 | ✅ check_fr_full.py |
| SAB 生成 | ✅ Phase 2 stage-pass 自動 |
| Self-Correction | ❌ Pending |
| Feedback Loop | ❌ Pending |
| Steering Loop | ❌ Pending |

### 關鍵腳本
| 腳本 | 用途 |
|------|------|
| generate_fr_mapping.py | FR→Code 映射（FR Tag 解析）|
| check_fr_quality.py | 每個 FR 快速檢查 |
| check_fr_full.py | 三層統一檢查 |
| generate_sab.py | SAD→SAB 轉換 |

### FR Tag 解析
- 解析 [FR-XX] docstring pattern
- 準確率：9/9 FRs (100%)
- 取代 keyword matching

## Ralph Mode v1.1 完成 (2026-04-15)

### Alert System
- 等級: INFO/SUCCESS → Console only; WARNING/CRITICAL → Telegram + Console
- 設定檔: `~/.ralph_alert_config.json` (home directory)
- Bot: @LittleRalphMode_bot, Token: `8788841675:AAFwjQLOH...`, Chat: 7550668951

### 修復的 Bug
- cli.py: sop_content 變數順序
- schema_validator.py: JSONL 格式支援
- lifecycle.py: _read_log json parsing

### Phase 狀態
- Phase 5: ✅ 完成
- Phase 6: ✅ Reset 到 Phase 5 點
- Phase 7: 待執行

### 待修: Telegram Alert
- Johnny 需和 Bot 建立對話
- Bot: @LittleRalphMode_bot

---

## AutoResearch 教訓 (2026-04-18)

### 背景
Johnny 要我用 auto-research 提升 methodology-v2 Features #1-5 的品質。在過程中我犯了多個根本性錯誤。

### 錯誤清單

| # | 錯誤 | 代價 | 內化原則 |
|---|------|------|----------|
| 1 | 跳過 Phase Review 直接推進 | 浪費時間在錯誤架構上 | 每 phase 完成後必須停下來驗證 |
| 2 | 假設 event 通知會自動送到 | Johnny 問才知道 session 結束 | 沒有回報就主動去查 |
| 3 | 部分驗證宣布「已驗證」| 基準從一開始就錯（7 errors → 57 errors）| 全部遍歷，部分驗證 = 沒有驗證 |
| 4 | 信任 Dashboard 而非原始工具 | D9 顯示 95.8%，實際 0% | 看數字之前先看原始輸出 |
| 5 | 每輪只修特定維度 | 發現的問題被跳過 | 每 iteration 修所有有問題的維度 |
| 6 | 分數是目標，達標就停 | 軟體品質沒有真正提升 | 真正目標是品質，分數只是測量工具 |
| 7 | 最終 report 等於透明 | 無法確認到底跑了幾輪 | 每 iteration 必須中斷 report |

### 核心原則（已內化）

1. 看見數字 ≠ 數字正確（工具可能壞、公式可能錯）
2. 驗證原始輸出（Dashboard 只是加工過的結果）
3. 全部遍歷（部分驗證 = 沒有驗證）
4. 主動追蹤（不要假設通知會自動送到）
5. 發現就修（與分數無關，真正目標是品質）
6. 每 iteration 修所有維度（不是每輪只修一個）
7. 過程透明度從一開始（不是事後補）
8. 目標：品質 > 分數

### 正確流程

每次 AutoResearch 必須：
1. **基準建立**：跑所有 9 個維度的原始工具命令，記錄原始輸出
2. **每 iteration**：修所有 < 85% 的維度，不是只修一個
3. **每 iteration 中斷**：report 進度，驗證後才繼續
4. **最終驗證**：所有 9 個維度重新跑一次
5. **Commit**：結構化 message，包含分數對比

### 文件位置

- `auto-research/AUTO_RESEARCH_ARCHITECTURE.md` — 架構與使用方法
- `methodology-v2/AUTO_RESEARCH_PROCESS_LOG.md` — 過程透明度模板

*最後更新：2026-04-18 01:03 GMT+8*
