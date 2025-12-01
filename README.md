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
├── 🧪 跨語言測試展示 / Cross-Language Testing
│   ├── string_reverser.py    # Python版本字串反轉器
│   ├── test_string_reverser.py # pytest測試檔案
│   └── golang/               # Golang版本實作
│
├── 🔄 GitHub Actions CI/CD
│   └── .github/workflows/    # 自動化部署設定
│
└── 📊 資料分析相關
    └── data/                 # 測試資料集
```

---

## 🚀 功能展示 / Features

### 1. 🤖 自動化ML分析系統

每當推送到分支時，會自動：
- 生成教育資料集
- 執行多模型ML分析 (Logistic Regression, Random Forest, KNN, SVM)
- 產生完整的HTML分析報告
- 部署到GitHub Pages

#### 🔗 查看即時報告 / View Live Reports:
- **主頁面**: https://rylin-lai.github.io/NCU_EDM_SHARING/
- **分支報告**: https://rylin-lai.github.io/NCU_EDM_SHARING/branch-{分支名稱}/

### 2. 🧪 自動化測試展示

展示完整的測試策略，包括：
- **Unit Tests**: 純Python模組測試（快速、隔離）
- **Integration Tests**: Python與Golang跨語言測試
- 測試資料一致性檢查
- 邊界條件與效能測試
- 專業的測試結構設計

### 3. 🔄 CI/CD自動化流程

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

2. **安裝Python依賴**:
   ```bash
   cd auto_ml_demo
   pip install -r requirements.txt
   ```

3. **手動執行ML分析**:
   ```bash
   # 生成資料集
   python educational_dataset_generator.py --students 300 --output data/
   
   # 執行ML分析
   python ml_report_generator.py --data data/educational_data_2024_Fall.csv --output reports/
   ```

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

### 1. **Python 自動化技能**
- 資料科學工作流程 (pandas, scikit-learn, matplotlib)
- 自動化腳本開發
- HTML報告生成
- JSON資料處理

### 2. **測試驅動開發 (TDD)**
- pytest框架使用
- 跨語言測試策略
- 測試資料管理
- 持續整合測試

### 3. **DevOps 實務**
- GitHub Actions設定
- CI/CD pipeline設計
- 自動化部署
- 多分支管理

### 4. **軟體工程最佳實務**
- 程式碼組織結構
- 文檔撰寫
- 版本控制
- 跨平台相容性

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