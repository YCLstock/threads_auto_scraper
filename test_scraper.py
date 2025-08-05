"""
Threads 爬蟲腳本單元測試
測試 scraper.py 的各項功能
"""

import pytest
import json
import os
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock
from dataclasses import asdict

from scraper import ThreadsScraper, ThreadsPost

class TestThreadsPost:
    """測試 ThreadsPost 數據結構"""
    
    def test_threads_post_creation(self):
        """測試 ThreadsPost 實例創建"""
        post = ThreadsPost(
            post_id="test123",
            username="testuser",
            content="Test content",
            timestamp="2025-08-05T12:00:00Z",
            likes=10,
            replies=5,
            reposts=2,
            images=["image1.jpg"],
            post_url="https://threads.com/@testuser/post/test123",
            scraped_at="2025-08-05T12:30:00Z"
        )
        
        assert post.post_id == "test123"
        assert post.username == "testuser"
        assert post.content == "Test content"
        assert post.likes == 10
        assert post.replies == 5
        assert post.reposts == 2
        assert len(post.images) == 1
    
    def test_threads_post_to_dict(self):
        """測試 ThreadsPost 轉換為字典"""
        post = ThreadsPost(
            post_id="test123",
            username="testuser",
            content="Test content",
            timestamp="2025-08-05T12:00:00Z",
            likes=10,
            replies=5,
            reposts=2,
            images=[],
            post_url="https://threads.com/@testuser/post/test123",
            scraped_at="2025-08-05T12:30:00Z"
        )
        
        post_dict = asdict(post)
        assert isinstance(post_dict, dict)
        assert post_dict['post_id'] == "test123"
        assert post_dict['username'] == "testuser"

