#!/usr/bin/env python3
"""
TLSH 分析工具 - 支援兩種使用案例
TLSH Analyzer Tool - Supporting Two Use Cases

案例1: 比較兩個文字的相似性 (適用於企業資料外洩調查)
Case 1: Compare similarity between two texts (for enterprise data leak investigation)

案例2: 對資料集進行 DBSCAN 分群分析
Case 2: DBSCAN clustering analysis on datasets
"""

import argparse
import sys
import os
import json
import tlsh
from typing import List, Tuple, Dict

# 添加 pylib 到路徑以便導入 / Add pylib to path for imports
sys.path.append('./pylib')
try:
    from tlsh_lib import tlsh_csvfile, runDBSCAN, tlist2cdata, sim_affinity
    from printCluster import outputClusters
except ImportError:
    print("錯誤：無法導入 TLSH 函式庫。請確保 pylib 目錄存在。")
    print("Error: Could not import TLSH libraries. Make sure pylib directory exists.")
    sys.exit(1)


class TLSHAnalyzer:
    """TLSH 分析器類別 / TLSH Analyzer Class"""
    
    def __init__(self):
        self.verbose = False
    
    def calculate_tlsh_hash(self, text: str) -> str:
        """
        計算文字的 TLSH 雜湊值
        Calculate TLSH hash for text content
        
        Args:
            text: 輸入文字 / Input text
        Returns:
            TLSH 雜湊字串 / TLSH hash string
        """
        if len(text) < 50:  # TLSH 需要最小長度 / TLSH requires minimum length
            raise ValueError("文字太短，無法計算 TLSH（最少需要50字元）/ Text too short for TLSH calculation (minimum 50 characters)")
        
        tlsh_obj = tlsh.Tlsh()
        tlsh_obj.update(text.encode('utf-8'))
        tlsh_obj.final()
        return tlsh_obj.hexdigest()
    
    def compare_two_texts(self, text1: str, text2: str) -> Dict:
        """
        案例 1: 比較兩個文字的相似性
        Case 1: Compare similarity between two texts
        
        這個功能適用於企業資料外洩調查，可以快速判斷兩個檔案是否包含相同資料
        This function is suitable for enterprise data leak investigation,
        to quickly determine if two files contain the same data
        """
        if self.verbose:
            print("🔍 案例 1: 比較兩個文字字串的相似性")
            print("🔍 Case 1: Comparing two text strings")
        
        try:
            # 計算 TLSH 雜湊 / Calculate TLSH hashes
            hash1 = self.calculate_tlsh_hash(text1)
            hash2 = self.calculate_tlsh_hash(text2)
            
            # 計算距離 / Calculate distance
            t1 = tlsh.Tlsh()
            t1.fromTlshStr(hash1)
            t2 = tlsh.Tlsh()
            t2.fromTlshStr(hash2)
            
            distance = t1.diff(t2)
            
            # 分類相似性 / Classify similarity
            if distance == 0:
                similarity_class = "完全相同 / Identical"
                risk_level = "無風險 / None"
            elif distance <= 50:
                similarity_class = "非常相似 / Very Similar"
                risk_level = "高風險 / High"
            elif distance <= 100:
                similarity_class = "相似 / Similar"
                risk_level = "中等風險 / Medium"
            else:
                similarity_class = "不同 / Different"
                risk_level = "低風險 / Low"
            
            result = {
                "case": "two_text_comparison",
                "text1_length": len(text1),
                "text2_length": len(text2),
                "tlsh_hash1": hash1,
                "tlsh_hash2": hash2,
                "distance": distance,
                "similarity_class": similarity_class,
                "risk_level": risk_level,
                "interpretation": {
                    "zh": f"距離 {distance}: {similarity_class}，風險等級：{risk_level.split(' / ')[0]}",
                    "en": f"Distance {distance}: {similarity_class.split(' / ')[1]}, Risk level: {risk_level.split(' / ')[1]}"
                }
            }
            
            if self.verbose:
                print(f"  距離 / Distance: {distance}")
                print(f"  分類 / Classification: {similarity_class}")
                print(f"  風險等級 / Risk Level: {risk_level}")
            
            return result
            
        except Exception as e:
            raise ValueError(f"比較文字時發生錯誤 / Error comparing texts: {str(e)}")
    
    def analyze_file_dataset(self, csv_file: str, eps: int = 30, min_samples: int = 2) -> Dict:
        """
        案例 2: 分析檔案資料集的分群
        Case 2: Analyze clustering of file dataset
        
        使用 DBSCAN 演算法對 TLSH 雜湊進行分群，適用於惡意軟體家族分類或資料譜系追蹤
        Use DBSCAN algorithm to cluster TLSH hashes, suitable for malware family classification
        or data lineage tracking
        """
        if self.verbose:
            print(f"🔍 案例 2: 分析資料集 {csv_file} 的分群")
            print(f"🔍 Case 2: Analyzing dataset clustering from {csv_file}")
        
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"找不到 CSV 檔案 / CSV file not found: {csv_file}")
        
        # 從 CSV 載入 TLSH 資料 / Load TLSH data from CSV
        try:
            (tlist, labels) = tlsh_csvfile(csv_file)
            if tlist is None:
                raise ValueError("無法從 CSV 載入 TLSH 資料 / Failed to load TLSH data from CSV")
            
            if self.verbose:
                print(f"  已載入 {len(tlist)} 個 TLSH 雜湊")
                print(f"  Loaded {len(tlist)} TLSH hashes")
            
            # 執行 DBSCAN 分群 / Run DBSCAN clustering
            dbscan_result = runDBSCAN(tlist, eps=eps, min_samples=min_samples)
            cluster_labels = dbscan_result.labels_
            
            # 分析結果 / Analyze results
            n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
            n_noise = list(cluster_labels).count(-1)
            n_clustered = len(cluster_labels) - n_noise
            
            # 取得家族資訊（如果可用）/ Get family information if available
            family_labels = labels[0] if labels and len(labels) > 0 else None
            unique_families = len(set(family_labels)) if family_labels else 0
            
            result = {
                "case": "dataset_clustering",
                "csv_file": csv_file,
                "total_samples": len(tlist),
                "clustering_params": {
                    "eps": eps,
                    "min_samples": min_samples
                },
                "results": {
                    "n_clusters": n_clusters,
                    "n_noise": n_noise,
                    "n_clustered": n_clustered,
                    "clustering_efficiency": round((n_clustered / len(tlist)) * 100, 2)
                },
                "family_info": {
                    "unique_families": unique_families,
                    "has_family_labels": family_labels is not None
                },
                "summary": {
                    "zh": f"找到 {n_clusters} 個群集，{n_noise} 個雜訊點，分群效率 {round((n_clustered / len(tlist)) * 100, 2)}%",
                    "en": f"Found {n_clusters} clusters, {n_noise} noise points, clustering efficiency {round((n_clustered / len(tlist)) * 100, 2)}%"
                }
            }
            
            if self.verbose:
                print(f"  找到群集 / Clusters found: {n_clusters}")
                print(f"  雜訊點 / Noise points: {n_noise}")
                print(f"  分群效率 / Clustering efficiency: {result['results']['clustering_efficiency']}%")
            
            return result
            
        except Exception as e:
            raise ValueError(f"分析資料集時發生錯誤 / Error analyzing dataset: {str(e)}")
    
    def run_case_1_example(self) -> Dict:
        """執行案例 1 的預設範例 / Run default example for Case 1"""
        # 企業資料外洩情境範例 / Enterprise data leak scenario example
        original_data = '''
        {"customer_id": "CUST_12345", "name": "張小明", "email": "ming.zhang@email.com", 
         "phone": "+886-2-1234-5678", "address": "台北市信義區信義路五段7號", 
         "order_history": [{"order_id": "ORD_001", "product": "企業軟體授權", "amount": 8999.99}],
         "account_status": "active", "created_date": "2023-12-01"}
        ''' * 3
        
        modified_data = '''
        {"customer_id": "CUST_12345", "name": "張小明", "email": "ming.zhang@email.com", 
         "phone": "+886-2-1234-5678", "address": "台北市信義區信義路五段7號", 
         "order_history": [{"order_id": "ORD_001", "product": "企業軟體授權", "amount": 8999.99}],
         "account_status": "active", "created_date": "2023-12-01", "last_access": "2024-03-15"}
        ''' * 3
        
        return self.compare_two_texts(original_data, modified_data)
    
    def run_case_2_example(self) -> Dict:
        """執行案例 2 的預設範例 / Run default example for Case 2"""
        csv_file = "./data/mb_1K.csv"
        if os.path.exists(csv_file):
            return self.analyze_file_dataset(csv_file)
        else:
            # 如果檔案不存在，建立最小範例 / Create minimal example if file doesn't exist
            return {
                "case": "dataset_clustering",
                "csv_file": csv_file,
                "error": {
                    "zh": "找不到範例資料集。請提供包含 TLSH 資料的有效 CSV 檔案。",
                    "en": "Sample dataset not found. Please provide a valid CSV file with TLSH data."
                }
            }


