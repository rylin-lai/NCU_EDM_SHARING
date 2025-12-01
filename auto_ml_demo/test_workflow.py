#!/usr/bin/env python3
"""
Test Workflow Script
測試工作流程腳本

這個腳本用來測試整個ML自動化工作流程
This script tests the complete ML automation workflow
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description, cwd=None):
    """執行命令並處理錯誤"""
    print(f"🔄 {description}")
    print(f"   Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"✅ {description} - Success")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()[:200]}...")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"   Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ {description} - Exception: {str(e)}")
        return False

def test_local_workflow():
    """測試本地工作流程"""
    
    print("🧪 Testing Local ML Workflow")
    print("=" * 50)
    
    # 確保在正確的目錄
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 測試步驟
    steps = [
        {
            "cmd": [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            "desc": "Installing dependencies",
            "required": True
        },
        {
            "cmd": [sys.executable, "educational_dataset_generator.py", "--students", "100", "--semester", "2024_Test"],
            "desc": "Generating test dataset",
            "required": True
        },
        {
            "cmd": [sys.executable, "ml_report_generator.py", "--data", "data/educational_data_2024_Test.csv", "--output", "test_reports/"],
            "desc": "Running ML analysis",
            "required": True
        },
        {
            "cmd": [sys.executable, "create_pages_structure.py"],
            "desc": "Creating pages structure",
            "required": False
        }
    ]
    
    # 創建測試目錄
    os.makedirs("data", exist_ok=True)
    os.makedirs("test_reports", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    results = []
    
    for step in steps:
        success = run_command(step["cmd"], step["desc"])
        results.append(success)
        
        if step["required"] and not success:
            print(f"\n❌ Critical step failed: {step['desc']}")
            print("Stopping test workflow.")
            return False
    
    # 檢查生成的檔案
    print(f"\n📊 Checking generated files:")
    
    files_to_check = [
        "data/educational_data_2024_Test.csv",
        "data/educational_data_2024_Test.json",
        "test_reports/ml_analysis_report.html",
        "test_reports/analysis_summary.json"
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"   ✅ {file_path} ({size} bytes)")
        else:
            print(f"   ❌ {file_path} (missing)")
    
    # 統計結果
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📈 Test Results: {success_count}/{total_count} steps passed")
    
    if success_count == total_count:
        print("🎉 All tests passed! The workflow is ready for production.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def validate_github_workflow():
    """驗證GitHub workflow檔案"""
    
    print("\n🔍 Validating GitHub Workflow")
    print("=" * 30)
    
    workflow_file = Path("../.github/workflows/auto-ml-report.yml")
    
    if not workflow_file.exists():
        print("❌ GitHub workflow file not found")
        return False
    
    print("✅ GitHub workflow file exists")
    
    # 檢查檔案內容的基本結構
    try:
        content = workflow_file.read_text()
        
        required_sections = [
            "name:",
            "on:",
            "jobs:",
            "setup-deployment-info:",
            "generate-dataset:",
            "run-ml-analysis:",
            "deploy-to-pages:"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing required sections: {', '.join(missing_sections)}")
            return False
        else:
            print("✅ All required sections present")
        
        # 檢查是否使用了正確的 action 版本
        if "actions/upload-artifact@v3" in content:
            print("⚠️  Found deprecated artifact action v3, should use v4")
        else:
            print("✅ Using correct artifact action versions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading workflow file: {e}")
        return False

def main():
    """主要測試函數"""
    
    print("🎯 Auto ML Demo - Workflow Test")
    print("=" * 60)
    print("This script tests the complete ML automation pipeline")
    print("此腳本測試完整的ML自動化管線\n")
    
    # 檢查Python版本
    python_version = sys.version_info
    print(f"🐍 Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return 1
    else:
        print("✅ Python version OK")
    
    # 執行測試
    tests = [
        ("Local Workflow", test_local_workflow),
        ("GitHub Workflow", validate_github_workflow)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            all_passed = False
        
        print()  # 空行分隔
    
    # 最終結果
    print("🏁 Final Test Results")
    print("=" * 30)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The workflow is ready for production use")
        print("✅ 工作流程已準備好用於生產環境")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Please fix the issues before using in production")
        print("⚠️  請在生產使用前修復問題")
        return 1

if __name__ == "__main__":
    sys.exit(main())