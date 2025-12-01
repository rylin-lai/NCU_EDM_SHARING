# 🐍 Python Workshop - NCU Sharing Session
**2025/12/03 中央大學 Python 工作坊分享**

## 📋 專案概覽 / Project Overview

這個repository展示了Python在日常開發中的多種應用，包括自動化ML分析、跨語言測試、以及CI/CD整合。

This repository demonstrates various Python applications in daily development, including automated ML analysis, cross-language testing, and CI/CD integration.

---

## 🗂️ 專案結構 / Project Structure

```
workshop_materials/
├── 🤖 auto_ml_demo/           # 自動化機器學習展示
│   ├── educational_dataset_generator.py
│   ├── ml_report_generator.py
│   ├── create_pages_structure.py
│   └── requirements.txt
│
├── 🔍 TLSH 相似度分析 / TLSH Similarity Analysis
│   ├── pylib/tlsh_analyzer.py    # TLSH 主要分析工具
│   ├── pylib/tlsh_lib.py         # TLSH 核心函式庫
│   ├── pylib/hac_lib.py          # 階層式分群函式庫
│   ├── tlsh_basic_tutorial.ipynb # TLSH 基礎教學
│   ├── tlsh_db_scan.ipynb        # DBSCAN 分群教學
│   └── data/                     # 測試資料集
│       ├── malicious_phish.csv
│       ├── mb_10K.csv
│       └── mb_1K.csv
│
├── 🧪 跨語言開發展示 / Cross-Language Development
│   ├── string_reverser.py         # Python版本字串反轉器
│   ├── test_string_reverser.py    # 整合測試檔案
│   ├── test_string_reverser_unit.py # 單元測試檔案
│   └── golang/main.go             # Golang版本實作
│
├── 🔄 GitHub Actions CI/CD
│   └── .github/workflows/        # 自動化部署設定
│
└── 📊 Jupyter Notebooks
    ├── tlsh_basic_tutorial.ipynb  # TLSH基礎教學
    └── tlsh_db_scan.ipynb         # DBSCAN分群實作
```

---

## 🚀 功能展示 / Features

### 1. 🔍 TLSH 相似度分析系統

**TLSH (Trend Locality Sensitive Hashing)** - 企業級資料外洩檢測和文件相似度分析

#### 核心功能:
- **文件相似度比較**: 檢測資料外洩或重複文件
- **DBSCAN 分群分析**: 自動發現相似文件群集
- **惡意軟體檢測**: 基於行為模式的檢測
- **大規模資料處理**: 支援10K+文件的高效分析

#### 🔧 使用方式:
```bash
# 比較兩個文件的相似度
python pylib/tlsh_analyzer.py --case1 --text1 "原始文件內容" --text2 "可能洩漏的文件"

# 對資料集進行DBSCAN分群
python pylib/tlsh_analyzer.py --case2 --csv data/malicious_phish.csv --eps 50

# 互動式教學 (推薦!)
jupyter notebook tlsh_basic_tutorial.ipynb
```

### 2. 🧪 跨語言開發工作流程

展示現代軟體開發的完整流程：**Python POC → Golang Production → Python Testing**

#### 🐍 Python 原型開發:
- **`string_reverser.py`**: 快速原型實作
- 完整功能驗證和API設計
- JSON輸出格式定義

#### 🚀 Golang 生產版本:
- **`golang/main.go`**: 高效能生產實作
- 相同的API和輸出格式
- 適合高並發環境

#### 🧪 自動化測試策略:
- **Unit Tests** (`test_string_reverser_unit.py`): 純Python模組測試（快速、隔離）
- **Integration Tests** (`test_string_reverser.py`): Python與Golang跨語言一致性測試
- 測試覆蓋率報告和效能測試

### 3. 🤖 自動化ML分析系統

#### 🔄 自動分析 (推送觸發)
每當推送到分支時，會自動：
- 生成教育資料集
- 執行多模型ML分析 (Logistic Regression, Random Forest, KNN, SVM)
- 產生完整的HTML分析報告
- 部署到GitHub Pages

**🔗 查看即時報告**:
- **主頁面**: https://rylin-lai.github.io/NCU_EDM_SHARING/
- **分支報告**: https://rylin-lai.github.io/NCU_EDM_SHARING/branch-{分支名稱}/

#### 🎯 手動分析 (自定義參數)
透過GitHub Actions手動觸發：
- **自選分析分支**: 指定要分析的branch
- **自定義資料集大小**: 100-2000學生數據
- **可選目標變數**: Pass_course, Final_grade, Engagement_level
- **個人化報告**: 下載完整的HTML分析包
- **離線查看**: 獨立的HTML報告，可在任何地方開啟

