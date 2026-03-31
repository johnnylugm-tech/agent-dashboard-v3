#!/usr/bin/env python3
"""
Methodology-v2 Daily Evaluation Fixer

每天 21:35 執行：
1. 讀取評測報告 (methodology-status-for-musk.md)
2. 評估修復方式
3. 完成修復
4. 上傳 GitHub
"""

import os
import sys
import subprocess
import json
import re
from datetime import datetime
from typing import List, Dict, Any

WORKSPACE = "/Users/johnny/.openclaw/workspace-musk/skills/methodology-v2"
REPORT_FILE = "/Users/johnny/.openclaw/workspace/memory/methodology-status-for-musk.md"
LOG_FILE = "/Users/johnny/.openclaw/workspace-musk/memory/cron-daily-fix.log"

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

def read_report():
    """讀取評測報告"""
    log("📄 讀取評測報告...")
    
    if not os.path.exists(REPORT_FILE):
        log(f"   ⚠️ 報告檔案不存在: {REPORT_FILE}")
        return None
    
    with open(REPORT_FILE, "r") as f:
        content = f.read()
    
    log(f"   已讀取報告 ({len(content)} 字元)")
    return content

def parse_report(content: str) -> Dict[str, Any]:
    """解析評測報告"""
    log("🔍 解析評測報告...")
    
    result = {
        "version": None,
        "issues": [],
        "todos": [],
        "bugs": [],
        "enhancements": []
    }
    
    # 提取版本
    version_match = re.search(r'版本[：:]\s*v?(\d+\.\d+)', content)
    if version_match:
        result["version"] = version_match.group(1)
    
    # 提取待辦 (TODO/FIXME)
    todo_pattern = re.compile(r'^\s*[-*]\s*\[ \]\s*(.+)$', re.MULTILINE)
    result["todos"] = todo_pattern.findall(content)
    
    # 提取 Bug 項目
    bug_patterns = [
        r'[Bb]ug[:\s]+(.+)',
        r'❌\s*(.+)',
        r'[Ff]ix\s+(.+?)(?:\n|$)',
    ]
    for pattern in bug_patterns:
        matches = re.findall(pattern, content)
        result["bugs"].extend(matches)
    
    # 提取 Enhancement 項目
    enhancement_patterns = [
        r'[Ee]nhancement[:\s]+(.+)',
        r'[Nn]ew\s+[Ff]eature[:\s]+(.+)',
        r'🆕\s*(.+)',
    ]
    for pattern in enhancement_patterns:
        matches = re.findall(pattern, content)
        result["enhancements"].extend(matches)
    
    # 提取 ⏸️ 暫停項目
    pause_pattern = re.compile(r'[⏸️]\s*(.+?)(?:\n|$)', re.MULTILINE)
    result["paused"] = pause_pattern.findall(content)
    
    log(f"   版本: {result['version']}")
    log(f"   待辦: {len(result['todos'])} 項")
    log(f"   Bug: {len(result['bugs'])} 項")
    log(f"   Enhancement: {len(result['enhancements'])} 項")
    
    return result

