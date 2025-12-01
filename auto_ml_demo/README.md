# 🤖 Automated ML Analysis Demo

這個展示案例說明如何使用 Python + GitHub Actions 建立完全自動化的機器學習分析管線。

This demo shows how to create a fully automated machine learning analysis pipeline using Python + GitHub Actions.

## 🎯 展示內容 / What This Demonstrates

### 1. **資料生成自動化 / Automated Data Generation**
- 基於 Week12 教育資料集的生成器
- 可設定參數的合成資料產生
- 自動產生元資料和統計資訊

### 2. **機器學習管線 / ML Pipeline**
- 自動資料前處理和特徵工程
- 多模型比較 (Logistic Regression, Random Forest, KNN, SVM)
- 分群分析 (K-Means, Hierarchical Clustering)
- 自動模型評估和視覺化

### 3. **報表生成 / Report Generation**
- 自動產生 HTML 報表
- 整合圖表和統計結果
- 響應式網頁設計

### 4. **CI/CD 自動化 / CI/CD Automation**
- GitHub Actions 工作流程
- 自動部署到 GitHub Pages
- 定時執行和手動觸發

## 📁 檔案結構 / File Structure

```
auto_ml_demo/
├── educational_dataset_generator.py   # 教育資料集生成器
├── ml_report_generator.py            # ML 報表生成器
├── create_pages_structure.py         # GitHub Pages 結構建立
├── requirements.txt                  # Python 依賴套件
└── README.md                        # 說明文件
```

## 🚀 多分支部署功能 / Multi-Branch Deployment

✨ **每個學生都可以有自己的ML分析報表！**

- **主分支**: 部署到根路徑 `https://username.github.io/repo/`
- **PR**: 部署到 `https://username.github.io/repo/pr-123/`
- **學生分支**: 部署到 `https://username.github.io/repo/branch-student1/`

📖 **詳細說明**: 請參閱 [MULTI_BRANCH_DEPLOYMENT.md](./MULTI_BRANCH_DEPLOYMENT.md)

## 🚀 使用方法 / Usage

### 學生快速開始 / Quick Start for Students

1. **創建自己的分支 / Create your branch**
```bash
git checkout -b student-your-name
```

2. **可選：調整參數 / Optional: Adjust parameters**
```bash
# 修改 educational_dataset_generator.py 中的預設值
# 或透過 GitHub Actions 手動執行時設定參數
```

3. **推送觸發部署 / Push to trigger deployment**
```bash
git add .
git commit -m "Your name's ML analysis"
git push origin student-your-name
```

4. **查看結果 / View results**
- 訪問 `https://username.github.io/repository/branch-student-your-name/`
- 或在主頁面 `https://username.github.io/repository/` 找到你的部署

### 本地執行 / Local Execution

1. **安裝依賴 / Install Dependencies**
```bash
cd auto_ml_demo
pip install -r requirements.txt
```

2. **生成資料集 / Generate Dataset**
```bash
python educational_dataset_generator.py --students 300 --semester 2024_Fall
```

3. **執行 ML 分析 / Run ML Analysis**
```bash
python ml_report_generator.py --data data/educational_data_2024_Fall.csv
```

4. **建立 GitHub Pages 結構 / Create Pages Structure**
```bash
python create_pages_structure.py
```

### GitHub Actions 自動化 / GitHub Actions Automation

1. **推送到 GitHub / Push to GitHub**
```bash
git add .
git commit -m "Add automated ML demo"
git push
```

2. **自動觸發 / Automatic Trigger**
- 每次推送到 main/master 分支
- 每日午夜自動執行
- 手動觸發 (workflow_dispatch)

3. **檢視結果 / View Results**
- 訪問 `https://yourusername.github.io/repository-name/`
- 查看自動生成的 ML 分析報表

## 🎓 教學價值 / Educational Value

### 對學生來說 / For Students
- 看到熟悉的 Week12 資料集在生產環境的應用
- 學習如何將 Jupyter notebook 轉換為生產級 Python 腳本
- 理解 CI/CD 的概念和實際應用
- 🎯 **每個人都有專屬的ML報表**，增強學習動機
- 學習 Git 分支管理和協作開發

### 對講師來說 / For Instructors
- 完美的 2.5 小時工作坊內容
- 結合理論和實務的教學案例
- 展示 Python 在企業 DevOps 中的角色
- 📊 **即時監控所有學生進度**，透過總覽頁面
- 🔄 **支援多人同時實作**，不會互相干擾

### 課堂建議 / Classroom Recommendations

#### 🕐 **時間分配 (2.5小時)**
1. **理論介紹** (30分鐘): GitHub Actions + Python自動化概念
2. **Demo展示** (20分鐘): 展示完整工作流程
3. **學生實作** (80分鐘): 每個人創建自己的分支和部署
4. **結果分享** (30分鐘): 檢視和比較大家的結果
5. **Q&A討論** (10分鐘): 問題解答和延伸討論

#### 👥 **建議班級大小**
- **理想**: 10-20人
- **最大**: 30人 (超過需要考慮repository性能)

#### 📋 **課前準備清單**
- [ ] 學生都有 GitHub 帳號
- [ ] 講師已設定好主 repository
- [ ] 啟用 GitHub Pages
- [ ] 測試完整工作流程

## 🛠️ 技術堆疊 / Tech Stack

- **Python**: 資料處理和機器學習
- **scikit-learn**: 機器學習演算法
- **matplotlib/seaborn**: 資料視覺化
- **pandas**: 資料分析
- **GitHub Actions**: CI/CD 自動化
- **GitHub Pages**: 靜態網站部署

## 🎯 核心概念展示 / Core Concepts Demonstrated

1. **自動化管線 / Automation Pipeline**
   - 從資料生成到報表部署的完整自動化
   
2. **可重現性 / Reproducibility**
   - 版本控制的資料和程式碼
   - 固定的隨機種子和依賴版本

3. **可擴展性 / Scalability**
   - 參數化的資料生成
   - 模組化的程式碼結構

4. **企業級實務 / Enterprise Practices**
   - 錯誤處理和日誌記錄
   - 清晰的文件和註解
   - 標準化的專案結構

## 💡 擴展想法 / Extension Ideas

- 添加 A/B 測試功能
- 整合不同的機器學習框架 (TensorFlow, PyTorch)
- 添加資料品質檢查
- 實作模型監控和警報
- 整合雲端服務 (AWS, GCP, Azure)

---

這個展示案例完美地將學術學習與產業實務結合，為學生提供了寶貴的實際應用經驗！

This demo perfectly combines academic learning with industry practices, providing students with valuable real-world application experience!