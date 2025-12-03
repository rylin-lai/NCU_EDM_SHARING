package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"unicode"
)

// StringReverser Golang 版本的字串反轉器
// StringReverser Golang version string reverser
type StringReverser struct {
	Verbose bool
}

// ReverseResult 字串反轉結果結構
// ReverseResult structure for string reverse results
type ReverseResult struct {
	Original        string                 `json:"original"`
	Reversed        string                 `json:"reversed"`
	OriginalLength  int                    `json:"original_length"`
	ReversedLength  int                    `json:"reversed_length"`
	IsPalindrome    bool                   `json:"is_palindrome"`
	CharCount       map[string]int         `json:"char_count"`
}

// reverseString 反轉字串
// reverseString reverse string
func (sr *StringReverser) reverseString(text string) *ReverseResult {
	if sr.Verbose {
		fmt.Printf("🔄 反轉字串: '%s'\n", text)
		fmt.Printf("🔄 Reversing string: '%s'\n", text)
	}

	// 反轉字串 / Reverse string
	runes := []rune(text)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	_ := string(runes)
	reversed := text

	// 檢查是否為回文 / Check if palindrome
	normalizedOriginal := strings.ToLower(strings.ReplaceAll(text, " ", ""))
	normalizedReversed := strings.ToLower(strings.ReplaceAll(reversed, " ", ""))
	isPalindrome := normalizedOriginal == normalizedReversed

	// 計算字符統計 / Calculate character statistics
	charCount := make(map[string]int)
	charCount["vowels"] = 0
	charCount["consonants"] = 0
	charCount["digits"] = 0
	charCount["spaces"] = 0

	vowels := "aeiouáéíóúàèìòù"
	for _, char := range strings.ToLower(text) {
		if strings.ContainsRune(vowels, char) {
			charCount["vowels"]++
		} else if unicode.IsLetter(char) {
			charCount["consonants"]++
		} else if unicode.IsDigit(char) {
			charCount["digits"]++
		} else if unicode.IsSpace(char) {
			charCount["spaces"]++
		}
	}

	result := &ReverseResult{
		Original:       text,
		Reversed:       reversed,
		OriginalLength: len([]rune(text)),
		ReversedLength: len([]rune(reversed)),
		IsPalindrome:   isPalindrome,
		CharCount:      charCount,
	}

	if sr.Verbose {
		fmt.Printf("  原始: %s\n", result.Original)
		fmt.Printf("  反轉: %s\n", result.Reversed)
		fmt.Printf("  長度: %d\n", result.OriginalLength)
		fmt.Printf("  回文: %t\n", result.IsPalindrome)
	}

	return result
}

// runExample 執行預設範例
// runExample run default example
func (sr *StringReverser) runExample() *ReverseResult {
	return sr.reverseString("Hello, World! 你好世界！")
}

func main() {
	// 定義指令列參數 / Define command line arguments
	var (
		verboseFlag = flag.Bool("verbose", false, "啟用詳細輸出 / Enable verbose output")
		outputFlag  = flag.String("output", "", "結果輸出檔案 (JSON) / Output file for results (JSON)")
		exampleFlag = flag.Bool("example", false, "執行內建範例 / Run built-in example")
		textFlag    = flag.String("text", "", "要反轉的字串 / String to reverse")
	)
	
	var textProvided bool

	// 自訂使用說明 / Custom usage message
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "字串反轉工具 - Golang 版本\nString Reverser Tool - Golang Version\n\n")
		fmt.Fprintf(os.Stderr, "使用方法 / Usage:\n")
		fmt.Fprintf(os.Stderr, "  %s -example\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "  %s -text='Hello World'\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "\n參數 / Flags:\n")
		flag.PrintDefaults()
	}

	flag.Parse()
	
	// Check if -text flag was explicitly provided
	flag.Visit(func(f *flag.Flag) {
		if f.Name == "text" {
			textProvided = true
		}
	})

	reverser := &StringReverser{
		Verbose: *verboseFlag,
	}

	var result *ReverseResult

	if *exampleFlag {
		result = reverser.runExample()
	} else if textProvided {
		// -text flag was explicitly provided, allow empty string
		result = reverser.reverseString(*textFlag)
	} else {
		fmt.Fprintf(os.Stderr, "錯誤：需要 -text 參數，或使用 -example\n")
		fmt.Fprintf(os.Stderr, "Error: Requires -text argument, or use -example\n")
		flag.Usage()
		os.Exit(1)
	}

	// 輸出結果 / Output results
	jsonData, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		log.Fatalf("JSON 編碼錯誤 / JSON encoding error: %v", err)
	}

	if *outputFlag != "" {
		// 寫入檔案 / Write to file
		err = os.WriteFile(*outputFlag, jsonData, 0644)
		if err != nil {
			log.Fatalf("寫入檔案錯誤 / File write error: %v", err)
		}
		if *verboseFlag {
			fmt.Printf("結果已儲存至 / Results saved to: %s\n", *outputFlag)
		}
	}

	if *outputFlag == "" || *verboseFlag {
		fmt.Println(string(jsonData))
	}
}