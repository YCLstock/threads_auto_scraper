"""
Supabase 數據庫連接和操作模組
處理與 Supabase 數據庫的所有交互
"""

import os
import logging
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime, timezone
from dataclasses import asdict

if TYPE_CHECKING:
    from scraper import ThreadsPost

from supabase import create_client, Client
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

logger = logging.getLogger(__name__)

class SupabaseManager:
    """Supabase 數據庫管理器"""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL 和 SUPABASE_KEY 環境變數必須設置")
        
        try:
            self.client: Client = create_client(self.url, self.key)
            logger.info("Supabase 客戶端初始化成功")
        except Exception as e:
            logger.error(f"Supabase 客戶端初始化失敗: {e}")
            raise
    
    def insert_raw_post(self, post: 'ThreadsPost') -> bool:
        """
        插入單個原始貼文到 raw_posts 表
        
        Args:
            post: ThreadsPost 對象
            
        Returns:
            bool: 插入是否成功
        """
        try:
            # 轉換 ThreadsPost 為字典
            post_data = asdict(post)
            
            # 轉換圖片列表為 JSONB 格式
            post_data['images'] = post_data['images'] if post_data['images'] else []
            
            # 確保時間戳格式正確
            if isinstance(post_data['timestamp'], str):
                post_data['timestamp'] = datetime.fromisoformat(
                    post_data['timestamp'].replace('Z', '+00:00')
                ).isoformat()
            
            if isinstance(post_data['scraped_at'], str):
                post_data['scraped_at'] = datetime.fromisoformat(
                    post_data['scraped_at'].replace('Z', '+00:00')
                ).isoformat()
            
            # 執行插入操作（使用 upsert 避免重複）
            result = self.client.table('raw_posts').upsert(
                post_data,
                on_conflict='post_id'
            ).execute()
            
            if result.data:
                logger.debug(f"成功插入/更新貼文: {post.post_id}")
                return True
            else:
                logger.warning(f"插入貼文失敗，無數據返回: {post.post_id}")
                return False
                
        except Exception as e:
            logger.error(f"插入貼文 {post.post_id} 失敗: {e}")
            return False
    
    def insert_raw_posts_batch(self, posts: List['ThreadsPost']) -> Dict[str, int]:
        """
        批量插入原始貼文到 raw_posts 表
        
        Args:
            posts: ThreadsPost 列表
            
        Returns:
            Dict: 包含成功和失敗計數的字典
        """
        success_count = 0
        failure_count = 0
        
        if not posts:
            logger.warning("沒有貼文需要插入")
            return {'success': 0, 'failure': 0}
        
        # 轉換所有貼文為字典格式
        posts_data = []
        for post in posts:
            try:
                post_data = asdict(post)
                
                # 處理圖片列表
                post_data['images'] = post_data['images'] if post_data['images'] else []
                
                # 處理時間格式
                if isinstance(post_data['timestamp'], str):
                    post_data['timestamp'] = datetime.fromisoformat(
                        post_data['timestamp'].replace('Z', '+00:00')
                    ).isoformat()
                
                if isinstance(post_data['scraped_at'], str):
                    post_data['scraped_at'] = datetime.fromisoformat(
                        post_data['scraped_at'].replace('Z', '+00:00')
                    ).isoformat()
                
                posts_data.append(post_data)
                
            except Exception as e:
                logger.error(f"處理貼文 {post.post_id} 數據失敗: {e}")
                failure_count += 1
                continue
        
        # 批量插入數據
        try:
            if posts_data:
                result = self.client.table('raw_posts').upsert(
                    posts_data,
                    on_conflict='post_id'
                ).execute()
                
                if result.data:
                    success_count = len(result.data)
                    logger.info(f"批量插入成功: {success_count} 篇貼文")
                else:
                    logger.warning("批量插入失敗，無數據返回")
                    failure_count += len(posts_data)
            
        except Exception as e:
            logger.error(f"批量插入失敗: {e}")
            failure_count += len(posts_data)
        
        return {
            'success': success_count,
            'failure': failure_count
        }
    
    def get_existing_post_ids(self, post_ids: List[str]) -> List[str]:
        """
        檢查哪些貼文ID已經存在於數據庫中
        
        Args:
            post_ids: 要檢查的貼文ID列表
            
        Returns:
            List[str]: 已存在的貼文ID列表
        """
        try:
            if not post_ids:
                return []
            
            result = self.client.table('raw_posts').select('post_id').in_(
                'post_id', post_ids
            ).execute()
            
            if result.data:
                existing_ids = [row['post_id'] for row in result.data]
                logger.debug(f"發現 {len(existing_ids)} 個已存在的貼文ID")
                return existing_ids
            
            return []
            
        except Exception as e:
            logger.error(f"檢查已存在貼文ID失敗: {e}")
            return []
    
    def get_posts_by_username(self, username: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        根據用戶名獲取貼文
        
        Args:
            username: 用戶名
            limit: 返回貼文數量限制
            
        Returns:
            List[Dict]: 貼文數據列表
        """
        try:
            result = self.client.table('raw_posts').select('*').eq(
                'username', username
            ).order('timestamp', desc=True).limit(limit).execute()
            
            if result.data:
                logger.info(f"獲取用戶 {username} 的 {len(result.data)} 篇貼文")
                return result.data
            
            logger.info(f"用戶 {username} 沒有找到貼文")
            return []
            
        except Exception as e:
            logger.error(f"獲取用戶 {username} 貼文失敗: {e}")
            return []
    
    def get_posts_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        根據日期範圍獲取貼文
        
        Args:
            start_date: 開始日期
            end_date: 結束日期
            
        Returns:
            List[Dict]: 貼文數據列表
        """
        try:
            result = self.client.table('raw_posts').select('*').gte(
                'timestamp', start_date.isoformat()
            ).lte(
                'timestamp', end_date.isoformat()
            ).order('timestamp', desc=True).execute()
            
            if result.data:
                logger.info(f"獲取日期範圍 {start_date.date()} 到 {end_date.date()} 的 {len(result.data)} 篇貼文")
                return result.data
            
            return []
            
        except Exception as e:
            logger.error(f"根據日期範圍獲取貼文失敗: {e}")
            return []
    
    def get_posts_count(self) -> int:
        """
        獲取數據庫中的貼文總數
        
        Returns:
            int: 貼文總數
        """
        try:
            result = self.client.table('raw_posts').select(
                'post_id', count='exact'
            ).execute()
            
            count = result.count if result.count is not None else 0
            logger.info(f"數據庫中共有 {count} 篇貼文")
            return count
            
        except Exception as e:
            logger.error(f"獲取貼文總數失敗: {e}")
            return 0
    
    def delete_post(self, post_id: str) -> bool:
        """
        刪除指定的貼文
        
        Args:
            post_id: 要刪除的貼文ID
            
        Returns:
            bool: 刪除是否成功
        """
        try:
            result = self.client.table('raw_posts').delete().eq(
                'post_id', post_id
            ).execute()
            
            if result.data:
                logger.info(f"成功刪除貼文: {post_id}")
                return True
            
            logger.warning(f"刪除貼文失敗，可能不存在: {post_id}")
            return False
            
        except Exception as e:
            logger.error(f"刪除貼文 {post_id} 失敗: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        測試數據庫連接
        
        Returns:
            bool: 連接是否成功
        """
        try:
            # 嘗試執行一個簡單的查詢
            result = self.client.table('raw_posts').select(
                'post_id', count='exact'
            ).limit(1).execute()
            
            logger.info("Supabase 連接測試成功")
            return True
            
        except Exception as e:
            logger.error(f"Supabase 連接測試失敗: {e}")
            return False
    
    def create_tables_if_not_exists(self) -> bool:
        """
        創建數據表（如果不存在）
        注意：這通常在 Supabase 控制台中完成，這裡僅作為備用
        
        Returns:
            bool: 操作是否成功
        """
        try:
            # 這個方法主要用於文檔目的
            # 實際的表創建應該使用 database_schema.sql 文件
            logger.info("表創建應該在 Supabase 控制台或使用 SQL 文件完成")
            return True
            
        except Exception as e:
            logger.error(f"創建表失敗: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        獲取數據庫統計信息
        
        Returns:
            Dict: 包含各種統計信息的字典
        """
        stats = {
            'total_posts': 0,
            'unique_users': 0,
            'total_interactions': 0,
            'date_range': None
        }
        
        try:
            # 獲取貼文總數
            posts_result = self.client.table('raw_posts').select(
                'post_id', count='exact'
            ).execute()
            stats['total_posts'] = posts_result.count or 0
            
            # 獲取唯一用戶數
            users_result = self.client.table('raw_posts').select(
                'username', count='exact'
            ).execute()
            if users_result.data:
                unique_users = set(row['username'] for row in users_result.data)
                stats['unique_users'] = len(unique_users)
            
            # 獲取總互動數
            interactions_result = self.client.table('raw_posts').select(
                'likes, replies, reposts'
            ).execute()
            if interactions_result.data:
                total = sum(
                    row['likes'] + row['replies'] + row['reposts']
                    for row in interactions_result.data
                )
                stats['total_interactions'] = total
            
            # 獲取日期範圍
            date_result = self.client.table('raw_posts').select(
                'timestamp'
            ).order('timestamp', desc=False).limit(1).execute()
            
            if date_result.data:
                oldest = date_result.data[0]['timestamp']
                
                latest_result = self.client.table('raw_posts').select(
                    'timestamp'
                ).order('timestamp', desc=True).limit(1).execute()
                
                if latest_result.data:
                    newest = latest_result.data[0]['timestamp']
                    stats['date_range'] = {
                        'oldest': oldest,
                        'newest': newest
                    }
            
            logger.info(f"數據庫統計: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"獲取數據庫統計失敗: {e}")
            return stats