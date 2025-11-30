#!/usr/bin/env python3
"""
TLSH 分析器的 pytest 測試檔案
pytest test file for TLSH Analyzer

執行測試 / Run tests:
    pytest test_tlsh_analyzer.py -v
    pytest test_tlsh_analyzer.py::test_case1_identical_texts -v
    pytest test_tlsh_analyzer.py::TestTLSHAnalyzer::test_case2_invalid_csv -v
"""

import pytest
import sys
import os
import json
import tempfile
from unittest.mock import patch, mock_open

# 添加當前目錄到 Python 路徑 / Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tlsh_analyzer import TLSHAnalyzer


class TestTLSHAnalyzer:
    """TLSH 分析器測試類別 / TLSH Analyzer Test Class"""
    
    @pytest.fixture
    def analyzer(self):
        """建立測試用的分析器實例 / Create analyzer instance for testing"""
        return TLSHAnalyzer()
    
    @pytest.fixture
    def sample_texts(self):
        """測試用的範例文字 / Sample texts for testing"""
        return {
            "identical": "這是一個測試文字，用於檢驗 TLSH 的功能。" * 5,  # 相同文字 / Identical text
            "similar": "這是一個測試文字，用於檢驗 TLSH 的功能！" * 5,    # 相似文字 / Similar text  
            "different": "完全不同的文字內容，用來測試 TLSH 距離計算。" * 5  # 不同文字 / Different text
        }
    
    def test_calculate_tlsh_hash_success(self, analyzer, sample_texts):
        """測試成功計算 TLSH 雜湊 / Test successful TLSH hash calculation"""
        text = sample_texts["identical"]
        hash_result = analyzer.calculate_tlsh_hash(text)
        
        # 驗證 TLSH 雜湊格式 / Verify TLSH hash format
        assert isinstance(hash_result, str), "TLSH 雜湊應該是字串型別 / TLSH hash should be string type"
        assert len(hash_result) in [70, 72], "TLSH 雜湊長度應該是 70 或 72 字元 / TLSH hash length should be 70 or 72 characters"
    
    def test_calculate_tlsh_hash_too_short(self, analyzer):
        """測試文字太短時的錯誤處理 / Test error handling for text too short"""
        short_text = "太短"  # Too short
        
        with pytest.raises(ValueError, match="文字太短"):
            analyzer.calculate_tlsh_hash(short_text)
    
    def test_case1_identical_texts(self, analyzer, sample_texts):
        """測試案例 1：相同文字比較 / Test Case 1: Identical texts comparison"""
        text1 = sample_texts["identical"]
        text2 = sample_texts["identical"]
        
        result = analyzer.compare_two_texts(text1, text2)
        
        # 驗證結果結構 / Verify result structure
        assert result["case"] == "two_text_comparison", "案例類型應該正確 / Case type should be correct"
        assert result["distance"] == 0, "相同文字的距離應該是 0 / Distance for identical texts should be 0"
        assert "完全相同" in result["similarity_class"], "應該被分類為完全相同 / Should be classified as identical"
        assert "無風險" in result["risk_level"], "風險等級應該是無風險 / Risk level should be none"
    
    def test_case1_similar_texts(self, analyzer, sample_texts):
        """測試案例 1：相似文字比較 / Test Case 1: Similar texts comparison"""
        text1 = sample_texts["identical"]
        text2 = sample_texts["similar"]
        
        result = analyzer.compare_two_texts(text1, text2)
        
        # 驗證相似性檢測 / Verify similarity detection
        assert result["case"] == "two_text_comparison", "案例類型應該正確 / Case type should be correct"
        assert result["distance"] > 0, "不同文字的距離應該大於 0 / Distance for different texts should be > 0"
        assert result["distance"] < 100, "相似文字的距離應該相對較小 / Distance for similar texts should be relatively small"
        assert "interpretation" in result, "應該包含解釋 / Should contain interpretation"
    
    def test_case1_different_texts(self, analyzer, sample_texts):
        """測試案例 1：不同文字比較 / Test Case 1: Different texts comparison"""
        text1 = sample_texts["identical"]
        text2 = sample_texts["different"]
        
        result = analyzer.compare_two_texts(text1, text2)
        
        # 驗證差異檢測 / Verify difference detection
        assert result["case"] == "two_text_comparison", "案例類型應該正確 / Case type should be correct"
        assert result["distance"] > 100, "不同文字的距離應該較大 / Distance for different texts should be larger"
        assert "不同" in result["similarity_class"], "應該被分類為不同 / Should be classified as different"
    
    @patch('os.path.exists')
    def test_case2_csv_not_found(self, mock_exists, analyzer):
        """測試案例 2：CSV 檔案不存在 / Test Case 2: CSV file not found"""
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError, match="找不到 CSV 檔案"):
            analyzer.analyze_file_dataset("nonexistent.csv")
    
    @patch('tlsh_analyzer.tlsh_csvfile')
    @patch('os.path.exists')
    def test_case2_invalid_csv_data(self, mock_exists, mock_csvfile, analyzer):
        """測試案例 2：無效的 CSV 資料 / Test Case 2: Invalid CSV data"""
        mock_exists.return_value = True
        mock_csvfile.return_value = (None, None)  # 模擬載入失敗 / Simulate load failure
        
        with pytest.raises(ValueError, match="無法從 CSV 載入 TLSH 資料"):
            analyzer.analyze_file_dataset("test.csv")
    
    @patch('tlsh_analyzer.runDBSCAN')
    @patch('tlsh_analyzer.tlsh_csvfile')
    @patch('os.path.exists')
    def test_case2_successful_clustering(self, mock_exists, mock_csvfile, mock_dbscan, analyzer):
        """測試案例 2：成功的分群分析 / Test Case 2: Successful clustering analysis"""
        # 設定模擬資料 / Setup mock data
        mock_exists.return_value = True
        
        # 模擬 TLSH 資料 / Mock TLSH data
        mock_tlist = [
            "T125100322A5A40B05159F2A11A885A9D4E1EEB4E07F5488E5E5A5E1EA2EAE48E5E6A8E6A5E4A",
            "T125100322A5A40B05159F2A11A885A9D4E1EEB4E07F5488E5E5A5E1EA2EAE48E5E6A8E6A5E4B"
        ]
        mock_labels = [["family1", "family2"], [], []]
        mock_csvfile.return_value = (mock_tlist, mock_labels)
        
        # 模擬 DBSCAN 結果 / Mock DBSCAN results
        class MockDBSCANResult:
            labels_ = [0, 1]  # 兩個不同的群集 / Two different clusters
        
        mock_dbscan.return_value = MockDBSCANResult()
        
        # 執行測試 / Execute test
        result = analyzer.analyze_file_dataset("test.csv", eps=30, min_samples=2)
        
        # 驗證結果 / Verify results
        assert result["case"] == "dataset_clustering", "案例類型應該正確 / Case type should be correct"
        assert result["total_samples"] == 2, "樣本總數應該正確 / Total samples should be correct"
        assert result["results"]["n_clusters"] == 2, "群集數量應該正確 / Number of clusters should be correct"
        assert result["results"]["n_noise"] == 0, "雜訊點數量應該正確 / Number of noise points should be correct"
        assert "summary" in result, "應該包含摘要 / Should contain summary"
    
    def test_run_case_1_example(self, analyzer):
        """測試案例 1 的範例執行 / Test Case 1 example execution"""
        result = analyzer.run_case_1_example()
        
        # 驗證範例結果 / Verify example results
        assert result["case"] == "two_text_comparison", "應該是文字比較案例 / Should be text comparison case"
        assert "distance" in result, "應該包含距離 / Should contain distance"
        assert "similarity_class" in result, "應該包含相似性分類 / Should contain similarity class"
        assert "interpretation" in result, "應該包含中英文解釋 / Should contain Chinese and English interpretation"
    
    @patch('os.path.exists')
    def test_run_case_2_example_file_not_found(self, mock_exists, analyzer):
        """測試案例 2 的範例執行（檔案不存在）/ Test Case 2 example execution (file not found)"""
        mock_exists.return_value = False
        
        result = analyzer.run_case_2_example()
        
        # 驗證錯誤處理 / Verify error handling
        assert result["case"] == "dataset_clustering", "應該是資料集分群案例 / Should be dataset clustering case"
        assert "error" in result, "應該包含錯誤訊息 / Should contain error message"
        assert "zh" in result["error"], "應該包含中文錯誤訊息 / Should contain Chinese error message"
        assert "en" in result["error"], "應該包含英文錯誤訊息 / Should contain English error message"
    
    def test_verbose_mode(self, analyzer, sample_texts, capsys):
        """測試詳細模式輸出 / Test verbose mode output"""
        analyzer.verbose = True
        
        # 執行案例 1 / Execute Case 1
        analyzer.compare_two_texts(sample_texts["identical"], sample_texts["similar"])
        
        # 檢查是否有詳細輸出 / Check for verbose output
        captured = capsys.readouterr()
        assert "案例 1" in captured.out or "Case 1" in captured.out, "應該有詳細輸出 / Should have verbose output"


