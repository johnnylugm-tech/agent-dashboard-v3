#!/usr/bin/env python3
"""
Methodology-v2 Trend Analyzer & Auto-Optimizer (強化版)

每小時執行：
1. 收集真實 GitHub Issues
2. 分析痛點
3. 提出優化方案
4. 實現最高優先級項目
5. 更新文檔並發布 GitHub
"""

import os
import sys
import subprocess
import json
import re
from datetime import datetime
from typing import List, Dict, Any

WORKSPACE = "/Users/johnny/.openclaw/workspace-musk/skills/methodology-v2"
LOG_FILE = "/Users/johnny/.openclaw/workspace-musk/memory/cron-trend.log"

def log(msg):
    """寫入日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def run(cmd):
    """執行命令"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=WORKSPACE)
    return result.returncode, result.stdout, result.stderr

def check_quiet_hours():
    """檢查是否在安靜時段 (23:00-09:00)"""
    hour = datetime.now().hour
    if hour >= 23 or hour < 9:
        log("🌙 安靜時段 (23:00-09:00)，跳過執行")
        return True
    return False

def get_github_issues() -> List[Dict]:
    """獲取真實 GitHub Issues"""
    log("🔍 獲取 GitHub Issues...")
    
    try:
        # 使用 gh CLI 獲取 issues
        code, stdout, stderr = run(
            'gh issue list --repo johnnylugm-tech/methodology-v2 --state open --limit 20 --json "title,labels,comments"'
        )
        
        if code == 0 and stdout.strip():
            issues = json.loads(stdout)
            log(f"  ✅ 獲取 {len(issues)} 個 open issues")
            return issues
        else:
            log(f"  ⚠️ 無法獲取 issues: {stderr[:100] if stderr else 'Unknown error'}")
    except Exception as e:
        log(f"  ⚠️ API 錯誤: {e}")
    
    return []

def analyze_issue_trends(issues: List[Dict]) -> Dict[str, Any]:
    """分析 Issues 趨勢"""
    log("📊 分析 Issue 趨勢...")
    
    if not issues:
        return {
            "top_issues": [],
            "common_labels": [],
            "pain_points": []
        }
    
    # 統計標籤
    label_counts = {}
    for issue in issues:
        for label in issue.get("labels", []):
            name = label.get("name", "") if isinstance(label, dict) else label
            label_counts[name] = label_counts.get(name, 0) + 1
    
    # 最常見的標籤
    common_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Top issues (按 comments 數量)
    top_issues = sorted(issues, key=lambda x: x.get("comments", 0), reverse=True)[:5]
    
    # 痛點分析
    pain_points = []
    for issue in top_issues:
        title = issue.get("title", "")
        # 簡單關鍵詞匹配
        if any(k in title.lower() for k in ["bug", "error", "fix"]):
            pain_points.append({"title": title, "type": "bug", "priority": "high"})
        elif any(k in title.lower() for k in ["feature", "add", "support"]):
            pain_points.append({"title": title, "type": "enhancement", "priority": "medium"})
        else:
            pain_points.append({"title": title, "type": "other", "priority": "low"})
    
    return {
        "top_issues": top_issues,
        "common_labels": common_labels,
        "pain_points": pain_points
    }