**🚀 如何使用手動分析**:
1. 前往 **Actions** → **Manual ML Analysis**
2. 點擊 **Run workflow**
3. 選擇參數 (分支、資料集大小、目標變數等)
4. 等待分析完成
5. 下載 artifact 中的 ZIP 檔案
6. 解壓縮並開啟 `index.html`

### 4. 🔄 CI/CD自動化流程

- 每次推送自動觸發分析
- 多分支獨立部署
- 測試自動化執行
- 報告自動生成與部署

---

## 🛠️ 使用指南 / Usage Guide

### 快速開始 / Quick Start

1. **Clone專案**:
   ```bash
   git clone https://github.com/rylin-lai/NCU_EDM_SHARING.git
   cd NCU_EDM_SHARING
   ```

2. **安裝依賴**:
   ```bash
   # Python 依賴
   pip install -r auto_ml_demo/requirements.txt
   pip install tlsh pandas numpy scikit-learn matplotlib seaborn jupyter
   
   # Golang 依賴 (可選)
   cd golang && go mod tidy
   ```

### 🔍 TLSH 相似度分析

#### 情境1: 資料外洩檢測
```bash
# 比較兩個文件是否相似 (適用於資料外洩調查)
python pylib/tlsh_analyzer.py --case1 \
  --text1 "這是原始的機密文件內容..." \
  --text2 "這是可能洩漏的文件內容..."

# 從檔案比較
python pylib/tlsh_analyzer.py --case1 \
  --file1 data/original.txt \
  --file2 data/suspicious.txt
```

#### 情境2: 惡意軟體分群分析
```bash
# 對惡意軟體資料集進行DBSCAN分群
python pylib/tlsh_analyzer.py --case2 \
  --csv data/malicious_phish.csv \
  --eps 50 --min_samples 3

# 使用較小的資料集測試
python pylib/tlsh_analyzer.py --case2 \
  --csv data/mb_1K.csv \
  --eps 30 --min_samples 2
```

#### 📚 互動式教學
```bash
# 啟動 Jupyter 教學筆記本
jupyter notebook tlsh_basic_tutorial.ipynb

# DBSCAN 分群教學
jupyter notebook tlsh_db_scan.ipynb
```

### 🧪 跨語言開發測試

#### String Reverser 範例
```bash
# Python 版本
python string_reverser.py --text "Hello World" --example

# 建置 Golang 版本
cd golang
go build -o string-reverser
./string-reverser -text "Hello World" -example

# 執行跨語言測試
pytest test_string_reverser.py -v
pytest test_string_reverser_unit.py -v --cov=string_reverser
```

### 🤖 自動化ML分析

#### 本地執行
```bash
cd auto_ml_demo

# 生成教育資料集
python educational_dataset_generator.py --students 300 --output data/

# 執行ML分析
python ml_report_generator.py --data data/educational_data_2024_Fall.csv --output reports/
```

#### 🎯 GitHub Actions 手動分析
1. **前往 Actions 頁面**: https://github.com/rylin-lai/NCU_EDM_SHARING/actions
2. **選擇 "Manual ML Analysis"** workflow
3. **點擊 "Run workflow"** 並設定參數：
   - 目標分支 (如: `main`, `student-yourname`)
   - 資料集大小 (100-2000)
   - 學期識別 (如: `2024_Fall`)
   - 目標變數 (`Pass_course`, `Final_grade`, 等)
   - 分析名稱 (自定義)
4. **等待完成** (約3-5分鐘)
5. **下載結果**: 在 Artifacts 中下載 ZIP 檔案
6. **離線查看**: 解壓縮後開啟 `index.html`

**適用情境**:
- 🎓 學生想要自己的個人化分析
- 📊 教師需要不同參數的比較分析  
- 💼 展示給其他人的獨立報告
- 📱 離線環境下的報告查看

---

## 🧪 Testing 指南 / Testing Guide

我們的測試系統展示了完整的測試金字塔架構：

### 1. 🏃‍♂️ Unit Tests (單元測試)
**檔案**: `test_string_reverser_unit.py`
**特性**: 快速、隔離、只測試Python模組本身

```bash
# 執行純Unit Tests
pytest test_string_reverser_unit.py -v

# 產生覆蓋率報告
pytest test_string_reverser_unit.py --cov=string_reverser --cov-report=html

# 效能測試
pytest test_string_reverser_unit.py::TestStringReverserPerformance -v
```

**測試內容**:
- ✅ 字串反轉功能
- ✅ 回文檢測
- ✅ 字符統計
- ✅ 邊界條件 (空字串、單字符、Unicode)
- ✅ 效能測試
- ✅ 輸入驗證

