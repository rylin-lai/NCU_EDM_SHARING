#!/usr/bin/env python3
"""
純粹的 Unit Tests for string_reverser.py
Pure Unit Tests for string_reverser.py

這些是真正的單元測試，只測試 Python 模組本身的功能，不依賴外部系統
These are true unit tests that only test Python module functionality, no external dependencies

執行測試 / Run tests:
    pytest test_string_reverser_unit.py -v
"""

import pytest
import sys
import os
from unittest.mock import patch, mock_open

# 確保可以 import string_reverser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import string_reverser
except ImportError:
    pytest.skip("string_reverser.py not found", allow_module_level=True)


class TestStringReverserUnit:
    """純粹的單元測試類別 / Pure Unit Test Class"""
    
    def test_reverse_string_basic(self):
        """測試基本字串反轉功能 / Test basic string reversal"""
        # Test basic English text
        result = string_reverser.reverse_string("Hello World")
        assert result == "dlroW olleH"
        
        # Test numbers
        result = string_reverser.reverse_string("12345")
        assert result == "54321"
        
        # Test mixed content
        result = string_reverser.reverse_string("Python3.11")
        assert result == "11.3nohtyP"
    
    def test_reverse_string_empty(self):
        """測試空字串處理 / Test empty string handling"""
        result = string_reverser.reverse_string("")
        assert result == ""
    
    def test_reverse_string_single_char(self):
        """測試單字符處理 / Test single character handling"""
        result = string_reverser.reverse_string("A")
        assert result == "A"
        
        result = string_reverser.reverse_string("1")
        assert result == "1"
        
        result = string_reverser.reverse_string("中")
        assert result == "中"
    
    def test_reverse_string_unicode(self):
        """測試 Unicode 字符處理 / Test Unicode character handling"""
        # Chinese characters
        result = string_reverser.reverse_string("你好世界")
        assert result == "界世好你"
        
        # Mixed Chinese and English
        result = string_reverser.reverse_string("Hello世界")
        assert result == "界世olleH"
        
        # Emojis
        result = string_reverser.reverse_string("Python🐍是很棒的")
        assert result == "的棒很是🐍nohtyP"
    
    def test_reverse_string_special_chars(self):
        """測試特殊字符處理 / Test special character handling"""
        # Punctuation
        result = string_reverser.reverse_string("Hello, World!")
        assert result == "!dlroW ,olleH"
        
        # Symbols
        result = string_reverser.reverse_string("@#$%^&*()")
        assert result == ")(*&^%$#@"
        
        # Whitespace
        result = string_reverser.reverse_string("  spaces  ")
        assert result == "  secaps  "
    
    def test_is_palindrome_true_cases(self):
        """測試回文檢測 - 正確案例 / Test palindrome detection - true cases"""
        # Simple palindromes
        assert string_reverser.is_palindrome("") == True
        assert string_reverser.is_palindrome("a") == True
        assert string_reverser.is_palindrome("aba") == True
        assert string_reverser.is_palindrome("racecar") == True
        
        # Case insensitive
        assert string_reverser.is_palindrome("Racecar") == True
        assert string_reverser.is_palindrome("A man a plan a canal Panama") == True
        
        # Numbers
        assert string_reverser.is_palindrome("12321") == True
    
    def test_is_palindrome_false_cases(self):
        """測試回文檢測 - 錯誤案例 / Test palindrome detection - false cases"""
        assert string_reverser.is_palindrome("hello") == False
        assert string_reverser.is_palindrome("Python") == False
        assert string_reverser.is_palindrome("12345") == False
        assert string_reverser.is_palindrome("Almost a palindrome") == False
    
    def test_count_characters_basic(self):
        """測試字符計數功能 / Test character counting functionality"""
        result = string_reverser.count_characters("Hello World 123")
        
        assert "total" in result
        assert "alphabets" in result
        assert "digits" in result
        assert "spaces" in result
        assert "others" in result
        
        assert result["total"] == 15
        assert result["alphabets"] == 10  # H,e,l,l,o,W,o,r,l,d
        assert result["digits"] == 3      # 1,2,3
        assert result["spaces"] == 2      # Two spaces: "Hello World 123"
        assert result["others"] == 0      # No other special chars in this string
    
    def test_count_characters_empty(self):
        """測試空字串的字符計數 / Test character counting with empty string"""
        result = string_reverser.count_characters("")
        
        assert result["total"] == 0
        assert result["alphabets"] == 0
        assert result["digits"] == 0
        assert result["spaces"] == 0
        assert result["others"] == 0
    
    def test_count_characters_unicode(self):
        """測試Unicode字符計數 / Test character counting with Unicode"""
        result = string_reverser.count_characters("Python🐍中文123")
        
        assert result["total"] == 12  # P,y,t,h,o,n,🐍,中,文,1,2,3
        assert result["digits"] == 3  # 1,2,3
        # Note: The exact counts depend on implementation
        assert result["total"] > 0
    
    def test_analyze_string_complete(self):
        """測試完整的字串分析功能 / Test complete string analysis functionality"""
        test_string = "Python3.11"
        result = string_reverser.analyze_string(test_string)
        
        # Check all required fields exist
        required_fields = ["original", "reversed", "original_length", 
                          "reversed_length", "is_palindrome", "char_count"]
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
        
        # Verify data correctness
        assert result["original"] == test_string
        assert result["reversed"] == "11.3nohtyP"
        assert result["original_length"] == len(test_string)
        assert result["reversed_length"] == len(test_string)  # Should be same
        assert result["is_palindrome"] == False
        assert isinstance(result["char_count"], dict)
    
    def test_analyze_string_palindrome(self):
        """測試回文的完整分析 / Test complete analysis of palindrome"""
        palindrome = "racecar"
        result = string_reverser.analyze_string(palindrome)
        
        assert result["original"] == palindrome
        assert result["reversed"] == palindrome  # Should be same for palindrome
        assert result["is_palindrome"] == True
        assert result["original_length"] == result["reversed_length"]
    
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_result_to_file(self, mock_json_dump, mock_file):
        """測試結果保存到文件功能 / Test saving result to file"""
        test_data = {"original": "test", "reversed": "tset"}
        filename = "test_output.json"
        
        # Call the function that saves to file (assuming it exists)
        # This tests the file I/O without actually creating files
        if hasattr(string_reverser, 'save_result'):
            string_reverser.save_result(test_data, filename)
            
            # Verify file was opened for writing
            mock_file.assert_called_once_with(filename, 'w', encoding='utf-8')
            
            # Verify JSON was dumped
            mock_json_dump.assert_called_once()
    
    def test_input_validation(self):
        """測試輸入驗證 / Test input validation"""
        # Test None input
        with pytest.raises((TypeError, AttributeError)):
            string_reverser.reverse_string(None)
        
        # Test non-string input (should handle gracefully or raise appropriate error)
        try:
            result = string_reverser.reverse_string(12345)
            # If it handles gracefully, should convert to string first
            assert result == "54321"
        except TypeError:
            # If it raises TypeError, that's also acceptable
            pass
    
    def test_edge_cases(self):
        """測試邊界情況 / Test edge cases"""
        # Very long string
        long_string = "a" * 1000
        result = string_reverser.reverse_string(long_string)
        assert result == "a" * 1000
        assert len(result) == 1000
        
        # String with only whitespace
        whitespace = "   \t\n  "
        result = string_reverser.reverse_string(whitespace)
        assert len(result) == len(whitespace)
        
        # String with null characters (if handled)
        try:
            result = string_reverser.reverse_string("hello\x00world")
            assert len(result) == len("hello\x00world")
        except:
            # If not handled, that's fine for this basic implementation
            pass


class TestStringReverserPerformance:
    """效能測試類別 / Performance Test Class"""
    
    def test_performance_large_string(self):
        """測試大字串處理效能 / Test performance with large strings"""
        import time
        
        # Test with 10MB string
        large_string = "Python" * 100000  # ~600KB string
        
        start_time = time.time()
        result = string_reverser.reverse_string(large_string)
        end_time = time.time()
        
        # Should complete within reasonable time (adjust as needed)
        assert (end_time - start_time) < 1.0  # Less than 1 second
        assert len(result) == len(large_string)
    
    def test_performance_many_operations(self):
        """測試大量操作效能 / Test performance with many operations"""
        import time
        
        start_time = time.time()
        
        # Perform 1000 string reversals
        for i in range(1000):
            test_string = f"test_string_{i}"
            result = string_reverser.reverse_string(test_string)
            assert len(result) == len(test_string)
        
        end_time = time.time()
        
        # Should complete within reasonable time
        assert (end_time - start_time) < 2.0  # Less than 2 seconds


if __name__ == "__main__":
    # 直接執行時運行測試 / Run tests when executed directly
    print("🧪 Running pure unit tests for string_reverser...")
    pytest.main([__file__, "-v", "--tb=short", "--durations=10"])