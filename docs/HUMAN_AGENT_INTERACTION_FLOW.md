# Human-Agent Interaction Flow

> **版本**：v6.09.0  
> **基於**：methodology-v2 v6.03-v6.08 強化功能  
> **目的**：建立標準的人類與 Agent 互動流程，確保 100% 落實 SKILL.md 規範

---

## 📋 概述

本文件定義了 **Johnny（人類）** 與 **Agent（AI）** 在 8 階段開發流程中的標準互動模式。

### 核心原則

1. **HITL（Human-in-the-Loop）**：每個 Phase 結束必須由 Johnny 確認才能進入下一 Phase
2. **A/B 協作**：Agent A 執行 × Agent B 審查，角色分離
3. **Framework Enforcement**：所有產出必須通過 FrameworkEnforcer BLOCK 檢查
4. **可追溯性**：每個 FR 必須追蹤到邏輯驗證方法

---

## 🔄 整體流程圖

```
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 1: 需求規格                          │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 2: 架構設計                          │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 3: 代碼實現                          │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 4: 測試                              │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
┌─────────────────────────────────────────────────────────────────┐
│                      Phase 5: 系統驗證                            │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 6: 品質確認                          │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 7: 風險管理                          │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
┌─────────────────────────────────────────────────────────────────┐
│                        Phase 8: 配置發布                          │
│                    Agent A → Agent B → Johnny HITL               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HITL CONFIRM
                                   ↓
                         ✅ 專案完成
```

---

## 🔀 每 Phase 標準流程

```
Phase N 開始
    ↓
Agent A: 執行 Phase N 工作
    ↓
Agent A: 呼叫 FrameworkEnforcer BLOCK
    ↓
[如果是 BLOCK 失敗]
    → Agent A: 修復問題
    → 回到 BLOCK 檢查
    ↓
[如果是 BLOCK 通過]
    ↓
Agent A: 生成 STAGE_PASS.md
    ↓
【HITL 介入點 - Johnny 審核】
    ↓
Johnny: 手動執行 phase-verify --phase N
    ↓
Johnny: 根據清單確認內容
    ↓
[如果通過]
    → Johnny: CONFIRM
    → 進入下一 Phase
[如果不通過]
    → Johnny: REJECT
    → Agent A: 回到 Phase N 重新執行
```

---

## 👤 Johnny 的介入點 (HITL)

### Johnny 職責

| 職責 | 說明 |
|------|------|
| **審核產出** | 檢查每 Phase 產出是否滿足需求 |
| **確認質量** | 驗證 FrameworkEnforcer 報告 |
| **最終決策** | CONFIRM 或 REJECT |
| **手動驗證** | 執行 CLI 指令確認系統狀態 |

### Johnny 審核清單

| Phase | 必檢內容 | 驗證方法 |
|-------|----------|----------|
| **1** | SRS.md 隨機抽 3 條 FR，追蹤到邏輯驗證方法 | 閱讀 SRS.md + TRACEABILITY |
| **2** | SAD.md 模組邊界圖是否合理 | 視覺化檢查架構圖 |
| **3** | 隨機抽 1 個測試，確認邊界條件 | 閱讀測試檔案 |
| **4** | TEST_RESULTS.md pytest 輸出真實性 | 比對實際 pytest 輸出 |
| **5** | BASELINE.md 功能對照表 | 逐一對照 FR 狀態 |
| **6** | QUALITY_REPORT.md 問題根源分析 | 檢查 Layer 1-3 分析深度 |
| **7** | RISK_REGISTER.md 演練記錄 | 確認模擬演練證據 |
| **8** | CONFIG_RECORDS.md pip freeze 輸出 | 比對 requirements.txt |

### Johnny 確認指令

```bash
# Phase 驗證
python cli.py phase-verify --phase N

# Framework BLOCK 檢查
python cli.py enforce --level BLOCK

# STAGE_PASS 生成
python cli.py stage-pass --phase N --project /path

# Claims 驗證
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_all())"
```

