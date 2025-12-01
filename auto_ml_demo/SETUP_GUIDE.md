# 🚀 Setup Guide - GitHub Pages 配置指南

## ⚠️ 重要：首次設置步驟 (必須手動完成)

GitHub Pages 需要手動啟用才能使用 GitHub Actions 自動部署。
###
## 📋 必要設置清單 / Required Setup Checklist

### 1. 🔧 手動啟用 GitHub Pages / Manually Enable GitHub Pages

**⚠️ 這個步驟必須由 repository 擁有者手動完成**

1. 前往你的 GitHub repository
2. 點擊 **Settings** 標籤  
3. 向下滾動找到 **Pages** 選項（左側選單）
4. 在 "Build and deployment" 區段：
   - **Source**: 選擇 **"GitHub Actions"** 
   - ⚠️ **重要**: 不要選擇 "Deploy from a branch"

![Pages Setup](https://docs.github.com/assets/cb-20628/images/help/pages/github-pages-deploy-github-actions.png)

### 2. 🔑 確認 Actions 權限 / Verify Actions Permissions

1. 在 repository Settings 中
2. 點擊 **Actions** → **General**
3. 確認以下設定：
   - **Actions permissions**: "Allow all actions and reusable workflows"
   - **Workflow permissions**: "Read and write permissions" 
   - **Allow GitHub Actions to create and approve pull requests**: ✅ 勾選

### 3. ⚡ 確認 Repository 權限 / Repository Permissions

確保你對此 repository 有 **Admin** 或 **Write** 權限：
- Fork 的 repository 可能需要額外的權限設定
- 組織的 repository 可能需要組織管理員協助設定

### 4. 🛡️ 設定環境保護規則 / Environment Protection Rules

**重要**: 允許所有分支部署到 GitHub Pages

1. 前往 repository Settings → **Environments**
2. 點擊 **"github-pages"** 環境（如果不存在會自動創建）
3. 在 **"Deployment branches"** 區段：
   - 選擇 **"No restriction"** 
   - 這樣所有分支都可以部署，實現多分支功能
4. 確保沒有其他阻擋性的保護規則

### 5. ✅ 驗證設置 / Verify Setup

**首先確認 Pages 已正確設置：**
1. 在 repository 的 Settings → Pages 中，應該看到：
   ```
   ✅ Your site is ready to be published at https://username.github.io/repository-name/
   ```
   
**然後測試 workflow：**
1. 推送任何變更到 repository
2. 檢查 **Actions** 標籤，確認 workflow 正在執行
3. 等待 workflow 完成（約 3-5 分鐘）
4. 訪問 `https://{username}.github.io/{repository-name}/`

## 🔧 故障排除 / Troubleshooting

### 問題 1: "Get Pages site failed" 或 "Resource not accessible by integration"

**原因**: GitHub Pages 尚未手動啟用

**解決方案**:
1. 📍 **必須先手動啟用 Pages**：Settings → Pages → Source 選擇 "GitHub Actions"
2. 確認你有 repository 的管理員權限
3. 如果是 Fork 的 repository，可能需要在你的 Fork 中重新設定

### 問題 2: Workflow 執行但 Pages 沒有更新

**解決方案**:
1. 檢查 workflow logs，查看 "Deploy to GitHub Pages" 步驟
2. 確認 Pages 設定中的 Source 是 "GitHub Actions" 而不是 "Deploy from a branch"
3. 等待 5-10 分鐘，Pages 部署可能需要額外時間

### 問題 3: 403 Forbidden 或權限錯誤

**解決方案**:
1. 檢查 repository Settings → Actions → General
2. 確認 "Workflow permissions" 設為 "Read and write permissions"
3. 確認 "Allow GitHub Actions to create and approve pull requests" 已勾選

### 問題 4: "Branch is not allowed to deploy" 或環境保護規則

**錯誤訊息**: `Branch "xxx" is not allowed to deploy to github-pages due to environment protection rules`

**解決方案**:
1. 前往 repository Settings → Environments
2. 點擊 "github-pages" 環境
3. 在 "Deployment branches" 中：
   - 選擇 "No restriction" 
   - 或添加你的分支到允許列表
4. 移除任何不必要的保護規則

### 問題 5: Fork Repository 的特殊設定

如果你 Fork 了這個 repository：
1. 在你的 Fork 中重新啟用 GitHub Pages
2. 確認 Actions 在 Fork 中已啟用
3. 檢查環境保護規則（見問題 4）
4. 可能需要手動觸發第一次 workflow 執行

## 🎯 快速測試 / Quick Test

完成設置後，執行快速測試：

```bash
# Clone repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# 創建測試分支
git checkout -b test-deployment

# 做一個小修改觸發 workflow
echo "# Test" >> auto_ml_demo/README.md
git add .
git commit -m "Test deployment"
git push origin test-deployment
```

然後檢查：
1. GitHub Actions 是否執行
2. Pages 是否成功部署
3. 訪問 `https://yourusername.github.io/your-repo/branch-test-deployment/`

## 📚 更多資源 / Additional Resources

- [GitHub Pages 官方文檔](https://docs.github.com/en/pages)
- [GitHub Actions 官方文檔](https://docs.github.com/en/actions)
- [本項目的 MULTI_BRANCH_DEPLOYMENT.md](./MULTI_BRANCH_DEPLOYMENT.md)

---

完成設置後，每次推送分支都會自動生成獨立的ML分析報表！🎉

After setup completion, every branch push will automatically generate independent ML analysis reports!