def propose_solutions(analysis: Dict[str, Any]) -> List[Dict]:
    """根據實際分析提出解決方案"""
    log("📋 提出解決方案...")
    
    solutions = []
    pain_points = analysis.get("pain_points", [])
    
    # 根據痛點生成方案
    for pp in pain_points:
        title = pp["title"]
        priority = pp["priority"]
        
        # 關鍵詞匹配
        if "bug" in title.lower() or "error" in title.lower():
            solution = {
                "title": f"修復: {title[:50]}",
                "description": "根據 GitHub Issue 提出的修復方案",
                "module": "core",
                "effort": "low",
                "impact": "high",
                "source": "GitHub Issue",
                "priority": "high" if priority == "high" else "medium"
            }
        elif "security" in title.lower() or "safe" in title.lower():
            solution = {
                "title": f"強化安全: {title[:50]}",
                "description": "新增安全檢測規則",
                "module": "guardrails",
                "effort": "medium",
                "impact": "high",
                "source": "GitHub Issue",
                "priority": "high"
            }
        elif "test" in title.lower():
            solution = {
                "title": f"強化測試: {title[:50]}",
                "description": "新增測試案例",
                "module": "test_framework",
                "effort": "low",
                "impact": "medium",
                "source": "GitHub Issue",
                "priority": "medium"
            }
        else:
            solution = {
                "title": f"優化: {title[:50]}",
                "description": "根據用戶反饋優化",
                "module": "general",
                "effort": "medium",
                "impact": "medium",
                "source": "GitHub Issue",
                "priority": priority
            }
        
        solutions.append(solution)
    
    # 如果沒有真實 issues，使用輪換方案
    if not solutions:
        import random
        # 輪換池，每次執行會隨機選擇
        pool = [
            {"title": "強化 Guardrails 安全模組", "description": "新增更多安全檢測規則", "module": "guardrails", "effort": "medium", "impact": "high", "source": "輪換", "priority": "high"},
            {"title": "強化 LLM Providers 模組", "description": "新增 Provider 支援", "module": "llm_providers", "effort": "medium", "impact": "high", "source": "輪換", "priority": "high"},
            {"title": "增強 AutoQualityGate 穩定性", "description": "添加重試機制", "module": "auto_quality_gate.py", "effort": "low", "impact": "high", "source": "輪換", "priority": "high"},
            {"title": "新增測試案例", "description": "擴展測試覆蓋率", "module": "test_framework", "effort": "low", "impact": "medium", "source": "輪換", "priority": "medium"},
            {"title": "優化文件結構", "description": "改善文檔完整性", "module": "docs", "effort": "low", "impact": "medium", "source": "輪換", "priority": "medium"},
        ]
        # 根據時間（分鐘）選擇，保持一段時間內一致
        minute = datetime.now().minute
        seed = minute // 20  # 每20分鐘輪換一次
        random.seed(seed)
        solutions = random.sample(pool, min(3, len(pool)))
        random.seed()  # 重置隨機種子
        log(f"   🎲 輪換選擇: {[s['title'][:20] for s in solutions]}")
    
    # 按優先級排序
    priority_order = {"high": 0, "medium": 1, "low": 2}
    solutions.sort(key=lambda x: priority_order.get(x["priority"], 1))
    
    return solutions[:5]

def implement_solution(solution: Dict) -> bool:
    """實現解決方案"""
    log(f"🚀 實現方案: {solution['title']}")
    log(f"   描述: {solution['description']}")
    log(f"   模組: {solution['module']}")
    log(f"   來源: {solution['source']}")
    
    try:
        module = solution["module"]
        
        # 根據模組執行不同的實現
        if module == "guardrails":
            return implement_guardrails_improvement(solution)
        elif module == "llm_providers":
            return implement_llm_providers_improvement(solution)
        elif module == "auto_quality_gate.py":
            return implement_quality_gate_improvement(solution)
        elif module == "test_framework":
            return implement_test_framework_improvement(solution)
        elif module == "core":
            return implement_core_improvement(solution)
        else:
            log(f"   ⚠️ 未知模組: {module}")
            return False
            
    except Exception as e:
        log(f"   ❌ 實現失敗: {e}")
        return False

def implement_guardrails_improvement(solution: Dict) -> bool:
    """實現 Guardrails 改進"""
    log("   🔧 新增安全檢測規則...")
    
    guardrails_path = f"{WORKSPACE}/guardrails/guardrails.py"
    if not os.path.exists(guardrails_path):
        log("   ⚠️ guardrails.py 不存在")
        return False
    
    try:
        with open(guardrails_path, "r") as f:
            content = f.read()
        
        # 檢查是否已有新規則
        if "XSS" in content or "cross-site" in content.lower():
            log("   ⚠️ XSS 規則已存在")
            return False
        
        # 添加 XSS 檢測規則
        new_rule = '''
    # XSS Detection Rule
    def check_xss(self, text: str) -> bool:
        """檢測 XSS 攻擊"""
        xss_patterns = [
            r"<script",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"onclick=",
        ]
        for pattern in xss_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
'''
        # 在類別末尾添加新方法
        if new_rule not in content:
            content = content.rstrip() + new_rule + "\n"
            with open(guardrails_path, "w") as f:
                f.write(content)
            log("   ✅ XSS 檢測規則已添加")
            return True
        
        return False
    except Exception as e:
        log(f"   ❌ 錯誤: {e}")
        return False

def implement_llm_providers_improvement(solution: Dict) -> bool:
    """實現 LLM Providers 改進"""
    log("   🔧 新增 Provider 支援...")
    
    llm_path = f"{WORKSPACE}/llm_providers/llm_providers.py"
    if not os.path.exists(llm_path):
        log("   ⚠️ llm_providers.py 不存在")
        return False
    
    try:
        with open(llm_path, "r") as f:
            content = f.read()
        
        if "Groq" in content or "groq" in content.lower():
            log("   ⚠️ Groq 支援已存在")
            return False
        
        # 添加 Groq Provider
        new_provider = '''
    # Groq Provider
    elif provider == "groq":
        return {
            "name": "Groq",
            "models": ["llama-3.1-8b", "mixtral-8x7b"],
            "supports": ["chat", "completion"],
        }
'''
        content = content.rstrip() + new_provider + "\n"
        
        with open(llm_path, "w") as f:
            f.write(content)
        log("   ✅ Groq Provider 已添加")
        return True
    except Exception as e:
        log(f"   ❌ 錯誤: {e}")
        return False

