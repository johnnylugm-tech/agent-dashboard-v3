# CLI Reference

> **版本**：v6.09.0  
> **基於**：methodology-v2 cli.py  
> **目的**：提供所有 CLI 指令速查和範例

---

## 📋 概述

所有 CLI 指令位於 `skills/methodology-v2/cli.py`，可通过以下方式调用：

```bash
# 完整路徑
python skills/methodology-v2/cli.py <command>

# 或設定 alias
alias methodology="python /Users/johnny/.openclaw/workspace-musk/skills/methodology-v2/cli.py"
```

---

## 🔧 Phase 管理指令

### phase-verify — Phase 真相驗證

驗證指定 Phase 的產出是否滿足要求。

```bash
python cli.py phase-verify --phase N --project /path
```

| 參數 | 必填 | 說明 |
|------|------|------|
| `--phase N` | ✅ | Phase 號碼 (1-8) |
| `--project` | ❌ | 專案根目錄 (預設: `.`) |

**範例**：

```bash
# 驗證 Phase 1
python cli.py phase-verify --phase 1

# 驗證 Phase 4，指定專案
python cli.py phase-verify --phase 4 --project /path/to/project
```

---

### stage-pass — STAGE_PASS 生成器

生成指定 Phase 的 STAGE_PASS.md，確認該 Phase 品質通過。

```bash
python cli.py stage-pass --phase N --project /path
```

| 參數 | 必填 | 說明 |
|------|------|------|
| `--phase N` | ✅ | Phase 號碼 (1-8) |
| `--project` | ❌ | 專案根目錄 (預設: `.`) |

**範例**：

```bash
# 生成 Phase 1 STAGE_PASS
python cli.py stage-pass --phase 1

# 生成 Phase 5 STAGE_PASS
python cli.py stage-pass --phase 5 --project /path/to/project
```

---

## 🔒 Framework Enforcement 指令

### enforce — Framework 執行檢查

執行 FrameworkEnforcer 檢查，驗證所有 BLOCK/WARN 等級規則。

```bash
python cli.py enforce --level BLOCK --project /path
```

| 參數 | 必填 | 說明 |
|------|------|------|
| `--level` | ✅ | 檢查等級：`BLOCK` 或 `WARN` |
| `--project` | ❌ | 專案根目錄 (預設: `.`) |

**BLOCK 等級檢查**：

| 檢查項 | 門檻 |
|--------|------|
| SPEC_TRACKING | 完整性 ≥ 90% |
| CONSTITUTION_SCORE | 分數 ≥ 60 |

**WARN 等級檢查**：

| 檢查項 | 說明 |
|--------|------|
| DECISION_FRAMEWORK | Decision Framework 已建立 |
| ENHANCED_CHECKLIST | 增強檢查清單已建立 |

**範例**：

```bash
# BLOCK 等級檢查
python cli.py enforce --level BLOCK

# WARN 等級檢查
python cli.py enforce --level WARN

# 指定專案執行 BLOCK 檢查
python cli.py enforce --level BLOCK --project /path/to/project
```

---

### enforcement — 互動式 Enforcement 管理

```bash
python cli.py enforcement <action>
```

| Action | 說明 |
|--------|------|
| `run` | 執行所有 enforcement 檢查 |
| `check` | 檢查 enforcement 狀態 |
| `config` | 顯示/設定 enforcement 設定 |

**範例**：

```bash
# 執行所有檢查
python cli.py enforcement run

# 檢查狀態
python cli.py enforcement check

# 顯示設定
python cli.py enforcement config
```

---

## ✅ Constitution 檢查指令

### 執行 Constitution Runner

```bash
python quality_gate/constitution/runner.py --type <type>
```

| 參數 | 說明 |
|------|------|
| `--type srs` | SRS (需求規格) Constitution |
| `--type sad` | SAD (架構設計) Constitution |
| `--type test_plan` | Test Plan Constitution |
| `--type test_results` | Test Results Constitution |
| `--type code` | 代碼 Constitution |

**範例**：

```bash
# SRS Constitution
python quality_gate/constitution/runner.py --type srs

# SAD Constitution
python quality_gate/constitution/runner.py --type sad

# Test Plan Constitution
python quality_gate/constitution/runner.py --type test_plan
```

---

## 🔍 Claims 驗證指令

### Claims Verifier

驗證系統 Claims 的真實性。

```bash
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_all())"
```

| 方法 | 說明 |
|------|------|
| `verify_all()` | 驗證所有 Claims |
| `verify_phase(N)` | 驗證指定 Phase Claims |
| `verify_artifact(path)` | 驗證指定產出 Claims |

**範例**：

```bash
# 驗證所有 Claims
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_all())"

# 驗證 Phase 3 Claims
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_phase(3))"

# 驗證特定產出
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_artifact('04-testing/TEST_RESULTS.md'))"
```

