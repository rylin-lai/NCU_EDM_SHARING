# TLSH 分析器 - Golang 版本 / TLSH Analyzer - Golang Version

這是 TLSH 分析器的 Golang 實作版本，提供與 Python 版本相同的功能。  
This is the Golang implementation of TLSH analyzer, providing the same functionality as the Python version.

## 功能特色 / Features

### 案例 1：文字相似性比較 / Case 1: Text Similarity Comparison
- 比較兩個文字字串的 TLSH 距離 / Compare TLSH distance between two text strings
- 適用於企業資料外洩檢測 / Suitable for enterprise data leak detection
- 自動風險等級分類 / Automatic risk level classification

### 案例 2：資料集分群分析 / Case 2: Dataset Clustering Analysis  
- 模擬 DBSCAN 分群演算法 / Simulate DBSCAN clustering algorithm
- 支援 CSV 檔案輸入 / Support CSV file input
- 分群效率統計 / Clustering efficiency statistics

## 建置和執行 / Build and Run

### 建置執行檔 / Build Executable
```bash
# 進入 golang 目錄 / Enter golang directory
cd golang

# 建置 / Build
go build -o tlsh-analyzer main.go

# 或直接執行 / Or run directly
go run main.go
```

### 使用範例 / Usage Examples

#### 案例 1 - 內建範例 / Case 1 - Built-in Example
```bash
./tlsh-analyzer -case=case1 -example -verbose
```

#### 案例 1 - 自訂文字比較 / Case 1 - Custom Text Comparison
```bash
./tlsh-analyzer -case=case1 -text1="第一個文字內容" -text2="第二個文字內容" -verbose
```

#### 案例 2 - 資料集分析 / Case 2 - Dataset Analysis
```bash
./tlsh-analyzer -case=case2 -example -verbose
./tlsh-analyzer -case=case2 -csv="../data/mb_1K.csv" -eps=30 -min_samples=2
```

#### 儲存結果到檔案 / Save Results to File
```bash
./tlsh-analyzer -case=case1 -example -output=results.json
```

### 參數說明 / Parameter Description

| 參數 / Parameter | 說明 / Description |
|------------------|-------------------|
| `-case` | 指定分析案例 (case1 或 case2) / Specify analysis case (case1 or case2) |
| `-verbose` | 啟用詳細輸出 / Enable verbose output |
| `-example` | 使用內建範例 / Use built-in example |
| `-output` | 結果輸出檔案路徑 / Output file path for results |
| `-text1` | 比較的第一個文字 / First text for comparison |
| `-text2` | 比較的第二個文字 / Second text for comparison |
| `-csv` | CSV 檔案路徑 / CSV file path |
| `-eps` | DBSCAN eps 參數 / DBSCAN eps parameter |
| `-min_samples` | DBSCAN min_samples 參數 / DBSCAN min_samples parameter |

## 與 Python 版本的比較 / Comparison with Python Version

### 相同功能 / Same Functionality
✅ 支援兩種分析案例 / Support two analysis cases  
✅ JSON 格式輸出 / JSON format output  
✅ 中英雙語支援 / Chinese and English bilingual support  
✅ 詳細模式和安靜模式 / Verbose and quiet modes  
✅ 檔案輸出功能 / File output functionality  

### 差異 / Differences
- **語言** / **Language**: Golang vs Python
- **依賴** / **Dependencies**: 無外部依賴 vs 需要 TLSH 函式庫 / No external dependencies vs requires TLSH library
- **效能** / **Performance**: 編譯型，較快 vs 解釋型，較慢 / Compiled, faster vs interpreted, slower
- **部署** / **Deployment**: 單一執行檔 vs 需要 Python 環境 / Single executable vs requires Python environment

## 測試 / Testing

### 基本功能測試 / Basic Functionality Test
```bash
# 測試案例 1 / Test Case 1
./tlsh-analyzer -case=case1 -example

# 測試案例 2 / Test Case 2  
./tlsh-analyzer -case=case2 -example

# 測試說明文件 / Test help documentation
./tlsh-analyzer -help
```

### 與 Python 版本比較測試 / Comparison Test with Python Version
```bash
# Python 版本 / Python version
python ../tlsh_analyzer.py case1 --example > python_result.json

# Golang 版本 / Golang version  
./tlsh-analyzer -case=case1 -example > golang_result.json

# 比較結果 / Compare results
diff python_result.json golang_result.json
```

## 注意事項 / Notes

⚠️ **重要** / **Important**: 這是簡化版本的實作，使用模擬的 TLSH 距離計算。  
⚠️ **Important**: This is a simplified implementation using simulated TLSH distance calculation.

在生產環境中使用時，建議：  
For production use, it's recommended to:

1. 整合真正的 TLSH 函式庫 / Integrate real TLSH library
2. 實作真正的 DBSCAN 演算法 / Implement real DBSCAN algorithm  
3. 增加更多的錯誤處理 / Add more error handling
4. 優化效能和記憶體使用 / Optimize performance and memory usage

## 開發計劃 / Development Plan

### 短期目標 / Short-term Goals
- [ ] 整合 Go-TLSH 函式庫 / Integrate Go-TLSH library
- [ ] 實作真正的 CSV 檔案讀取 / Implement real CSV file reading
- [ ] 增加單元測試 / Add unit tests

### 長期目標 / Long-term Goals  
- [ ] 實作完整的 DBSCAN 演算法 / Implement complete DBSCAN algorithm
- [ ] 支援更多檔案格式 / Support more file formats
- [ ] 效能最佳化 / Performance optimization
- [ ] 建置 Docker 映像檔 / Build Docker image