#!/usr/bin/env python3
"""
ML Report Generator - Production Version
機器學習報表生成器 - 生產版本

這個腳本會自動讀取教育資料集，執行完整的ML分析，並生成HTML報表
This script automatically reads educational datasets, performs complete ML analysis, and generates HTML reports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
import argparse
from datetime import datetime
import sys
import warnings
warnings.filterwarnings('ignore')

# ML imports
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    silhouette_score
)

# Visualization
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for GitHub Actions
plt.style.use('seaborn-v0_8')


class MLReportGenerator:
    """機器學習報表生成器 / ML Report Generator"""
    
    def __init__(self, output_dir="reports"):
        """
        初始化報表生成器
        Initialize report generator
        
        Args:
            output_dir: 報表輸出目錄 / Report output directory
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.plots_dir = self.output_dir / "plots"
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        
        self.results = {}
        self.plots = []
    
    def load_and_preprocess_data(self, data_path):
        """
        載入和前處理資料
        Load and preprocess data
        """
        print(f"🔄 Loading data from {data_path}")
        
        df = pd.read_csv(data_path)
        
        # 基本資訊 / Basic information
        self.results['data_info'] = {
            'shape': df.shape,
            'columns': list(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'dtypes': df.dtypes.astype(str).to_dict()
        }
        
        print(f"✅ Loaded dataset with shape: {df.shape}")
        return df
    
    def prepare_features_and_target(self, df, target_col='Pass_course'):
        """
        準備特徵和目標變數
        Prepare features and target variables
        """
        if target_col not in df.columns:
            print(f"❌ Target column '{target_col}' not found. Available columns: {df.columns.tolist()}")
            return None, None, None, None, None
        
        # 分離特徵和目標 / Separate features and target
        feature_cols = [col for col in df.columns if col not in [
            target_col, 'student_id', 'generated_at', 'semester'
        ]]
        
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        
        # 處理類別變數 / Handle categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        label_encoders = {}
        
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            label_encoders[col] = le
        
        # 標準化數值特徵 / Standardize numerical features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 分割訓練和測試集 / Split train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.results['preprocessing'] = {
            'feature_columns': feature_cols,
            'categorical_columns': list(categorical_cols),
            'target_distribution': y.value_counts().to_dict(),
            'train_size': X_train.shape[0],
            'test_size': X_test.shape[0]
        }
        
        return X_train, X_test, y_train, y_test, feature_cols
    
    def run_classification_analysis(self, X_train, X_test, y_train, y_test, feature_cols):
        """
        執行分類分析
        Run classification analysis
        """
        print("🔄 Running classification analysis...")
        
        # 定義模型 / Define models
        models = {
            'Logistic Regression': LogisticRegression(max_iter=50, random_state=36),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'SVM': SVC(kernel='rbf', probability=True, random_state=42)
        }
        
        classification_results = {}
        
        for name, model in models.items():
            print(f"  🔄 Training {name}...")
            
            # 訓練模型 / Train model
            model.fit(X_train, y_train)
            
            # 預測 / Predict
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # 計算指標 / Calculate metrics
            results = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1': f1_score(y_test, y_pred, average='weighted')
            }
            
            if y_proba is not None:
                results['auc'] = roc_auc_score(y_test, y_proba)
            
            # 交叉驗證 / Cross validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1_weighted')
            results['cv_f1_mean'] = cv_scores.mean()
            results['cv_f1_std'] = cv_scores.std()
            
            classification_results[name] = results
        
        self.results['classification'] = classification_results
        
        # 生成分類結果圖表 / Generate classification plots
        self._plot_classification_results(classification_results)
        
        return classification_results
    
    def run_clustering_analysis(self, X_train, feature_cols):
        """
        執行分群分析
        Run clustering analysis
        """
        print("🔄 Running clustering analysis...")
        
        clustering_results = {}
        
        # K-Means 分析 / K-Means analysis
        print("  🔄 K-Means clustering...")
        
        # 尋找最佳K值 / Find optimal K
        k_range = range(2, 8)
        inertias = []
        silhouette_scores = []
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(X_train)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X_train, cluster_labels))
        
        # 選擇最佳K值（基於silhouette score）/ Select best K based on silhouette score
        best_k_idx = np.argmax(silhouette_scores)
        best_k = list(k_range)[best_k_idx]
        
        # 用最佳K值進行最終分群 / Final clustering with best K
        final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        final_labels = final_kmeans.fit_predict(X_train)
        
        clustering_results['kmeans'] = {
            'best_k': best_k,
            'best_silhouette': silhouette_scores[best_k_idx],
            'inertias': inertias,
            'silhouette_scores': silhouette_scores,
            'cluster_sizes': np.bincount(final_labels).tolist()
        }
        
        # 階層式分群 / Hierarchical clustering
        print("  🔄 Hierarchical clustering...")
        
        hierarchical = AgglomerativeClustering(n_clusters=best_k)
        hier_labels = hierarchical.fit_predict(X_train)
        hier_silhouette = silhouette_score(X_train, hier_labels)
        
        clustering_results['hierarchical'] = {
            'n_clusters': best_k,
            'silhouette_score': hier_silhouette,
            'cluster_sizes': np.bincount(hier_labels).tolist()
        }
        
        self.results['clustering'] = clustering_results
        
        # 生成分群圖表 / Generate clustering plots
        self._plot_clustering_results(clustering_results, X_train)
        
        return clustering_results
    
    def _plot_classification_results(self, results):
        """生成分類結果圖表 / Generate classification result plots"""
        
        # 模型比較圖 / Model comparison plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        models = list(results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1']
        
        # 各項指標比較 / Metrics comparison
        for i, metric in enumerate(metrics):
            ax = [ax1, ax2, ax3, ax4][i]
            values = [results[model].get(metric, 0) for model in models]
            bars = ax.bar(models, values, alpha=0.7)
            ax.set_title(f'{metric.capitalize()} Comparison')
            ax.set_ylabel(metric.capitalize())
            ax.set_ylim(0, 1)
            
            # 添加數值標籤 / Add value labels
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                       f'{value:.3f}', ha='center', va='bottom')
            
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plot_path = self.plots_dir / "classification_comparison.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.plots.append(("Classification Model Comparison", plot_path.name))
    
    def _plot_clustering_results(self, results, X_train):
        """生成分群結果圖表 / Generate clustering result plots"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Elbow curve / 手肘曲線
        k_range = range(2, 8)
        ax1.plot(k_range, results['kmeans']['inertias'], 'bo-')
        ax1.set_title('Elbow Method for Optimal K')
        ax1.set_xlabel('Number of Clusters (K)')
        ax1.set_ylabel('Inertia')
        ax1.grid(True, alpha=0.3)
        
        # Silhouette scores / 輪廓分數
        ax2.plot(k_range, results['kmeans']['silhouette_scores'], 'ro-')
        ax2.set_title('Silhouette Score vs K')
        ax2.set_xlabel('Number of Clusters (K)')
        ax2.set_ylabel('Silhouette Score')
        ax2.grid(True, alpha=0.3)
        
        # K-Means cluster sizes / K-Means 群集大小
        kmeans_sizes = results['kmeans']['cluster_sizes']
        ax3.bar(range(len(kmeans_sizes)), kmeans_sizes, alpha=0.7, color='skyblue')
        ax3.set_title('K-Means Cluster Sizes')
        ax3.set_xlabel('Cluster ID')
        ax3.set_ylabel('Number of Students')
        
        # Hierarchical cluster sizes / 階層式群集大小
        hier_sizes = results['hierarchical']['cluster_sizes']
        ax4.bar(range(len(hier_sizes)), hier_sizes, alpha=0.7, color='lightcoral')
        ax4.set_title('Hierarchical Cluster Sizes')
        ax4.set_xlabel('Cluster ID')
        ax4.set_ylabel('Number of Students')
        
        plt.tight_layout()
        plot_path = self.plots_dir / "clustering_analysis.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.plots.append(("Clustering Analysis", plot_path.name))
    
    def generate_html_report(self, dataset_path):
        """
        生成HTML報表
        Generate HTML report
        """
        print("🔄 Generating HTML report...")
        
        # 讀取資料集元資料 / Read dataset metadata
        metadata_path = Path(dataset_path).with_suffix('.json')
        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        # 生成HTML內容 / Generate HTML content
        html_content = self._create_html_template(metadata)
        
        # 儲存HTML報表 / Save HTML report
        report_path = self.output_dir / "ml_analysis_report.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 生成摘要JSON / Generate summary JSON
        summary_path = self.output_dir / "analysis_summary.json"
        summary = {
            'generated_at': datetime.now().isoformat(),
            'dataset_info': self.results.get('data_info', {}),
            'best_classification_model': self._get_best_classification_model(),
            'all_classification_models': self.results.get('classification', {}),
            'clustering_summary': self.results.get('clustering', {}),
            'report_path': str(report_path.name),
            'plots': [plot_name for plot_name, _ in self.plots]
        }
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ HTML report generated: {report_path}")
        print(f"✅ Analysis summary saved: {summary_path}")
        
        return report_path
    
    def _get_best_classification_model(self):
        """獲取最佳分類模型 / Get best classification model"""
        if 'classification' not in self.results:
            return None
        
        best_model = None
        best_f1 = 0
        
        for model_name, metrics in self.results['classification'].items():
            if metrics.get('f1', 0) > best_f1:
                best_f1 = metrics['f1']
                best_model = {
                    'name': model_name,
                    'f1_score': best_f1,
                    'accuracy': metrics.get('accuracy', 0),
                    'auc': metrics.get('auc', None)
                }
        
        return best_model
    
    def _create_html_template(self, metadata):
        """建立HTML模板 / Create HTML template"""
        
        # CSS 樣式 / CSS styles
        css_styles = """
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
            .section { margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff; }
            .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
            .metric-card { background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .metric-value { font-size: 24px; font-weight: bold; color: #007bff; }
            .metric-label { font-size: 14px; color: #666; margin-top: 5px; }
            .plot-container { text-align: center; margin: 20px 0; }
            .plot-container img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #007bff; color: white; }
            .timestamp { color: #666; font-style: italic; }
            .highlight { background-color: #e7f3ff; padding: 10px; border-radius: 4px; margin: 10px 0; }
        </style>
        """
        
        # 動態內容生成 / Dynamic content generation
        data_info = self.results.get('data_info', {})
        classification_results = self.results.get('classification', {})
        clustering_results = self.results.get('clustering', {})
        
        # 資料集資訊表格 / Dataset info table
        dataset_info_html = f"""
        <table>
            <tr><th>項目 / Item</th><th>值 / Value</th></tr>
            <tr><td>資料集形狀 / Dataset Shape</td><td>{data_info.get('shape', 'N/A')}</td></tr>
            <tr><td>特徵數量 / Number of Features</td><td>{len(data_info.get('columns', [])) - 1}</td></tr>
            <tr><td>訓練集大小 / Training Set Size</td><td>{self.results.get('preprocessing', {}).get('train_size', 'N/A')}</td></tr>
            <tr><td>測試集大小 / Test Set Size</td><td>{self.results.get('preprocessing', {}).get('test_size', 'N/A')}</td></tr>
        </table>
        """
        
        # 分類結果表格 / Classification results table
        classification_html = ""
        if classification_results:
            classification_html = "<table><tr><th>模型 / Model</th><th>準確率 / Accuracy</th><th>F1分數 / F1 Score</th><th>AUC</th></tr>"
            for model_name, metrics in classification_results.items():
                auc_value = f"{metrics.get('auc', 0):.3f}" if metrics.get('auc') else "N/A"
                classification_html += f"""
                <tr>
                    <td>{model_name}</td>
                    <td>{metrics.get('accuracy', 0):.3f}</td>
                    <td>{metrics.get('f1', 0):.3f}</td>
                    <td>{auc_value}</td>
                </tr>
                """
            classification_html += "</table>"
        
        # 分群結果 / Clustering results
        clustering_html = ""
        if clustering_results:
            kmeans_info = clustering_results.get('kmeans', {})
            hierarchical_info = clustering_results.get('hierarchical', {})
            
            clustering_html = f"""
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{kmeans_info.get('best_k', 'N/A')}</div>
                    <div class="metric-label">最佳K值 / Optimal K</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{kmeans_info.get('best_silhouette', 0):.3f}</div>
                    <div class="metric-label">K-Means輪廓分數 / Silhouette Score</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{hierarchical_info.get('silhouette_score', 0):.3f}</div>
                    <div class="metric-label">階層式輪廓分數 / Hierarchical Silhouette</div>
                </div>
            </div>
            """
        
        # 圖表HTML / Plots HTML
        plots_html = ""
        for plot_title, plot_filename in self.plots:
            plots_html += f"""
            <div class="section">
                <h3>{plot_title}</h3>
                <div class="plot-container">
                    <img src="plots/{plot_filename}" alt="{plot_title}">
                </div>
            </div>
            """
        
        # 主HTML結構 / Main HTML structure
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>機器學習分析報表 / ML Analysis Report</title>
            {css_styles}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 機器學習分析報表 / ML Analysis Report</h1>
                    <p class="timestamp">生成時間 / Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h2>📊 資料集資訊 / Dataset Information</h2>
                    {dataset_info_html}
                </div>
                
                <div class="section">
                    <h2>🎯 分類分析結果 / Classification Analysis Results</h2>
                    <div class="highlight">
                        最佳模型 / Best Model: <strong>{self._get_best_classification_model_name()}</strong>
                    </div>
                    {classification_html}
                </div>
                
                <div class="section">
                    <h2>🔍 分群分析結果 / Clustering Analysis Results</h2>
                    {clustering_html}
                </div>
                
                {plots_html}
                
                <div class="section">
                    <h2>ℹ️ 元資料 / Metadata</h2>
                    <p>資料集檔案 / Dataset File: <code>{metadata.get('filename', 'N/A')}</code></p>
                    <p>生成種子 / Generator Seed: <code>{metadata.get('generator_seed', 'N/A')}</code></p>
                    <p>資料生成時間 / Data Generated: <code>{metadata.get('generated_at', 'N/A')}</code></p>
                </div>
                
                <div class="section">
                    <h2>🚀 關於這個報表 / About This Report</h2>
                    <p>這個報表由 <strong>Python 自動化管線</strong> 生成，展示了從資料載入到模型評估的完整機器學習工作流程。</p>
                    <p>This report is generated by an <strong>automated Python pipeline</strong>, showcasing a complete machine learning workflow from data loading to model evaluation.</p>
                    
                    <div class="highlight">
                        <p>🎯 <strong>教學重點 / Learning Points:</strong></p>
                        <ul>
                            <li>🔄 自動化資料分析管線 / Automated data analysis pipeline</li>
                            <li>📊 多模型效能比較 / Multi-model performance comparison</li>
                            <li>🎯 分群與分類整合分析 / Integrated clustering and classification analysis</li>
                            <li>📈 視覺化結果呈現 / Visualized result presentation</li>
                            <li>🚀 GitHub Actions CI/CD 整合 / GitHub Actions CI/CD integration</li>
                        </ul>
                    </div>
                </div>
                
                <footer style="text-align: center; margin-top: 40px; padding: 20px; color: #666; border-top: 1px solid #eee;">
                    <p>Generated by ML Report Generator | Python Workshop @ NCU</p>
                    <p>🐍 Python + 🤖 sklearn + 📊 matplotlib + 🚀 GitHub Actions</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _get_best_classification_model_name(self):
        """獲取最佳分類模型名稱 / Get best classification model name"""
        best_model = self._get_best_classification_model()
        return best_model['name'] if best_model else "N/A"


def main():
    """主要執行函數 / Main execution function"""
    
    parser = argparse.ArgumentParser(
        description="ML Report Generator - 機器學習報表生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例 / Examples:

  基本報表生成 / Basic report generation:
    python ml_report_generator.py --data data/educational_data_2024_Fall.csv

  指定輸出目錄 / Specify output directory:
    python ml_report_generator.py --data data/educational_data_2024_Fall.csv --output reports/
    
  自訂目標變數 / Custom target variable:
    python ml_report_generator.py --data data/custom_data.csv --target custom_target_column
        """)
    
    parser.add_argument('--data', '-d', type=str, required=True,
                       help='輸入資料集路徑 / Input dataset path')
    parser.add_argument('--output', '-o', type=str, default="reports",
                       help='報表輸出目錄 / Report output directory (default: reports)')
    parser.add_argument('--target', '-t', type=str, default="Pass_course",
                       help='目標變數欄位名稱 / Target variable column name (default: Pass_course)')
    
    args = parser.parse_args()
    
    try:
        # 檢查輸入檔案 / Check input file
        data_path = Path(args.data)
        if not data_path.exists():
            print(f"❌ Data file not found: {data_path}")
            return 1
        
        # 初始化報表生成器 / Initialize report generator
        generator = MLReportGenerator(output_dir=args.output)
        
        # 載入資料 / Load data
        df = generator.load_and_preprocess_data(data_path)
        
        # 準備特徵和目標 / Prepare features and target
        X_train, X_test, y_train, y_test, feature_cols = generator.prepare_features_and_target(
            df, target_col=args.target
        )
        
        if X_train is None:
            return 1
        
        # 執行分析 / Run analysis
        generator.run_classification_analysis(X_train, X_test, y_train, y_test, feature_cols)
        generator.run_clustering_analysis(X_train, feature_cols)
        
        # 生成報表 / Generate report
        report_path = generator.generate_html_report(data_path)
        
        print(f"\n✅ 報表生成完成！ / Report generation completed!")
        print(f"📊 HTML報表：{report_path}")
        print(f"📂 圖表目錄：{generator.plots_dir}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating report: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())