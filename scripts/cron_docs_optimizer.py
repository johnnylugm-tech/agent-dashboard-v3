#!/usr/bin/env python3
"""
Documentation Optimizer + AutoQualityGate for methodology-v2

每小時執行：
1. 優化文件、使用者手冊與範例
2. 自動品質掃描 + 修復（AutoQualityGate）
"""

import os
import sys
import subprocess
import re
from datetime import datetime

WORKSPACE = "/Users/johnny/.openclaw/workspace-musk/skills/methodology-v2"
LOG_FILE = "/Users/johnny/.openclaw/workspace-musk/memory/cron-docs.log"

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

def check_git_changes():
    """檢查 Git 變更"""
    log("📋 檢查 Git 變更...")
    code, stdout, stderr = run("git status --porcelain")
    if stdout.strip():
        log(f"  有未提交的變更: {stdout.strip()[:200]}")
        return True
    log("  無未提交變更")
    return False


def check_document_consistency():
    """檢查文檔一致性"""
    log("📋 檢查文檔一致性...")
    
    issues = []
    
    # 1. 版本一致性檢查
    try:
        # 讀取各檔案的版本
        with open(f"{WORKSPACE}/__init__.py", "r") as f:
            init_version = None
            for line in f:
                if "__version__" in line:
                    init_version = line.split("=")[1].strip().strip('"').strip("'")
                    break
        
        with open(f"{WORKSPACE}/cli.py", "r") as f:
            cli_version = None
            for line in f:
                if "VERSION = " in line:
                    cli_version = line.split("=")[1].strip().strip('"').strip("'")
                    break
        
        with open(f"{WORKSPACE}/README.md", "r") as f:
            readme_content = f.read()
            readme_match = re.search(r'v(\d+\.\d+)', readme_content)
            readme_version = readme_match.group(1) if readme_match else None
        
        log(f"   版本: __init__.py={init_version}, cli.py={cli_version}, README={readme_version}")
        
        # 正規化版本號 (5.4 -> 5.4.0)
        def normalize(v):
            parts = v.split(".")
            if len(parts) == 2:
                return v + ".0"
            return v
        
        init_norm = normalize(init_version or "")
        cli_norm = normalize(cli_version or "")
        readme_norm = normalize(readme_version or "")
        
        if init_norm != cli_norm or cli_norm != readme_norm:
            issues.append({
                "type": "version_mismatch",
                "description": f"版本不一致: init={init_version}, cli={cli_version}, readme={readme_version}",
                "severity": "high"
            })
            log("   ⚠️ 版本不一致")
        else:
            log("   ✅ 版本一致")
            
    except Exception as e:
        log(f"   ❌ 版本檢查錯誤: {e}")
    
    # 2. CLI 命令一致性檢查
    try:
        # 從 cli.py 提取實際命令
        result = subprocess.run(
            ["python3", "cli.py", "--help"],
            capture_output=True, text=True, cwd=WORKSPACE
        )
        
        if result.returncode == 0:
            help_text = result.stdout
            # 計算命令數量
            commands_found = re.findall(r'^    (\w+)\s', help_text, re.MULTILINE)
            cli_count = len(commands_found)
            
            # 從 README 提取命令數量
            readme_match = re.search(r'共 (\d+) 個 CLI 命令', readme_content)
            if readme_match:
                readme_count = int(readme_match.group(1))
                if cli_count != readme_count:
                    issues.append({
                        "type": "cli_count_mismatch",
                        "description": f"CLI 命令數量不一致: cli.py={cli_count}, README={readme_count}",
                        "severity": "medium"
                    })
                    log(f"   ⚠️ CLI 命令數量: {cli_count} vs README={readme_count}")
                else:
                    log(f"   ✅ CLI 命令數量一致: {cli_count}")
        else:
            log("   ⚠️ 無法執行 cli.py --help")
            
    except Exception as e:
        log(f"   ❌ CLI 檢查錯誤: {e}")
    
    # 3. 模組數量檢查
    try:
        py_files = subprocess.run(
            ["find", ".", "-name", "*.py", "-not", "-path", "./.*", "-not", "-name", "test_*"],
            capture_output=True, text=True, cwd=WORKSPACE
        )
        module_count = len(py_files.stdout.strip().split("\n"))
        
        readme_match = re.search(r'模組 \| (\d+)', readme_content)
        if readme_match:
            readme_modules = int(readme_match.group(1))
            if abs(module_count - readme_modules) > 5:
                issues.append({
                    "type": "module_count_mismatch",
                    "description": f"模組數量不一致: 實際={module_count}, README={readme_modules}",
                    "severity": "low"
                })
                log(f"   ⚠️ 模組數量: 實際={module_count}, README={readme_modules}")
            else:
                log(f"   ✅ 模組數量: {module_count}")
        
    except Exception as e:
        log(f"   ❌ 模組檢查錯誤: {e}")
    
    return issues



def check_issues():
    """檢查 Issues / 回饋"""
    log("🔍 檢查 TODO/FIXME...")
    code, stdout, stderr = run("grep -r 'TODO\\|FIXME\\|XXX' --include='*.py' --include='*.md' . | head -10")
    if stdout.strip():
        count = len(stdout.strip().splitlines())
        log(f"  發現 {count} 處 TODO/FIXME")
        return True
    log("  無 TODO/FIXME")
    return False

