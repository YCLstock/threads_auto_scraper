"""
Threads 數據爬蟲腳本
實現穩定抓取 Threads 平台貼文數據並存入 Supabase
"""

import json
import time
import random
import hashlib
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
from retry import retry
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 導入數據庫管理器
try:
    from database import SupabaseManager
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.warning("Supabase 模組不可用，將僅保存到 JSON 文件")

@dataclass
class ThreadsPost:
    """Threads 貼文數據結構"""
    post_id: str
    username: str
    content: str
    timestamp: str
    likes: int
    replies: int
    reposts: int
    images: List[str]
    post_url: str
    scraped_at: str

class ThreadsScraper:
    """Threads 爬蟲主類"""
    
    def __init__(self):
        self.base_url = os.getenv('THREADS_BASE_URL', 'https://www.threads.com')
        self.delay_min = int(os.getenv('SCRAPER_DELAY_MIN', '2'))
        self.delay_max = int(os.getenv('SCRAPER_DELAY_MAX', '5'))
        self.timeout = int(os.getenv('SCRAPER_TIMEOUT', '30'))
        self.retry_attempts = int(os.getenv('SCRAPER_RETRY_ATTEMPTS', '3'))
        self.headless = os.getenv('HEADLESS_MODE', 'true').lower() == 'true'
        
        self.ua = UserAgent()
        self.session = self._create_session()
        self.driver = None
        
        # 載入帳號列表
        self.accounts = self._load_accounts()
        
        # 初始化 Supabase 管理器
        self.db_manager = None
        if SUPABASE_AVAILABLE:
            try:
                self.db_manager = SupabaseManager()
                logger.info("Supabase 數據庫連接已建立")
            except Exception as e:
                logger.error(f"無法連接到 Supabase: {e}")
                self.db_manager = None
        
    def _create_session(self) -> requests.Session:
        """創建HTTP會話"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        return session
    
    def _load_accounts(self) -> List[str]:
        """載入要爬取的帳號列表"""
        try:
            with open('accounts.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('accounts', [])
        except FileNotFoundError:
            logger.error("accounts.json 文件未找到")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"解析 accounts.json 失敗: {e}")
            return []
    
    def _init_driver(self) -> webdriver.Chrome:
        """初始化 Chrome WebDriver"""
        if self.driver:
            return self.driver
            
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return self.driver
        except Exception as e:
            logger.error(f"初始化 Chrome Driver 失敗: {e}")
            raise
    
    def _random_delay(self):
        """隨機延遲以避免被封鎖"""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def _generate_post_id(self, username: str, content: str, timestamp: str) -> str:
        """生成貼文唯一ID"""
        raw_string = f"{username}_{content[:100]}_{timestamp}"
        return hashlib.md5(raw_string.encode('utf-8')).hexdigest()
    
    def _extract_post_data_selenium(self, username: str) -> List[ThreadsPost]:
        """使用 Selenium 提取用戶貼文數據"""
        posts = []
        driver = self._init_driver()
        
        try:
            # 訪問用戶主頁
            user_url = f"{self.base_url}/@{username}"
            logger.info(f"正在爬取用戶: {username}")
            
            driver.get(user_url)
            self._random_delay()
            
            # 等待頁面載入
            wait = WebDriverWait(driver, self.timeout)
            
            # 滾動頁面載入更多貼文
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 5  # 限制滾動次數避免無限滾動
            
            while scroll_attempts < max_scrolls:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self._random_delay()
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                    
                last_height = new_height
                scroll_attempts += 1
            
            # 提取貼文元素
            post_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="post"]')
            
            for element in post_elements[:20]:  # 限制每次最多抓取20篇貼文
                try:
                    post_data = self._parse_post_element(element, username)
                    if post_data:
                        posts.append(post_data)
                except Exception as e:
                    logger.warning(f"解析貼文失敗: {e}")
                    continue
            
            logger.info(f"成功爬取 {username} 的 {len(posts)} 篇貼文")
            
        except TimeoutException:
            logger.error(f"載入 {username} 頁面超時")
        except Exception as e:
            logger.error(f"爬取 {username} 失敗: {e}")
        
        return posts
    
    def _parse_post_element(self, element, username: str) -> Optional[ThreadsPost]:
        """解析單個貼文元素"""
        try:
            # 提取貼文內容
            content_elem = element.find_element(By.CSS_SELECTOR, '[data-testid="post-text"]')
            content = content_elem.text if content_elem else ""
            
            # 提取互動數據 (讚、回覆、轉發)
            likes = self._extract_interaction_count(element, 'like')
            replies = self._extract_interaction_count(element, 'reply')
            reposts = self._extract_interaction_count(element, 'repost')
            
            # 提取時間戳
            timestamp_elem = element.find_element(By.CSS_SELECTOR, 'time')
            timestamp_str = timestamp_elem.get_attribute('datetime') if timestamp_elem else datetime.now(timezone.utc).isoformat()
            
            # 提取圖片
            images = []
            img_elements = element.find_elements(By.CSS_SELECTOR, 'img[src*="cdninstagram"]')
            for img in img_elements:
                src = img.get_attribute('src')
                if src and 'cdninstagram' in src:
                    images.append(src)
            
            # 生成貼文URL和ID
            post_url = f"{self.base_url}/@{username}/post/placeholder"
            post_id = self._generate_post_id(username, content, timestamp_str)
            
            return ThreadsPost(
                post_id=post_id,
                username=username,
                content=content,
                timestamp=timestamp_str,
                likes=likes,
                replies=replies,
                reposts=reposts,
                images=images,
                post_url=post_url,
                scraped_at=datetime.now(timezone.utc).isoformat()
            )
            
        except NoSuchElementException:
            return None
        except Exception as e:
            logger.error(f"解析貼文元素失敗: {e}")
            return None
    
    def _extract_interaction_count(self, element, interaction_type: str) -> int:
        """提取互動數量"""
        try:
            # 根據不同的互動類型查找對應元素
            selectors = {
                'like': '[aria-label*="like"], [aria-label*="讚"]',
                'reply': '[aria-label*="reply"], [aria-label*="回覆"]',
                'repost': '[aria-label*="repost"], [aria-label*="轉發"]'
            }
            
            selector = selectors.get(interaction_type, '')
            if not selector:
                return 0
                
            interaction_elem = element.find_element(By.CSS_SELECTOR, selector)
            aria_label = interaction_elem.get_attribute('aria-label')
            
            if aria_label:
                # 從 aria-label 中提取數字
                import re
                numbers = re.findall(r'\d+', aria_label)
                return int(numbers[0]) if numbers else 0
            
            return 0
            
        except (NoSuchElementException, ValueError):
            return 0
    
    @retry(tries=3, delay=2, backoff=2)
    def scrape_user_posts(self, username: str) -> List[ThreadsPost]:
        """爬取指定用戶的貼文"""
        try:
            posts = self._extract_post_data_selenium(username)
            logger.info(f"成功爬取用戶 {username}: {len(posts)} 篇貼文")
            return posts
        except Exception as e:
            logger.error(f"爬取用戶 {username} 失敗: {e}")
            raise
    
    def scrape_all_accounts(self) -> List[ThreadsPost]:
        """爬取所有帳號的貼文"""
        all_posts = []
        
        for username in self.accounts:
            try:
                posts = self.scrape_user_posts(username)
                all_posts.extend(posts)
                self._random_delay()  # 在不同用戶之間增加延遲
            except Exception as e:
                logger.error(f"跳過用戶 {username}: {e}")
                continue
        
        logger.info(f"總共爬取了 {len(all_posts)} 篇貼文")
        return all_posts
    
    def save_to_database(self, posts: List[ThreadsPost]) -> Dict[str, int]:
        """將貼文數據保存到 Supabase 數據庫"""
        if not self.db_manager:
            logger.error("數據庫管理器未初始化，無法保存到數據庫")
            return {'success': 0, 'failure': len(posts)}
        
        if not posts:
            logger.warning("沒有貼文需要保存")
            return {'success': 0, 'failure': 0}
        
        # 檢查哪些貼文已存在
        post_ids = [post.post_id for post in posts]
        existing_ids = self.db_manager.get_existing_post_ids(post_ids)
        
        # 過濾出新貼文
        new_posts = [post for post in posts if post.post_id not in existing_ids]
        
        if existing_ids:
            logger.info(f"跳過 {len(existing_ids)} 個已存在的貼文")
        
        if not new_posts:
            logger.info("所有貼文都已存在，無需保存")
            return {'success': 0, 'failure': 0, 'skipped': len(existing_ids)}
        
        # 批量插入新貼文
        result = self.db_manager.insert_raw_posts_batch(new_posts)
        result['skipped'] = len(existing_ids)
        
        logger.info(f"數據庫保存結果: 成功 {result['success']}, 失敗 {result['failure']}, 跳過 {result['skipped']}")
        return result
    
    def save_to_json(self, posts: List[ThreadsPost], filename: str = None):
        """將貼文數據保存為JSON文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"threads_posts_{timestamp}.json"
        
        posts_data = [asdict(post) for post in posts]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts_data, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"數據已保存到 {filename}")
    
    def save_posts(self, posts: List[ThreadsPost], save_to_db: bool = True, save_to_json: bool = True) -> Dict[str, Any]:
        """
        保存貼文數據到數據庫和/或JSON文件
        
        Args:
            posts: 要保存的貼文列表
            save_to_db: 是否保存到數據庫
            save_to_json: 是否保存到JSON文件
            
        Returns:
            Dict: 保存結果統計
        """
        results = {
            'database': {'success': 0, 'failure': 0, 'skipped': 0},
            'json': {'saved': False, 'filename': None}
        }
        
        if not posts:
            logger.warning("沒有貼文需要保存")
            return results
        
        # 保存到數據庫
        if save_to_db and self.db_manager:
            results['database'] = self.save_to_database(posts)
        elif save_to_db and not self.db_manager:
            logger.warning("數據庫不可用，跳過數據庫保存")
        
        # 保存到JSON文件
        if save_to_json:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"threads_posts_{timestamp}.json"
                self.save_to_json(posts, filename)
                results['json'] = {'saved': True, 'filename': filename}
            except Exception as e:
                logger.error(f"保存JSON文件失敗: {e}")
                results['json'] = {'saved': False, 'filename': None}
        
        return results
    
    def close(self):
        """清理資源"""
        if self.driver:
            self.driver.quit()
        if self.session:
            self.session.close()

def main():
    """主執行函數"""
    scraper = ThreadsScraper()
    
    try:
        # 爬取所有帳號的貼文
        posts = scraper.scrape_all_accounts()
        
        if posts:
            # 保存數據（同時保存到數據庫和JSON文件）
            save_results = scraper.save_posts(posts, save_to_db=True, save_to_json=True)
            
            # 輸出保存結果
            db_result = save_results['database']
            json_result = save_results['json']
            
            logger.info(f"爬蟲執行完成，共獲得 {len(posts)} 篇貼文")
            logger.info(f"數據庫保存: 成功 {db_result['success']}, 失敗 {db_result['failure']}, 跳過 {db_result['skipped']}")
            
            if json_result['saved']:
                logger.info(f"JSON文件已保存: {json_result['filename']}")
            else:
                logger.warning("JSON文件保存失敗")
        else:
            logger.warning("未獲得任何貼文數據")
    
    except KeyboardInterrupt:
        logger.info("用戶中斷爬蟲執行")
    except Exception as e:
        logger.error(f"爬蟲執行失敗: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()