def main():
    parser = argparse.ArgumentParser(
        description="TLSH 分析器 - 支援兩種 TLSH 使用案例的分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例 / Examples:

  案例 1 - 比較兩個文字 / Case 1 - Compare two texts:
    python tlsh_analyzer.py case1 --text1 "您的第一個文字..." --text2 "您的第二個文字..."
    python tlsh_analyzer.py case1 --example  # 使用內建範例 / Use built-in example

  案例 2 - 分析資料集 / Case 2 - Analyze dataset:
    python tlsh_analyzer.py case2 --csv data/mb_1K.csv
    python tlsh_analyzer.py case2 --example  # 使用內建範例 / Use built-in example
    python tlsh_analyzer.py case2 --csv data/mb_1K.csv --eps 20 --min_samples 3

  一般選項 / General options:
    --verbose    顯示詳細輸出 / Show detailed output
    --output     將結果保存為 JSON 檔案 / Save results to JSON file
        """)
    
    parser.add_argument('case', choices=['case1', 'case2'], 
                       help='選擇分析案例 / Choose analysis case')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='啟用詳細輸出 / Enable verbose output')
    parser.add_argument('--output', '-o', type=str, 
                       help='結果輸出檔案 (JSON) / Output file for results (JSON)')
    parser.add_argument('--example', action='store_true', 
                       help='執行內建範例 / Run built-in example')
    
    # 案例 1 專用參數 / Case 1 specific arguments
    parser.add_argument('--text1', type=str, help='比較的第一個文字 / First text for comparison')
    parser.add_argument('--text2', type=str, help='比較的第二個文字 / Second text for comparison')
    
    # 案例 2 專用參數 / Case 2 specific arguments
    parser.add_argument('--csv', type=str, help='包含 TLSH 資料的 CSV 檔案 / CSV file with TLSH data')
    parser.add_argument('--eps', type=int, default=30, help='DBSCAN eps 參數 (預設: 30) / DBSCAN eps parameter (default: 30)')
    parser.add_argument('--min_samples', type=int, default=2, help='DBSCAN min_samples 參數 (預設: 2) / DBSCAN min_samples parameter (default: 2)')
    
    args = parser.parse_args()
    
    analyzer = TLSHAnalyzer()
    analyzer.verbose = args.verbose
    
    try:
        if args.case == 'case1':
            if args.example:
                result = analyzer.run_case_1_example()
            elif args.text1 and args.text2:
                result = analyzer.compare_two_texts(args.text1, args.text2)
            else:
                print("錯誤：案例 1 需要 --text1 和 --text2 參數，或使用 --example")
                print("Error: Case 1 requires --text1 and --text2 arguments, or use --example")
                return 1
                
        elif args.case == 'case2':
            if args.example:
                result = analyzer.run_case_2_example()
            elif args.csv:
                result = analyzer.analyze_file_dataset(args.csv, args.eps, args.min_samples)
            else:
                print("錯誤：案例 2 需要 --csv 參數，或使用 --example")
                print("Error: Case 2 requires --csv argument, or use --example")
                return 1
        
        # 輸出結果 / Output results
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            if args.verbose:
                print(f"結果已儲存至 {args.output}")
                print(f"Results saved to {args.output}")
        
        if not args.verbose or not args.output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return 0
        
    except Exception as e:
        print(f"錯誤 / Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())