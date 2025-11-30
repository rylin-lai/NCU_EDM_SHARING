# GitHub Actions CI/CD 設置 / GitHub Actions CI/CD Setup

這個專案包含一個簡潔的 GitHub Actions workflow，用於自動測試 Python 和 Golang 實作的 TLSH 分析器。  
This project includes a streamlined GitHub Actions workflow for automatically testing both Python and Golang implementations of TLSH analyzer.

## Workflow 檔案 / Workflow File

### PR 測試套件 / PR Test Suite
**檔案**: `.github/workflows/pr-test.yml`

這是精簡但完整的測試 workflow，包含以下功能：  
This is a streamlined yet comprehensive test workflow with the following features:

### 工作流程步驟 / Workflow Steps

#### 1. 🐍 Python 測試步驟 / Python Test Step
- **環境設置** / **Environment Setup**: Python 3.10
- **功能測試** / **Functionality Tests**:
  - 測試簡化版文字分析器 (`tlsh_text_analyzer.py`)
  - 內建範例執行 / Built-in example execution
  - 自訂文字比較測試 / Custom text comparison test
  - JSON 輸出驗證 / JSON output validation
  - pytest 測試套件執行 / pytest test suite execution

#### 2. 🚀 Golang 測試步驟 / Golang Test Step  
- **環境設置** / **Environment Setup**: Go 1.20
- **建置和測試** / **Build and Test**:
  - 交叉編譯到 Linux x86_64 / Cross-compile to Linux x86_64
  - Binary 檔案驗證 / Binary file validation
  - 內建範例執行 / Built-in example execution
  - 自訂文字比較測試 / Custom text comparison test
  - JSON 輸出測試 / JSON output testing

#### 3. 🔄 結果比較步驟 / Result Comparison Step
- **跨語言驗證** / **Cross-language Validation**:
  - 相同輸入的結果比較 / Same input result comparison
  - 距離值有效性檢查 / Distance value validity check
  - 工具輸出合理性驗證 / Tool output reasonableness validation
  - 測試結果上傳 / Test result upload

## 觸發條件 / Trigger Conditions

這個 workflow 會在以下情況自動執行：  
This workflow automatically runs when:

### Pull Request 觸發 / Pull Request Triggers
```yaml
on:
  pull_request:
    branches: [ main, master ]  # 或 "*" 為所有分支 / or "*" for all branches
    paths:
      - '**.py'           # Python 檔案變更 / Python file changes
      - '**.go'           # Go 檔案變更 / Go file changes  
      - 'golang/**'       # Golang 目錄變更 / Golang directory changes
      - 'pylib/**'        # Python 函式庫變更 / Python library changes
      - 'test_*.py'       # 測試檔案變更 / Test file changes
      - '.github/workflows/**'  # Workflow 檔案變更 / Workflow file changes
```

### Push 觸發 / Push Triggers
- 推送到主要分支時 / When pushing to main branches
- 修改相關檔案時 / When modifying relevant files

## 測試流程示例 / Test Flow Example

### 開發流程 / Development Flow
1. **建立分支** / **Create Branch**
   ```bash
   git checkout -b feature/improve-tlsh-analysis
   ```

2. **修改程式碼** / **Modify Code**
   ```bash
   # 修改 Python 或 Golang 程式碼
   # Modify Python or Golang code
   vim tlsh_text_analyzer.py
   vim golang/main.go
   ```

3. **提交變更** / **Commit Changes**
   ```bash
   git add .
   git commit -m "Improve TLSH distance calculation"
   git push origin feature/improve-tlsh-analysis
   ```

4. **建立 Pull Request** / **Create Pull Request**
   - GitHub Actions 自動觸發 / GitHub Actions auto-triggers
   - 查看測試結果 / View test results
   - 等待所有檢查通過 / Wait for all checks to pass

### 測試結果解讀 / Test Result Interpretation

#### ✅ 成功狀態 / Success Status
- 所有測試通過 / All tests passed
- 跨語言驗證一致 / Cross-language validation consistent  
- 可以安全合併 / Safe to merge

