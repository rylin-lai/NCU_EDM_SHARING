# 跨平台測試架構 / Cross-platform Testing Architecture

## 🎯 設計目標 / Design Goals

使用 **pytest 同時測試 Python 和 Golang 實作**，確保兩個版本的功能對等性和一致性。  
Use **pytest to test both Python and Golang implementations simultaneously**, ensuring functional parity and consistency between versions.

## 📁 測試檔案架構 / Test File Architecture

```
workshop_materials/
├── test_tlsh_analyzer.py         # Python 專用單元測試 / Python-specific unit tests  
├── test_cross_platform.py        # 跨平台整合測試 / Cross-platform integration tests
├── tlsh_text_analyzer.py         # Python 實作 / Python implementation
└── golang/
    └── tlsh-text-analyzer-linux  # Golang binary / Golang binary
```

## 🧪 測試類型 / Test Types

### 1. **Python 專用測試** (`test_tlsh_analyzer.py`)
- **Mock 測試** / **Mock Tests**: 測試內部函數和邏輯
- **單元測試** / **Unit Tests**: 測試個別功能模組  
- **錯誤處理** / **Error Handling**: 邊界條件和異常情況

### 2. **跨平台整合測試** (`test_cross_platform.py`)
- **功能對等測試** / **Functional Parity Tests**: 確保兩個實作產生相同結果
- **介面一致性** / **Interface Consistency**: 驗證輸入輸出格式一致
- **效能比較** / **Performance Comparison**: 比較兩個實作的執行效能
- **錯誤處理一致性** / **Error Handling Consistency**: 確保錯誤處理行為一致

## 🔬 測試案例 / Test Cases

### `TestCrossPlatform` 類別包含以下測試：

#### ✅ `test_both_implementations_example`
- **目的** / **Purpose**: 測試內建範例功能
- **驗證** / **Validation**: 
  - JSON 結構完整性 / JSON structure integrity
  - 距離值合理性 / Distance value reasonableness
  - 分類結果有效性 / Classification result validity

#### ✅ `test_both_implementations_custom_text` 
- **目的** / **Purpose**: 測試自訂文字比較
- **驗證** / **Validation**:
  - 文字長度計算 / Text length calculation
  - TLSH 雜湊格式 / TLSH hash format
  - UTF-8 編碼處理 / UTF-8 encoding handling

#### ✅ `test_both_implementations_identical_text`
- **目的** / **Purpose**: 測試相同文字處理
- **驗證** / **Validation**:
  - 距離值必須為 0 / Distance must be 0
  - 分類為 "Identical" / Classified as "Identical"

#### ✅ `test_error_handling_short_text`
- **目的** / **Purpose**: 測試錯誤處理一致性
- **驗證** / **Validation**:
  - 兩個實作都應該拒絕過短文字 / Both should reject too-short text

#### ⚡ `test_performance_comparison`
- **目的** / **Purpose**: 效能基準比較
- **測量** / **Measurement**:
  - 執行時間 / Execution time
  - 相對速度提升 / Relative speedup

## 🚀 GitHub Actions 整合 / GitHub Actions Integration

### 新的 Workflow 流程：

```yaml
steps:
1. Checkout code          # 檢出程式碼
2. Setup Python & Go      # 設置環境  
3. Install dependencies    # 安裝依賴
4. Build Golang Binary     # 建置 Golang binary
5. Run Cross-platform Tests # 執行跨平台 pytest 測試
6. Upload Results          # 上傳測試結果
```

### 關鍵改進 / Key Improvements:

- ✅ **統一測試框架** / **Unified Test Framework**: 都用 pytest
- ✅ **自動化比較** / **Automated Comparison**: 自動比較兩個實作
- ✅ **詳細報告** / **Detailed Reporting**: 清楚的測試失敗原因
- ✅ **效能監控** / **Performance Monitoring**: 追蹤效能變化

## 💻 本地執行 / Local Execution

