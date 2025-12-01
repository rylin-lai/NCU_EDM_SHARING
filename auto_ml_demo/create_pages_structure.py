#!/usr/bin/env python3
"""
GitHub Pages Structure Creator
建立 GitHub Pages 結構腳本
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def create_pages_structure():
    """建立簡單的單頁 GitHub Pages 結構"""
    
    # 建立目錄結構
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)
    
    # 尋找報表文件 - 檢查多個可能路徑
    reports_found = False
    summary_data = {}
    
    # 可能的報表路徑
    possible_paths = [
        Path("reports"),
        Path("../reports"), 
        Path("auto_ml_demo/reports"),
        Path("./reports")
    ]
    
    for reports_dir in possible_paths:
        if reports_dir.exists():
            print(f"📁 Found reports directory: {reports_dir}")
            reports_found = True
            
            # 讀取分析摘要
            summary_file = reports_dir / "analysis_summary.json"
            if summary_file.exists():
                try:
                    import json
                    with open(summary_file, 'r', encoding='utf-8') as f:
                        summary_data = json.load(f)
                    print(f"📊 Loaded analysis summary")
                except Exception as e:
                    print(f"⚠️ Could not load summary: {e}")
            break
    
    if not reports_found:
        print("⚠️ No reports directory found, creating placeholder")
    
    # 建立簡單的單頁報告
    create_simple_single_page(public_dir, summary_data)
    
    print(f"✅ Simple single-page GitHub Pages created in {public_dir}")

def create_simple_single_page(public_dir, summary_data):
    """創建簡單的單頁報告"""
    
    # 提取關鍵數據
    dataset_info = summary_data.get('dataset_info', {})
    best_model = summary_data.get('best_classification_model', {})
    clustering_info = summary_data.get('clustering_summary', {})
    generation_time = summary_data.get('generated_at', datetime.now().isoformat())
    
    # 格式化數據
    dataset_shape = dataset_info.get('shape', 'Unknown')
    best_model_name = best_model.get('name', 'Unknown') if best_model else 'Unknown'
    best_f1_score = best_model.get('f1_score', 0) if best_model else 0
    best_accuracy = best_model.get('accuracy', 0) if best_model else 0
    
    # 簡化的單頁HTML
    simple_html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Python ML 自動化展示 / Automated ML Demo</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: #333;
        }}
        .container {{ 
            max-width: 1000px; margin: 0 auto; 
            background: white; border-radius: 15px; 
            padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header {{ 
            text-align: center; margin-bottom: 30px; 
            padding: 20px; background: #f8f9fa; border-radius: 10px;
        }}
        .section {{ 
            margin: 25px 0; padding: 20px; 
            background: #f8f9fa; border-radius: 8px; 
            border-left: 4px solid #007bff;
        }}
        .metrics {{ 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; margin: 20px 0;
        }}
        .metric-card {{ 
            background: white; padding: 15px; border-radius: 8px; 
            text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-value {{ 
            font-size: 24px; font-weight: bold; color: #007bff; 
        }}
        .metric-label {{ 
            font-size: 14px; color: #666; margin-top: 5px; 
        }}
        .status-badge {{ 
            display: inline-block; padding: 5px 10px; 
            background: #28a745; color: white; border-radius: 15px; 
            font-size: 12px; font-weight: bold;
        }}
        .footer {{ 
            text-align: center; margin-top: 30px; 
            padding: 20px; color: #666; border-top: 1px solid #eee;
        }}
        .tech-stack {{ 
            display: flex; flex-wrap: wrap; gap: 10px; 
            justify-content: center; margin: 15px 0;
        }}
        .tech-tag {{ 
            padding: 5px 12px; background: #e9ecef; 
            border-radius: 20px; font-size: 12px; color: #495057;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Python 自動化 ML 展示</h1>
            <h2>Automated Machine Learning Pipeline Demo</h2>
            <span class="status-badge">✅ 部署成功 / Deployment Success</span>
            <p style="margin-top: 15px; color: #666;">
                展示 Python 在企業環境中的自動化機器學習應用<br>
                Demonstrating Python's automated ML applications in enterprise environments
            </p>
        </div>
        
        <div class="section">
            <h3>📊 分析結果概覽 / Analysis Overview</h3>
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-value">{dataset_shape}</div>
                    <div class="metric-label">資料集大小 / Dataset Size</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{best_model_name}</div>
                    <div class="metric-label">最佳模型 / Best Model</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{best_accuracy:.3f}</div>
                    <div class="metric-label">準確率 / Accuracy</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{best_f1_score:.3f}</div>
                    <div class="metric-label">F1分數 / F1 Score</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h3>🚀 自動化流程展示 / Automation Pipeline</h3>
            <p><strong>這個頁面展示了完整的 Python 自動化流程：</strong></p>
            <div style="background: white; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p>✅ <strong>資料生成</strong>：自動產生教育資料集<br>
                ✅ <strong>ML分析</strong>：多模型分類與分群分析<br>
                ✅ <strong>報表生成</strong>：自動化HTML報表<br>
                ✅ <strong>CI/CD部署</strong>：GitHub Actions自動部署<br>
                ✅ <strong>多分支支援</strong>：每個學生分支獨立報表</p>
            </div>
        </div>
        
        <div class="section">
            <h3>💼 企業級Python應用 / Enterprise Python Applications</h3>
            <div style="background: white; padding: 15px; border-radius: 5px;">
                <p><strong>這個系統展示了軟體工程師日常使用的Python技能：</strong></p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>📈 <strong>數據科學</strong>：scikit-learn, pandas, matplotlib</li>
                    <li>🔄 <strong>自動化</strong>：CI/CD pipeline, GitHub Actions</li>
                    <li>🌐 <strong>網頁部署</strong>：GitHub Pages, 靜態網站生成</li>
                    <li>📊 <strong>報表系統</strong>：自動化HTML/PDF報表生成</li>
                    <li>🧪 <strong>測試與品質</strong>：自動化測試, 程式碼檢查</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h3>🛠️ 技術堆疊 / Tech Stack</h3>
            <div class="tech-stack">
                <span class="tech-tag">🐍 Python 3.11</span>
                <span class="tech-tag">🤖 scikit-learn</span>
                <span class="tech-tag">📊 matplotlib</span>
                <span class="tech-tag">🐼 pandas</span>
                <span class="tech-tag">🚀 GitHub Actions</span>
                <span class="tech-tag">📄 GitHub Pages</span>
                <span class="tech-tag">🔄 CI/CD</span>
                <span class="tech-tag">📈 Data Science</span>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🎓 Python Enterprise Workshop Demo</strong></p>
            <p style="font-size: 14px; color: #888;">
                生成時間 / Generated: {generation_time[:19].replace('T', ' ')}<br>
                展示如何用Python建立企業級自動化系統
            </p>
        </div>
    </div>
</body>
</html>'''
    
    with open(public_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(simple_html)
    
    print(f"✅ Created simple single-page report")

if __name__ == "__main__":
    create_pages_structure()