def implement_quality_gate_improvement(solution: Dict) -> bool:
    """實現 QualityGate 改進"""
    log("   🔧 增強 QualityGate 穩定性...")
    
    gate_path = f"{WORKSPACE}/auto_quality_gate.py"
    if not os.path.exists(gate_path):
        log("   ⚠️ auto_quality_gate.py 不存在")
        return False
    
    try:
        with open(gate_path, "r") as f:
            content = f.read()
        
        if "retry" in content.lower() and "max_retries" in content.lower():
            log("   ⚠️ 重試機制已存在")
            return False
        
        # 添加重試裝飾器
        retry_decorator = '''
def with_retry(max_retries=3, delay=1):
    """重試裝飾器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

'''
        content = retry_decorator + content
        
        with open(gate_path, "w") as f:
            f.write(content)
        log("   ✅ 重試機制已添加")
        return True
    except Exception as e:
        log(f"   ❌ 錯誤: {e}")
        return False

def implement_test_framework_improvement(solution: Dict) -> bool:
    """實現 Test Framework 改進"""
    log("   🔧 新增測試案例...")
    
    test_path = f"{WORKSPACE}/test_framework/test_framework.py"
    if not os.path.exists(test_path):
        log("   ⚠️ test_framework.py 不存在")
        return False
    
    return False

def implement_core_improvement(solution: Dict) -> bool:
    """實現 Core 改進"""
    log("   🔧 Core 改進...")
    return False

def update_documentation(solution: Dict):
    """更新文檔"""
    log("📝 更新文檔...")
    
    readme_path = f"{WORKSPACE}/README.md"
    if not os.path.exists(readme_path):
        return
    
    with open(readme_path, "r") as f:
        content = f.read()
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    new_feature = f"\n### 🆕 {solution['title']} ({timestamp})\n- {solution['description']}\n- 來源: {solution['source']}\n"
    
    if "## ⭐ 關鍵亮點" in content:
        content = content.replace(
            "## ⭐ 關鍵亮點",
            f"## ⭐ 關鍵亮點{new_feature}"
        )
    
    with open(readme_path, "w") as f:
        f.write(content)
    
    log("   ✅ README.md 已更新")

def sync_and_push(solution: Dict):
    """同步並發布"""
    log("🔄 同步並發布到 GitHub...")
    
    try:
        code, stdout, stderr = run("git status --porcelain")
        
        if not stdout.strip():
            log("   無變更需要發布")
            return False
        
        run("git add -A")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"feat(auto): {solution['title'][:40]} - {timestamp}"
        
        code, stdout, stderr = run(f'git commit -m "{msg}"')
        if code != 0:
            log(f"   ⚠️ 提交失敗: {stderr[:100]}")
            return False
        
        log("   ✅ 提交成功")
        
        code, stdout, stderr = run("git push origin main")
        if code != 0:
            log(f"   ⚠️ 推送失敗: {stderr[:100]}")
            return False
        
        log("   ✅ 推送成功")
        log(f"   🎉 已發布: {msg}")
        return True
        
    except Exception as e:
        log(f"   ❌ 發布失敗: {e}")
        return False

def main():
    """主函數"""
    log("=" * 70)
    log("🚀 Methodology-v2 Trend Analyzer (強化版) 啟動")
    log("=" * 70)
    
    try:
        # 檢查安靜時段
        if check_quiet_hours():
            log("=" * 70)
            return
        
        # 1. 獲取真實 GitHub Issues
        issues = get_github_issues()
        
        # 2. 分析趨勢
        analysis = analyze_issue_trends(issues)
        
        log(f"\n📊 分析結果:")
        log(f"   Top Issues: {len(analysis['top_issues'])}")
        log(f"   常見標籤: {[l[0] for l in analysis['common_labels'][:3]]}")
        log(f"   痛點: {len(analysis['pain_points'])}")
        
        # 3. 提出方案
        solutions = propose_solutions(analysis)
        
        log(f"\n📋 優先級排序:")
        for i, sol in enumerate(solutions[:3], 1):
            log(f"   {i}. [{sol['priority'].upper()}] {sol['title'][:40]}")
        
        # 4. 實現最高優先級方案
        if solutions:
            top_solution = solutions[0]
            success = implement_solution(top_solution)
            
            if success:
                update_documentation(top_solution)
                sync_and_push(top_solution)
            else:
                log("   ⚠️ 跳過發布（實現未成功或無變更）")
        else:
            log("   ⚠️ 無可用方案")
        
        log("\n✅ 完成!")
        
    except Exception as e:
        log(f"❌ 錯誤: {e}")
        import traceback
        log(traceback.format_exc()[:500])
    
    log("=" * 70)

if __name__ == "__main__":
    main()