### 2. 🔗 Integration Tests (整合測試)
**檔案**: `test_string_reverser.py`  
**特性**: 測試Python與Golang系統整合

#### 🐍 Python + 🚀 Golang 跨語言整合測試

**前置準備 / Prerequisites:**
```bash
# 1. 安裝pytest
pip install pytest

# 2. 建置Golang版本 (如果要測試跨語言功能)
cd golang
go build -o string-reverser
cd ..
```

**執行測試 / Run Tests:**

```bash
# 執行完整測試套件
pytest test_string_reverser.py -v

# 執行特定測試
pytest test_string_reverser.py::TestStringReverser::test_both_implementations_example -v

# 產生詳細報告
pytest test_string_reverser.py -v --tb=long

# 只測試Python版本 (如果沒有Golang)
python test_string_reverser.py
```

**整合測試涵蓋範圍 / Integration Test Coverage:**

✅ **跨語言一致性**
- Python與Golang結果比對
- 內建範例文字測試
- 自訂文字反轉測試
- JSON輸出格式一致性

✅ **系統整合**
- 外部程序調用
- 文件I/O操作
- 錯誤處理機制
- 環境依賴檢查

### 🎯 測試策略總結

| 測試類型 | 執行速度 | 依賴性 | 覆蓋範圍 | 使用時機 |
|---------|---------|--------|---------|---------|
| **Unit Tests** | ⚡ 快速 | 🚫 無依賴 | 📝 單一模組 | 開發過程中 |
| **Integration Tests** | 🐌 較慢 | ⚠️ 外部依賴 | 🔗 系統整合 | 部署前驗證 |

**測試輸出範例 / Sample Output:**
```
🧪 Running string reverser cross-platform tests...
test_string_reverser.py::TestStringReverser::test_both_implementations_example PASSED
test_string_reverser.py::TestStringReverser::test_both_implementations_custom_text PASSED
test_string_reverser.py::TestStringReverser::test_both_implementations_palindrome PASSED
test_string_reverser.py::TestStringReverser::test_both_implementations_empty_string PASSED

🐍 Python result: '!dlroW ,olleH'
🚀 Golang result: '!dlroW ,olleH'
✅ Both implementations produced identical results
```

---

## 🎯 教學重點 / Learning Points

### 1. **資訊安全與TLSH應用**
- 雜湊演算法在資安的應用 (TLSH vs MD5/SHA)
- 資料外洩檢測實務
- 惡意軟體分析與分群
- 大規模文件相似度計算
- DBSCAN無監督學習在資安的應用

### 2. **跨語言開發策略**
- Python原型開發 (快速驗證想法)
- Golang生產環境部署 (高效能需求)
- API一致性設計
- 跨語言測試自動化

### 3. **Python 全端自動化技能**
- 資料科學工作流程 (pandas, scikit-learn, matplotlib)
- 網路安全工具開發 (TLSH, 檔案分析)
- 自動化腳本與報告生成
- JSON資料處理與API設計

### 4. **現代測試策略**
- pytest框架專業使用
- 測試金字塔 (Unit → Integration → E2E)
- 跨語言測試策略
- 測試覆蓋率與效能測試
- CI/CD中的測試自動化

### 5. **DevOps 與自動化**
- GitHub Actions進階應用
- 多分支CI/CD pipeline
- 自動化部署與報告生成
- 測試結果可視化

### 6. **軟體工程最佳實務**
- 模組化程式設計
- 跨平台相容性
- 技術文檔撰寫
- 版本控制與協作開發

---

## 🤝 貢獻 / Contributing

歡迎學生fork此專案並創建自己的分析分支！每個分支都會自動產生獨立的分析報告。

Students are welcome to fork this project and create their own analysis branches! Each branch will automatically generate an independent analysis report.

### 建立自己的分析 / Create Your Own Analysis

1. Fork這個repository
2. 創建新分支: `git checkout -b student-{你的名字}`
3. 修改 `auto_ml_demo/` 中的參數
4. 推送分支: `git push origin student-{你的名字}`
5. 查看你的專屬報告: `https://{你的用戶名}.github.io/NCU_EDM_SHARING/branch-student-{你的名字}/`

---

## 📚 相關資源 / Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [pytest Documentation](https://docs.pytest.org/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Go Testing Package](https://golang.org/pkg/testing/)

---

## 📞 聯絡 / Contact

**Workshop Date**: 2025/12/03  
**Location**: 中央大學 (NCU)  
**Topic**: Python在軟體工程師日常工作中的應用

---

*🎓 這個專案展示了Python在現代軟體開發中的實際應用，從資料科學到自動化測試，從CI/CD到跨語言整合。*