#### ❌ 失敗狀態 / Failure Status
- 查看具體失敗的 job / Check specific failed job
- 檢查錯誤日誌 / Review error logs
- 修復問題後重新提交 / Fix issues and resubmit

#### ⚠️ 部分成功 / Partial Success
- 核心功能正常但效能有差異 / Core functions work but performance differs
- 檢查效能基準測試結果 / Check performance benchmark results

## 本地測試 / Local Testing

在提交 PR 之前，可以在本地運行相同的測試：  
Before submitting PR, run the same tests locally:

### Python 測試 / Python Tests
```bash
cd workshop_materials

# 基本功能測試 / Basic functionality test
python tlsh_text_analyzer.py --example --verbose

# pytest 測試 / pytest tests
python -m pytest test_tlsh_analyzer.py -v

# 覆蓋率測試 / Coverage test
python -m pytest test_tlsh_analyzer.py --cov=tlsh_text_analyzer
```

### Golang 測試 / Golang Tests
```bash
cd workshop_materials/golang

# 建置 / Build
go build -o tlsh-text-analyzer main.go

# 測試 / Test
./tlsh-text-analyzer -example -verbose
```

### 跨語言驗證 / Cross-language Validation
```bash
cd workshop_materials

# 執行相同測試 / Run same tests
python tlsh_text_analyzer.py --example --output python_result.json
./golang/tlsh-text-analyzer -example -output golang_result.json

# 比較結果 / Compare results  
diff python_result.json golang_result.json
```

## 故障排除 / Troubleshooting

### 常見問題 / Common Issues

#### 1. Python 依賴安裝失敗 / Python Dependency Installation Failure
```bash
# 本地測試 / Local test
pip install tlsh-python numpy pandas matplotlib pytest
```

#### 2. Golang 建置失敗 / Golang Build Failure
```bash
# 檢查 Go 版本 / Check Go version
go version

# 清理模組快取 / Clean module cache
go clean -modcache
go mod tidy
```

#### 3. 跨語言驗證失敗 / Cross-language Validation Failure
- 檢查輸入文字編碼 / Check input text encoding
- 確認 TLSH 計算邏輯一致性 / Verify TLSH calculation logic consistency
- 允許合理的數值差異 / Allow reasonable numerical differences

#### 4. 效能測試超時 / Performance Test Timeout
- 減少測試資料大小 / Reduce test data size  
- 檢查無限迴圈 / Check for infinite loops
- 優化演算法實作 / Optimize algorithm implementation

## 產出檔案 / Artifacts

GitHub Actions 會保存以下檔案供下載：  
GitHub Actions saves the following files for download:

### 測試結果 / Test Results
- `python-test-results-{version}` - Python 測試結果 / Python test results
- `golang-binary-{version}` - Golang 編譯產物 / Golang build artifacts  
- `cross-validation-results` - 跨語言驗證結果 / Cross-language validation results

### 下載方式 / Download Method
1. 進入 GitHub Actions 頁面 / Go to GitHub Actions page
2. 點選特定的 workflow run / Click specific workflow run  
3. 滾動到底部的 "Artifacts" 區域 / Scroll to "Artifacts" section at bottom
4. 下載所需檔案 / Download required files

## 自訂設置 / Custom Configuration

### 修改測試參數 / Modify Test Parameters

編輯 workflow 檔案來調整：  
Edit workflow files to adjust:

- **Python 版本** / **Python Versions**: 修改 `strategy.matrix.python-version`
- **Go 版本** / **Go Versions**: 修改 `strategy.matrix.go-version`  
- **測試超時** / **Test Timeout**: 添加 `timeout-minutes: 10`
- **觸發條件** / **Trigger Conditions**: 修改 `on.pull_request.paths`

### 添加額外測試 / Add Additional Tests

```yaml
- name: Custom Test / 自訂測試
  run: |
    echo "Adding your custom test here"
    # 你的自訂測試指令 / Your custom test commands
```

---

**建立日期 / Created**: 2024-11-30  
**維護者 / Maintainer**: TLSH Workshop Team  
**相關文件 / Related Docs**: `PROJECT_STRUCTURE.md`, `README.md`