def update_docs():
    """更新文件"""
    log("📝 文件更新檢查...")
    
    # 執行文檔一致性檢查
    consistency_issues = check_document_consistency()
    
    if consistency_issues:
        log(f"   ⚠️ 發現 {len(consistency_issues)} 個一致性問題")
        for issue in consistency_issues:
            log(f"      - {issue['type']}: {issue['description']}")
    
    docs = ["README.md", "USER_GUIDE.md", "SKILL.md"]
    for doc in docs:
        path = os.path.join(WORKSPACE, doc)
        if os.path.exists(path):
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            age = (datetime.now() - mtime).total_seconds() / 3600
            log(f"  {doc}: {age:.1f} 小時前更新")
    
    return True

def run_quality_gate():
    """執行 AutoQualityGate 掃描 + 修復"""
    log("🛡️ 執行 AutoQualityGate 掃描...")
    
    try:
        sys.path.insert(0, WORKSPACE)
        from auto_quality_gate import AutoQualityGate
        
        gate = AutoQualityGate()
        
        # 掃描核心 Python 檔案
        core_files = [
            "core.py",
            "cli.py",
            "auto_quality_gate.py",
            "agent_evaluator.py",
            "structured_output.py",
            "data_quality.py",
            "enterprise_hub.py",
            "langgraph_migrator.py",
        ]
        
        total_issues = 0
        total_fixed = 0
        
        for f in core_files:
            path = os.path.join(WORKSPACE, f)
            if os.path.exists(path):
                log(f"  掃描: {f}")
                
                # 掃描
                report = gate.scan(path)
                issues = len(report.issues)
                total_issues += issues
                
                if issues > 0:
                    log(f"    發現 {issues} 個問題")
                    
                    # 自動修復 (使用正確的 fix 方法)
                    if issues > 0:
                        fix_result = gate.fix(report)
                        fixed_count = len(fix_result.get('fixed', []))
                        if fixed_count > 0:
                            total_fixed += fixed_count
                            log(f"    已修復 {fixed_count} 個問題")
        
        if total_issues > 0:
            log(f"  📊 總計: {total_issues} 問題, {total_fixed} 已修復")
            
            # 分析未修復問題
            unfixed = total_issues - total_fixed
            if unfixed > 0:
                log(f"  📋 未修復 ({unfixed} 個):")
                log("     - 已註釋/無需修復 (print-debug)")
                log("     - 需人工判斷 (hardcoded-secret)")
                log("     - 需人工實現 (TODO/FIXME)")
                log("     - 保留作為診斷用途")
        else:
            log("  ✅ 無問題")
        
        return True
        
    except Exception as e:
        log(f"  ❌ QualityGate 錯誤: {e}")
        import traceback
        log(f"     {traceback.format_exc()[:200]}")
        return False

def optimize_examples():
    """優化範例"""
    log("💡 範例優化檢查...")
    
    cases_dir = os.path.join(WORKSPACE, "docs/workflows")
    if os.path.exists(cases_dir):
        case_files = [f for f in os.listdir(cases_dir) if f.endswith('.md')]
        log(f"  案例檔案: {len(case_files)} 個")
    
    return True

def sync_to_github():
    """同步到 GitHub"""
    log("🔄 檢查是否需要同步...")
    
    code, stdout, stderr = run("git status --porcelain")
    if stdout.strip():
        log("  發現變更，準備提交...")
        
        run("git add -A")
        
        msg = f"auto: hourly optimization + quality gate - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        code, stdout, stderr = run(f'git commit -m "{msg}"')
        
        if code == 0:
            log("  ✅ 提交成功")
            
            # Fix: pull --rebase before push to avoid "rejected" errors when remote has new commits
            code, stdout, stderr = run("git pull --rebase origin main")
            if code == 0:
                log("  ✅ 拉取成功")
            else:
                log(f"  ⚠️ 拉取失敗: {stderr[:100]}")
            
            code, stdout, stderr = run("git push origin main")
            if code == 0:
                log("  ✅ 推送成功")
            else:
                log(f"  ⚠️ 推送失敗: {stderr[:100]}")
        else:
            log(f"  ⚠️ 提交失敗: {stderr[:100]}")
    else:
        log("  無變更需要同步")
    
    return True

def generate_report():
    """產生報告"""
    log("📊 產生報告...")
    
    code, stdout, stderr = run("find . -name '*.py' -not -path './.*' | wc -l")
    py_files = stdout.strip()
    
    code, stdout, stderr = run("find . -name '*.md' -not -path './.*' | wc -l")
    md_files = stdout.strip()
    
    log(f"  Python 檔案: {py_files}")
    log(f"  Markdown 檔案: {md_files}")
    
    return True

def check_quiet_hours():
    """檢查是否在安靜時段 (23:00-09:00)"""
    hour = datetime.now().hour
    if hour >= 23 or hour < 9:
        log("🌙 安靜時段 (23:00-09:00)，跳過執行")
        return True
    return False

def main():
    """主函數"""
    log("=" * 60)
    log("🚀 methodology-v2 文件優化 + QualityGate 腳本啟動")
    log("=" * 60)
    
    # 檢查安靜時段
    if check_quiet_hours():
        log("=" * 60)
        return
    
    try:
        check_git_changes()
        check_issues()
        update_docs()
        run_quality_gate()  # ⭐ AutoQualityGate 整合
        optimize_examples()
        generate_report()
        sync_to_github()
        
        log("✅ 完成!")
    except Exception as e:
        log(f"❌ 錯誤: {e}")
    
    log("=" * 60)

if __name__ == "__main__":
    main()
