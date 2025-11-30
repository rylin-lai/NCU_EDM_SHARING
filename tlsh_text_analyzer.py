#!/usr/bin/env python3
"""
TLSH 文字分析工具 - 只支援文字相似性比較
TLSH Text Analyzer Tool - Text similarity comparison only

專注於企業資料外洩檢測的文字相似性分析
Focus on text similarity analysis for enterprise data leak detection
"""

import argparse
import sys
import json
import tlsh
from typing import Dict


class TLSHTextAnalyzer:
    """TLSH 文字分析器類別 (只支援文字比較) / TLSH Text Analyzer Class (text comparison only)"""
    
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
        比較兩個文字的相似性
        Compare similarity between two texts
        
        這個功能適用於企業資料外洩調查，可以快速判斷兩個檔案是否包含相同資料
        This function is suitable for enterprise data leak investigation,
        to quickly determine if two files contain the same data
        """
        if self.verbose:
            print("🔍 比較兩個文字字串的相似性")
            print("🔍 Comparing two text strings")
        
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
                "case": "text_comparison",
                "text1_length": len(text1),
                "text2_length": len(text2),
                "tlsh_hash1": hash1,
                "tlsh_hash2": hash2,
                "distance": distance,
                "similarity_class": similarity_class,
                "risk_level": risk_level,
                "interpretation": {
                    "zh": f"距離 {distance}: {similarity_class.split(' / ')[0]}，風險等級：{risk_level.split(' / ')[0]}",
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
    
    def run_example(self) -> Dict:
        """執行預設範例 / Run default example"""
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


def main():
    parser = argparse.ArgumentParser(
        description="TLSH 文字分析器 - 只支援文字相似性比較",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例 / Examples:

  比較兩個文字 / Compare two texts:
    python tlsh_text_analyzer.py --text1 "您的第一個文字..." --text2 "您的第二個文字..."
    python tlsh_text_analyzer.py --example  # 使用內建範例 / Use built-in example

  一般選項 / General options:
    --verbose    顯示詳細輸出 / Show detailed output
    --output     將結果保存為 JSON 檔案 / Save results to JSON file
        """)
    
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='啟用詳細輸出 / Enable verbose output')
    parser.add_argument('--output', '-o', type=str, 
                       help='結果輸出檔案 (JSON) / Output file for results (JSON)')
    parser.add_argument('--example', action='store_true', 
                       help='執行內建範例 / Run built-in example')
    
    # 文字比較參數 / Text comparison arguments
    parser.add_argument('--text1', type=str, help='比較的第一個文字 / First text for comparison')
    parser.add_argument('--text2', type=str, help='比較的第二個文字 / Second text for comparison')
    
    args = parser.parse_args()
    
    analyzer = TLSHTextAnalyzer()
    analyzer.verbose = args.verbose
    
    try:
        if args.example:
            result = analyzer.run_example()
        elif args.text1 and args.text2:
            result = analyzer.compare_two_texts(args.text1, args.text2)
        else:
            print("錯誤：需要 --text1 和 --text2 參數，或使用 --example")
            print("Error: Requires --text1 and --text2 arguments, or use --example")
            parser.print_help()
            return 1
        
        # 輸出結果 / Output results
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            if args.verbose:
                print(f"結果已儲存至 {args.output}")
                print(f"Results saved to {args.output}")
        
        if not args.output or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return 0
        
    except Exception as e:
        print(f"錯誤 / Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())