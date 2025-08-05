-- Threads 趨勢儀表板資料庫架構
-- 版本: 2.0 (Supabase PostgreSQL)

-- 1. 原始數據表 (Raw Data Table)
CREATE TABLE raw_posts (
    post_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    content TEXT,
    timestamp TIMESTAMPTZ NOT NULL,
    likes INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    reposts INTEGER DEFAULT 0,
    images JSONB DEFAULT '[]'::jsonb,
    post_url TEXT,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 分析結果表 - 貼文指標
CREATE TABLE processed_post_metrics (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(255) REFERENCES raw_posts(post_id) ON DELETE CASCADE,
    total_interactions INTEGER NOT NULL,
    heat_density FLOAT NOT NULL,
    freshness_score FLOAT NOT NULL, -- 新鮮度分數 (0-1)
    engagement_rate FLOAT DEFAULT 0, -- 互動率
    viral_potential FLOAT DEFAULT 0, -- 病毒傳播潛力
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(post_id)
);

-- 3. 分析結果表 - 主題摘要
CREATE TABLE processed_topic_summary (
    topic_id SERIAL PRIMARY KEY,
    topic_keywords TEXT[] NOT NULL, -- 關鍵字陣列
    topic_name VARCHAR(200), -- 主題名稱
    post_count INTEGER NOT NULL,
    average_heat_density FLOAT NOT NULL,
    total_interactions INTEGER DEFAULT 0,
    dominant_sentiment VARCHAR(20) DEFAULT 'neutral', -- positive/negative/neutral
    trending_score FLOAT DEFAULT 0, -- 趨勢分數
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 分析結果表 - 關鍵字趨勢
CREATE TABLE processed_keyword_trends (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    post_count INTEGER NOT NULL,
    total_interactions INTEGER DEFAULT 0,
    average_sentiment FLOAT DEFAULT 0, -- 平均情感分數
    momentum_score FLOAT DEFAULT 0, -- 動量分數 (趨勢變化率)
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(keyword, date)
);

-- 5. 貼文主題關聯表 (多對多關係)
CREATE TABLE post_topic_relations (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(255) REFERENCES raw_posts(post_id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES processed_topic_summary(topic_id) ON DELETE CASCADE,
    relevance_score FLOAT DEFAULT 0, -- 相關性分數 (0-1)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(post_id, topic_id)
);

-- 6. 用戶活動統計表
CREATE TABLE user_activity_stats (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    total_posts INTEGER DEFAULT 0,
    total_interactions INTEGER DEFAULT 0,
    average_engagement_rate FLOAT DEFAULT 0,
    follower_growth_rate FLOAT DEFAULT 0,
    influence_score FLOAT DEFAULT 0,
    last_active TIMESTAMPTZ,
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(username)
);

-- 索引優化
CREATE INDEX idx_raw_posts_timestamp ON raw_posts(timestamp);
CREATE INDEX idx_raw_posts_username ON raw_posts(username);
CREATE INDEX idx_raw_posts_scraped_at ON raw_posts(scraped_at);

CREATE INDEX idx_post_metrics_heat_density ON processed_post_metrics(heat_density);
CREATE INDEX idx_post_metrics_total_interactions ON processed_post_metrics(total_interactions);

CREATE INDEX idx_keyword_trends_date ON processed_keyword_trends(date);
CREATE INDEX idx_keyword_trends_keyword ON processed_keyword_trends(keyword);
CREATE INDEX idx_keyword_trends_momentum ON processed_keyword_trends(momentum_score);

CREATE INDEX idx_topic_summary_trending ON processed_topic_summary(trending_score);

-- 觸發器：自動更新 updated_at 欄位
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_raw_posts_updated_at BEFORE UPDATE ON raw_posts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_topic_summary_updated_at BEFORE UPDATE ON processed_topic_summary FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_stats_updated_at BEFORE UPDATE ON user_activity_stats FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- RLS (Row Level Security) 政策設定 - 預留給 Supabase
-- ALTER TABLE raw_posts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE processed_post_metrics ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE processed_topic_summary ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE processed_keyword_trends ENABLE ROW LEVEL SECURITY;

-- 檢視表：熱門貼文綜合視圖
CREATE VIEW hot_posts_view AS
SELECT 
    rp.post_id,
    rp.username,
    rp.content,
    rp.timestamp,
    rp.post_url,
    ppm.total_interactions,
    ppm.heat_density,
    ppm.freshness_score,
    ppm.engagement_rate,
    ppm.viral_potential
FROM raw_posts rp
JOIN processed_post_metrics ppm ON rp.post_id = ppm.post_id
ORDER BY ppm.heat_density DESC, ppm.total_interactions DESC;

-- 檢視表：趨勢關鍵字視圖
CREATE VIEW trending_keywords_view AS
SELECT 
    keyword,
    SUM(post_count) as total_posts,
    SUM(total_interactions) as total_interactions,
    AVG(momentum_score) as avg_momentum,
    MAX(date) as latest_date
FROM processed_keyword_trends
WHERE date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY keyword
ORDER BY avg_momentum DESC, total_interactions DESC;