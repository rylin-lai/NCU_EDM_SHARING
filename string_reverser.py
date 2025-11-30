#!/usr/bin/env python3
"""
簡單字串反轉工具 - Python 版本
Simple String Reverser Tool - Python Version

這是一個簡單的範例，用來展示 Python POC → Golang production → Python test 的流程
This is a simple example to demonstrate Python POC → Golang production → Python test workflow
"""

import argparse
import sys
import json


class StringReverser:
    """字串反轉器類別 / String Reverser Class"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def reverse_string(self, text: str) -> dict:
        """
        反轉字串
        Reverse string
        
        Args:
            text: 輸入字串 / Input string
        Returns:
            包含原始字串、反轉字串和統計資訊的字典 / Dict with original, reversed string and stats
        """
        if self.verbose:
            print(f"🔄 反轉字串: '{text}'")
            print(f"🔄 Reversing string: '{text}'")
        
        reversed_text = text[::-1]
        
        result = {
            "original": text,
            "reversed": reversed_text,
            "original_length": len(text),
            "reversed_length": len(reversed_text),
            "is_palindrome": text.lower().replace(" ", "") == reversed_text.lower().replace(" ", ""),
            "char_count": {
                "vowels": sum(1 for c in text.lower() if c in 'aeiouáéíóúàèìòù'),
                "consonants": sum(1 for c in text.lower() if c.isalpha() and c not in 'aeiouáéíóúàèìòù'),
                "digits": sum(1 for c in text if c.isdigit()),
                "spaces": sum(1 for c in text if c.isspace())
            }
        }
        
        if self.verbose:
            print(f"  原始: {result['original']}")
            print(f"  反轉: {result['reversed']}")
            print(f"  長度: {result['original_length']}")
            print(f"  回文: {result['is_palindrome']}")
        
        return result
    
    def run_example(self) -> dict:
        """執行預設範例 / Run default example"""
        return self.reverse_string("Hello, World! 你好世界！")


def main():
    parser = argparse.ArgumentParser(
        description="字串反轉工具 - Python 版本 / String Reverser Tool - Python Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例 / Examples:

  反轉字串 / Reverse string:
    python string_reverser.py --text "Hello World"
    python string_reverser.py --example  # 使用內建範例 / Use built-in example

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
    parser.add_argument('--text', type=str, 
                       help='要反轉的字串 / String to reverse')
    
    args = parser.parse_args()
    
    reverser = StringReverser(verbose=args.verbose)
    
    try:
        if args.example:
            result = reverser.run_example()
        elif args.text:
            result = reverser.reverse_string(args.text)
        else:
            print("錯誤：需要 --text 參數，或使用 --example")
            print("Error: Requires --text argument, or use --example")
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