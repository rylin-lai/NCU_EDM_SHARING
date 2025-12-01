# 🚀 Multi-Branch GitHub Pages Deployment

## 🎯 功能說明 / Features

這個系統支援**多分支和PR同時部署到GitHub Pages**，每個學生都可以看到自己的ML分析結果！

This system supports **multi-branch and PR deployment to GitHub Pages**, allowing each student to see their own ML analysis results!

## 📁 部署結構 / Deployment Structure

```
GitHub Pages Root
├── index.html                    # 主頁面，列出所有部署
├── deployments.json             # 部署記錄
├── ml_analysis_report.html      # main分支的報表
├── plots/                       # main分支的圖表
├── pr-123/                      # PR #123 的部署
│   ├── ml_analysis_report.html
│   └── plots/
├── branch-student1/             # student1分支的部署  
│   ├── ml_analysis_report.html
│   └── plots/
└── branch-student2/             # student2分支的部署
    ├── ml_analysis_report.html
    └── plots/
```

## 🎯 部署規則 / Deployment Rules

### 1. **主分支 / Main Branch**
- **觸發條件**: Push 到 `main` 或 `master` 分支
- **部署路徑**: 根目錄 (`/`)
- **URL**: `https://username.github.io/repository/`

### 2. **Pull Request**
- **觸發條件**: 創建或更新 PR
- **部署路徑**: `/pr-{PR編號}/`
- **URL**: `https://username.github.io/repository/pr-123/`

### 3. **其他分支 / Other Branches**
- **觸發條件**: Push 到任何其他分支
- **部署路徑**: `/branch-{分支名稱}/`
- **URL**: `https://username.github.io/repository/branch-student1/`

## 🎓 教學應用 / Educational Applications

### 對學生 / For Students
```bash
# 學生創建自己的分支
git checkout -b student-alice
git add .
git commit -m "Alice's ML analysis"
git push origin student-alice

# 🎉 自動觸發部署到 /branch-student-alice/
```

### 對講師 / For Instructors
- **總覽頁面**: 一目了然看到所有學生的部署
- **比較分析**: 可以比較不同學生的結果
- **進度追蹤**: 看到每個學生最後更新時間
- **版本控制**: 每次更新都會記錄時間戳

## 🔧 技術實作 / Technical Implementation

### 1. **路徑檢測邏輯**
```yaml
# 自動檢測部署類型
if PR: 
  path = "pr-{number}"
elif main/master:
  path = ""  # root
else:
  path = "branch-{name}"
```

### 2. **多環境支援**
- 每個部署環境完全獨立
- 不同分支的資料集參數可以不同
- 支援同時進行多個實驗

### 3. **智慧索引頁面**
- 自動更新部署列表
- 顏色編碼區分不同類型
- 顯示作者和時間資訊

## 🚦 使用流程 / Usage Workflow

### 學生工作流程 / Student Workflow
1. **Fork 或 Clone** repository
2. **創建自己的分支**: `git checkout -b student-yourname`
3. **修改參數**: 可以調整 dataset size, semester 等
4. **Push 分支**: `git push origin student-yourname`
5. **檢視結果**: 訪問 `{github-pages-url}/branch-student-yourname/`

### 講師工作流程 / Instructor Workflow
1. **檢視總覽**: 訪問主頁面看到所有學生部署
2. **個別檢查**: 點擊進入每個學生的報表
3. **比較結果**: 在不同分支間切換比較
4. **追蹤進度**: 透過時間戳了解學生活動

## 💡 進階功能 / Advanced Features

### 1. **自動清理**
```yaml
# 可以設定自動清理舊的PR部署
retention-days: 30
```

### 2. **權限控制**
- 只有有權限的用戶可以觸發部署
- 可以限制特定分支的部署權限

### 3. **通知整合**
- 部署完成自動通知
- 可整合 Slack, Teams 等通知系統

## 🎯 教學優勢 / Educational Benefits

### 1. **視覺化學習**
- 每個學生都能看到自己的結果
- 即時反饋和視覺化報表

### 2. **協作學習**
- 學生可以互相查看和學習
- 促進技術交流和討論

### 3. **版本控制**
- 學習 Git 分支管理
- 理解 CI/CD 流程

### 4. **企業實務**
- 模擬真實的企業開發環境
- 學習多環境部署概念

## 🔍 監控和維護 / Monitoring & Maintenance

### 查看部署狀態
- GitHub Actions 頁面查看建置狀態
- GitHub Pages 設定查看部署歷史

### 故障排除
```bash
# 檢查 workflow logs
# 查看 GitHub Actions 執行記錄
# 確認 GitHub Pages 設定正確
```

---

這個多分支部署系統完美展示了現代 DevOps 實務，讓學生體驗到企業級的自動化工作流程！

This multi-branch deployment system perfectly demonstrates modern DevOps practices, giving students hands-on experience with enterprise-level automated workflows!