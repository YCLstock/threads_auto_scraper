"""
Threads 數據處理腳本
從 Supabase 讀取原始數據，進行分析處理，並將結果存回數據庫
"""

import logging
import os
import re
import jieba
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import warnings

# 機器學習和NLP相關
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

# 自定義模組
from database import SupabaseManager
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('process_data.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 忽略警告
warnings.filterwarnings('ignore')

# 下載必要的NLTK數據
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except Exception as e:
    logger.warning(f"NLTK數據下載失敗: {e}")

@dataclass
class PostMetrics:
    """貼文指標數據結構"""
    post_id: str
    total_interactions: int
    heat_density: float
    freshness_score: float
    engagement_rate: float
    viral_potential: float

@dataclass 
class TopicSummary:
    """主題摘要數據結構"""
    topic_id: int
    topic_keywords: List[str]
    topic_name: str
    post_count: int
    average_heat_density: float
    total_interactions: int
    dominant_sentiment: str
    trending_score: float

@dataclass
class KeywordTrend:
    """關鍵字趨勢數據結構"""
    keyword: str
    date: str
    post_count: int
    total_interactions: int
    average_sentiment: float
    momentum_score: float

class DataProcessor:
    """數據處理器主類"""
    
    def __init__(self):
        self.db_manager = SupabaseManager()
        
        # 初始化中文分詞
        jieba.initialize()
        
        # 載入中文停用詞
        self.chinese_stopwords = self._load_chinese_stopwords()
        
        # 初始化情感分析器
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            logger.warning(f"情感分析器初始化失敗: {e}")
            self.sentiment_analyzer = None
        
        # 配置參數
        self.min_interactions_threshold = int(os.getenv('MIN_INTERACTIONS_THRESHOLD', '5'))
        self.max_topics = int(os.getenv('MAX_TOPICS', '20'))
        self.keyword_min_freq = int(os.getenv('KEYWORD_MIN_FREQ', '3'))
        
    def _load_chinese_stopwords(self) -> set:
        """載入中文停用詞"""
        stopwords_set = set()
        
        # 基本中文停用詞
        basic_stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '這', '上', '也', '很', '到',
            '說', '要', '去', '你', '會', '著', '沒有', '看', '好', '自己', '這個', '現在', '可以', '沒', '就是',
            '還', '把', '從', '給', '對', '時候', '那', '來', '因為', '什麼', '那個', '他', '她', '它', '我們',
            '你們', '他們', '這樣', '那樣', '怎麼', '為什麼', '多少', '哪裡', '什麼時候', '怎樣', '多麼',
            '非常', '最', '更', '太', '特別', '真的', '確實', '當然', '或者', '但是', '然而', '所以', '因此',
            '如果', '雖然', '儘管', '不過', '而且', '另外', '此外', '總之', '首先', '其次', '最後', '另一方面'
        }
        
        # 添加英文停用詞
        try:
            english_stopwords = set(stopwords.words('english'))
            stopwords_set.update(english_stopwords)
        except Exception:
            pass
        
        stopwords_set.update(basic_stopwords)
        
        # 添加特定領域停用詞
        social_media_stopwords = {
            'threads', 'instagram', 'meta', 'facebook', 'twitter', 'x',
            'like', 'follow', 'share', 'comment', 'post', 'thread',
            'http', 'https', 'www', 'com', 'html', 'jpg', 'png', 'gif'
        }
        stopwords_set.update(social_media_stopwords)
        
        return stopwords_set
    
    def fetch_raw_posts(self, days_back: int = 7) -> pd.DataFrame:
        """
        從數據庫獲取原始貼文數據
        
        Args:
            days_back: 回溯天數
            
        Returns:
            pd.DataFrame: 貼文數據框
        """
        try:
            # 計算日期範圍
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=days_back)
            
            # 從數據庫獲取數據
            posts_data = self.db_manager.get_posts_by_date_range(start_date, end_date)
            
            if not posts_data:
                logger.warning("沒有找到符合條件的貼文數據")
                return pd.DataFrame()
            
            # 轉換為DataFrame
            df = pd.DataFrame(posts_data)
            
            # 數據清理和類型轉換
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['scraped_at'] = pd.to_datetime(df['scraped_at'])
            df['likes'] = df['likes'].fillna(0).astype(int)
            df['replies'] = df['replies'].fillna(0).astype(int)
            df['reposts'] = df['reposts'].fillna(0).astype(int)
            df['content'] = df['content'].fillna('')
            
            # 計算總互動數
            df['total_interactions'] = df['likes'] + df['replies'] + df['reposts']
            
            logger.info(f"成功載入 {len(df)} 篇貼文數據")
            return df
            
        except Exception as e:
            logger.error(f"獲取原始貼文數據失敗: {e}")
            return pd.DataFrame()
    
    def calculate_heat_density(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算貼文熱度密度
        
        Args:
            df: 貼文數據框
            
        Returns:
            pd.DataFrame: 包含熱度密度的數據框
        """
        if df.empty:
            return df
        
        try:
            # 計算時間衰減因子
            current_time = datetime.now(timezone.utc)
            df['hours_since_post'] = (current_time - df['timestamp']).dt.total_seconds() / 3600
            
            # 時間衰減函數（指數衰減）
            decay_rate = 0.1  # 衰減率
            df['time_decay'] = np.exp(-decay_rate * df['hours_since_post'] / 24)  # 24小時為基準
            
            # 基礎熱度分數
            df['base_heat'] = (
                df['likes'] * 1.0 +      # 讚的權重
                df['replies'] * 2.0 +    # 回覆的權重（更高，表示更多互動）
                df['reposts'] * 1.5      # 轉發的權重
            )
            
            # 考慮內容長度對熱度的影響
            df['content_length'] = df['content'].str.len()
            df['length_factor'] = np.log1p(df['content_length']) / 10  # 對數歸一化
            
            # 計算最終熱度密度
            df['heat_density'] = (
                df['base_heat'] * df['time_decay'] * (1 + df['length_factor'])
            )
            
            # 歸一化到0-100範圍
            if df['heat_density'].max() > 0:
                df['heat_density'] = (df['heat_density'] / df['heat_density'].max()) * 100
            
            logger.info(f"完成 {len(df)} 篇貼文的熱度密度計算")
            return df
            
        except Exception as e:
            logger.error(f"計算熱度密度失敗: {e}")
            return df
    
    def calculate_freshness_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算貼文新鮮度分數
        
        Args:
            df: 貼文數據框
            
        Returns:
            pd.DataFrame: 包含新鮮度分數的數據框
        """
        if df.empty:
            return df
        
        try:
            current_time = datetime.now(timezone.utc)
            df['hours_since_post'] = (current_time - df['timestamp']).dt.total_seconds() / 3600
            
            # 新鮮度評分：24小時內為1.0，之後指數衰減
            df['freshness_score'] = np.exp(-df['hours_since_post'] / 24) 
            
            # 確保分數在0-1範圍內
            df['freshness_score'] = df['freshness_score'].clip(0, 1)
            
            return df
            
        except Exception as e:
            logger.error(f"計算新鮮度分數失敗: {e}")
            return df
    
    def calculate_engagement_rate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算參與率（基於用戶歷史表現）
        
        Args:
            df: 貼文數據框
            
        Returns:
            pd.DataFrame: 包含參與率的數據框
        """
        if df.empty:
            return df
        
        try:
            # 計算每個用戶的平均互動數
            user_avg_interactions = df.groupby('username')['total_interactions'].mean()
            
            # 計算當前貼文相對於該用戶平均表現的比率
            df['user_avg_interactions'] = df['username'].map(user_avg_interactions)
            df['engagement_rate'] = df['total_interactions'] / df['user_avg_interactions'].fillna(1)
            
            # 處理無窮大值和空值
            df['engagement_rate'] = df['engagement_rate'].replace([np.inf, -np.inf], 1.0).fillna(1.0)
            
            # 歸一化到合理範圍
            df['engagement_rate'] = np.log1p(df['engagement_rate'])
            
            return df
            
        except Exception as e:
            logger.error(f"計算參與率失敗: {e}")
            return df
    
    def calculate_viral_potential(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        計算病毒傳播潛力
        
        Args:
            df: 貼文數據框
            
        Returns:
            pd.DataFrame: 包含病毒傳播潛力的數據框
        """
        if df.empty:
            return df
        
        try:
            # 病毒傳播潛力基於多個因素
            # 1. 轉發率（轉發/總互動）
            df['repost_ratio'] = df['reposts'] / (df['total_interactions'] + 1)
            
            # 2. 互動速度（互動數/發布時間）
            df['interaction_velocity'] = df['total_interactions'] / (df['hours_since_post'] + 1)
            
            # 3. 內容特徵（是否包含熱門關鍵字、話題標籤等）
            df['has_hashtag'] = df['content'].str.contains('#', na=False).astype(int)
            df['has_mention'] = df['content'].str.contains('@', na=False).astype(int)
            df['has_url'] = df['content'].str.contains('http', na=False).astype(int)
            
            # 綜合計算病毒傳播潛力
            df['viral_potential'] = (
                df['repost_ratio'] * 0.4 +
                np.log1p(df['interaction_velocity']) * 0.3 +
                (df['has_hashtag'] + df['has_mention'] + df['has_url']) * 0.1 +
                df['freshness_score'] * 0.2
            )
            
            # 歸一化到0-1範圍
            if df['viral_potential'].max() > 0:
                df['viral_potential'] = df['viral_potential'] / df['viral_potential'].max()
            
            return df
            
        except Exception as e:
            logger.error(f"計算病毒傳播潛力失敗: {e}")
            return df
    
    def extract_keywords(self, texts: List[str], max_features: int = 100) -> List[Tuple[str, float]]:
        """
        從文本中提取關鍵詞
        
        Args:
            texts: 文本列表
            max_features: 最大特徵數
            
        Returns:
            List[Tuple[str, float]]: 關鍵詞和權重的元組列表
        """
        if not texts:
            return []
        
        try:
            # 預處理文本
            processed_texts = []
            for text in texts:
                if pd.isna(text) or not text.strip():
                    continue
                
                # 中文分詞
                words = jieba.cut(text.lower())
                
                # 過濾停用詞和短詞
                filtered_words = [
                    word.strip() for word in words 
                    if (len(word.strip()) > 1 and 
                        word.strip() not in self.chinese_stopwords and
                        not word.strip().isdigit() and
                        re.match(r'^[a-zA-Z\u4e00-\u9fff]+$', word.strip()))
                ]
                
                if filtered_words:
                    processed_texts.append(' '.join(filtered_words))
            
            if not processed_texts:
                return []
            
            # 使用TF-IDF提取關鍵詞
            vectorizer = TfidfVectorizer(
                max_features=max_features,
                min_df=self.keyword_min_freq,
                max_df=0.8,
                ngram_range=(1, 2)
            )
            
            tfidf_matrix = vectorizer.fit_transform(processed_texts)
            feature_names = vectorizer.get_feature_names_out()
            
            # 計算每個詞的平均TF-IDF分數
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # 創建關鍵詞-分數對
            keyword_scores = list(zip(feature_names, mean_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return keyword_scores[:50]  # 返回前50個關鍵詞
            
        except Exception as e:
            logger.error(f"提取關鍵詞失敗: {e}")
            return []
    
    def perform_topic_clustering(self, df: pd.DataFrame) -> List[TopicSummary]:
        """
        執行主題聚類分析
        
        Args:
            df: 貼文數據框
            
        Returns:
            List[TopicSummary]: 主題摘要列表
        """
        if df.empty or len(df) < 5:
            logger.warning("數據量不足，無法進行主題聚類")
            return []
        
        try:
            # 過濾掉互動數過低的貼文
            filtered_df = df[df['total_interactions'] >= self.min_interactions_threshold].copy()
            
            if len(filtered_df) < 3:
                logger.warning("符合條件的貼文數量太少，無法進行聚類")
                return []
            
            # 提取文本特徵
            texts = filtered_df['content'].fillna('').tolist()
            processed_texts = []
            
            for text in texts:
                words = jieba.cut(text.lower())
                filtered_words = [
                    word.strip() for word in words 
                    if (len(word.strip()) > 1 and 
                        word.strip() not in self.chinese_stopwords)
                ]
                processed_texts.append(' '.join(filtered_words))
            
            # 使用TF-IDF向量化
            vectorizer = TfidfVectorizer(
                max_features=200,
                min_df=2,
                max_df=0.8,
                ngram_range=(1, 2)
            )
            
            tfidf_matrix = vectorizer.fit_transform(processed_texts)
            
            # 確定聚類數量
            n_clusters = min(self.max_topics, max(2, len(filtered_df) // 10))
            
            # K-means聚類
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)
            
            # 分析每個聚類
            feature_names = vectorizer.get_feature_names_out()
            topics = []
            
            for cluster_id in range(n_clusters):
                cluster_mask = cluster_labels == cluster_id
                cluster_posts = filtered_df[cluster_mask]
                
                if len(cluster_posts) < 2:
                    continue
                
                # 獲取聚類中心的特徵
                cluster_center = kmeans.cluster_centers_[cluster_id]
                top_indices = cluster_center.argsort()[-10:][::-1]
                cluster_keywords = [feature_names[i] for i in top_indices if cluster_center[i] > 0]
                
                if not cluster_keywords:
                    continue
                
                # 生成主題名稱
                topic_name = self._generate_topic_name(cluster_keywords, cluster_posts['content'].tolist())
                
                # 計算主題統計
                total_interactions = cluster_posts['total_interactions'].sum()
                avg_heat_density = cluster_posts['heat_density'].mean()
                post_count = len(cluster_posts)
                
                # 分析情感傾向
                dominant_sentiment = self._analyze_cluster_sentiment(cluster_posts['content'].tolist())
                
                # 計算趨勢分數
                trending_score = self._calculate_trending_score(cluster_posts)
                
                topics.append(TopicSummary(
                    topic_id=cluster_id + 1,
                    topic_keywords=cluster_keywords[:5],
                    topic_name=topic_name,
                    post_count=post_count,
                    average_heat_density=avg_heat_density,
                    total_interactions=total_interactions,
                    dominant_sentiment=dominant_sentiment,
                    trending_score=trending_score
                ))
            
            logger.info(f"完成主題聚類分析，識別出 {len(topics)} 個主題")
            return topics
            
        except Exception as e:
            logger.error(f"主題聚類分析失敗: {e}")
            return []
    
    def _generate_topic_name(self, keywords: List[str], contents: List[str]) -> str:
        """生成主題名稱"""
        if not keywords:
            return "未知主題"
        
        # 簡單的主題命名邏輯
        primary_keyword = keywords[0]
        
        # 根據關鍵詞特徵判斷主題類別
        tech_keywords = ['ai', '人工智慧', '科技', '技術', '軟體', '程式', '數據']
        finance_keywords = ['投資', '股票', '金融', '經濟', '市場', '價格', '利率']
        social_keywords = ['社會', '政治', '新聞', '事件', '討論', '觀點']
        life_keywords = ['生活', '健康', '美食', '旅行', '娛樂', '電影', '音樂']
        
        if any(keyword in primary_keyword for keyword in tech_keywords):
            return f"科技趨勢 - {primary_keyword}"
        elif any(keyword in primary_keyword for keyword in finance_keywords):
            return f"財經動態 - {primary_keyword}"
        elif any(keyword in primary_keyword for keyword in social_keywords):
            return f"社會議題 - {primary_keyword}"
        elif any(keyword in primary_keyword for keyword in life_keywords):
            return f"生活分享 - {primary_keyword}"
        else:
            return f"熱門話題 - {primary_keyword}"
    
    def _analyze_cluster_sentiment(self, contents: List[str]) -> str:
        """分析聚類的情感傾向"""
        if not self.sentiment_analyzer or not contents:
            return "neutral"
        
        try:
            sentiment_scores = []
            for content in contents:
                if content and content.strip():
                    scores = self.sentiment_analyzer.polarity_scores(content)
                    sentiment_scores.append(scores['compound'])
            
            if not sentiment_scores:
                return "neutral"
            
            avg_sentiment = np.mean(sentiment_scores)
            
            if avg_sentiment > 0.1:
                return "positive"
            elif avg_sentiment < -0.1:
                return "negative"
            else:
                return "neutral"
                
        except Exception:
            return "neutral"
    
    def _calculate_trending_score(self, cluster_posts: pd.DataFrame) -> float:
        """計算主題的趨勢分數"""
        try:
            # 基於時間分佈和互動增長計算趨勢分數
            posts_sorted = cluster_posts.sort_values('timestamp')
            
            if len(posts_sorted) < 2:
                return 0.0
            
            # 計算時間跨度內的互動增長趨勢
            time_diff = (posts_sorted['timestamp'].iloc[-1] - posts_sorted['timestamp'].iloc[0]).total_seconds() / 3600
            
            if time_diff <= 0:
                return 0.0
            
            # 互動密度隨時間的變化
            interaction_velocity = posts_sorted['total_interactions'].sum() / time_diff
            
            # 結合新鮮度和互動速度
            avg_freshness = posts_sorted['freshness_score'].mean()
            trending_score = interaction_velocity * avg_freshness
            
            return min(trending_score / 100, 1.0)  # 歸一化到0-1
            
        except Exception:
            return 0.0
    
    def analyze_keyword_trends(self, df: pd.DataFrame, days: int = 7) -> List[KeywordTrend]:
        """
        分析關鍵詞趨勢
        
        Args:
            df: 貼文數據框
            days: 分析天數
            
        Returns:
            List[KeywordTrend]: 關鍵詞趨勢列表
        """
        if df.empty:
            return []
        
        try:
            # 按日期分組數據
            df['date'] = df['timestamp'].dt.date
            
            # 提取所有文本的關鍵詞
            all_keywords = self.extract_keywords(df['content'].tolist(), max_features=50)
            top_keywords = [kw[0] for kw in all_keywords[:20]]  # 取前20個關鍵詞
            
            keyword_trends = []
            
            for keyword in top_keywords:
                # 找到包含該關鍵詞的貼文
                keyword_posts = df[df['content'].str.contains(keyword, case=False, na=False)]
                
                if len(keyword_posts) < self.keyword_min_freq:
                    continue
                
                # 按日期分組統計
                daily_stats = keyword_posts.groupby('date').agg({
                    'post_id': 'count',
                    'total_interactions': 'sum',
                    'timestamp': 'count'
                }).rename(columns={'post_id': 'post_count'})
                
                # 計算每天的趨勢數據
                for date, stats in daily_stats.iterrows():
                    # 計算動量分數（基於最近幾天的變化）
                    momentum_score = self._calculate_keyword_momentum(
                        keyword, date, df, days=3
                    )
                    
                    # 情感分析
                    keyword_posts_day = keyword_posts[keyword_posts['date'] == date]
                    avg_sentiment = self._analyze_sentiment_for_posts(
                        keyword_posts_day['content'].tolist()
                    )
                    
                    keyword_trends.append(KeywordTrend(
                        keyword=keyword,
                        date=date.isoformat(),
                        post_count=int(stats['post_count']),
                        total_interactions=int(stats['total_interactions']),
                        average_sentiment=avg_sentiment,
                        momentum_score=momentum_score
                    ))
            
            logger.info(f"完成 {len(set(kt.keyword for kt in keyword_trends))} 個關鍵詞的趨勢分析")
            return keyword_trends
            
        except Exception as e:
            logger.error(f"關鍵詞趨勢分析失敗: {e}")
            return []
    
    def _calculate_keyword_momentum(self, keyword: str, current_date, df: pd.DataFrame, days: int = 3) -> float:
        """計算關鍵詞動量分數"""
        try:
            # 獲取關鍵詞在最近幾天的出現頻率
            end_date = pd.to_datetime(current_date)
            start_date = end_date - timedelta(days=days)
            
            recent_posts = df[
                (df['timestamp'].dt.date >= start_date.date()) & 
                (df['timestamp'].dt.date <= end_date.date()) &
                (df['content'].str.contains(keyword, case=False, na=False))
            ]
            
            if len(recent_posts) < 2:
                return 0.0
            
            # 按天分組計算頻率變化
            daily_counts = recent_posts.groupby(recent_posts['timestamp'].dt.date).size()
            
            if len(daily_counts) < 2:
                return 0.0
            
            # 計算變化率
            values = daily_counts.values
            momentum = (values[-1] - values[0]) / (len(values) - 1) if len(values) > 1 else 0
            
            return max(0, momentum)  # 只關注正向動量
            
        except Exception:
            return 0.0
    
    def _analyze_sentiment_for_posts(self, contents: List[str]) -> float:
        """分析貼文列表的平均情感分數"""
        if not self.sentiment_analyzer or not contents:
            return 0.0
        
        try:
            scores = []
            for content in contents:
                if content and content.strip():
                    sentiment_scores = self.sentiment_analyzer.polarity_scores(content)
                    scores.append(sentiment_scores['compound'])
            
            return np.mean(scores) if scores else 0.0
            
        except Exception:
            return 0.0
    
    def save_processed_data(self, post_metrics: List[PostMetrics], 
                          topic_summaries: List[TopicSummary],
                          keyword_trends: List[KeywordTrend]) -> Dict[str, int]:
        """
        保存處理後的數據到數據庫
        
        Args:
            post_metrics: 貼文指標列表
            topic_summaries: 主題摘要列表  
            keyword_trends: 關鍵詞趨勢列表
            
        Returns:
            Dict[str, int]: 保存結果統計
        """
        results = {
            'post_metrics_saved': 0,
            'topics_saved': 0,
            'trends_saved': 0,
            'errors': 0
        }
        
        try:
            # 保存貼文指標
            if post_metrics:
                for metric in post_metrics:
                    try:
                        metric_data = {
                            'post_id': metric.post_id,
                            'total_interactions': metric.total_interactions,
                            'heat_density': metric.heat_density,
                            'freshness_score': metric.freshness_score,
                            'engagement_rate': metric.engagement_rate,
                            'viral_potential': metric.viral_potential,
                            'processed_at': datetime.now(timezone.utc).isoformat()
                        }
                        
                        result = self.db_manager.client.table('processed_post_metrics').upsert(
                            metric_data, on_conflict='post_id'
                        ).execute()
                        
                        if result.data:
                            results['post_metrics_saved'] += 1
                        
                    except Exception as e:
                        logger.error(f"保存貼文指標失敗: {e}")
                        results['errors'] += 1
            
            # 保存主題摘要
            if topic_summaries:
                for topic in topic_summaries:
                    try:
                        topic_data = {
                            'topic_keywords': topic.topic_keywords,
                            'topic_name': topic.topic_name,
                            'post_count': topic.post_count,
                            'average_heat_density': topic.average_heat_density,
                            'total_interactions': topic.total_interactions,
                            'dominant_sentiment': topic.dominant_sentiment,
                            'trending_score': topic.trending_score,
                            'processed_at': datetime.now(timezone.utc).isoformat()
                        }
                        
                        result = self.db_manager.client.table('processed_topic_summary').insert(
                            topic_data
                        ).execute()
                        
                        if result.data:
                            results['topics_saved'] += 1
                            
                    except Exception as e:
                        logger.error(f"保存主題摘要失敗: {e}")
                        results['errors'] += 1
            
            # 保存關鍵詞趨勢
            if keyword_trends:
                for trend in keyword_trends:
                    try:
                        trend_data = {
                            'keyword': trend.keyword,
                            'date': trend.date,
                            'post_count': trend.post_count,
                            'total_interactions': trend.total_interactions,
                            'average_sentiment': trend.average_sentiment,
                            'momentum_score': trend.momentum_score,
                            'processed_at': datetime.now(timezone.utc).isoformat()
                        }
                        
                        result = self.db_manager.client.table('processed_keyword_trends').upsert(
                            trend_data, on_conflict='keyword,date'
                        ).execute()
                        
                        if result.data:
                            results['trends_saved'] += 1
                            
                    except Exception as e:
                        logger.error(f"保存關鍵詞趨勢失敗: {e}")
                        results['errors'] += 1
            
            logger.info(f"數據保存完成: {results}")
            return results
            
        except Exception as e:
            logger.error(f"保存處理數據失敗: {e}")
            results['errors'] += 1
            return results
    
    def run_full_analysis(self, days_back: int = 7) -> Dict[str, Any]:
        """
        執行完整的數據分析流程
        
        Args:
            days_back: 分析回溯天數
            
        Returns:
            Dict[str, Any]: 分析結果摘要
        """
        logger.info(f"開始執行數據分析，回溯 {days_back} 天")
        
        results_summary = {
            'posts_processed': 0,
            'metrics_calculated': 0,
            'topics_identified': 0,
            'keywords_analyzed': 0,
            'save_results': {},
            'execution_time': 0,
            'errors': []
        }
        
        start_time = datetime.now()
        
        try:
            # 1. 獲取原始數據
            logger.info("步驟 1: 獲取原始貼文數據")
            df = self.fetch_raw_posts(days_back)
            
            if df.empty:
                logger.warning("沒有數據可供分析")
                return results_summary
            
            results_summary['posts_processed'] = len(df)
            
            # 2. 計算貼文指標
            logger.info("步驟 2: 計算貼文指標")
            df = self.calculate_heat_density(df)
            df = self.calculate_freshness_score(df)
            df = self.calculate_engagement_rate(df)
            df = self.calculate_viral_potential(df)
            
            # 創建貼文指標對象
            post_metrics = []
            for _, row in df.iterrows():
                post_metrics.append(PostMetrics(
                    post_id=row['post_id'],
                    total_interactions=int(row['total_interactions']),
                    heat_density=float(row['heat_density']),
                    freshness_score=float(row['freshness_score']),
                    engagement_rate=float(row['engagement_rate']),
                    viral_potential=float(row['viral_potential'])
                ))
            
            results_summary['metrics_calculated'] = len(post_metrics)
            
            # 3. 主題聚類分析
            logger.info("步驟 3: 執行主題聚類分析")
            topic_summaries = self.perform_topic_clustering(df)
            results_summary['topics_identified'] = len(topic_summaries)
            
            # 4. 關鍵詞趨勢分析
            logger.info("步驟 4: 分析關鍵詞趨勢")
            keyword_trends = self.analyze_keyword_trends(df, days_back)
            results_summary['keywords_analyzed'] = len(set(kt.keyword for kt in keyword_trends))
            
            # 5. 保存處理結果
            logger.info("步驟 5: 保存分析結果")
            save_results = self.save_processed_data(post_metrics, topic_summaries, keyword_trends)
            results_summary['save_results'] = save_results
            
            # 計算執行時間
            end_time = datetime.now()
            results_summary['execution_time'] = (end_time - start_time).total_seconds()
            
            logger.info(f"數據分析完成，耗時 {results_summary['execution_time']:.2f} 秒")
            logger.info(f"處理摘要: {results_summary}")
            
            return results_summary
            
        except Exception as e:
            error_msg = f"數據分析執行失敗: {e}"
            logger.error(error_msg)
            results_summary['errors'].append(error_msg)
            
            end_time = datetime.now()
            results_summary['execution_time'] = (end_time - start_time).total_seconds()
            
            return results_summary

def main():
    """主執行函數"""
    logger.info("啟動 Threads 數據處理程序")
    
    try:
        processor = DataProcessor()
        
        # 執行完整分析
        results = processor.run_full_analysis(days_back=7)
        
        # 輸出結果摘要
        print("\n" + "="*50)
        print("數據處理結果摘要")
        print("="*50)
        print(f"處理貼文數量: {results['posts_processed']}")
        print(f"計算指標數量: {results['metrics_calculated']}")
        print(f"識別主題數量: {results['topics_identified']}")
        print(f"分析關鍵詞數量: {results['keywords_analyzed']}")
        print(f"執行時間: {results['execution_time']:.2f} 秒")
        
        if results['save_results']:
            save_res = results['save_results']
            print(f"保存結果:")
            print(f"  - 貼文指標: {save_res.get('post_metrics_saved', 0)}")
            print(f"  - 主題摘要: {save_res.get('topics_saved', 0)}")
            print(f"  - 關鍵詞趨勢: {save_res.get('trends_saved', 0)}")
            print(f"  - 錯誤數量: {save_res.get('errors', 0)}")
        
        if results['errors']:
            print("錯誤信息:")
            for error in results['errors']:
                print(f"  - {error}")
        
    except KeyboardInterrupt:
        logger.info("用戶中斷程序執行")
    except Exception as e:
        logger.error(f"程序執行失敗: {e}")

if __name__ == "__main__":
    main()