class TestMainFunction:
    """主要函數測試類別 / Main function test class"""
    
    @patch('sys.argv', ['tlsh_analyzer.py', 'case1', '--example'])
    @patch('tlsh_analyzer.TLSHAnalyzer')
    def test_main_case1_example(self, mock_analyzer_class):
        """測試主函數案例 1 範例 / Test main function Case 1 example"""
        from tlsh_analyzer import main
        
        # 設定模擬 / Setup mock
        mock_analyzer = mock_analyzer_class.return_value
        mock_analyzer.run_case_1_example.return_value = {"case": "two_text_comparison", "distance": 0}
        
        # 執行主函數 / Execute main function
        result = main()
        
        # 驗證 / Verify
        assert result == 0, "主函數應該回傳 0 表示成功 / Main function should return 0 for success"
        mock_analyzer.run_case_1_example.assert_called_once()
    
    @patch('sys.argv', ['tlsh_analyzer.py', 'case1'])
    def test_main_case1_missing_arguments(self, capsys):
        """測試主函數案例 1 缺少參數 / Test main function Case 1 missing arguments"""
        from tlsh_analyzer import main
        
        result = main()
        
        # 驗證錯誤處理 / Verify error handling
        assert result == 1, "應該回傳 1 表示錯誤 / Should return 1 for error"
        captured = capsys.readouterr()
        assert "錯誤" in captured.out or "Error" in captured.out, "應該顯示錯誤訊息 / Should show error message"