### Johnny 回應格式

```
【HITL 審核 Phase N】

✅ CONFIRM
- [x] 產出完整
- [x] FrameworkEnforcer BLOCK 通過
- [x] A/B 審查完成

或

❌ REJECT
原因：
1. [具體問題]
2. [具體問題]

請 Agent 修復後重新提交。
```

---

## 📦 Phase 1: 需求規格

### 目的
建立完整的需求規格文檔 (SRS.md)，作為整個專案的需求基線。

### 產出物
- `01-requirements/SRS.md`
- `01-requirements/SPEC_TRACKING.md`
- `01-requirements/TRACEABILITY_MATRIX.md`
- `DEVELOPMENT_LOG.md` (Phase 1 段落)

### 驗證 Checkpoint
- [ ] SRS.md 包含所有 FR (功能需求)
- [ ] 每個 FR 有邏輯驗證方法
- [ ] SPEC_TRACKING.md 完整性 ≥ 90%
- [ ] Constitution Score ≥ 60
- [ ] FrameworkEnforcer BLOCK 通過

### Johnny 審核重點
- 隨機抽 3 條 FR，追蹤到邏輯驗證方法

---

## 📦 Phase 2: 架構設計

### 目的
建立系統架構文檔 (SAD.md)，定義模組邊界和介面。

### 產出物
- `02-architecture/SAD.md`
- `02-architecture/MODULE_BOUNDARY.md`
- `TRACEABILITY_MATRIX.md` (更新)
- `DEVELOPMENT_LOG.md` (Phase 2 段落)

### 驗證 Checkpoint
- [ ] SAD.md 包含模組邊界圖
- [ ] 每個 FR 映射到對應模組
- [ ] Constitution Score ≥ 60
- [ ] FrameworkEnforcer BLOCK 通過

### Johnny 審核重點
- SAD.md 模組邊界圖是否合理

---

## 📦 Phase 3: 代碼實現

### 目的
根據 SAD.md 實作代碼，並撰寫單元測試。

### 產出物
- `src/` (代碼檔案)
- `tests/` (單元測試)
- `03-implementation/CODE_STANDARD.md`
- `03-implementation/COMPLIANCE_MATRIX.md`
- `DEVELOPMENT_LOG.md` (Phase 3 段落)

### 驗證 Checkpoint
- [ ] 代碼覆蓋率 ≥ 70%
- [ ] 單元測試包含邊界條件和負面測試
- [ ] 同行邏輯審查完成
- [ ] FrameworkEnforcer BLOCK 通過

### Johnny 審核重點
- 隨機抽 1 個測試，確認邊界條件

---

## 📦 Phase 4: 測試

### 目的
建立完整的測試計劃和結果記錄。

### 產出物
- `04-testing/TEST_PLAN.md`
- `04-testing/TEST_RESULTS.md`
- `04-testing/FAILURE_ANALYSIS.md`
- `DEVELOPMENT_LOG.md` (Phase 4 段落)

### 驗證 Checkpoint
- [ ] TEST_PLAN.md 完整規格
- [ ] TEST_RESULTS.md pytest 輸出真實
- [ ] 失敗案例有根本原因分析
- [ ] FrameworkEnforcer BLOCK 通過

### Johnny 審核重點
- TEST_RESULTS.md pytest 輸出真實性

---

## 📦 Phase 5: 系統驗證

### 目的
驗證系統是否滿足 BASELINE 功能對照表。

### 產出物
- `05-validation/BASELINE.md`
- `05-validation/MONITORING_PLAN.md`
- `05-validation/VALIDATION_RESULTS.md`
- `DEVELOPMENT_LOG.md` (Phase 5 段落)

### 驗證 Checkpoint
- [ ] BASELINE.md 功能對照表完整
- [ ] MONITORING_PLAN.md 四個閾值定義
- [ ] 測試通過率 = 100%
- [ ] FrameworkEnforcer BLOCK 通過

