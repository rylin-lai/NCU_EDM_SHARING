#!/usr/bin/env python3
"""
字串反轉器的 pytest 測試檔案
pytest test file for String Reverser

這個測試檔案會同時測試 Python 和 Golang 版本的字串反轉器
This test file will test both Python and Golang versions of the string reverser

執行測試 / Run tests:
    pytest test_string_reverser.py -v
"""

import pytest
import subprocess
import json
import os
import sys
from pathlib import Path


class TestStringReverser:
    """字串反轉器測試類別 / String Reverser Test Class"""
    
    @pytest.fixture(scope="class")
    def setup_environment(self):
        """設置測試環境 / Setup test environment"""
        # 檢查 Python 腳本是否存在 / Check if Python script exists
        python_script = Path("string_reverser.py")
        if not python_script.exists():
            pytest.skip("Python script not found: string_reverser.py")
        
        # 檢查 Golang binary 是否存在 / Check if Golang binary exists
        golang_dir = Path("golang")
        golang_binary = golang_dir / "string-reverser"
        
        if not golang_dir.exists():
            pytest.skip("Golang directory not found: golang/")
        
        if not golang_binary.exists():
            pytest.skip(f"Golang binary not found: {golang_binary}. Please build it first with 'cd golang && go build -o string-reverser'")
            
        return {
            "python_script": str(python_script),
            "golang_binary": str(golang_binary)
        }
    
    
    def run_python_reverser(self, script_path: str, *args) -> dict:
        """
        執行 Python 版本的反轉器
        Run Python version of reverser
        """
        cmd = [sys.executable, script_path] + list(args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
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
            pytest.fail(f"Python reverser failed: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail("Python reverser timeout")
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse Python reverser JSON output: {e}")
    
    def run_golang_reverser(self, binary_path: str, *args) -> dict:
        """
        執行 Golang 版本的反轉器
        Run Golang version of reverser
        """
        cmd = [binary_path] + list(args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
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
            pytest.fail(f"Golang reverser failed: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail("Golang reverser timeout")
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse Golang reverser JSON output: {e}")
    
    def test_both_implementations_example(self, setup_environment):
        """測試兩個實作的內建範例 / Test built-in example of both implementations"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        try:
            # 執行 Python 版本 / Run Python version
            python_result = self.run_python_reverser(
                python_script, "--example", "--output", "python_example.json"
            )
            
            # 執行 Golang 版本 / Run Golang version
            golang_result = self.run_golang_reverser(
                golang_binary, "-example", "-output", "golang_example.json"
            )
            
            # 基本結構檢查 / Basic structure validation
            for result, name in [(python_result, "Python"), (golang_result, "Golang")]:
                assert "original" in result, f"{name} result missing 'original' field"
                assert "reversed" in result, f"{name} result missing 'reversed' field"
                assert "original_length" in result, f"{name} result missing 'original_length' field"
                assert "reversed_length" in result, f"{name} result missing 'reversed_length' field"
                assert "is_palindrome" in result, f"{name} result missing 'is_palindrome' field"
                assert "char_count" in result, f"{name} result missing 'char_count' field"
            
            # 長度檢查 / Length validation
            assert python_result["original_length"] == python_result["reversed_length"]
            assert golang_result["original_length"] == golang_result["reversed_length"]
            
            # 原始字串應該相同 / Original strings should be the same
            assert python_result["original"] == golang_result["original"]
            
            # 反轉結果應該相同 / Reversed results should be the same
            assert python_result["reversed"] == golang_result["reversed"]
            
            print(f"\n🐍 Python result: '{python_result['reversed']}'")
            print(f"🚀 Golang result: '{golang_result['reversed']}'")
            print(f"✅ Both implementations produced identical results")
            
        finally:
            # 清理測試檔案 / Cleanup test files
            try:
                os.remove("python_example.json")
                os.remove("golang_example.json")
            except FileNotFoundError:
                pass
    
    def test_both_implementations_custom_text(self, setup_environment):
        """測試兩個實作的自訂文字 / Test custom text of both implementations"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        test_text = "Python與Golang測試123"
        
        try:
            # 執行 Python 版本 / Run Python version
            python_result = self.run_python_reverser(
                python_script, 
                "--text", test_text,
                "--output", "python_custom.json"
            )
            
            # 執行 Golang 版本 / Run Golang version
            golang_result = self.run_golang_reverser(
                golang_binary,
                "-text", test_text,
                "-output", "golang_custom.json"
            )
            
            # 驗證結果一致 / Verify results are consistent
            assert python_result["original"] == golang_result["original"]
            assert python_result["reversed"] == golang_result["reversed"]
            assert python_result["original_length"] == golang_result["original_length"]
            assert python_result["is_palindrome"] == golang_result["is_palindrome"]
            
            # 字符統計應該相似（允許些微差異）/ Character counts should be similar (allow minor differences)
            assert python_result["char_count"]["digits"] == golang_result["char_count"]["digits"]
            
            print(f"\n📝 Original: '{test_text}'")
            print(f"🔄 Reversed: '{python_result['reversed']}'")
            print(f"📊 Character counts match between implementations")
            
        finally:
            # 清理測試檔案 / Cleanup test files
            try:
                os.remove("python_custom.json")
                os.remove("golang_custom.json")
            except FileNotFoundError:
                pass
    
    def test_both_implementations_palindrome(self, setup_environment):
        """測試兩個實作處理回文的情況 / Test both implementations with palindrome"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        palindrome_text = "A man a plan a canal Panama"
        
        try:
            # 執行 Python 版本 / Run Python version
            python_result = self.run_python_reverser(
                python_script,
                "--text", palindrome_text,
                "--output", "python_palindrome.json"
            )
            
            # 執行 Golang 版本 / Run Golang version
            golang_result = self.run_golang_reverser(
                golang_binary,
                "-text", palindrome_text,
                "-output", "golang_palindrome.json"
            )
            
            # 兩個實作都應該識別出這是回文 / Both implementations should identify this as palindrome
            assert python_result["is_palindrome"] == True, "Python should identify palindrome"
            assert golang_result["is_palindrome"] == True, "Golang should identify palindrome"
            
            # 反轉結果應該相同 / Reversed results should be the same
            assert python_result["reversed"] == golang_result["reversed"]
            
            print(f"\n🔄 Palindrome test: '{palindrome_text}'")
            print(f"✅ Both implementations correctly identified palindrome")
            
        finally:
            # 清理測試檔案 / Cleanup test files
            try:
                os.remove("python_palindrome.json")
                os.remove("golang_palindrome.json")
            except FileNotFoundError:
                pass
    
    def test_both_implementations_empty_string(self, setup_environment):
        """測試兩個實作處理空字串 / Test both implementations with empty string"""
        python_script = setup_environment["python_script"]
        golang_binary = setup_environment["golang_binary"]
        
        empty_text = ""
        
        try:
            # 執行 Python 版本 / Run Python version
            python_result = self.run_python_reverser(
                python_script,
                "--text", empty_text
            )
            
            # 執行 Golang 版本 / Run Golang version
            golang_result = self.run_golang_reverser(
                golang_binary,
                "-text", empty_text
            )
            
            # 空字串的反轉應該還是空字串 / Reverse of empty string should be empty string
            assert python_result["original"] == ""
            assert python_result["reversed"] == ""
            assert golang_result["original"] == ""
            assert golang_result["reversed"] == ""
            
            # 長度應該是 0 / Length should be 0
            assert python_result["original_length"] == 0
            assert golang_result["original_length"] == 0
            
            # 空字串是回文 / Empty string is palindrome
            assert python_result["is_palindrome"] == True
            assert golang_result["is_palindrome"] == True
            
            print(f"\n✅ Both implementations correctly handled empty string")
            
        finally:
            # 不需要清理檔案，因為沒有輸出檔案 / No files to cleanup since no output files
            pass


if __name__ == "__main__":
    # 直接執行時運行測試 / Run tests when executed directly
    print("🧪 Running string reverser cross-platform tests...")
    pytest.main([__file__, "-v", "--tb=short"])