### 執行所有跨平台測試 / Run All Cross-platform Tests
```bash
# 確保 Golang binary 存在 / Ensure Golang binary exists
cd golang && go build -o tlsh-text-analyzer-linux main.go && cd ..

# 執行跨平台測試 / Run cross-platform tests  
python -m pytest test_cross_platform.py -v

# 執行特定測試 / Run specific test
python -m pytest test_cross_platform.py::TestCrossPlatform::test_both_implementations_example -v
```

### 執行效能測試 / Run Performance Tests
```bash
# 只執行效能測試 / Run only performance tests
python -m pytest test_cross_platform.py -v -m performance
```

### 執行完整測試套件 / Run Complete Test Suite
```bash
# 執行所有測試 / Run all tests
python -m pytest test_tlsh_analyzer.py test_cross_platform.py -v
```

## 📊 測試結果解讀 / Test Result Interpretation

### ✅ 成功案例 / Success Cases
```
✅ test_both_implementations_example PASSED
✅ test_both_implementations_custom_text PASSED  
✅ test_both_implementations_identical_text PASSED
```
**意義** / **Meaning**: 兩個實作功能對等，結果一致

### ❌ 失敗案例 / Failure Cases
```
❌ test_both_implementations_example FAILED
```
**可能原因** / **Possible Causes**:
- Golang binary 不存在或無法執行 / Golang binary missing or not executable
- 兩個實作產生不同結果 / Two implementations produce different results
- JSON 格式不一致 / JSON format inconsistency

### ⚠️ 效能警告 / Performance Warnings
```
⚡ Golang time: 0.001 seconds
⚡ Python time: 0.050 seconds  
📊 Speedup: 50.00x
```
**解讀** / **Interpretation**: Golang 比 Python 快 50 倍，這是正常的

## 🔧 故障排除 / Troubleshooting

### 常見問題 / Common Issues

#### 1. **Golang binary 不存在** / **Golang binary not found**
```bash
cd golang
go build -o tlsh-text-analyzer-linux main.go
chmod +x tlsh-text-analyzer-linux
```

#### 2. **JSON 解析失敗** / **JSON parsing failed**  
- 檢查輸出是否包含額外的除錯訊息 / Check for debug messages in output
- 使用 `--output` 參數保存到檔案 / Use `--output` to save to file

#### 3. **距離值差異過大** / **Distance values differ significantly**
- 檢查兩個實作的 TLSH 演算法是否一致 / Check TLSH algorithm consistency
- 驗證輸入文字編碼 / Verify input text encoding

#### 4. **測試超時** / **Test timeout**
- 減少測試文字長度 / Reduce test text length
- 檢查是否有無限迴圈 / Check for infinite loops

## 🎯 測試覆蓋率目標 / Test Coverage Goals

### 功能覆蓋率 / Functional Coverage
- ✅ **基本功能** / **Basic Functionality**: 100%
- ✅ **錯誤處理** / **Error Handling**: 100%  
- ✅ **邊界條件** / **Edge Cases**: 90%+
- ✅ **效能基準** / **Performance Baseline**: 基礎測量 / Basic measurement

### 平台覆蓋率 / Platform Coverage  
- ✅ **Linux x86_64** / **Linux x86_64**: GitHub Actions
- ✅ **macOS** / **macOS**: 本地開發 / Local development
- ⚠️ **Windows** / **Windows**: 可選支援 / Optional support

## 📈 未來改進 / Future Improvements

### 短期目標 / Short-term Goals
- [ ] 添加更多邊界條件測試 / Add more edge case tests
- [ ] 集成真正的 TLSH 函式庫 / Integrate real TLSH library  
- [ ] 添加記憶體使用量測試 / Add memory usage tests

### 長期目標 / Long-term Goals
- [ ] 支援更多檔案格式測試 / Support more file format tests
- [ ] 自動化效能回歸檢測 / Automated performance regression detection
- [ ] 建立測試資料庫 / Build test database

---

**維護者** / **Maintainer**: TLSH Workshop Team  
**最後更新** / **Last Updated**: 2024-11-30  
**相關文件** / **Related Docs**: `GITHUB_ACTIONS_README.md`, `PROJECT_STRUCTURE.md`