### Johnny 審核重點
- BASELINE.md 功能對照表

---

## 📦 Phase 6: 品質確認

### 目的
進行 Constitution ≥ 80% 全面檢查，生成品質報告。

### 產出物
- `06-quality/QUALITY_REPORT.md`
- `06-quality/ROOT_CAUSE_ANALYSIS.md`
- `06-quality/IMPROVEMENT_SUGGESTIONS.md`
- `DEVELOPMENT_LOG.md` (Phase 6 段落)

### 驗證 Checkpoint
- [ ] Constitution Score ≥ 80
- [ ] 問題根源分析 (Layer 1-3)
- [ ] 改進建議有 P0/P1/P2 分級
- [ ] FrameworkEnforcer BLOCK 通過

### Johnny 審核重點
- QUALITY_REPORT.md 問題根源分析

---

## 📦 Phase 7: 風險管理

### 目的
識別和管理專案風險，進行風險演練。

### 產出物
- `07-risk/RISK_REGISTER.md`
- `07-risk/RISK_DRILL_RECORDS.md`
- `07-risk/DECISION_GATE.md`
- `DEVELOPMENT_LOG.md` (Phase 7 段落)

### 驗證 Checkpoint
- [ ] 五維度風險識別完整
- [ ] 四層緩解措施定義
- [ ] Decision Gate 確認通過
- [ ] 風險演練記錄完整

### Johnny 審核重點
- RISK_REGISTER.md 演練記錄

---

## 📦 Phase 8: 配置發布

### 目的
完成配置管理，生成發布清單。

### 產出物
- `08-deployment/CONFIG_RECORDS.md`
- `08-deployment/RELEASE_CHECKLIST.md`
- `08-deployment/ROLLBACK_SOP.md`
- `08-deployment/FINAL_REPORT.md`
- `DEVELOPMENT_LOG.md` (Phase 8 段落)

### 驗證 Checkpoint
- [ ] CONFIG_RECORDS.md 八章節完整
- [ ] pip freeze 輸出與 requirements.txt 一致
- [ ] 回滾 SOP 已定義
- [ ] 方法論閉環確認

### Johnny 審核重點
- CONFIG_RECORDS.md pip freeze 輸出

---

## 🔧 CLI 指令速查

### Phase 管理

```bash
# Phase 驗證
python cli.py phase-verify --phase N

# STAGE_PASS 生成
python cli.py stage-pass --phase N --project /path

# 強制進入下一 Phase
python cli.py phase-advance --phase N --project /path
```

### Framework Enforcement

```bash
# BLOCK 等級檢查
python cli.py enforce --level BLOCK

# WARN 等級檢查
python cli.py enforce --level WARN

# 完整報告
python cli.py enforce --level BLOCK --project /path
```

### Claims 驗證

```bash
# 驗證所有 Claims
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_all())"

# 驗證特定 Phase
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_phase(N))"
```

### Constitution 檢查

```bash
# SRS Constitution
python quality_gate/constitution/runner.py --type srs

# SAD Constitution
python quality_gate/constitution/runner.py --type sad

# Test Plan Constitution
python quality_gate/constitution/runner.py --type test_plan
```

---

## 📂 檔案結構

```
docs/
├── HUMAN_AGENT_INTERACTION_FLOW.md  # 本文件
├── PHASE_PROMPTS.md                 # Phase Prompt 模板集合
└── CLI_REFERENCE.md                 # CLI 指令參考
```

---

## 🔗 相關文檔

- [SKILL.md](../skills/methodology-v2/SKILL.md) - 方法論完整定義
- [PHASE_PROMPTS.md](./PHASE_PROMPTS.md) - Agent Prompt 模板
- [CLI_REFERENCE.md](./CLI_REFERENCE.md) - CLI 指令完整參考

---

## 📝 修訂歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| v6.09.0 | 2026-03-31 | 初始版本，整合 v6.01-v6.08 強化功能 |
