"""
熱度計算邏輯單元測試
測試 process_data.py 中的熱度密度計算功能
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch
import sys
import os

# 添加項目根目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from process_data import DataProcessor, PostMetrics

class TestHeatCalculation:
    """熱度計算測試類"""
    
    @pytest.fixture
    def processor(self):
        """創建測試用的數據處理器"""
        with patch('process_data.SupabaseManager'), \
             patch('process_data.jieba'), \
             patch('process_data.SentimentIntensityAnalyzer'):
            processor = DataProcessor()
            return processor
    
    @pytest.fixture
    def sample_posts_df(self):
        """創建測試用的貼文數據"""
        current_time = datetime.now(timezone.utc)
        
        # 創建不同時間點的測試數據
        data = {
            'post_id': ['post_1', 'post_2', 'post_3', 'post_4', 'post_5'],
            'username': ['user1', 'user2', 'user3', 'user4', 'user5'],
            'content': [
                '這是一篇很棒的文章，值得分享！',
                '短文',
                '這是一篇非常長的文章，包含了很多有趣的內容和觀點，希望大家喜歡並積極參與討論',
                '普通文章內容',
                '另一篇測試文章'
            ],
            'timestamp': [
                current_time - timedelta(hours=1),    # 1小時前
                current_time - timedelta(hours=6),    # 6小時前
                current_time - timedelta(hours=24),   # 24小時前
                current_time - timedelta(hours=48),   # 48小時前
                current_time - timedelta(minutes=30)  # 30分鐘前
            ],
            'likes': [100, 50, 200, 30, 80],
            'replies': [20, 10, 40, 5, 15],
            'reposts': [15, 5, 30, 2, 10],
            'total_interactions': [135, 65, 270, 37, 105]
        }
        
        return pd.DataFrame(data)
    
    def test_calculate_heat_density_basic(self, processor, sample_posts_df):
        """測試基本熱度密度計算"""
        result_df = processor.calculate_heat_density(sample_posts_df)
        
        # 檢查是否添加了必要的列
        assert 'heat_density' in result_df.columns
        assert 'time_decay' in result_df.columns
        assert 'base_heat' in result_df.columns
        assert 'length_factor' in result_df.columns
        
        # 檢查數據類型
        assert result_df['heat_density'].dtype == np.float64
        assert result_df['time_decay'].dtype == np.float64
        
        # 檢查值的範圍
        assert (result_df['heat_density'] >= 0).all()
        assert (result_df['heat_density'] <= 100).all()
        assert (result_df['time_decay'] > 0).all()
        assert (result_df['time_decay'] <= 1).all()
    
    def test_time_decay_calculation(self, processor, sample_posts_df):
        """測試時間衰減計算"""
        result_df = processor.calculate_heat_density(sample_posts_df)
        
        # 最新的貼文應該有最高的時間衰減因子
        newest_post_idx = result_df['hours_since_post'].idxmin()
        oldest_post_idx = result_df['hours_since_post'].idxmax()
        
        assert result_df.loc[newest_post_idx, 'time_decay'] > result_df.loc[oldest_post_idx, 'time_decay']
        
        # 檢查指數衰減公式是否正確應用
        for idx, row in result_df.iterrows():
            expected_decay = np.exp(-0.1 * row['hours_since_post'] / 24)
            assert abs(row['time_decay'] - expected_decay) < 1e-10
    
    def test_base_heat_calculation(self, processor, sample_posts_df):
        """測試基礎熱度分數計算"""
        result_df = processor.calculate_heat_density(sample_posts_df)
        
        # 檢查基礎熱度計算公式
        for idx, row in result_df.iterrows():
            expected_base_heat = (
                row['likes'] * 1.0 +
                row['replies'] * 2.0 +
                row['reposts'] * 1.5
            )
            assert abs(row['base_heat'] - expected_base_heat) < 1e-10
        
        # 回覆權重最高，轉發次之，讚最低
        high_reply_post = result_df[result_df['replies'] == 40].iloc[0]
        assert high_reply_post['base_heat'] > high_reply_post['likes'] + high_reply_post['reposts']
    
    def test_length_factor_calculation(self, processor, sample_posts_df):
        """測試內容長度因子計算"""
        result_df = processor.calculate_heat_density(sample_posts_df)
        
        # 檢查長度因子計算
        for idx, row in result_df.iterrows():
            expected_length_factor = np.log1p(len(row['content'])) / 10
            assert abs(row['length_factor'] - expected_length_factor) < 1e-10
        
        # 較長的內容應該有較高的長度因子
        longest_content_idx = result_df['content_length'].idxmax()
        shortest_content_idx = result_df['content_length'].idxmin()
        
        assert result_df.loc[longest_content_idx, 'length_factor'] > result_df.loc[shortest_content_idx, 'length_factor']
    
    def test_heat_density_normalization(self, processor, sample_posts_df):
        """測試熱度密度歸一化"""
        result_df = processor.calculate_heat_density(sample_posts_df)
        
        # 檢查歸一化結果
        assert result_df['heat_density'].max() <= 100
        assert result_df['heat_density'].min() >= 0
        
        # 最高熱度應該接近100（考慮浮點精度）
        assert result_df['heat_density'].max() >= 99.0
    
    def test_empty_dataframe(self, processor):
        """測試空數據框處理"""
        empty_df = pd.DataFrame()
        result_df = processor.calculate_heat_density(empty_df)
        
        assert result_df.empty
        assert len(result_df) == 0
    
    def test_single_post(self, processor):
        """測試單個貼文處理"""
        single_post_data = {
            'post_id': ['post_1'],
            'username': ['user1'],
            'content': ['測試文章'],
            'timestamp': [datetime.now(timezone.utc)],
            'likes': [10],
            'replies': [5],
            'reposts': [2],
            'total_interactions': [17]
        }
        
        single_df = pd.DataFrame(single_post_data)
        result_df = processor.calculate_heat_density(single_df)
        
        assert len(result_df) == 1
        assert 'heat_density' in result_df.columns
        assert result_df['heat_density'].iloc[0] == 100.0  # 唯一貼文應該得到最高分
    
    def test_zero_interactions(self, processor):
        """測試零互動貼文處理"""
        zero_interaction_data = {
            'post_id': ['post_1', 'post_2'],
            'username': ['user1', 'user2'],
            'content': ['文章1', '文章2'],
            'timestamp': [datetime.now(timezone.utc)] * 2,
            'likes': [0, 10],
            'replies': [0, 5],
            'reposts': [0, 2],
            'total_interactions': [0, 17]
        }
        
        df = pd.DataFrame(zero_interaction_data)
        result_df = processor.calculate_heat_density(df)
        
        # 零互動貼文應該有零熱度密度
        zero_interaction_post = result_df[result_df['total_interactions'] == 0]
        assert zero_interaction_post['heat_density'].iloc[0] == 0.0
    
    def test_extreme_values(self, processor):
        """測試極值處理"""
        extreme_data = {
            'post_id': ['post_1', 'post_2'],
            'username': ['user1', 'user2'],
            'content': ['短', 'a' * 10000],  # 極短和極長內容
            'timestamp': [
                datetime.now(timezone.utc),
                datetime.now(timezone.utc) - timedelta(days=365)  # 極舊貼文
            ],
            'likes': [0, 1000000],  # 極低和極高讚數
            'replies': [0, 100000],
            'reposts': [0, 50000],
            'total_interactions': [0, 1150000]
        }
        
        df = pd.DataFrame(extreme_data)
        result_df = processor.calculate_heat_density(df)
        
        # 確保沒有產生無窮大或NaN值
        assert not np.isinf(result_df['heat_density']).any()
        assert not result_df['heat_density'].isna().any()
        
        # 值仍在合理範圍內
        assert (result_df['heat_density'] >= 0).all()
        assert (result_df['heat_density'] <= 100).all()
    
    def test_missing_values(self, processor):
        """測試缺失值處理"""
        missing_data = {
            'post_id': ['post_1', 'post_2', 'post_3'],
            'username': ['user1', 'user2', 'user3'],
            'content': ['內容1', None, '內容3'],
            'timestamp': [datetime.now(timezone.utc)] * 3,
            'likes': [10, None, 30],
            'replies': [5, 15, None],
            'reposts': [2, 8, 12],
            'total_interactions': [17, 23, 42]
        }
        
        df = pd.DataFrame(missing_data)
        
        # 先進行數據清理（模擬主程序的處理）
        df['content'] = df['content'].fillna('')
        df['likes'] = df['likes'].fillna(0)
        df['replies'] = df['replies'].fillna(0)
        df['reposts'] = df['reposts'].fillna(0)
        
        result_df = processor.calculate_heat_density(df)
        
        # 確保處理後沒有NaN值
        assert not result_df['heat_density'].isna().any()
        assert not result_df['base_heat'].isna().any()
    
    def test_heat_density_consistency(self, processor):
        """測試熱度密度計算的一致性"""
        # 創建兩個相同的數據集
        data = {
            'post_id': ['post_1', 'post_2'],
            'username': ['user1', 'user2'],
            'content': ['測試內容1', '測試內容2'],
            'timestamp': [datetime.now(timezone.utc)] * 2,
            'likes': [50, 50],
            'replies': [10, 10],
            'reposts': [5, 5],
            'total_interactions': [65, 65]
        }
        
        df1 = pd.DataFrame(data)
        df2 = pd.DataFrame(data)
        
        result1 = processor.calculate_heat_density(df1)
        result2 = processor.calculate_heat_density(df2)
        
        # 相同輸入應該產生相同輸出
        pd.testing.assert_series_equal(
            result1['heat_density'], 
            result2['heat_density'], 
            check_names=False
        )
    
    def test_performance_with_large_dataset(self, processor):
        """測試大數據集性能"""
        # 創建較大的測試數據集
        n_posts = 1000
        current_time = datetime.now(timezone.utc)
        
        large_data = {
            'post_id': [f'post_{i}' for i in range(n_posts)],
            'username': [f'user_{i % 100}' for i in range(n_posts)],
            'content': [f'測試內容 {i}' * (i % 10 + 1) for i in range(n_posts)],
            'timestamp': [current_time - timedelta(hours=i % 72) for i in range(n_posts)],
            'likes': np.random.randint(0, 1000, n_posts),
            'replies': np.random.randint(0, 200, n_posts),
            'reposts': np.random.randint(0, 100, n_posts)
        }
        
        large_data['total_interactions'] = (
            large_data['likes'] + large_data['replies'] + large_data['reposts']
        )
        
        large_df = pd.DataFrame(large_data)
        
        import time
        start_time = time.time()
        result_df = processor.calculate_heat_density(large_df)
        end_time = time.time()
        
        # 檢查處理時間（應該在合理範圍內）
        processing_time = end_time - start_time
        assert processing_time < 5.0  # 5秒內完成
        
        # 檢查結果正確性
        assert len(result_df) == n_posts
        assert 'heat_density' in result_df.columns
        assert not result_df['heat_density'].isna().any()

# 集成測試
class TestHeatCalculationIntegration:
    """熱度計算集成測試"""
    
    @pytest.fixture
    def processor(self):
        """創建真實的數據處理器（需要環境配置）"""
        try:
            return DataProcessor()
        except Exception:
            pytest.skip("需要完整環境配置才能運行集成測試")
    
    def test_full_heat_calculation_pipeline(self, processor):
        """測試完整的熱度計算管道"""
        # 創建模擬真實場景的數據
        realistic_data = {
            'post_id': ['real_post_1', 'real_post_2', 'real_post_3'],
            'username': ['influencer1', 'regular_user', 'brand_account'],
            'content': [
                '🔥 今天分享一個超級實用的技巧！大家一定要看看 #技巧分享 #實用',
                '剛吃了一個很好吃的蛋糕',
                '我們公司最新產品上線了！歡迎大家試用並給我們反饋 https://example.com'
            ],
            'timestamp': [
                datetime.now(timezone.utc) - timedelta(hours=2),
                datetime.now(timezone.utc) - timedelta(hours=12),
                datetime.now(timezone.utc) - timedelta(hours=36)
            ],
            'likes': [500, 25, 150],
            'replies': [80, 3, 20],
            'reposts': [45, 1, 10],
            'total_interactions': [625, 29, 180]
        }
        
        df = pd.DataFrame(realistic_data)
        result_df = processor.calculate_heat_density(df)
        
        # 驗證結果符合預期
        assert len(result_df) == 3
        
        # 網紅帖子應該有最高熱度
        influencer_post = result_df[result_df['username'] == 'influencer1'].iloc[0]
        regular_post = result_df[result_df['username'] == 'regular_user'].iloc[0]
        
        assert influencer_post['heat_density'] > regular_post['heat_density']
        
        # 檢查所有必要欄位都存在
        required_columns = [
            'heat_density', 'base_heat', 'time_decay', 
            'length_factor', 'hours_since_post', 'content_length'
        ]
        
        for col in required_columns:
            assert col in result_df.columns

if __name__ == "__main__":
    # 運行測試
    pytest.main([__file__, "-v", "--tb=short"])