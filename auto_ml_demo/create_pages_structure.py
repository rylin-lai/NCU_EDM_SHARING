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
    """建立 GitHub Pages 的目錄結構和索引頁面"""
    
    # 建立目錄結構
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)
    
    plots_dir = public_dir / "plots"
    plots_dir.mkdir(exist_ok=True)
    
    # 複製報表檔案
    reports_dir = Path("reports")
    if reports_dir.exists():
        for item in reports_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, public_dir)
            elif item.is_dir() and item.name == "plots":
                for plot in item.iterdir():
                    if plot.suffix in ['.png', '.jpg', '.svg']:
                        shutil.copy2(plot, plots_dir)
    
    # 建立主索引頁面
    create_main_index(public_dir)
    
    # 建立圖表索引頁面
    create_plots_index(plots_dir)
    
    print(f"✅ GitHub Pages structure created in {public_dir}")

def create_main_index(public_dir):
    """建立主索引頁面"""
    
    index_html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Automated ML Analysis Dashboard</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 1200px; margin: 0 auto; 
            background: white; border-radius: 15px; 
            padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .header {{ 
            text-align: center; margin-bottom: 40px; 
            padding: 20px; background: #f8f9fa; 
            border-radius: 10px;
        }}
        .dashboard-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; margin: 30px 0; 
        }}
        .card {{ 
            background: white; padding: 25px; 
            border-radius: 10px; border: 2px solid #e9ecef; 
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card:hover {{ 
            transform: translateY(-5px); 
            box-shadow: 0 8px 25px rgba(0,0,0,0.15); 
        }}
        .card h3 {{ color: #495057; margin-top: 0; }}
        .btn {{ 
            display: inline-block; padding: 12px 24px; 
            background: #007bff; color: white; 
            text-decoration: none; border-radius: 6px; 
            transition: background 0.3s ease;
        }}
        .btn:hover {{ background: #0056b3; }}
        .timestamp {{ 
            color: #6c757d; font-style: italic; 
            text-align: center; margin-top: 30px; 
        }}
        .feature-list {{ 
            list-style: none; padding: 0; 
        }}
        .feature-list li {{ 
            padding: 8px 0; border-bottom: 1px solid #eee; 
        }}
        .feature-list li:before {{ 
            content: "✅ "; color: #28a745; 
            font-weight: bold; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Automated ML Analysis Dashboard</h1>
            <h2>自動化機器學習分析儀表板</h2>
            <p>Real-time educational data analysis powered by Python & GitHub Actions</p>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>📊 Latest ML Analysis Report</h3>
                <p>Complete machine learning analysis with classification and clustering results.</p>
                <a href="ml_analysis_report.html" class="btn">View Full Report / 檢視完整報表</a>
            </div>
            
            <div class="card">
                <h3>📈 Analysis Summary</h3>
                <p>Key metrics and performance indicators in JSON format.</p>
                <a href="analysis_summary.json" class="btn">Download Summary / 下載摘要</a>
            </div>
            
            <div class="card">
                <h3>🎨 Visualizations</h3>
                <p>Interactive charts and plots generated from the analysis.</p>
                <a href="plots/" class="btn">Browse Plots / 瀏覽圖表</a>
            </div>
        </div>
        
        <div class="card">
            <h3>🚀 About This Automation</h3>
            <p>This dashboard is automatically generated using:</p>
            <ul class="feature-list">
                <li>Python for data generation and ML analysis</li>
                <li>scikit-learn for machine learning models</li>
                <li>matplotlib & seaborn for visualizations</li>
                <li>GitHub Actions for CI/CD automation</li>
                <li>GitHub Pages for web deployment</li>
            </ul>
        </div>
        
        <div class="timestamp">
            Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        </div>
    </div>
</body>
</html>'''
    
    with open(public_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)

def create_plots_index(plots_dir):
    """建立圖表目錄的索引頁面"""
    
    # 獲取所有圖表檔案
    plot_files = list(plots_dir.glob("*.png")) + list(plots_dir.glob("*.jpg")) + list(plots_dir.glob("*.svg"))
    
    plots_html = '''<!DOCTYPE html>
<html>
<head>
    <title>ML Analysis Plots</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .plots-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .plot { 
            background: white; padding: 20px; border-radius: 8px; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; 
        }
        .plot img { max-width: 100%; height: auto; border-radius: 4px; }
        .plot h3 { color: #333; margin-top: 0; }
        .back-btn { 
            display: inline-block; padding: 10px 20px; 
            background: #007bff; color: white; text-decoration: none; 
            border-radius: 4px; margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="../" class="back-btn">← Back to Dashboard</a>
            <h1>📊 ML Analysis Visualizations</h1>
        </div>
        <div class="plots-grid">'''
    
    for plot_file in sorted(plot_files):
        filename = plot_file.name
        plots_html += f'''
            <div class="plot">
                <h3>{filename}</h3>
                <img src="{filename}" alt="{filename}">
            </div>'''
    
    plots_html += '''
        </div>
    </div>
</body>
</html>'''
    
    with open(plots_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(plots_html)

if __name__ == "__main__":
    create_pages_structure()