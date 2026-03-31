# Phase Prompt Templates

> **版本**：v6.09.0  
> **用途**：提供每個 Phase 的標準 Agent Prompt 模板，確保 100% 落實 SKILL.md 規範

---

## 📋 概述

每個 Phase Prompt 包含：
- **5W1H 結構**：WHO/WHAT/WHEN/WHERE/WHY/HOW
- **A/B 協作要求**：Agent A 執行 × Agent B 審查
- **產出物清單**：明確的交付文件
- **驗證 Checkpoint**：FrameworkEnforcer 檢查點

---

## Phase 1: 需求規格 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `architect` | 撰寫 SRS.md、SPEC_TRACKING.md、TRACEABILITY_MATRIX.md |
| **Agent B** | `reviewer` | 審查 SRS 完整性、邏輯一致性 |

### WHAT — 做什麼？

為 {專案名稱} 建立需求規格文檔。

### WHEN — 何時執行？

專案啟動後第一個 Phase，所有其他 Phase 的前置條件。

### WHERE — 在哪裡執行？

`01-requirements/` 目錄。

### WHY — 為什麼？

建立需求基線、ASPICE 合規、防止規格漂移。

### HOW — 如何執行？

1. 使用 architect persona 建立 SRS.md
2. 使用 reviewer persona 審查 FR 完整性
3. 執行 Constitution SRS 檢查
4. 建立 SPEC_TRACKING.md
5. 建立 TRACEABILITY_MATRIX.md

### 產出物

```markdown
- 01-requirements/SRS.md
- 01-requirements/SPEC_TRACKING.md
- 01-requirements/TRACEABILITY_MATRIX.md
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# 執行 Constitution SRS 檢查
python quality_gate/constitution/runner.py --type srs

# 執行 Phase 驗證
python cli.py phase-verify --phase 1
```

---

## Phase 2: 架構設計 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `architect` | 設計 SAD.md、MODULE_BOUNDARY.md |
| **Agent B** | `reviewer` | 審查架構合理性、模組邊界 |

### WHAT — 做什麼？

為 {專案名稱} 建立系統架構文檔。

### WHEN — 何時執行？

Phase 1 完成並通過 Johnny HITL CONFIRM 之後。

### WHERE — 在哪裡執行？

`02-architecture/` 目錄。

### WHY — 為什麼？

定義模組邊界和介面，確保 FR 映射到實作。

### HOW — 如何執行？

1. 使用 architect persona 建立 SAD.md
2. 使用 reviewer persona 執行 A/B 架構審查
3. 執行 Constitution SAD 檢查
4. 更新 TRACEABILITY_MATRIX.md (FR → 模組映射)
5. 建立 MODULE_BOUNDARY.md

### 產出物

```markdown
- 02-architecture/SAD.md
- 02-architecture/MODULE_BOUNDARY.md
- TRACEABILITY_MATRIX.md (更新)
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# 執行 Constitution SAD 檢查
python quality_gate/constitution/runner.py --type sad

# 執行 Phase 驗證
python cli.py phase-verify --phase 2
```

---

## Phase 3: 代碼實現 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `developer` | 實作代碼、撰寫單元測試 |
| **Agent B** | `reviewer` | 同行邏輯審查、代碼規範審查 |

### WHAT — 做什麼？

根據 SAD.md 實作代碼，並撰寫單元測試。

### WHEN — 何時執行？

Phase 2 完成並通過 Johnny HITL CONFIRM 之後。

### WHERE — 在哪裡執行？

`src/` 和 `tests/` 目錄。

### WHY — 為什麼？

將需求轉化為可運行的代碼，建立測試覆蓋。

### HOW — 如何執行？

1. **領域知識確認**：實作前查閱領域知識清單
2. **邏輯正確性自我檢查**：輸出≤輸入、分支一致、Lazy check
3. **代碼實作**：遵循 CODE_STANDARD.md
4. **單元測試**：包含邊界測試和負面測試
5. **同行邏輯審查**：Agent B 確認邏輯正確性
6. **合規矩陣更新**：確認 FR → 邏輯驗證方法映射

### 產出物

