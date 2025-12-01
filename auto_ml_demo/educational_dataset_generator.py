#!/usr/bin/env python3
"""
Educational Dataset Generator - Production Version
基於Week12的教育資料集生成器 - 生產版本

這個腳本會生成與Week12相同結構的教育資料集，但加入了更多變化和現實性
This script generates educational datasets with the same structure as Week12 but with more variation and realism
"""

import numpy as np
import pandas as pd
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import sys


class EducationalDataGenerator:
    """教育資料生成器 / Educational Data Generator"""
    
    def __init__(self, seed=42):
        """
        初始化生成器
        Initialize generator
        
        Args:
            seed: 隨機種子，確保結果可重現 / Random seed for reproducibility
        """
        np.random.seed(seed)
        self.seed = seed
    
    def generate_student_data(self, n_students=300, semester="2024_Fall"):
        """
        生成學生學習資料
        Generate student learning data
        
        Args:
            n_students: 學生數量 / Number of students
            semester: 學期標識 / Semester identifier
        
        Returns:
            DataFrame: 包含學生資料的 DataFrame / DataFrame containing student data
        """
        
        # 設置不同的參數讓資料更真實 / Set parameters for more realistic data
        help_seeking = np.random.poisson(lam=4, size=n_students)
        help_seeking = np.clip(help_seeking, 0, 10)

        # 前測分數 - 加入一些偏差 / Pretest scores with some bias
        pretest_score = np.clip(np.random.normal(loc=70, scale=12, size=n_students), 0, 100)
        
        # 影片觀看時間 - 受到前測分數影響 / Video hours influenced by pretest score
        video_hours = np.clip(
            np.random.normal(loc=5 + (pretest_score - 70) * 0.02, scale=2, size=n_students), 
            0, None
        )
        
        # 作業分數 - 受多個因素影響 / Assignment score influenced by multiple factors
        assignment_base = 60 + 0.2 * pretest_score + 2 * help_seeking + np.random.normal(0, 8, n_students)
        assignment_score = np.clip(assignment_base, 0, 100)

        # 入學方式 - 現實的分布 / Admission type with realistic distribution
        admission_types = np.random.choice(
            ['Recommendation', 'Exam', 'Special'],
            size=n_students,
            p=[0.4, 0.45, 0.15]
        )
        
        # 新增：學習風格資料 / New: Learning style data
        learning_styles = np.random.choice(
            ['Visual', 'Auditory', 'Kinesthetic', 'Reading'],
            size=n_students,
            p=[0.35, 0.25, 0.25, 0.15]
        )
        
        # 新增：出席率 / New: Attendance rate
        attendance_rate = np.random.beta(a=8, b=2, size=n_students)  # 偏向高出席率
        attendance_rate = np.clip(attendance_rate, 0.3, 1.0)
        
        # 通過課程的邏輯函數 - 更複雜的模型 / Pass course logic - more complex model
        logit = (
            -6
            + 0.25 * help_seeking
            + 0.035 * pretest_score
            + 0.025 * assignment_score
            + 3 * attendance_rate
            + 0.1 * (admission_types == 'Recommendation').astype(int)
            + 0.05 * (admission_types == 'Special').astype(int)
            + 0.5 * (learning_styles == 'Visual').astype(int)
        )
        prob_pass = 1 / (1 + np.exp(-logit))
        pass_course = (np.random.rand(n_students) < prob_pass).astype(int)
        
        # 建立 DataFrame / Create DataFrame
        df = pd.DataFrame({
            'student_id': [f"{semester}_STU_{i:04d}" for i in range(n_students)],
            'semester': semester,
            'HelpSeeking': help_seeking.astype(int),
            'Pretest_score': np.round(pretest_score, 2),
            'Video_hours': np.round(video_hours, 2),
            'Assignment_score': np.round(assignment_score, 2),
            'Attendance_rate': np.round(attendance_rate, 3),
            'Admission_type': admission_types,
            'Learning_style': learning_styles,
            'Pass_course': pass_course,
            'generated_at': datetime.now().isoformat()
        })
        
        return df
    
    def generate_time_series_data(self, n_students=100, weeks=16):
        """
        生成時間序列學習資料（週別追蹤）
        Generate time series learning data (weekly tracking)
        """
        
        data_rows = []
        
        for student_id in range(n_students):
            # 學生基本特性 / Student base characteristics
            base_engagement = np.random.normal(0.7, 0.2)
            base_ability = np.random.normal(0.6, 0.15)
            
            for week in range(1, weeks + 1):
                # 週別活動會有趨勢和波動 / Weekly activities with trends and fluctuations
                week_factor = max(0.1, 1 - week * 0.05)  # 學期末活動下降
                
                help_requests = max(0, int(np.random.poisson(
                    lam=base_engagement * week_factor * 3
                )))
                
                video_minutes = max(0, np.random.normal(
                    loc=base_engagement * week_factor * 180, 
                    scale=60
                ))
                
                quiz_score = np.clip(
                    np.random.normal(
                        loc=base_ability * 85 + help_requests * 2, 
                        scale=12
                    ), 0, 100
                )
                
                data_rows.append({
                    'student_id': f"TS_STU_{student_id:04d}",
                    'week': week,
                    'help_requests': help_requests,
                    'video_minutes': int(video_minutes),
                    'quiz_score': round(quiz_score, 1),
                    'engagement_level': round(base_engagement * week_factor, 3)
                })
        
        return pd.DataFrame(data_rows)
    
    def save_dataset(self, df, filepath, metadata=None):
        """
        儲存資料集並生成元資料
        Save dataset and generate metadata
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # 儲存主要資料 / Save main data
        df.to_csv(filepath, index=False)
        
        # 生成元資料 / Generate metadata
        metadata = metadata or {}
        metadata.update({
            'filename': str(filepath.name),
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'generated_at': datetime.now().isoformat(),
            'generator_seed': self.seed,
            'summary_stats': {
                col: {
                    'mean': float(df[col].mean()) if df[col].dtype in ['int64', 'float64'] else None,
                    'std': float(df[col].std()) if df[col].dtype in ['int64', 'float64'] else None,
                    'min': float(df[col].min()) if df[col].dtype in ['int64', 'float64'] else None,
                    'max': float(df[col].max()) if df[col].dtype in ['int64', 'float64'] else None,
                    'unique_values': int(df[col].nunique())
                }
                for col in df.columns if col != 'generated_at'
            }
        })
        
        # 儲存元資料 / Save metadata
        metadata_path = filepath.with_suffix('.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dataset saved: {filepath}")
        print(f"✅ Metadata saved: {metadata_path}")
        print(f"📊 Shape: {df.shape}")
        
        return filepath, metadata_path


def main():
    """主要執行函數 / Main execution function"""
    
    parser = argparse.ArgumentParser(
        description="Educational Dataset Generator - 教育資料集生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例 / Examples:

  基本生成 / Basic generation:
    python educational_dataset_generator.py

  自訂參數 / Custom parameters:
    python educational_dataset_generator.py --students 500 --semester 2024_Spring
    
  生成時間序列資料 / Generate time series data:
    python educational_dataset_generator.py --timeseries --students 200 --weeks 12
    
  指定輸出目錄 / Specify output directory:
    python educational_dataset_generator.py --output data/custom/
        """)
    
    parser.add_argument('--students', '-n', type=int, default=300,
                       help='學生數量 / Number of students (default: 300)')
    parser.add_argument('--semester', '-s', type=str, default="2024_Fall",
                       help='學期標識 / Semester identifier (default: 2024_Fall)')
    parser.add_argument('--output', '-o', type=str, default="data/",
                       help='輸出目錄 / Output directory (default: data/)')
    parser.add_argument('--seed', type=int, default=42,
                       help='隨機種子 / Random seed (default: 42)')
    parser.add_argument('--timeseries', action='store_true',
                       help='生成時間序列資料 / Generate time series data')
    parser.add_argument('--weeks', type=int, default=16,
                       help='時間序列週數 / Number of weeks for time series (default: 16)')
    parser.add_argument('--both', action='store_true',
                       help='同時生成兩種資料集 / Generate both dataset types')
    
    args = parser.parse_args()
    
    # 初始化生成器 / Initialize generator
    generator = EducationalDataGenerator(seed=args.seed)
    
    try:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if args.timeseries or args.both:
            print("🔄 Generating time series dataset...")
            print("🔄 正在生成時間序列資料集...")
            
            ts_df = generator.generate_time_series_data(
                n_students=args.students, 
                weeks=args.weeks
            )
            
            ts_filepath = output_dir / f"educational_timeseries_{args.semester}.csv"
            generator.save_dataset(
                ts_df, 
                ts_filepath, 
                metadata={
                    'dataset_type': 'time_series',
                    'weeks': args.weeks,
                    'description': 'Weekly student learning activity tracking data'
                }
            )
        
        if not args.timeseries or args.both:
            print("\n🔄 Generating cross-sectional dataset...")
            print("🔄 正在生成橫斷面資料集...")
            
            df = generator.generate_student_data(
                n_students=args.students,
                semester=args.semester
            )
            
            cs_filepath = output_dir / f"educational_data_{args.semester}.csv"
            generator.save_dataset(
                df, 
                cs_filepath,
                metadata={
                    'dataset_type': 'cross_sectional',
                    'semester': args.semester,
                    'description': 'Student performance and characteristics data for machine learning'
                }
            )
        
        print(f"\n✅ All datasets generated successfully!")
        print(f"✅ 所有資料集生成成功！")
        print(f"📁 Output directory: {output_dir.absolute()}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating datasets: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())