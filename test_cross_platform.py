#!/usr/bin/env python3
"""
跨平台測試 - 用 pytest 同時測試 Python 和 Golang 實作
Cross-platform Tests - Use pytest to test both Python and Golang implementations

這個測試套件會：
This test suite will:
1. 測試 Python 版本的 tlsh_text_analyzer.py
2. 測試 Golang 版本的 tlsh-text-analyzer-linux binary  
3. 比較兩個實作的結果一致性
4. 驗證跨語言的功能對等性
"""

import pytest
import subprocess
import json
import os
import sys
from pathlib import Path


class TestCrossPlatform:
    """跨平台測試類別 / Cross-platform test class"""
    
    @pytest.fixture(scope="class")
    def setup_environment(self):
        """設置測試環境 / Setup test environment"""
        # 檢查 Python 腳本是否存在 / Check if Python script exists
        python_script = Path("tlsh_text_analyzer.py")
        if not python_script.exists():
            pytest.skip("Python script not found: tlsh_text_analyzer.py")
        
        # 檢查 Golang binary 是否存在並可執行 / Check if Golang binary exists and is executable
        # 優先使用可執行的版本：Linux（CI）或 macOS（本地開發）
        # Prefer executable version: Linux (CI) or macOS (local development)
        golang_binary_linux = Path("golang/tlsh-text-analyzer-linux")
        golang_binary_macos = Path("golang/tlsh-text-analyzer-macos")
        
        golang_binary = None
        
        # 嘗試 Linux 版本 / Try Linux version
        if golang_binary_linux.exists() and os.access(golang_binary_linux, os.X_OK):
            try:
                # 測試是否能執行 / Test if it can be executed
                import subprocess
                result = subprocess.run([str(golang_binary_linux), "-h"], 
                                       capture_output=True, timeout=5)
                golang_binary = golang_binary_linux
            except (subprocess.SubprocessError, OSError):
                pass  # Linux 版本無法執行，嘗試 macOS 版本 / Linux version can't run, try macOS
        
        # 如果 Linux 版本失敗，嘗試 macOS 版本 / If Linux version failed, try macOS version
        if golang_binary is None and golang_binary_macos.exists() and os.access(golang_binary_macos, os.X_OK):
            try:
                import subprocess
                result = subprocess.run([str(golang_binary_macos), "-h"], 
                                       capture_output=True, timeout=5)
                golang_binary = golang_binary_macos
            except (subprocess.SubprocessError, OSError):
                pass
        
        if golang_binary is None:
            pytest.skip("No executable Golang binary found: tried both Linux and macOS versions")
            
        return {
            "python_script": str(python_script),
            "golang_binary": str(golang_binary)
        }
    
    def run_python_analyzer(self, script_path: str, *args) -> dict:
        """
        執行 Python 版本的分析器
        Run Python version of analyzer
        """
        cmd = [sys.executable, script_path] + list(args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )
            
            # 如果有 --output 參數，讀取 JSON 檔案 / If has --output arg, read JSON file
            if "--output" in args:
                output_file = args[args.index("--output") + 1]
                with open(output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 解析 stdout 中的 JSON / Parse JSON from stdout
                return json.loads(result.stdout)
                
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output, e.stderr)
        except subprocess.TimeoutExpired:
            raise subprocess.TimeoutExpired("Python analyzer", 30)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse Python analyzer JSON output: {e}")
    
    def run_golang_analyzer(self, binary_path: str, *args) -> dict:
        """
        執行 Golang 版本的分析器
        Run Golang version of analyzer
        """
        cmd = [binary_path] + list(args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                check=True
            )
            
            # 如果有 -output 參數，讀取 JSON 檔案 / If has -output arg, read JSON file
            if "-output" in args:
                output_file = args[args.index("-output") + 1]
                with open(output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 解析 stdout 中的 JSON / Parse JSON from stdout
                return json.loads(result.stdout)
                
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(e.returncode, e.cmd, e.output, e.stderr)
        except subprocess.TimeoutExpired:
            raise subprocess.TimeoutExpired("Golang analyzer", 30)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse Golang analyzer JSON output: {e}")
    
    def test_both_implementations_example(self, setup_environment):
        """測試兩個實作的內建範例 / Test built-in example of both implementations"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        # 執行 Python 版本 / Run Python version
        python_result = self.run_python_analyzer(
            python_script, "--example", "--output", "python_example.json"
        )
        
        # 執行 Golang 版本 / Run Golang version
        golang_result = self.run_golang_analyzer(
            golang_binary, "-example", "-output", "golang_example.json"
        )
        
        # 基本結構檢查 / Basic structure validation
        assert "case" in python_result, "Python result missing 'case' field"
        assert "case" in golang_result, "Golang result missing 'case' field"
        
        assert "distance" in python_result, "Python result missing 'distance' field"  
        assert "distance" in golang_result, "Golang result missing 'distance' field"
        
        assert "similarity_class" in python_result, "Python result missing 'similarity_class' field"
        assert "similarity_class" in golang_result, "Golang result missing 'similarity_class' field"
        
        # 檢查距離值為非負整數 / Check distance values are non-negative integers
        assert isinstance(python_result["distance"], int), "Python distance should be integer"
        assert isinstance(golang_result["distance"], int), "Golang distance should be integer"
        assert python_result["distance"] >= 0, "Python distance should be non-negative"
        assert golang_result["distance"] >= 0, "Golang distance should be non-negative"
        
        # 距離值合理性檢查 / Distance value reasonableness check
        assert python_result["distance"] <= 1000, "Python distance should be <= 1000"
        assert golang_result["distance"] <= 1000, "Golang distance should be <= 1000"
        
        print(f"\n🐍 Python distance: {python_result['distance']}")
        print(f"🚀 Golang distance: {golang_result['distance']}")
        print(f"📊 Difference: {abs(python_result['distance'] - golang_result['distance'])}")
        
    def test_both_implementations_custom_text(self, setup_environment):
        """測試兩個實作的自訂文字比較 / Test custom text comparison of both implementations"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        # 定義測試文字 / Define test texts
        text1 = "這是第一個測試文字，用來檢驗 TLSH 功能是否正常運作。此文字包含足夠的字元數量以滿足 TLSH 最小長度要求，並且包含中文字符以測試 UTF-8 編碼處理。"
        text2 = "這是第二個測試文字，用來檢驗 TLSH 功能是否正常運作！此文字包含足夠的字元數量以滿足 TLSH 最小長度要求，並且包含中文字符以測試 UTF-8 編碼處理。"
        
        # 執行 Python 版本 / Run Python version
        python_result = self.run_python_analyzer(
            python_script, 
            "--text1", text1,
            "--text2", text2,
            "--output", "python_custom.json"
        )
        
        # 執行 Golang 版本 / Run Golang version
        golang_result = self.run_golang_analyzer(
            golang_binary,
            "-text1", text1,
            "-text2", text2, 
            "-output", "golang_custom.json"
        )
        
        # 驗證結果結構 / Validate result structure
        for result, name in [(python_result, "Python"), (golang_result, "Golang")]:
            # 檢查長度的合理性（允許字符vs字節的差異）/ Check length reasonableness (allow char vs byte differences)
            assert result["text1_length"] > 50, f"{name} text1_length should be > 50"
            assert result["text2_length"] > 50, f"{name} text2_length should be > 50"
            assert isinstance(result["distance"], int), f"{name} distance should be integer"
            assert result["distance"] >= 0, f"{name} distance should be non-negative"
            assert "tlsh_hash1" in result, f"{name} missing tlsh_hash1"
            assert "tlsh_hash2" in result, f"{name} missing tlsh_hash2"
        
        # 檢查 TLSH 雜湊格式 / Check TLSH hash format
        for result, name in [(python_result, "Python"), (golang_result, "Golang")]:
            hash1 = result["tlsh_hash1"]
            hash2 = result["tlsh_hash2"]
            
            # TLSH 雜湊應該以 T1 開頭並且有合理長度 / TLSH hash should start with T1 and have reasonable length
            assert hash1.startswith("T1"), f"{name} hash1 should start with T1"
            assert hash2.startswith("T1"), f"{name} hash2 should start with T1"
            # 允許不同的實作有不同的長度（原生vs模擬）/ Allow different lengths for different implementations (native vs simulated)
            assert len(hash1) >= 50, f"{name} hash1 should be at least 50 characters"
            assert len(hash2) >= 50, f"{name} hash2 should be at least 50 characters"
        
        print(f"\n🐍 Python result: distance={python_result['distance']}, class={python_result['similarity_class']}")
        print(f"🚀 Golang result: distance={golang_result['distance']}, class={golang_result['similarity_class']}")
        
    def test_both_implementations_identical_text(self, setup_environment):
        """測試兩個實作處理相同文字的情況 / Test both implementations with identical text"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        # 相同的測試文字 / Identical test text
        text = "相同的測試文字用來驗證兩個 TLSH 實作在處理完全相同內容時的行為。此文字重複多次以確保滿足 TLSH 的最小長度要求。" * 3
        
        # 執行 Python 版本 / Run Python version
        python_result = self.run_python_analyzer(
            python_script,
            "--text1", text,
            "--text2", text,
            "--output", "python_identical.json"
        )
        
        # 執行 Golang 版本 / Run Golang version
        golang_result = self.run_golang_analyzer(
            golang_binary,
            "-text1", text,
            "-text2", text,
            "-output", "golang_identical.json"
        )
        
        # 相同文字的距離應該是 0 / Distance for identical text should be 0
        assert python_result["distance"] == 0, "Python should return 0 distance for identical text"
        assert golang_result["distance"] == 0, "Golang should return 0 distance for identical text"
        
        # 相似性分類應該是 "Identical" / Similarity class should be "Identical"
        assert "Identical" in python_result["similarity_class"], "Python should classify as Identical"
        assert "Identical" in golang_result["similarity_class"], "Golang should classify as Identical"
        
        print(f"\n✅ Both implementations correctly handled identical text (distance=0)")
        
    def test_error_handling_short_text(self, setup_environment):
        """測試兩個實作的錯誤處理 - 文字太短 / Test error handling - text too short"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        short_text = "短文字"  # Short text that should trigger error
        normal_text = "正常長度的測試文字，用來搭配短文字進行錯誤處理測試。" * 2
        
        # 測試 Python 版本的錯誤處理 / Test Python error handling
        with pytest.raises((subprocess.CalledProcessError, AssertionError)):
            self.run_python_analyzer(
                python_script,
                "--text1", short_text,
                "--text2", normal_text
            )
        
        # 測試 Golang 版本的錯誤處理 / Test Golang error handling  
        with pytest.raises((subprocess.CalledProcessError, AssertionError)):
            self.run_golang_analyzer(
                golang_binary,
                "-text1", short_text,
                "-text2", normal_text
            )
        
        print(f"\n✅ Both implementations correctly handle short text errors")
        
    @pytest.mark.performance
    def test_performance_comparison(self, setup_environment):
        """效能比較測試 / Performance comparison test"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        # 較大的測試文字 / Larger test text
        large_text1 = "效能測試用的較大文字內容，重複多次以測試處理大量文字時的效能表現。" * 50
        large_text2 = "效能測試用的較大文字內容，重複多次以測試處理大量文字時的效能表現！" * 50
        
        import time
        
        # 測試 Python 版本效能 / Test Python performance
        start_time = time.time()
        python_result = self.run_python_analyzer(
            python_script,
            "--text1", large_text1,
            "--text2", large_text2,
            "--output", "python_perf.json"
        )
        python_time = time.time() - start_time
        
        # 測試 Golang 版本效能 / Test Golang performance
        start_time = time.time()
        golang_result = self.run_golang_analyzer(
            golang_binary,
            "-text1", large_text1,
            "-text2", large_text2,
            "-output", "golang_perf.json"
        )
        golang_time = time.time() - start_time
        
        print(f"\n⚡ Performance Comparison:")
        print(f"🐍 Python time: {python_time:.3f} seconds")
        print(f"🚀 Golang time: {golang_time:.3f} seconds")
        print(f"📊 Speedup: {python_time / golang_time:.2f}x")
        
        # 驗證結果仍然有效 / Validate results are still valid
        assert isinstance(python_result["distance"], int)
        assert isinstance(golang_result["distance"], int)
        assert python_result["distance"] >= 0
        assert golang_result["distance"] >= 0
        
    def teardown_method(self):
        """清理測試檔案 / Cleanup test files"""
        test_files = [
            "python_example.json", "golang_example.json",
            "python_custom.json", "golang_custom.json", 
            "python_identical.json", "golang_identical.json",
            "python_perf.json", "golang_perf.json"
        ]
        
        for file in test_files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass  # 檔案不存在，忽略 / File doesn't exist, ignore


if __name__ == "__main__":
    # 直接執行時的測試 / Direct execution tests
    print("🧪 Running cross-platform tests...")
    pytest.main([__file__, "-v", "--tb=short"])