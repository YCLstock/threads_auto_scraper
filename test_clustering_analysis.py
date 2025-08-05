"""
聚類分析功能單元測試
測試 process_data.py 中的主題聚類分析功能
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# 添加項目根目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from process_data import DataProcessor, TopicSummary

class TestClusteringAnalysis:
    """聚類分析測試類"""
    
    @pytest.fixture
    def processor(self):
        """創建測試用的數據處理器"""
        with patch('process_data.SupabaseManager'), \
             patch('process_data.jieba'), \
             patch('process_data.SentimentIntensityAnalyzer'):
            processor = DataProcessor()
            return processor
    
    @pytest.fixture
    def sample_clustering_df(self):
        """創建聚類分析測試數據"""
        base_time = datetime.now(timezone.utc)
        
        # 創建不同主題的測試貼文
        data = []
        
        # 科技主題貼文
        tech_posts = [
            'AI人工智慧技術發展迅速',
            '機器學習算法優化方法',
            '深度學習神經網絡應用',
            '數據科學分析技術',
            '雲端計算平台服務'
        ]
        
        # 財經主題貼文
        finance_posts = [
            '股票投資策略分析',
            '加密貨幣市場趨勢',
            '房地產投資機會',
            '基金理財規劃建議',
            '經濟指標影響分析'
        ]
        
        # 生活主題貼文
        life_posts = [
            '健康飲食生活習慣',
            '運動健身計劃分享',
            '旅行攻略經驗分享',
            '美食餐廳推薦評價',
            '電影音樂娛樂推薦'
        ]
        
        all_posts = [
            (tech_posts, 'tech'),
            (finance_posts, 'finance'), 
            (life_posts, 'life')
        ]
        
        post_id = 0
        for posts_list, category in all_posts:
            for i, content in enumerate(posts_list):
                # 不同主題有不同的互動水平
                if category == 'tech':
                    base_interactions = 150
                elif category == 'finance':
                    base_interactions = 100
                else:  # life
                    base_interactions = 80
                
                likes = base_interactions + np.random.randint(-30, 50)
                replies = max(1, likes // 5 + np.random.randint(-5, 10))
                reposts = max(0, likes // 8 + np.random.randint(-3, 8))
                
                data.append({
                    'post_id': f'post_{post_id}',
                    'username': f'user_{category}_{i}',
                    'content': content,
                    'timestamp': base_time - timedelta(hours=np.random.randint(1, 72)),
                    'likes': likes,
                    'replies': replies,
                    'reposts': reposts,
                    'total_interactions': likes + replies + reposts,
                    'heat_density': np.random.uniform(20, 90),
                    'freshness_score': np.random.uniform(0.3, 1.0)
                })
                post_id += 1
        
        return pd.DataFrame(data)
    
    def test_perform_topic_clustering_basic(self, processor, sample_clustering_df):
        """測試基本主題聚類功能"""
        with patch('process_data.jieba.cut') as mock_cut, \
             patch.object(processor, '_analyze_cluster_sentiment') as mock_sentiment, \
             patch.object(processor, '_calculate_trending_score') as mock_trending:
            
            # Mock jieba 分詞
            mock_cut.side_effect = lambda text: text.split()
            mock_sentiment.return_value = 'positive'
            mock_trending.return_value = 0.7
            
            topics = processor.perform_topic_clustering(sample_clustering_df)
            
            # 檢查返回類型和基本結構
            assert isinstance(topics, list)
            
            for topic in topics:
                assert isinstance(topic, TopicSummary)
                assert hasattr(topic, 'topic_id')
                assert hasattr(topic, 'topic_keywords')
                assert hasattr(topic, 'topic_name')
                assert hasattr(topic, 'post_count')
                assert hasattr(topic, 'average_heat_density')
                assert hasattr(topic, 'total_interactions')
                assert hasattr(topic, 'dominant_sentiment')
                assert hasattr(topic, 'trending_score')
                
                # 檢查數據類型
                assert isinstance(topic.topic_id, int)
                assert isinstance(topic.topic_keywords, list)
                assert isinstance(topic.topic_name, str)
                assert isinstance(topic.post_count, int)
                assert isinstance(topic.average_heat_density, (int, float))
                assert isinstance(topic.total_interactions, int)
                assert isinstance(topic.dominant_sentiment, str)
                assert isinstance(topic.trending_score, (int, float))
                
                # 檢查數據合理性
                assert topic.topic_id > 0
                assert len(topic.topic_keywords) > 0
                assert topic.post_count > 0
                assert topic.total_interactions >= 0
                assert 0 <= topic.trending_score <= 1
    
    def test_clustering_insufficient_data(self, processor):
        """測試數據不足時的聚類行為"""
        # 創建數據量不足的測試數據
        insufficient_data = pd.DataFrame({
            'post_id': ['post_1', 'post_2'],
            'content': ['短文本1', '短文本2'],
            'total_interactions': [5, 3],  # 低於閾值
            'heat_density': [10, 8],
            'freshness_score': [0.5, 0.6]
        })
        
        topics = processor.perform_topic_clustering(insufficient_data)
        
        # 數據不足時應該返回空列表
        assert isinstance(topics, list)
        assert len(topics) == 0
    
    def test_clustering_empty_dataframe(self, processor):
        """測試空數據框的聚類處理"""
        empty_df = pd.DataFrame()
        topics = processor.perform_topic_clustering(empty_df)
        
        assert isinstance(topics, list)
        assert len(topics) == 0
    
    def test_generate_topic_name(self, processor):
        """測試主題名稱生成功能"""
        # 測試科技類關鍵詞
        tech_keywords = ['AI', '人工智慧', '技術', '數據']
        tech_contents = ['AI技術發展', '數據分析應用']
        tech_name = processor._generate_topic_name(tech_keywords, tech_contents)
        
        assert isinstance(tech_name, str)
        assert len(tech_name) > 0
        assert 'AI' in tech_name or '科技' in tech_name
        
        # 測試財經類關鍵詞
        finance_keywords = ['投資', '股票', '金融', '市場']
        finance_contents = ['投資策略', '股票分析']
        finance_name = processor._generate_topic_name(finance_keywords, finance_contents)
        
        assert isinstance(finance_name, str)
        assert len(finance_name) > 0
        
        # 測試空關鍵詞
        empty_name = processor._generate_topic_name([], [])
        assert empty_name == "未知主題"
    
    def test_analyze_cluster_sentiment(self, processor):
        """測試聚類情感分析"""
        # 測試正面內容
        positive_contents = ['這個產品真的很棒！', '非常推薦大家', '效果超乎預期']
        
        # Mock 情感分析器
        with patch.object(processor, 'sentiment_analyzer') as mock_analyzer:
            mock_analyzer.polarity_scores.side_effect = [
                {'compound': 0.8}, {'compound': 0.7}, {'compound': 0.9}
            ]
            
            sentiment = processor._analyze_cluster_sentiment(positive_contents)
            assert sentiment in ['positive', 'negative', 'neutral']
        
        # 測試無情感分析器的情況
        processor.sentiment_analyzer = None
        sentiment = processor._analyze_cluster_sentiment(positive_contents)
        assert sentiment == 'neutral'
        
        # 測試空內容
        sentiment = processor._analyze_cluster_sentiment([])
        assert sentiment == 'neutral'
    
    def test_calculate_trending_score(self, processor):
        """測試趨勢分數計算"""
        current_time = datetime.now(timezone.utc)
        
        # 創建測試聚類數據
        cluster_data = pd.DataFrame({
            'timestamp': [
                current_time - timedelta(hours=6),
                current_time - timedelta(hours=3),
                current_time - timedelta(hours=1)
            ],
            'total_interactions': [100, 150, 200],
            'freshness_score': [0.7, 0.8, 0.9]
        })
        
        score = processor._calculate_trending_score(cluster_data)
        
        assert isinstance(score, (int, float))
        assert 0 <= score <= 1.0
        
        # 測試單條記錄
        single_record = pd.DataFrame({
            'timestamp': [current_time],
            'total_interactions': [100],
            'freshness_score': [0.8]
        })
        
        single_score = processor._calculate_trending_score(single_record)
        assert single_score == 0.0
        
        # 測試空數據框
        empty_df = pd.DataFrame(columns=['timestamp', 'total_interactions', 'freshness_score'])
        empty_score = processor._calculate_trending_score(empty_df)
        assert empty_score == 0.0
    
    def test_clustering_with_different_thresholds(self, processor, sample_clustering_df):
        """測試不同閾值下的聚類結果"""
        original_threshold = processor.min_interactions_threshold
        
        try:
            # 測試高閾值
            processor.min_interactions_threshold = 1000  # 很高的閾值
            with patch('process_data.jieba.cut') as mock_cut:
                mock_cut.side_effect = lambda text: text.split()
                topics_high = processor.perform_topic_clustering(sample_clustering_df)
                
            # 高閾值下應該沒有或很少聚類結果
            assert isinstance(topics_high, list)
            
            # 測試低閾值
            processor.min_interactions_threshold = 1  # 很低的閾值
            with patch('process_data.jieba.cut') as mock_cut, \
                 patch.object(processor, '_analyze_cluster_sentiment') as mock_sentiment, \
                 patch.object(processor, '_calculate_trending_score') as mock_trending:
                
                mock_cut.side_effect = lambda text: text.split()
                mock_sentiment.return_value = 'positive'
                mock_trending.return_value = 0.5
                
                topics_low = processor.perform_topic_clustering(sample_clustering_df)
            
            # 低閾值下應該有更多聚類結果
            assert isinstance(topics_low, list)
            
        finally:
            # 恢復原始閾值
            processor.min_interactions_threshold = original_threshold
    
    def test_clustering_with_different_cluster_numbers(self, processor, sample_clustering_df):
        """測試不同聚類數量的影響"""
        original_max_topics = processor.max_topics
        
        try:
            # 測試較少的聚類數
            processor.max_topics = 2
            with patch('process_data.jieba.cut') as mock_cut, \
                 patch.object(processor, '_analyze_cluster_sentiment') as mock_sentiment, \
                 patch.object(processor, '_calculate_trending_score') as mock_trending:
                
                mock_cut.side_effect = lambda text: text.split()
                mock_sentiment.return_value = 'neutral'
                mock_trending.return_value = 0.6
                
                topics = processor.perform_topic_clustering(sample_clustering_df)
            
            assert isinstance(topics, list)
            if len(topics) > 0:
                assert len(topics) <= 2
            
        finally:
            # 恢復原始設置
            processor.max_topics = original_max_topics
    
    def test_clustering_error_handling(self, processor, sample_clustering_df):
        """測試聚類過程中的錯誤處理"""
        with patch('process_data.jieba.cut') as mock_cut:
            # 模擬 jieba 分詞錯誤
            mock_cut.side_effect = Exception("分詞錯誤")
            
            topics = processor.perform_topic_clustering(sample_clustering_df)
            
            # 即使出錯也應該返回空列表，不應該拋出異常
            assert isinstance(topics, list)
    
    def test_clustering_with_special_characters(self, processor):
        """測試包含特殊字符的文本聚類"""
        special_data = pd.DataFrame({
            'post_id': [f'post_{i}' for i in range(5)],
            'username': [f'user_{i}' for i in range(5)],
            'content': [
                '這是包含emoji的文本😊👍',
                'Text with English and 中文混合',
                '@用戶名 #標籤 https://example.com',
                '數字123和符號!@#$%^&*()',
                '   空白   和   間距   '
            ],
            'total_interactions': [100, 120, 80, 90, 110],
            'heat_density': [50, 60, 40, 45, 55],
            'freshness_score': [0.8, 0.7, 0.9, 0.6, 0.8]
        })
        
        with patch('process_data.jieba.cut') as mock_cut, \
             patch.object(processor, '_analyze_cluster_sentiment') as mock_sentiment, \
             patch.object(processor, '_calculate_trending_score') as mock_trending:
            
            mock_cut.side_effect = lambda text: ['文本', '內容', '測試']
            mock_sentiment.return_value = 'neutral'
            mock_trending.return_value = 0.5
            
            topics = processor.perform_topic_clustering(special_data)
            
            # 應該能正常處理特殊字符
            assert isinstance(topics, list)
    
    def test_clustering_keyword_extraction_integration(self, processor, sample_clustering_df):
        """測試聚類與關鍵詞提取的集成"""
        with patch('process_data.jieba.cut') as mock_cut, \
             patch('process_data.TfidfVectorizer') as mock_vectorizer, \
             patch.object(processor, '_analyze_cluster_sentiment') as mock_sentiment, \
             patch.object(processor, '_calculate_trending_score') as mock_trending:
            
            # Mock TF-IDF 向量化器
            mock_tfidf_instance = MagicMock()
            mock_vectorizer.return_value = mock_tfidf_instance
            
            # 模擬向量化結果
            mock_tfidf_matrix = MagicMock()
            mock_tfidf_instance.fit_transform.return_value = mock_tfidf_matrix
            mock_tfidf_instance.get_feature_names_out.return_value = ['AI', '技術', '投資', '市場', '生活']
            
            # Mock K-means 聚類
            with patch('process_data.KMeans') as mock_kmeans:
                mock_kmeans_instance = MagicMock()
                mock_kmeans.return_value = mock_kmeans_instance
                
                # 模擬聚類結果
                mock_kmeans_instance.fit_predict.return_value = np.array([0, 0, 1, 1, 2])
                mock_kmeans_instance.cluster_centers_ = np.array([
                    [0.8, 0.6, 0.1, 0.1, 0.1],  # 科技聚類中心
                    [0.1, 0.1, 0.8, 0.6, 0.1],  # 財經聚類中心
                    [0.1, 0.1, 0.1, 0.1, 0.8]   # 生活聚類中心
                ])
                
                mock_cut.side_effect = lambda text: text.split()
                mock_sentiment.return_value = 'positive'
                mock_trending.return_value = 0.7
                
                topics = processor.perform_topic_clustering(sample_clustering_df)
                
                assert isinstance(topics, list)
                if len(topics) > 0:
                    for topic in topics:
                        assert len(topic.topic_keywords) > 0
                        assert all(isinstance(kw, str) for kw in topic.topic_keywords)

# 性能測試類
class TestClusteringPerformance:
    """聚類分析性能測試"""
    
    @pytest.fixture
    def processor(self):
        """創建測試用的數據處理器"""
        with patch('process_data.SupabaseManager'), \
             patch('process_data.jieba'), \
             patch('process_data.SentimentIntensityAnalyzer'):
            return DataProcessor()
    
    def test_clustering_performance_large_dataset(self, processor):
        """測試大數據集的聚類性能"""
        # 創建較大的測試數據集
        n_posts = 1000
        current_time = datetime.now(timezone.utc)
        
        large_data = pd.DataFrame({
            'post_id': [f'post_{i}' for i in range(n_posts)],
            'username': [f'user_{i % 100}' for i in range(n_posts)],
            'content': [f'測試內容 {i % 10}' for i in range(n_posts)],
            'timestamp': [current_time - timedelta(hours=i % 72) for i in range(n_posts)],
            'total_interactions': np.random.randint(50, 500, n_posts),
            'heat_density': np.random.uniform(20, 90, n_posts),
            'freshness_score': np.random.uniform(0.3, 1.0, n_posts)
        })
        
        with patch('process_data.jieba.cut') as mock_cut, \
             patch.object(processor, '_analyze_cluster_sentiment') as mock_sentiment, \
             patch.object(processor, '_calculate_trending_score') as mock_trending:
            
            mock_cut.side_effect = lambda text: text.split()
            mock_sentiment.return_value = 'neutral'
            mock_trending.return_value = 0.5
            
            import time
            start_time = time.time()
            topics = processor.perform_topic_clustering(large_data)
            end_time = time.time()
            
            # 檢查處理時間（應該在合理範圍內）
            processing_time = end_time - start_time
            assert processing_time < 30.0  # 30秒內完成
            
            # 檢查結果
            assert isinstance(topics, list)

if __name__ == "__main__":
    # 運行測試
    pytest.main([__file__, "-v", "--tb=short"])