```markdown
- src/ (代碼檔案)
- tests/ (單元測試)
- 03-implementation/CODE_STANDARD.md
- 03-implementation/COMPLIANCE_MATRIX.md
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# 代碼覆蓋率檢查
pytest --cov=src --cov-report=term-missing

# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# 執行 Constitution 檢查
python quality_gate/constitution/runner.py

# 執行 Phase 驗證
python cli.py phase-verify --phase 3
```

---

## Phase 4: 測試 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `tester` | 建立 TEST_PLAN.md、執行測試 |
| **Agent B** | `reviewer` | 第一次 A/B 審查（TEST_PLAN）、第二次 A/B 審查（TEST_RESULTS）|

> ⚠️ **Tester ≠ Developer**：角色必須分離

### WHAT — 做什麼？

建立完整的測試計劃，執行測試並記錄結果。

### WHEN — 何時執行？

Phase 3 完成並通過 Johnny HITL CONFIRM 之後。

### WHERE — 在哪裡執行？

`04-testing/` 目錄。

### WHY — 為什麼？

驗證代碼是否滿足需求，確保功能正確性。

### HOW — 如何執行？

1. **建立 TEST_PLAN.md**：完整規格定義
2. **第一次 A/B 審查**：Agent B 審查 TEST_PLAN
3. **執行測試**：按照 TEST_PLAN 執行
4. **建立 TEST_RESULTS.md**：記錄 pytest 輸出
5. **第二次 A/B 審查**：Agent B 審查 TEST_RESULTS
6. **失敗案例分析**：根本原因分析

### 產出物

```markdown
- 04-testing/TEST_PLAN.md
- 04-testing/TEST_RESULTS.md
- 04-testing/FAILURE_ANALYSIS.md
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# 執行所有測試
pytest -v --tb=short

# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# 執行 Constitution Test Plan 檢查
python quality_gate/constitution/runner.py --type test_plan

# 執行 Phase 驗證
python cli.py phase-verify --phase 4
```

---

## Phase 5: 系統驗證 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `validator` | 建立 BASELINE.md、執行驗證 |
| **Agent B** | `reviewer` | 第一次 A/B 審查、第二次 A/B 審查 |

### WHAT — 做什麼？

驗證系統是否滿足 BASELINE 功能對照表。

### WHEN — 何時執行？

Phase 4 完成並通過 Johnny HITL CONFIRM 之後。

### WHERE — 在哪裡執行？

`05-validation/` 目錄。

### WHY — 為什麼？

確認系統實作與需求一致，建立監控基線。

### HOW — 如何執行？

1. **建立 BASELINE.md**：功能對照表（FR 狀態）
2. **第一次 A/B 審查**：確認 BASELINE 完整性
3. **建立 MONITORING_PLAN.md**：定義四個閾值
4. **執行驗證測試**：確認測試通過率 = 100%
5. **第二次 A/B 審查**：確認驗證結果
6. **邏輯正確性複查**：確認輸出≤輸入等基本邏輯

### 產出物

```markdown
- 05-validation/BASELINE.md
- 05-validation/MONITORING_PLAN.md
- 05-validation/VALIDATION_RESULTS.md
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# 測試通過率確認
pytest -v --tb=short | grep -E "passed|failed"

# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# 執行 Phase 驗證
python cli.py phase-verify --phase 5
```

---

## Phase 6: 品質確認 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `quality_engineer` | 生成 QUALITY_REPORT.md |
| **Agent B** | `reviewer` | A/B 監控數據分析審查 |

### WHAT — 做什麼？

進行 Constitution ≥ 80% 全面檢查，生成品質報告。

### WHEN — 何時執行？

Phase 5 完成並通過 Johnny HITL CONFIRM 之後。

### WHERE — 在哪裡執行？

`06-quality/` 目錄。

### WHY — 為什麼？

識別品質問題，分析根本原因，提出改進建議。

### HOW — 如何執行？

1. **Constitution ≥ 80% 全面檢查**：所有檢查項
2. **品質問題根源分析**：
   - Layer 1：症狀（現象描述）
   - Layer 2：因素（哪些因素導致）
   - Layer 3：根本原因（為什麼會這樣）
3. **建立 QUALITY_REPORT.md**（7 章節）
4. **A/B 監控數據分析**：確認監控有效性
5. **持續監控維持**：定義監控規則