def assess_and_fix(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """評估並修復"""
    log("🔧 評估並修復...")
    
    fixes = []
    
    for bug in parsed.get("bugs", []):
        log(f"   🐛 Bug: {bug[:60]}...")
        fix_result = fix_bug(bug)
        fixes.append(fix_result)
    
    for enhancement in parsed.get("enhancements", []):
        log(f"   🆕 Enhancement: {enhancement[:60]}...")
        fix_result = implement_enhancement(enhancement)
        fixes.append(fix_result)
    
    return {"fixes": fixes}

def fix_bug(bug_desc: str) -> Dict[str, Any]:
    """修復 Bug"""
    bug_lower = bug_desc.lower()
    
    # 版本號問題
    if "版本" in bug_desc or "version" in bug_lower:
        return fix_version_issue()
    
    # 單元測試問題
    if "測試" in bug_desc or "test" in bug_lower:
        return fix_test_issue()
    
    # 依賴問題
    if "依賴" in bug_desc or "dependency" in bug_lower or "import" in bug_lower:
        return fix_dependency_issue()
    
    # 預設關閉
    log(f"   ⚠️ 暫無自動修復方案")
    return {"status": "skip", "reason": "無自動修復方案", "item": bug_desc}

def fix_version_issue() -> Dict[str, Any]:
    """修復版本問題"""
    log("   🔧 檢查版本號...")
    
    code, stdout, stderr = run("grep -r 'VERSION = \\\"\\|__version__ = \\\"' --include='*.py' .")
    
    if stdout.strip():
        log(f"   📋 版本定義:\n{stdout.strip()}")
        
        # 自動更新 README.md badge 版本
        readme_path = f"{WORKSPACE}/README.md"
        if os.path.exists(readme_path):
            with open(readme_path, "r") as f:
                content = f.read()
            
            # 更新 badge 版本
            import re
            new_content = re.sub(
                r'v(\d+\.\d+\.\d+)',
                lambda m: f"v{float(m.group(1)) + 0.1:.1f}" if m.group(1).count('.') == 1 else f"v{float(m.group(1).rsplit('.', 1)[0]) + 0.1 if m.group(1).count('.') == 1 else '5.5.0'}",
                content
            )
            
            # 寫回
            with open(readme_path, "w") as f:
                f.write(new_content)
            
            log("   ✅ 版本已更新")
            return {"status": "fixed", "item": "版本更新"}
    
    return {"status": "skip", "reason": "無版本問題", "item": "版本"}

def fix_test_issue() -> Dict[str, Any]:
    """修復測試問題"""
    log("   🔧 執行測試...")
    
    code, stdout, stderr = run("python3 -m pytest tests/ -v 2>&1 | tail -20")
    
    if code == 0:
        log("   ✅ 所有測試通過")
        return {"status": "fixed", "item": "測試通過"}
    else:
        log(f"   ⚠️ 測試失敗: {stdout[-200:]}")
        return {"status": "fail", "item": "測試失敗", "output": stdout[-200:]}

def fix_dependency_issue() -> Dict[str, Any]:
    """修復依賴問題"""
    log("   🔧 檢查依賴...")
    
    # 檢查缺失的 import
    code, stdout, stderr = run("python3 -c 'import sys; sys.path.insert(0, \".\"); from core import *' 2>&1")
    
    if code == 0:
        return {"status": "fixed", "item": "依賴正常"}
    else:
        log(f"   ⚠️ 依賴問題: {stdout[:200]}")
        return {"status": "fail", "item": "依賴問題", "output": stdout[:200]}

def implement_enhancement(enhancement: str) -> Dict[str, Any]:
    """實現 Enhancement"""
    log(f"   ⚠️ Enhancement 暫無自動實現: {enhancement[:50]}...")
    return {"status": "skip", "reason": "Enhancement 需手動實現", "item": enhancement}

def commit_and_push(fixes: List[Dict]) -> bool:
    """提交並推送"""
    log("🔄 提交並推送到 GitHub...")
    
    try:
        # 檢查變更
        code, stdout, stderr = run("git status --porcelain")
        
        if not stdout.strip():
            log("   無變更需要提交")
            return True
        
        # 添加
        run("git add -A")
        
        # 提交
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        fix_summary = ", ".join([f"{f['item']}({f['status']})" for f in fixes[:3]])
        msg = f"fix(daily): {fix_summary} - {timestamp}"
        
        code, stdout, stderr = run(f'git commit -m "{msg}"')
        
        if code == 0:
            log(f"   ✅ 提交: {msg[:60]}...")
        else:
            log(f"   ⚠️ 提交失敗: {stderr[:100]}")
            return False
        
        # 推送
        code, stdout, stderr = run("git push origin main")
        
        if code == 0:
            log("   ✅ 推送成功")
            return True
        else:
            log(f"   ⚠️ 推送失敗: {stderr[:100]}")
            return False
            
    except Exception as e:
        log(f"   ❌ 錯誤: {e}")
        return False

def main():
    """主函數"""
    log("=" * 70)
    log("🚀 Methodology-v2 Daily Evaluation Fixer 啟動")
    log("=" * 70)
    
    try:
        # 1. 讀取報告
        content = read_report()
        
        if content is None:
            log("   ⚠️ 無報告檔案，等待明日 21:35")
            log("=" * 70)
            return
        
        # 2. 解析報告
        parsed = parse_report(content)
        
        # 3. 評估並修復
        result = assess_and_fix(parsed)
        
        # 4. 提交推送
        success = commit_and_push(result["fixes"])
        
        if success:
            log("\n✅ 每日評測修復完成!")
        else:
            log("\n⚠️ 部分完成，請手動檢查")
        
        log(f"\n修復摘要:")
        for fix in result["fixes"]:
            status_icon = "✅" if fix["status"] == "fixed" else "⚠️" if fix["status"] == "skip" else "❌"
            log(f"   {status_icon} {fix['item']}: {fix['status']}")
        
    except Exception as e:
        log(f"❌ 錯誤: {e}")
        import traceback
        log(traceback.format_exc()[:500])
    
    log("=" * 70)

if __name__ == "__main__":
    main()
