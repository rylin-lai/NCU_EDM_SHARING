#!/usr/bin/env python3
"""
TLSH 文字分析器的 pytest 測試檔案
pytest test file for TLSH Text Analyzer

執行測試 / Run tests:
    pytest test_tlsh_analyzer.py -v
    pytest test_tlsh_analyzer.py::TestTLSHTextAnalyzer::test_calculate_tlsh_hash -v
"""

import pytest
import sys
import os
import json
from unittest.mock import patch

# 添加當前目錄到 Python 路徑 / Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tlsh_text_analyzer import TLSHTextAnalyzer


class TestTLSHTextAnalyzer:
    """TLSH 文字分析器測試類別 / TLSH Text Analyzer Test Class"""
    
    @pytest.fixture
    def analyzer(self):
        """建立測試用的分析器實例 / Create analyzer instance for testing"""
        return TLSHTextAnalyzer()

    def test_calculate_tlsh_hash(self, analyzer):
        """測試 TLSH 雜湊計算 / Test TLSH hash calculation"""
        # 測試正常文字 / Test normal text (make sure it's long enough)
        text = "這是一個測試文字，用來檢驗 TLSH 雜湊功能是否正常運作。此文字包含足夠的字元數量以滿足 TLSH 最小長度要求，並確保有足夠的變化來產生有效的雜湊值。"
        hash_result = analyzer.calculate_tlsh_hash(text)
        
        # 驗證雜湊格式 / Verify hash format
        assert hash_result.startswith("T1"), "TLSH 雜湊應該以 T1 開頭"
        assert len(hash_result) >= 50, "TLSH 雜湊長度應該至少 50 字符"
        
    def test_calculate_tlsh_hash_short_text(self, analyzer):
        """測試短文字的 TLSH 雜湊計算 / Test TLSH hash calculation for short text"""
        short_text = "短文字"  # Text too short for TLSH
        
        with pytest.raises(ValueError, match="文字太短"):
            analyzer.calculate_tlsh_hash(short_text)

    def test_compare_two_texts_identical(self, analyzer):
        """測試相同文字比較 / Test comparison of identical texts"""
        text = "相同的測試文字用來驗證 TLSH 比較功能。" * 3  # Repeat to meet minimum length
        
        result = analyzer.compare_two_texts(text, text)
        
        # 驗證結果結構 / Verify result structure
        assert "case" in result
        assert "distance" in result
        assert "similarity_class" in result
        assert "tlsh_hash1" in result
        assert "tlsh_hash2" in result
        
        # 相同文字距離應為 0 / Distance should be 0 for identical text
        assert result["distance"] == 0
        assert "Identical" in result["similarity_class"]

    def test_compare_two_texts_different(self, analyzer):
        """測試不同文字比較 / Test comparison of different texts"""
        text1 = "第一個測試文字，用來檢驗 TLSH 比較功能是否正常運作。此文字包含足夠的字元數量以滿足 TLSH 最小長度要求，並確保有足夠的變化來產生有效的雜湊值。"
        text2 = "第二個測試文字，用來檢驗 TLSH 比較功能是否正常運作！此文字包含足夠的字元數量以滿足 TLSH 最小長度要求，並確保有足夠的變化來產生有效的雜湊值。"
        
        result = analyzer.compare_two_texts(text1, text2)
        
        # 驗證結果結構 / Verify result structure
        assert "case" in result
        assert "distance" in result
        assert "similarity_class" in result
        assert isinstance(result["distance"], int)
        assert result["distance"] > 0  # Different texts should have distance > 0

    def test_compare_two_texts_short_text_error(self, analyzer):
        """測試短文字比較錯誤處理 / Test short text comparison error handling"""
        short_text = "短"
        normal_text = "正常長度的測試文字，用來測試錯誤處理功能。" * 2
        
        with pytest.raises(ValueError, match="文字太短"):
            analyzer.compare_two_texts(short_text, normal_text)

    def test_run_example(self, analyzer):
        """測試範例執行 / Test example execution"""
        result = analyzer.run_example()
        
        # 驗證結果結構 / Verify result structure
        assert "case" in result
        assert "distance" in result
        assert "similarity_class" in result
        assert isinstance(result["distance"], int)
        assert result["distance"] >= 0

    @patch('sys.argv', ['tlsh_text_analyzer.py', '--example'])
    def test_main_example_mode(self):
        """測試主函數範例模式 / Test main function example mode"""
        from tlsh_text_analyzer import main
        
        # 應該能正常執行 / Should execute normally
        result = main()
        assert result == 0

    @patch('sys.argv', ['tlsh_text_analyzer.py', '--text1', '測試文字一這是一個足夠長的文字用於 TLSH 測試確保滿足最小長度要求' * 2, '--text2', '測試文字二這是另一個足夠長的文字用於 TLSH 測試確保滿足最小長度要求' * 2])
    def test_main_text_comparison_mode(self):
        """測試主函數文字比較模式 / Test main function text comparison mode"""
        from tlsh_text_analyzer import main
        
        # 應該能正常執行 / Should execute normally  
        result = main()
        assert result == 0

    def test_main_invalid_arguments(self):
        """測試主函數無效參數 / Test main function invalid arguments"""
        from tlsh_text_analyzer import main
        
        with patch('sys.argv', ['tlsh_text_analyzer.py']):
            # 沒有參數應該顯示幫助並退出 / No arguments should show help and exit
            result = main()
            assert result == 1  # Error exit code


class TestErrorHandling:
    """錯誤處理測試類別 / Error handling test class"""
    
    def test_empty_text_handling(self):
        """測試空文字處理 / Test empty text handling"""
        analyzer = TLSHTextAnalyzer()
        
        with pytest.raises(ValueError):
            analyzer.calculate_tlsh_hash("")
            
    def test_none_text_handling(self):
        """測試 None 文字處理 / Test None text handling"""
        analyzer = TLSHTextAnalyzer()
        
        with pytest.raises((ValueError, TypeError)):
            analyzer.calculate_tlsh_hash(None)


class TestCommandLineInterface:
    """命令行介面測試類別 / Command line interface test class"""
    
    def test_help_option(self):
        """測試幫助選項 / Test help option"""
        from tlsh_text_analyzer import main
        
        with patch('sys.argv', ['tlsh_text_analyzer.py', '--help']):
            with pytest.raises(SystemExit):
                main()


if __name__ == "__main__":
    # 直接執行時運行測試 / Run tests when executed directly
    pytest.main([__file__, "-v"])