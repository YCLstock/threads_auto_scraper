"""
Supabase 數據庫集成測試
測試與 Supabase 數據庫的集成功能
"""

import pytest
import os
import json
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, MagicMock
from typing import List

from database import SupabaseManager
from scraper import ThreadsPost

# 測試專用的環境變數
TEST_SUPABASE_URL = "https://test-project.supabase.co"
TEST_SUPABASE_KEY = "test-anon-key"

class TestSupabaseManager:
    """測試 SupabaseManager 類"""
    
    @pytest.fixture
    def mock_supabase_client(self):
        """創建模擬的 Supabase 客戶端"""
        with patch('database.create_client') as mock_create:
            mock_client = Mock()
            mock_create.return_value = mock_client
            yield mock_client
    
    @pytest.fixture
    def db_manager(self, mock_supabase_client):
        """創建測試用的數據庫管理器"""
        with patch.dict(os.environ, {
            'SUPABASE_URL': TEST_SUPABASE_URL,
            'SUPABASE_KEY': TEST_SUPABASE_KEY
        }):
            return SupabaseManager()
    
    @pytest.fixture
    def sample_post(self):
        """創建測試用的貼文對象"""
        return ThreadsPost(
            post_id="test_post_123",
            username="testuser",
            content="這是一個測試貼文內容",
            timestamp="2025-08-05T12:00:00Z",
            likes=25,
            replies=5,
            reposts=3,
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
            post_url="https://threads.com/@testuser/post/test_post_123",
            scraped_at="2025-08-05T12:30:00Z"
        )
    
    def test_init_success(self, mock_supabase_client):
        """測試 SupabaseManager 成功初始化"""
        with patch.dict(os.environ, {
            'SUPABASE_URL': TEST_SUPABASE_URL,
            'SUPABASE_KEY': TEST_SUPABASE_KEY
        }):
            manager = SupabaseManager()
            assert manager.url == TEST_SUPABASE_URL
            assert manager.key == TEST_SUPABASE_KEY
            assert manager.client is not None
    
    def test_init_missing_env_vars(self):
        """測試缺少環境變數時的初始化失敗"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="SUPABASE_URL 和 SUPABASE_KEY 環境變數必須設置"):
                SupabaseManager()
    
    def test_insert_raw_post_success(self, db_manager, sample_post, mock_supabase_client):
        """測試成功插入單個貼文"""
        # 模擬成功的插入響應
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.upsert.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[{'post_id': 'test_post_123'}])
        
        result = db_manager.insert_raw_post(sample_post)
        
        assert result is True
        mock_supabase_client.table.assert_called_with('raw_posts')
        mock_table.upsert.assert_called_once()
        mock_table.execute.assert_called_once()
    
    def test_insert_raw_post_failure(self, db_manager, sample_post, mock_supabase_client):
        """測試插入貼文失敗"""
        # 模擬插入失敗
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.upsert.return_value = mock_table
        mock_table.execute.return_value = Mock(data=None)
        
        result = db_manager.insert_raw_post(sample_post)
        
        assert result is False
    
    def test_insert_raw_post_exception(self, db_manager, sample_post, mock_supabase_client):
        """測試插入貼文時發生異常"""
        # 模擬異常
        mock_supabase_client.table.side_effect = Exception("Database error")
        
        result = db_manager.insert_raw_post(sample_post)
        
        assert result is False
    
    def test_insert_raw_posts_batch_success(self, db_manager, mock_supabase_client):
        """測試批量插入貼文成功"""
        # 創建測試貼文列表
        posts = [
            ThreadsPost(
                post_id=f"test_post_{i}",
                username=f"user{i}",
                content=f"測試內容 {i}",
                timestamp="2025-08-05T12:00:00Z",
                likes=i * 10,
                replies=i * 2,
                reposts=i,
                images=[],
                post_url=f"https://threads.com/@user{i}/post/test_post_{i}",
                scraped_at="2025-08-05T12:30:00Z"
            )
            for i in range(1, 4)
        ]
        
        # 模擬成功的批量插入
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.upsert.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[
            {'post_id': 'test_post_1'},
            {'post_id': 'test_post_2'},
            {'post_id': 'test_post_3'}
        ])
        
        result = db_manager.insert_raw_posts_batch(posts)
        
        assert result['success'] == 3
        assert result['failure'] == 0
    
    def test_insert_raw_posts_batch_empty_list(self, db_manager):
        """測試批量插入空列表"""
        result = db_manager.insert_raw_posts_batch([])
        
        assert result['success'] == 0
        assert result['failure'] == 0
    
    def test_get_existing_post_ids(self, db_manager, mock_supabase_client):
        """測試獲取已存在的貼文ID"""
        test_ids = ["post1", "post2", "post3"]
        
        # 模擬查詢結果
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.in_.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[
            {'post_id': 'post1'},
            {'post_id': 'post3'}
        ])
        
        existing_ids = db_manager.get_existing_post_ids(test_ids)
        
        assert len(existing_ids) == 2
        assert 'post1' in existing_ids
        assert 'post3' in existing_ids
        assert 'post2' not in existing_ids
    
    def test_get_existing_post_ids_empty_list(self, db_manager):
        """測試傳入空列表時獲取已存在的貼文ID"""
        existing_ids = db_manager.get_existing_post_ids([])
        assert existing_ids == []
    
    def test_get_posts_by_username(self, db_manager, mock_supabase_client):
        """測試根據用戶名獲取貼文"""
        username = "testuser"
        
        # 模擬查詢結果
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.order.return_value = mock_table
        mock_table.limit.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[
            {
                'post_id': 'post1',
                'username': 'testuser',
                'content': '測試內容1',
                'likes': 10
            },
            {
                'post_id': 'post2',
                'username': 'testuser',
                'content': '測試內容2',
                'likes': 20
            }
        ])
        
        posts = db_manager.get_posts_by_username(username)
        
        assert len(posts) == 2
        assert posts[0]['username'] == 'testuser'
        assert posts[1]['username'] == 'testuser'
    
    def test_get_posts_by_date_range(self, db_manager, mock_supabase_client):
        """測試根據日期範圍獲取貼文"""
        start_date = datetime(2025, 8, 1, tzinfo=timezone.utc)
        end_date = datetime(2025, 8, 5, tzinfo=timezone.utc)
        
        # 模擬查詢結果
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.gte.return_value = mock_table
        mock_table.lte.return_value = mock_table
        mock_table.order.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[
            {
                'post_id': 'post1',
                'timestamp': '2025-08-03T12:00:00Z',
                'content': '範圍內的貼文'
            }
        ])
        
        posts = db_manager.get_posts_by_date_range(start_date, end_date)
        
        assert len(posts) == 1
        assert posts[0]['post_id'] == 'post1'
    
    def test_get_posts_count(self, db_manager, mock_supabase_client):
        """測試獲取貼文總數"""
        # 模擬計數查詢結果
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.execute.return_value = Mock(count=150)
        
        count = db_manager.get_posts_count()
        
        assert count == 150
    
    def test_delete_post_success(self, db_manager, mock_supabase_client):
        """測試成功刪除貼文"""
        post_id = "test_post_123"
        
        # 模擬成功刪除
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.delete.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[{'post_id': post_id}])
        
        result = db_manager.delete_post(post_id)
        
        assert result is True
    
    def test_delete_post_not_found(self, db_manager, mock_supabase_client):
        """測試刪除不存在的貼文"""
        post_id = "nonexistent_post"
        
        # 模擬刪除不存在的貼文
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.delete.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = Mock(data=None)
        
        result = db_manager.delete_post(post_id)
        
        assert result is False
    
    def test_test_connection_success(self, db_manager, mock_supabase_client):
        """測試數據庫連接成功"""
        # 模擬成功的連接測試
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        mock_table.select.return_value = mock_table
        mock_table.limit.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[])
        
        result = db_manager.test_connection()
        
        assert result is True
    
    def test_test_connection_failure(self, db_manager, mock_supabase_client):
        """測試數據庫連接失敗"""
        # 模擬連接失敗
        mock_supabase_client.table.side_effect = Exception("Connection error")
        
        result = db_manager.test_connection()
        
        assert result is False
    
    def test_get_database_stats(self, db_manager, mock_supabase_client):
        """測試獲取數據庫統計信息"""
        # 模擬各種統計查詢
        mock_table = Mock()
        mock_supabase_client.table.return_value = mock_table
        
        def mock_execute():
            # 根據調用次序返回不同的結果
            call_count = mock_table.execute.call_count
            if call_count == 0:  # 總貼文數
                return Mock(count=100)
            elif call_count == 1:  # 用戶數據
                return Mock(data=[
                    {'username': 'user1'},
                    {'username': 'user2'},
                    {'username': 'user1'}  # 重複用戶
                ])
            elif call_count == 2:  # 互動數據
                return Mock(data=[
                    {'likes': 10, 'replies': 5, 'reposts': 2},
                    {'likes': 20, 'replies': 10, 'reposts': 5}
                ])
            elif call_count == 3:  # 最早日期
                return Mock(data=[{'timestamp': '2025-08-01T12:00:00Z'}])
            elif call_count == 4:  # 最新日期
                return Mock(data=[{'timestamp': '2025-08-05T12:00:00Z'}])
            else:
                return Mock(data=[])
        
        mock_table.select.return_value = mock_table
        mock_table.order.return_value = mock_table
        mock_table.limit.return_value = mock_table
        mock_table.execute.side_effect = mock_execute
        
        stats = db_manager.get_database_stats()
        
        assert stats['total_posts'] == 100
        assert stats['unique_users'] == 2  # user1, user2
        assert stats['total_interactions'] == 52  # (10+5+2) + (20+10+5)
        assert stats['date_range'] is not None

class TestScraperDatabaseIntegration:
    """測試爬蟲與數據庫的集成"""
    
    @pytest.fixture
    def mock_db_manager(self):
        """創建模擬的數據庫管理器"""
        return Mock(spec=SupabaseManager)
    
    @pytest.fixture
    def sample_posts(self):
        """創建測試用的貼文列表"""
        return [
            ThreadsPost(
                post_id="integration_test_1",
                username="user1",
                content="集成測試內容1",
                timestamp="2025-08-05T12:00:00Z",
                likes=15,
                replies=3,
                reposts=1,
                images=[],
                post_url="https://threads.com/@user1/post/integration_test_1",
                scraped_at="2025-08-05T12:30:00Z"
            ),
            ThreadsPost(
                post_id="integration_test_2",
                username="user2",
                content="集成測試內容2",
                timestamp="2025-08-05T13:00:00Z",
                likes=25,
                replies=8,
                reposts=4,
                images=["https://example.com/image.jpg"],
                post_url="https://threads.com/@user2/post/integration_test_2",
                scraped_at="2025-08-05T13:30:00Z"
            )
        ]
    
    @patch('scraper.SupabaseManager')
    def test_scraper_with_database_success(self, mock_manager_class, sample_posts):
        """測試爬蟲成功保存到數據庫"""
        from scraper import ThreadsScraper
        
        # 設置模擬的數據庫管理器
        mock_db_manager = Mock()
        mock_manager_class.return_value = mock_db_manager
        mock_db_manager.get_existing_post_ids.return_value = []
        mock_db_manager.insert_raw_posts_batch.return_value = {
            'success': 2,
            'failure': 0
        }
        
        # 創建爬蟲實例
        scraper = ThreadsScraper()
        
        # 測試保存到數據庫
        result = scraper.save_to_database(sample_posts)
        
        assert result['success'] == 2
        assert result['failure'] == 0
        assert result['skipped'] == 0
        
        # 驗證調用
        mock_db_manager.get_existing_post_ids.assert_called_once()
        mock_db_manager.insert_raw_posts_batch.assert_called_once()
    
    @patch('scraper.SupabaseManager')
    def test_scraper_with_database_partial_exists(self, mock_manager_class, sample_posts):
        """測試爬蟲保存時部分貼文已存在"""
        from scraper import ThreadsScraper
        
        # 設置模擬的數據庫管理器
        mock_db_manager = Mock()
        mock_manager_class.return_value = mock_db_manager
        mock_db_manager.get_existing_post_ids.return_value = ["integration_test_1"]
        mock_db_manager.insert_raw_posts_batch.return_value = {
            'success': 1,
            'failure': 0
        }
        
        # 創建爬蟲實例
        scraper = ThreadsScraper()
        
        # 測試保存到數據庫
        result = scraper.save_to_database(sample_posts)
        
        assert result['success'] == 1
        assert result['failure'] == 0
        assert result['skipped'] == 1
    
    @patch('scraper.SupabaseManager')
    def test_scraper_without_database_manager(self, mock_manager_class, sample_posts):
        """測試沒有數據庫管理器時的行為"""
        from scraper import ThreadsScraper
        
        # 模擬數據庫管理器初始化失敗
        mock_manager_class.side_effect = Exception("Database connection failed")
        
        # 創建爬蟲實例
        scraper = ThreadsScraper()
        
        # 數據庫管理器應該是 None
        assert scraper.db_manager is None
        
        # 測試保存到數據庫（應該失敗）
        result = scraper.save_to_database(sample_posts)
        
        assert result['success'] == 0
        assert result['failure'] == 2
    
    def test_data_format_conversion(self, sample_posts):
        """測試數據格式轉換"""
        from dataclasses import asdict
        
        # 測試貼文數據轉換為字典格式
        post = sample_posts[0]
        post_dict = asdict(post)
        
        # 驗證必要欄位存在
        required_fields = [
            'post_id', 'username', 'content', 'timestamp',
            'likes', 'replies', 'reposts', 'images',
            'post_url', 'scraped_at'
        ]
        
        for field in required_fields:
            assert field in post_dict
        
        # 驗證數據類型
        assert isinstance(post_dict['likes'], int)
        assert isinstance(post_dict['replies'], int)
        assert isinstance(post_dict['reposts'], int)
        assert isinstance(post_dict['images'], list)

class TestDatabasePerformance:
    """數據庫性能測試"""
    
    @pytest.fixture
    def large_post_set(self):
        """創建大量測試貼文"""
        posts = []
        for i in range(100):
            posts.append(ThreadsPost(
                post_id=f"perf_test_{i}",
                username=f"perfuser{i % 10}",  # 10個不同用戶
                content=f"性能測試內容 {i} " + "x" * 100,  # 較長的內容
                timestamp="2025-08-05T12:00:00Z",
                likes=i * 2,
                replies=i,
                reposts=i // 2,
                images=[f"https://example.com/image{j}.jpg" for j in range(i % 3)],
                post_url=f"https://threads.com/@perfuser{i % 10}/post/perf_test_{i}",
                scraped_at="2025-08-05T12:30:00Z"
            ))
        return posts
    
    @patch('database.create_client')
    def test_batch_insert_performance(self, mock_create_client, large_post_set):
        """測試批量插入性能"""
        import time
        
        # 設置模擬客戶端
        mock_client = Mock()
        mock_create_client.return_value = mock_client
        
        mock_table = Mock()
        mock_client.table.return_value = mock_table
        mock_table.upsert.return_value = mock_table
        mock_table.execute.return_value = Mock(data=[{'post_id': f'perf_test_{i}'} for i in range(100)])
        
        # 創建數據庫管理器
        with patch.dict(os.environ, {
            'SUPABASE_URL': TEST_SUPABASE_URL,
            'SUPABASE_KEY': TEST_SUPABASE_KEY
        }):
            db_manager = SupabaseManager()
        
        # 測量批量插入時間
        start_time = time.time()
        result = db_manager.insert_raw_posts_batch(large_post_set)
        end_time = time.time()
        
        # 驗證結果
        assert result['success'] == 100
        assert result['failure'] == 0
        
        # 驗證批量插入比單個插入更高效
        batch_time = end_time - start_time
        assert batch_time < 1.0  # 批量插入應該很快（模擬環境）

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])