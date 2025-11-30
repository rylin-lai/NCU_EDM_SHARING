# TLSH Workshop Materials / TLSH 工作坊材料

This directory contains comprehensive tutorial materials for learning TLSH (Trend Micro Locality Sensitive Hash) for malware analysis.

本目錄包含學習用於惡意軟體分析的 TLSH（Trend Micro 位置敏感雜湊）的完整教學材料。

## Files / 檔案

### Jupyter Notebooks / Jupyter 筆記本
- `tlsh_basic_tutorial.ipynb` - Basic TLSH concepts and string comparison tutorial
- `tlsh_malware_analysis_tutorial.ipynb` - **NEW** Advanced malware analysis with real Malware Bazaar dataset

### Data / 資料
- `data/` - Workshop datasets
  - `mb_1K.csv` - Small sample dataset (1K malware samples)
  - `clust_389300.csv` - Full Malware Bazaar clustered dataset (389,300 samples)

### Scripts / 腳本
- `start_workshop.sh` - Launch script for Jupyter environment

## Getting Started / 開始使用

### Prerequisites / 先決條件
```bash
# Install required packages
pip install jupyter pandas matplotlib numpy scikit-learn tlsh-python
```

### Launch Notebooks / 啟動筆記本
```bash
# Start Jupyter
./start_workshop.sh

# Or manually
cd /Users/rylin_lai/code/tlsh/workshop_materials
jupyter notebook
```

## Tutorial Progression / 教學進程

### Basic Tutorial (tlsh_basic_tutorial.ipynb)
1. TLSH vs traditional hashing concepts
2. String similarity examples  
3. Basic clustering algorithms
4. Interactive exercises

### Advanced Tutorial (tlsh_malware_analysis_tutorial.ipynb) ⭐ NEW
1. **Real malware dataset analysis** with 389,300 samples
2. **Dendrogram interpretation** for malware families
3. **Unknown sample classification** using similarity search
4. **Multi-family relationship analysis** 
5. **Unlabeled cluster investigation**

## Dataset Information / 資料集資訊

### Real Malware Bazaar Data
- **Source**: https://bazaar.abuse.ch/
- **Size**: 389,300 malware samples from 2021
- **Pre-clustered**: 16,453 clusters using HAC-T algorithm (CDist=30)
- **Top families**: AgentTesla, Mirai, FormBook, Heodo, AveMariaRAT

### Cluster Data Format
| Column | Description |
|--------|-------------|
| tlsh | TLSH hash of cluster center |
| family | Most common malware family |
| firstSeen | First appearance date |
| label | Combined family+date+count |
| radius | Cluster radius |
| nitems | Number of samples |

## Key Learning Outcomes / 主要學習成果

- Understand TLSH similarity hashing for malware analysis
- Interpret dendrograms for family relationships
- Classify unknown samples using distance thresholds
- Investigate unlabeled malware clusters
- Apply clustering algorithms to real-world data

## Workshop Timeline / 工作坊時間表

- **Basic Tutorial**: 45 minutes
- **Advanced Tutorial**: 60 minutes  
- **Total**: ~2 hours with discussion

## Troubleshooting / 疑難排解

### Common Issues
1. **Import Error**: Ensure you're running from `workshop_materials/` directory
2. **Data Not Found**: Check that `data/` folder contains the CSV files
3. **TLSH Library**: Use `tlsh-python` package for compatibility

### Dependencies
- Python 3.7+
- Jupyter Notebook
- pandas, matplotlib, numpy
- scikit-learn
- tlsh-python

---

**Instructor**: Rylin Lai - Software Engineer, Trend Micro Commercial Endpoint
**Contact**: For questions about the workshop materials