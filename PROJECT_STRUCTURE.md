# TLSH Workshop Materials / TLSH 工作坊材料

這個目錄包含完整的 TLSH 工作坊材料，專注於文字相似性分析，包括 Python 文字分析工具、pytest 測試、Jupyter notebook 和 Golang binary。  
This directory contains complete TLSH workshop materials focusing on text similarity analysis, including Python text analysis tools, pytest tests, Jupyter notebooks, and Golang binary.

## 資料夾結構 / Directory Structure

```
workshop_materials/
├── PROJECT_STRUCTURE.md               # 專案結構說明 / Project structure documentation
├── tlsh_text_analyzer.py              # Python 文字分析器 (只支援文字比較) / Python text analyzer (text comparison only)
├── test_tlsh_analyzer.py              # pytest 測試套件 / pytest test suite
├── tlsh_basic_tutorial.ipynb          # TLSH 基礎教學 notebook / Basic TLSH tutorial notebook
├── tlsh_db_scan.ipynb                 # TLSH DBSCAN 分群 notebook / TLSH DBSCAN clustering notebook  
├── tlsh_testing_workshop.ipynb        # 新的測試工作坊 notebook / New testing workshop notebook
├── data/                              # 測試資料 / Test data
│   ├── mb_1K.csv                      # 1K 惡意軟體樣本 / 1K malware samples
│   └── mb_10K.csv                     # 10K 惡意軟體樣本 / 10K malware samples
├── pylib/                             # Python 函式庫 (包含完整功能) / Python libraries (complete functionality)
│   ├── tlsh_analyzer.py               # 完整版 TLSH 分析器 / Full TLSH analyzer with clustering
│   ├── tlsh_lib.py                    # TLSH 核心函式庫 / TLSH core library
│   ├── hac_lib.py                     # 分層聚類函式庫 / Hierarchical clustering library
│   ├── printCluster.py                # 群集輸出函式庫 / Cluster output library
│   └── myheap.py                      # 堆積資料結構 / Heap data structure
└── golang/                            # Golang 版本 (只支援文字比較) / Golang version (text comparison only)
    ├── main.go                        # Golang 主程式 / Golang main program
    ├── go.mod                         # Go 模組檔案 / Go module file
    ├── README.md                      # Golang 版本說明 / Golang version documentation
    └── tlsh-text-analyzer-linux       # 編譯好的 Linux binary / Compiled Linux binary (2.8MB)
```

## 檔案說明 / File Description

### 核心程式檔案 / Core Program Files

#### `tlsh_text_analyzer.py` - Python 文字分析器 (簡化版)
- **功能** / **Function**: 專注於文字相似性比較的 Python 實作
- **使用方式** / **Usage**: `python tlsh_text_analyzer.py --text1="..." --text2="..." [options]`
- **特色** / **Features**: 中英雙語、JSON 輸出、簡潔的企業資料外洩檢測

#### `pylib/tlsh_analyzer.py` - Python 完整版分析器
- **功能** / **Function**: 包含完整功能的 Python 實作，支援 DBSCAN 分群
- **使用方式** / **Usage**: 需要完整的 pylib 環境和相關依賴
- **特色** / **Features**: 完整的 TLSH 功能、分群分析、資料集處理

#### `golang/main.go` - Golang 文字分析器  
- **功能** / **Function**: Golang 實作版本，專注於文字比較
- **建置** / **Build**: `GOOS=linux GOARCH=amd64 go build -o tlsh-text-analyzer-linux main.go`
- **特色** / **Features**: 單一執行檔、靜態連結、無外部依賴

#### `golang/tlsh-text-analyzer-linux` - 編譯好的 Linux Binary
- **檔案大小** / **File Size**: 2.8MB
- **目標平台** / **Target Platform**: x86_64 Ubuntu 20+
- **使用方式** / **Usage**: `./tlsh-text-analyzer-linux -text1="..." -text2="..." [options]`

### 測試檔案 / Test Files

#### `test_tlsh_analyzer.py` - pytest 測試套件
- **測試範圍** / **Test Coverage**: 
  - 基本 TLSH 功能測試 / Basic TLSH functionality tests
  - 邊界條件測試 / Edge case tests  
  - 錯誤處理測試 / Error handling tests
  - 中文編碼測試 / Chinese encoding tests
- **執行方式** / **Execution**: `pytest test_tlsh_analyzer.py -v`

### Jupyter Notebooks

#### `tlsh_basic_tutorial.ipynb` - TLSH 基礎教學
- **內容** / **Content**: TLSH 基本概念、距離計算、企業應用案例
- **目標** / **Target**: TLSH 初學者、理解相似性雜湊概念

#### `tlsh_db_scan.ipynb` - TLSH DBSCAN 分群 
- **內容** / **Content**: 大規模資料集分群、DBSCAN 參數調整、結果視覺化
- **目標** / **Target**: 資料科學家、惡意軟體分析師

#### `tlsh_testing_workshop.ipynb` - 測試工作坊
- **內容** / **Content**: 
  - 企業資料外洩檢測演示 / Enterprise data leak detection demo
  - 大規模分群分析 / Large-scale clustering analysis  
  - Python 工具測試 / Python tool testing
  - 指令列工具示範 / Command line tool demonstration
- **目標** / **Target**: 工作坊參與者、實際應用案例

### 資料檔案 / Data Files