### 產出物

```markdown
- 06-quality/QUALITY_REPORT.md
- 06-quality/ROOT_CAUSE_ANALYSIS.md
- 06-quality/IMPROVEMENT_SUGGESTIONS.md
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# Constitution 分數確認
python quality_gate/constitution/runner.py

# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# 執行 Phase 驗證
python cli.py phase-verify --phase 6
```

---

## Phase 7: 風險管理 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `risk_manager` | 建立 RISK_REGISTER.md |
| **Agent B** | `reviewer` | A/B 風險識別審查 |

### WHAT — 做什麼？

識別和管理專案風險，進行風險演練。

### WHEN — 何時執行？

Phase 6 完成並通過 Johnny HITL CONFIRM 之後。

### WHERE — 在哪裡執行？

`07-risk/` 目錄。

### WHY — 為什麼？

識別潛在風險，定義緩解措施，確保專案交付能力。

### HOW — 如何執行？

1. **五維度風險識別**：
   - 技術風險
   - 人員風險
   - 資源風險
   - 外部風險
   - 時間風險
2. **四層緩解措施**：避免 → 轉移 → 減輕 → 接受
3. **Decision Gate 確認**：確認風險可接受
4. **風險演練**：模擬風險場景，驗證緩解措施
5. **建立 RISK_REGISTER.md**

### 產出物

```markdown
- 07-risk/RISK_REGISTER.md
- 07-risk/RISK_DRILL_RECORDS.md
- 07-risk/DECISION_GATE.md
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# Decision Gate 確認
python -c "from enforcement.decision_gate import verify_risk_acceptance"

# 執行 Phase 驗證
python cli.py phase-verify --phase 7
```

---

## Phase 8: 配置發布 - Agent Prompt

### WHO — 誰執行？

| 角色 | Persona | 職責 |
|------|---------|------|
| **Agent A** | `release_manager` | 建立 CONFIG_RECORDS.md |
| **Agent B** | `reviewer` | A/B 發布清單審查 |

### WHAT — 做什麼？

完成配置管理，生成發布清單。

### WHEN — 何時執行？

Phase 7 完成並通過 Johnny HITL CONFIRM 之後。

### WHERE — 在哪裡執行？

`08-deployment/` 目錄。

### WHY — 為什麼？

確保配置可追溯，發布過程可控，回滾方案可用。

### HOW — 如何執行？

1. **SUP.8 配置管理**：建立 CONFIG_RECORDS.md（8 章節）
2. **七區塊發布清單**：驗證每個區塊
3. **pip freeze 輸出**：確認與 requirements.txt 一致
4. **回滾 SOP**：定義回滾步驟
5. **方法論閉環確認**：確認 Phase 5-8 全程監控健康
6. **最終監控報告**：確認所有閾值正常

### 產出物

```markdown
- 08-deployment/CONFIG_RECORDS.md
- 08-deployment/RELEASE_CHECKLIST.md
- 08-deployment/ROLLBACK_SOP.md
- 08-deployment/FINAL_REPORT.md
- DEVELOPMENT_LOG.md
```

### 驗證 Checkpoint

```bash
# pip freeze 一致性確認
pip freeze > /tmp/freeze.txt
diff requirements.txt /tmp/freeze.txt

# 執行 FrameworkEnforcer BLOCK 檢查
python cli.py enforce --level BLOCK

# 執行 Phase 驗證
python cli.py phase-verify --phase 8
```

---

## 🔧 Prompt 模板使用方式

### 啟動 Phase 工作

```python
# 載入 Prompt 模板
with open("docs/PHASE_PROMPTS.md", "r") as f:
    prompts = f.read()

# 根據 Phase 號碼選擇模板
phase = 1
prompt = extract_phase_prompt(prompts, phase)

# 傳給 Agent
agent_a.execute(prompt)
```

### 提取 Phase Prompt

```python
import re

def extract_phase_prompt(content: str, phase: int) -> str:
    """從 PHASE_PROMPTS.md 提取指定 Phase 的 Prompt"""
    pattern = rf"## Phase {phase}:.*?(?=## Phase \d+:|$)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None
```

---

## 📝 修訂歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| v6.09.0 | 2026-03-31 | 初始版本 |