---

## 📊 品質檢查指令

### doc-checker — 文檔檢查

```bash
python quality_gate/doc_checker.py
```

檢查 ASPICE 文檔合規性。

---

### spec-track — 規格追蹤檢查

```bash
python cli.py spec-track check
```

檢查 SPEC_TRACKING.md 完整性。

---

## 🚀 Ralph Mode 指令

### Ralph Mode — 任務長時監控

```bash
# 初始化任務
python cli.py ralph init <task_id>

# 啟動監控
python cli.py ralph start <task_id> --interval 300

# 查看狀態
python cli.py ralph status <task_id>

# 列出所有任務
python cli.py ralph list --status running

# 停止監控
python cli.py ralph stop <task_id>

# 推進階段
python cli.py ralph advance <task_id> --to eval
```

**範例**：

```bash
# 初始化任務
python cli.py ralph init my-project

# 啟動監控（5 分鐘間隔）
python cli.py ralph start my-project --interval 300 --background

# 查看狀態
python cli.py ralph status my-project

# 推進到 eval 階段
python cli.py ralph advance my-project --to eval
```

---

## 🛠️ 其他有用指令

### wizard — 專案初始化精靈

```bash
python cli.py wizard
```

互動式建立新專案。

---

### term — PM 術語查詢

```bash
python cli.py term <query>
```

查詢 PM 術語定義。

---

### resources — 資源列表

```bash
python cli.py resources list
```

列出可用資源。

---

### eval — Agent 評估

```bash
# 建立評估
python cli.py eval create --name <name>

# 執行評估
python cli.py eval run <eval_id>

# 查看報告
python cli.py eval report <eval_id>
```

---

### quality — 資料品質

```bash
# 執行品質檢查
python cli.py quality check --path /path

# 生成品質報告
python cli.py quality report
```

---

### enterprise — 企業整合

```bash
# 查看狀態
python cli.py enterprise status

# 執行審計
python cli.py enterprise audit
```

---

## 📋 常用組合指令

### Phase 1 完成後標準流程

```bash
# 1. 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK --project /path

# 2. 執行 Constitution SRS 檢查
python quality_gate/constitution/runner.py --type srs

# 3. 生成 STAGE_PASS
python cli.py stage-pass --phase 1 --project /path

# 4. Johnny 驗證
python cli.py phase-verify --phase 1 --project /path
```

### Phase 4 完成後標準流程

```bash
# 1. 執行測試
pytest -v --tb=short

# 2. 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK --project /path

# 3. 執行 Constitution Test Plan 檢查
python quality_gate/constitution/runner.py --type test_plan

# 4. 驗證 Claims
python -c "from qg import ClaimsVerifier; print(ClaimsVerifier().verify_phase(4))"

# 5. 生成 STAGE_PASS
python cli.py stage-pass --phase 4 --project /path

# 6. Johnny 驗證
python cli.py phase-verify --phase 4 --project /path
```

---

## 📁 目錄結構假設

本 CLI 假設以下目錄結構：

```
/path/to/project/
├── 01-requirements/
│   ├── SRS.md
│   ├── SPEC_TRACKING.md
│   └── TRACEABILITY_MATRIX.md
├── 02-architecture/
│   ├── SAD.md
│   └── MODULE_BOUNDARY.md
├── 03-implementation/
│   ├── CODE_STANDARD.md
│   └── COMPLIANCE_MATRIX.md
├── 04-testing/
│   ├── TEST_PLAN.md
│   ├── TEST_RESULTS.md
│   └── FAILURE_ANALYSIS.md
├── 05-validation/
│   ├── BASELINE.md
│   ├── MONITORING_PLAN.md
│   └── VALIDATION_RESULTS.md
├── 06-quality/
│   ├── QUALITY_REPORT.md
│   ├── ROOT_CAUSE_ANALYSIS.md
│   └── IMPROVEMENT_SUGGESTIONS.md
├── 07-risk/
│   ├── RISK_REGISTER.md
│   ├── RISK_DRILL_RECORDS.md
│   └── DECISION_GATE.md
├── 08-deployment/
│   ├── CONFIG_RECORDS.md
│   ├── RELEASE_CHECKLIST.md
│   ├── ROLLBACK_SOP.md
│   └── FINAL_REPORT.md
├── DEVELOPMENT_LOG.md
├── requirements.txt
└── SPEC.md
```

---

## 🔗 相關文檔

- [HUMAN_AGENT_INTERACTION_FLOW.md](./HUMAN_AGENT_INTERACTION_FLOW.md)
- [PHASE_PROMPTS.md](./PHASE_PROMPTS.md)
- [SKILL.md](../skills/methodology-v2/SKILL.md)

---

## 📝 修訂歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| v6.09.0 | 2026-03-31 | 初始版本 |