#### `data/mb_1K.csv` - 1K 惡意軟體樣本
- **大小** / **Size**: 999 個樣本 / 999 samples
- **用途** / **Purpose**: 小規模測試、快速驗證
- **來源** / **Source**: Malware Bazaar 資料集

#### `data/mb_10K.csv` - 10K 惡意軟體樣本  
- **大小** / **Size**: ~10K 樣本 / ~10K samples
- **用途** / **Purpose**: 大規模效能測試、完整分群分析

### 函式庫檔案 / Library Files

#### `pylib/tlsh_lib.py` - TLSH 核心函式庫
- **功能** / **Functions**: 
  - CSV 檔案讀取 / CSV file reading
  - TLSH 距離計算 / TLSH distance calculation
  - DBSCAN 分群執行 / DBSCAN clustering execution

#### `pylib/hac_lib.py` - 分層聚類函式庫
- **功能** / **Functions**: Hierarchical Agglomerative Clustering (HAC-T)

#### `pylib/printCluster.py` - 群集輸出函式庫  
- **功能** / **Functions**: 分群結果格式化輸出

## 快速開始指南 / Quick Start Guide

### 1. Python 版本測試 / Python Version Testing
```bash
# 基本功能測試 / Basic functionality test
python tlsh_analyzer.py case1 --example --verbose

# 執行完整測試套件 / Run complete test suite  
pytest test_tlsh_analyzer.py -v

# Jupyter 互動式教學 / Jupyter interactive tutorial
jupyter notebook tlsh_testing_workshop.ipynb
```

### 2. Golang 版本測試 / Golang Version Testing
```bash
# 進入 golang 目錄 / Enter golang directory
cd golang

# 測試 Linux binary / Test Linux binary
./tlsh-analyzer-linux -case=case1 -example -verbose
./tlsh-analyzer-linux -case=case2 -example -verbose

# 重新建置 (如需要) / Rebuild (if needed)
GOOS=linux GOARCH=amd64 go build -o tlsh-analyzer-linux main.go
```

### 3. 跨語言驗證 / Cross-language Validation  
```bash
# Python 版本結果 / Python version result
python tlsh_analyzer.py case1 --example > python_result.json

# Golang 版本結果 / Golang version result  
./golang/tlsh-analyzer-linux -case=case1 -example > golang_result.json

# 比較結果 / Compare results
diff python_result.json golang_result.json
```

## 使用案例對應 / Use Case Mapping

### 案例 1: 企業資料外洩檢測 / Case 1: Enterprise Data Leak Detection

| 場景 / Scenario | Python 指令 / Python Command | Golang 指令 / Golang Command |
|-----------------|------------------------------|------------------------------|
| 內建範例 / Built-in Example | `python tlsh_analyzer.py case1 --example` | `./tlsh-analyzer-linux -case=case1 -example` |
| 自訂文字 / Custom Text | `python tlsh_analyzer.py case1 --text1 "..." --text2 "..."` | `./tlsh-analyzer-linux -case=case1 -text1="..." -text2="..."` |
| 儲存結果 / Save Results | `python tlsh_analyzer.py case1 --example --output result.json` | `./tlsh-analyzer-linux -case=case1 -example -output=result.json` |

### 案例 2: 資料集分群分析 / Case 2: Dataset Clustering Analysis

| 場景 / Scenario | Python 指令 / Python Command | Golang 指令 / Golang Command |
|-----------------|------------------------------|------------------------------|
| 內建範例 / Built-in Example | `python tlsh_analyzer.py case2 --example` | `./tlsh-analyzer-linux -case=case2 -example` |
| 自訂資料集 / Custom Dataset | `python tlsh_analyzer.py case2 --csv data/mb_1K.csv` | `./tlsh-analyzer-linux -case=case2 -csv=../data/mb_1K.csv` |
| 調整參數 / Adjust Parameters | `python tlsh_analyzer.py case2 --csv data/mb_1K.csv --eps 25 --min_samples 3` | `./tlsh-analyzer-linux -case=case2 -csv=../data/mb_1K.csv -eps=25 -min_samples=3` |

## 開發資訊 / Development Information

### 技術規格 / Technical Specifications
- **Python 版本** / **Python Version**: 3.7+
- **Golang 版本** / **Golang Version**: 1.19+  
- **支援平台** / **Supported Platforms**: Linux, macOS, Windows
- **輸出格式** / **Output Format**: JSON, Console

### 效能基準 / Performance Benchmarks
- **Python 版本啟動時間** / **Python Startup Time**: ~200ms
- **Golang 版本啟動時間** / **Golang Startup Time**: ~5ms
- **記憶體使用** / **Memory Usage**: Python ~50MB, Golang ~10MB
- **檔案大小** / **File Size**: Python script ~15KB, Golang binary ~3MB

### 已知限制 / Known Limitations
- Golang 版本使用簡化的 TLSH 距離計算 / Golang version uses simplified TLSH distance calculation
- 大型資料集 (>10K) 可能需要較長處理時間 / Large datasets (>10K) may require longer processing time  
- 部分進階 DBSCAN 功能僅在 Python 版本中可用 / Some advanced DBSCAN features only available in Python version

---

**建立日期 / Created**: 2024-11-30  
**最後更新 / Last Updated**: 2024-11-30  
**版本 / Version**: 1.0.0