class TestIntegration:
    """整合測試類別 / Integration test class"""
    
    def test_json_output_encoding(self, tmp_path):
        """測試 JSON 輸出的中文編碼 / Test Chinese encoding in JSON output"""
        analyzer = TLSHAnalyzer()
        
        # 使用包含中文的測試資料 / Use test data containing Chinese
        text1 = "這是一個包含中文的測試文字，用於驗證編碼是否正確。" * 3
        text2 = "這是一個包含中文的測試文字，用於驗證編碼是否正確！" * 3
        
        result = analyzer.compare_two_texts(text1, text2)
        
        # 寫入臨時檔案 / Write to temporary file
        output_file = tmp_path / "test_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # 讀回並驗證中文字元 / Read back and verify Chinese characters
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "相似" in content, "應該正確保存中文字元 / Should correctly save Chinese characters"
            
        # 驗證 JSON 格式有效 / Verify JSON format is valid
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded_result = json.load(f)
            assert loaded_result["case"] == "two_text_comparison", "JSON 應該可以正確載入 / JSON should load correctly"


# pytest 執行配置 / pytest execution configuration
if __name__ == "__main__":
    import pytest
    
    print("執行 TLSH 分析器測試 / Running TLSH Analyzer Tests")
    print("=" * 50)
    
    # 執行所有測試 / Run all tests
    pytest.main([__file__, "-v", "--tb=short"])