class TestThreadsScraper:
    """測試 ThreadsScraper 主類"""
    
    @pytest.fixture
    def scraper(self):
        """創建測試用的 scraper 實例"""
        return ThreadsScraper()
    
    @pytest.fixture
    def mock_accounts_file(self, tmp_path):
        """創建測試用的 accounts.json 文件"""
        accounts_data = {
            "accounts": ["testuser1", "testuser2", "testuser3"]
        }
        accounts_file = tmp_path / "accounts.json"
        with open(accounts_file, 'w', encoding='utf-8') as f:
            json.dump(accounts_data, f)
        return accounts_file
    
    def test_scraper_initialization(self, scraper):
        """測試 scraper 初始化"""
        assert scraper.base_url == 'https://www.threads.com'
        assert scraper.delay_min >= 2
        assert scraper.delay_max >= scraper.delay_min
        assert scraper.timeout > 0
        assert scraper.retry_attempts > 0
        assert hasattr(scraper, 'ua')
        assert hasattr(scraper, 'session')
    
    def test_create_session(self, scraper):
        """測試 HTTP 會話創建"""
        session = scraper._create_session()
        
        assert session is not None
        assert 'User-Agent' in session.headers
        assert 'Accept' in session.headers
        assert 'Accept-Language' in session.headers
    
    @patch('scraper.open')
    @patch('scraper.json.load')
    def test_load_accounts_success(self, mock_json_load, mock_open, scraper):
        """測試成功載入帳號列表"""
        mock_json_load.return_value = {
            "accounts": ["user1", "user2", "user3"]
        }
        
        accounts = scraper._load_accounts()
        
        assert len(accounts) == 3
        assert "user1" in accounts
        assert "user2" in accounts
        assert "user3" in accounts
    
    @patch('scraper.open', side_effect=FileNotFoundError())
    def test_load_accounts_file_not_found(self, mock_open, scraper):
        """測試帳號文件不存在的情況"""
        accounts = scraper._load_accounts()
        assert accounts == []
    
    @patch('scraper.open')
    @patch('scraper.json.load', side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
    def test_load_accounts_invalid_json(self, mock_json_load, mock_open, scraper):
        """測試無效 JSON 格式的情況"""
        accounts = scraper._load_accounts()
        assert accounts == []
    
    def test_generate_post_id(self, scraper):
        """測試貼文 ID 生成"""
        username = "testuser"
        content = "This is a test post content"
        timestamp = "2025-08-05T12:00:00Z"
        
        post_id = scraper._generate_post_id(username, content, timestamp)
        
        assert isinstance(post_id, str)
        assert len(post_id) == 32  # MD5 hash length
        
        # 同樣的輸入應該產生同樣的 ID
        post_id2 = scraper._generate_post_id(username, content, timestamp)
        assert post_id == post_id2
        
        # 不同的輸入應該產生不同的 ID
        post_id3 = scraper._generate_post_id(username, "Different content", timestamp)
        assert post_id != post_id3
    
    def test_random_delay(self, scraper):
        """測試隨機延遲功能"""
        import time
        
        start_time = time.time()
        scraper._random_delay()
        end_time = time.time()
        
        delay = end_time - start_time
        assert delay >= scraper.delay_min
        # 允許一定的誤差
        assert delay <= scraper.delay_max + 0.5
    
    def test_extract_interaction_count(self, scraper):
        """測試互動數量提取功能"""
        # 創建模擬的 DOM 元素
        mock_element = Mock()
        mock_interaction_elem = Mock()
        mock_interaction_elem.get_attribute.return_value = "15 likes"
        mock_element.find_element.return_value = mock_interaction_elem
        
        count = scraper._extract_interaction_count(mock_element, 'like')
        assert count == 15
    
    def test_extract_interaction_count_no_element(self, scraper):
        """測試找不到互動元素的情況"""
        from selenium.common.exceptions import NoSuchElementException
        
        mock_element = Mock()
        mock_element.find_element.side_effect = NoSuchElementException()
        
        count = scraper._extract_interaction_count(mock_element, 'like')
        assert count == 0
    
    def test_extract_interaction_count_no_numbers(self, scraper):
        """測試互動元素沒有數字的情況"""
        mock_element = Mock()
        mock_interaction_elem = Mock()
        mock_interaction_elem.get_attribute.return_value = "No numbers here"
        mock_element.find_element.return_value = mock_interaction_elem
        
        count = scraper._extract_interaction_count(mock_element, 'like')
        assert count == 0
    
    @patch('scraper.webdriver.Chrome')
    def test_init_driver(self, mock_chrome, scraper):
        """測試 WebDriver 初始化"""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        driver = scraper._init_driver()
        
        assert driver == mock_driver
        mock_driver.execute_script.assert_called()
    
    def test_parse_post_element_success(self, scraper):
        """測試成功解析貼文元素"""
        # 創建模擬的貼文元素
        mock_element = Mock()
        
        # 模擬內容元素
        mock_content_elem = Mock()
        mock_content_elem.text = "This is test content"
        
        # 模擬時間元素
        mock_time_elem = Mock()
        mock_time_elem.get_attribute.return_value = "2025-08-05T12:00:00Z"
        
        # 模擬圖片元素
        mock_img_elem = Mock()
        mock_img_elem.get_attribute.return_value = "https://cdninstagram.com/image.jpg"
        
        # 設置 find_element 行為
        def mock_find_element(by, selector):
            if 'post-text' in selector:
                return mock_content_elem
            elif selector == 'time':
                return mock_time_elem
            return Mock()
        
        def mock_find_elements(by, selector):
            if 'cdninstagram' in selector:
                return [mock_img_elem]
            return []
        
        mock_element.find_element.side_effect = mock_find_element
        mock_element.find_elements.side_effect = mock_find_elements
        
        # 模擬互動數量提取
        with patch.object(scraper, '_extract_interaction_count', return_value=5):
            post = scraper._parse_post_element(mock_element, "testuser")
        
        assert post is not None
        assert post.username == "testuser"
        assert post.content == "This is test content"
        assert post.likes == 5
        assert post.replies == 5
        assert post.reposts == 5
        assert len(post.images) == 1
    
    def test_parse_post_element_no_content(self, scraper):
        """測試解析沒有內容的貼文元素"""
        from selenium.common.exceptions import NoSuchElementException
        
        mock_element = Mock()
        mock_element.find_element.side_effect = NoSuchElementException()
        
        post = scraper._parse_post_element(mock_element, "testuser")
        assert post is None
    
    def test_save_to_json(self, scraper, tmp_path):
        """測試保存數據到 JSON 文件"""
        posts = [
            ThreadsPost(
                post_id="test1",
                username="user1",
                content="Content 1",
                timestamp="2025-08-05T12:00:00Z",
                likes=10,
                replies=5,
                reposts=2,
                images=[],
                post_url="https://threads.com/@user1/post/test1",
                scraped_at="2025-08-05T12:30:00Z"
            ),
            ThreadsPost(
                post_id="test2",
                username="user2",
                content="Content 2",
                timestamp="2025-08-05T13:00:00Z",
                likes=20,
                replies=10,
                reposts=5,
                images=["image.jpg"],
                post_url="https://threads.com/@user2/post/test2",
                scraped_at="2025-08-05T13:30:00Z"
            )
        ]
        
        # 切換到臨時目錄
        os.chdir(tmp_path)
        
        filename = "test_posts.json"
        scraper.save_to_json(posts, filename)
        
        # 驗證文件是否被創建
        assert os.path.exists(filename)
        
        # 驗證文件內容
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        assert len(loaded_data) == 2
        assert loaded_data[0]['post_id'] == "test1"
        assert loaded_data[1]['post_id'] == "test2"
    
    def test_save_to_json_auto_filename(self, scraper, tmp_path):
        """測試自動生成文件名"""
        posts = [
            ThreadsPost(
                post_id="test1",
                username="user1",
                content="Content 1",
                timestamp="2025-08-05T12:00:00Z",
                likes=10,
                replies=5,
                reposts=2,
                images=[],
                post_url="https://threads.com/@user1/post/test1",
                scraped_at="2025-08-05T12:30:00Z"
            )
        ]
        
        os.chdir(tmp_path)
        
        with patch('scraper.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "20250805_123000"
            scraper.save_to_json(posts)
        
        expected_filename = "threads_posts_20250805_123000.json"
        assert os.path.exists(expected_filename)
    
    @patch('scraper.ThreadsScraper._extract_post_data_selenium')
    def test_scrape_user_posts_success(self, mock_extract, scraper):
        """測試成功爬取用戶貼文"""
        mock_posts = [
            ThreadsPost(
                post_id="test1",
                username="testuser",
                content="Test content",
                timestamp="2025-08-05T12:00:00Z",
                likes=10,
                replies=5,
                reposts=2,
                images=[],
                post_url="https://threads.com/@testuser/post/test1",
                scraped_at="2025-08-05T12:30:00Z"
            )
        ]
        mock_extract.return_value = mock_posts
        
        posts = scraper.scrape_user_posts("testuser")
        
        assert len(posts) == 1
        assert posts[0].username == "testuser"
        mock_extract.assert_called_once_with("testuser")
    
    @patch('scraper.ThreadsScraper.scrape_user_posts')
    def test_scrape_all_accounts(self, mock_scrape_user, scraper):
        """測試爬取所有帳號"""
        # 設置測試帳號
        scraper.accounts = ["user1", "user2"]
        
        # 模擬每個用戶的貼文
        mock_scrape_user.side_effect = [
            [ThreadsPost("post1", "user1", "content1", "2025-08-05T12:00:00Z", 
                        10, 5, 2, [], "url1", "2025-08-05T12:30:00Z")],
            [ThreadsPost("post2", "user2", "content2", "2025-08-05T13:00:00Z", 
                        20, 10, 5, [], "url2", "2025-08-05T13:30:00Z")]
        ]
        
        all_posts = scraper.scrape_all_accounts()
        
        assert len(all_posts) == 2
        assert all_posts[0].username == "user1"
        assert all_posts[1].username == "user2"
        assert mock_scrape_user.call_count == 2
    
    def test_close(self, scraper):
        """測試資源清理"""
        mock_driver = Mock()
        mock_session = Mock()
        
        scraper.driver = mock_driver
        scraper.session = mock_session
        
        scraper.close()
        
        mock_driver.quit.assert_called_once()
        mock_session.close.assert_called_once()

class TestScraperIntegration:
    """爬蟲集成測試"""
    
    @pytest.fixture
    def scraper_with_mock_accounts(self, tmp_path):
        """創建帶有模擬帳號文件的爬蟲"""
        # 創建測試帳號文件
        accounts_data = {"accounts": ["testuser"]}
        accounts_file = tmp_path / "accounts.json"
        with open(accounts_file, 'w', encoding='utf-8') as f:
            json.dump(accounts_data, f)
        
        # 切換到測試目錄
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        scraper = ThreadsScraper()
        
        yield scraper
        
        # 清理
        scraper.close()
        os.chdir(original_cwd)
    
    def test_full_workflow_with_mocked_data(self, scraper_with_mock_accounts):
        """測試完整的爬蟲工作流程（使用模擬數據）"""
        scraper = scraper_with_mock_accounts
        
        # 模擬爬取結果
        with patch.object(scraper, '_extract_post_data_selenium') as mock_extract:
            mock_posts = [
                ThreadsPost(
                    post_id="integration_test",
                    username="testuser",
                    content="Integration test content",
                    timestamp="2025-08-05T12:00:00Z",
                    likes=100,
                    replies=50,
                    reposts=25,
                    images=["test_image.jpg"],
                    post_url="https://threads.com/@testuser/post/integration_test",
                    scraped_at="2025-08-05T12:30:00Z"
                )
            ]
            mock_extract.return_value = mock_posts
            
            # 執行爬取
            all_posts = scraper.scrape_all_accounts()
            
            # 驗證結果
            assert len(all_posts) == 1
            assert all_posts[0].post_id == "integration_test"
            assert all_posts[0].likes == 100
            
            # 測試保存功能
            scraper.save_to_json(all_posts, "integration_test.json")
            assert os.path.exists("integration_test.json")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])