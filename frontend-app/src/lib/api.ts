import { supabase, isSupabaseConfigured, RawPost, ProcessedPostMetric, ProcessedTopicSummary, ProcessedKeywordTrend } from './supabase'

// 獲取熱度氣泡圖數據
export async function getHeatBubbleData() {
  try {
    const { data, error } = await supabase
      .from('raw_posts')
      .select(`
        post_id,
        username,
        content,
        timestamp,
        likes,
        replies,
        reposts,
        post_url,
        processed_post_metrics!inner(
          total_interactions,
          heat_density,
          freshness_score,
          engagement_rate,
          viral_potential
        )
      `)
      .order('timestamp', { ascending: false })
      .limit(50)

    if (error) {
      console.error('Error fetching heat bubble data:', error)
      return []
    }

    // 轉換數據格式
    return data?.map(post => ({
      post_id: post.post_id,
      username: post.username,
      content: post.content,
      timestamp: post.timestamp,
      total_interactions: post.processed_post_metrics[0]?.total_interactions || 0,
      heat_density: post.processed_post_metrics[0]?.heat_density || 0,
      freshness_score: post.processed_post_metrics[0]?.freshness_score || 0,
      engagement_rate: post.processed_post_metrics[0]?.engagement_rate || 0,
      viral_potential: post.processed_post_metrics[0]?.viral_potential || 0,
      post_url: post.post_url
    })) || []
  } catch (error) {
    console.error('Failed to fetch heat bubble data:', error)
    return []
  }
}

// 獲取關鍵詞趨勢數據
export async function getKeywordTrendsData() {
  try {
    // 獲取最近7天的關鍵詞趨勢
    const sevenDaysAgo = new Date()
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
    
    const { data, error } = await supabase
      .from('processed_keyword_trends')
      .select('*')
      .gte('date', sevenDaysAgo.toISOString().split('T')[0])
      .order('date', { ascending: true })

    if (error) {
      console.error('Error fetching keyword trends data:', error)
      return []
    }

    // 按關鍵詞分組數據
    const keywordGroups: { [key: string]: any[] } = {}
    data?.forEach(trend => {
      if (!keywordGroups[trend.keyword]) {
        keywordGroups[trend.keyword] = []
      }
      keywordGroups[trend.keyword].push({
        date: trend.date,
        post_count: trend.post_count,
        total_interactions: trend.total_interactions,
        momentum_score: trend.momentum_score
      })
    })

    // 轉換為前端需要的格式
    const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
    return Object.entries(keywordGroups).map(([keyword, data], index) => ({
      keyword,
      data,
      color: colors[index % colors.length],
      total_mentions: data.reduce((sum, item) => sum + item.post_count, 0)
    }))
  } catch (error) {
    console.error('Failed to fetch keyword trends data:', error)
    return []
  }
}

// 獲取主題樹狀圖數據
export async function getTopicTreemapData() {
  try {
    const { data, error } = await supabase
      .from('processed_topic_summary')
      .select('*')
      .order('total_interactions', { ascending: false })
      .limit(10)

    if (error) {
      console.error('Error fetching topic treemap data:', error)
      return []
    }

    // 轉換數據格式
    const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16']
    
    return data?.map((topic, index) => ({
      topic_id: topic.topic_id,
      topic_name: topic.topic_name,
      topic_keywords: topic.topic_keywords,
      post_count: topic.post_count,
      average_heat_density: topic.average_heat_density,
      total_interactions: topic.total_interactions,
      dominant_sentiment: topic.dominant_sentiment,
      trending_score: topic.trending_score,
      size: topic.total_interactions,
      color: colors[index % colors.length],
      children: topic.topic_keywords.slice(0, 3).map((keyword, i) => ({
        name: keyword,
        value: Math.floor(topic.total_interactions / (i + 2)),
        sentiment: topic.dominant_sentiment,
        posts: Math.floor(topic.post_count / (i + 2))
      }))
    })) || []
  } catch (error) {
    console.error('Failed to fetch topic treemap data:', error)
    return []
  }
}

// 獲取儀表板統計數據
export async function getDashboardStats() {
  try {
    // 並行獲取各種統計數據
    const [postsResult, metricsResult, topicsResult, trendsResult] = await Promise.all([
      supabase.from('raw_posts').select('post_id', { count: 'exact', head: true }),
      supabase.from('processed_post_metrics').select('total_interactions').order('created_at', { ascending: false }).limit(1000),
      supabase.from('processed_topic_summary').select('topic_id', { count: 'exact', head: true }),
      supabase.from('processed_keyword_trends').select('keyword').order('created_at', { ascending: false }).limit(500)
    ])

    const totalPosts = postsResult.count || 0
    const totalTopics = topicsResult.count || 0
    
    // 計算總互動數
    const totalInteractions = metricsResult.data?.reduce((sum, metric) => sum + metric.total_interactions, 0) || 0
    
    // 計算活躍關鍵詞數
    const uniqueKeywords = new Set(trendsResult.data?.map(trend => trend.keyword) || [])
    const activeKeywords = uniqueKeywords.size

    return {
      total_posts: totalPosts,
      total_interactions: totalInteractions,
      active_topics: totalTopics,
      trending_keywords: activeKeywords,
      last_updated: new Date().toISOString()
    }
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error)
    return {
      total_posts: 0,
      total_interactions: 0,
      active_topics: 0,
      trending_keywords: 0,
      last_updated: new Date().toISOString()
    }
  }
}

// 測試數據庫連接
export async function testConnection() {
  // 首先檢查配置
  if (!isSupabaseConfigured) {
    console.warn('Supabase not configured properly')
    return false
  }

  try {
    const { data, error } = await supabase
      .from('raw_posts')
      .select('post_id')
      .limit(1)

    if (error) {
      console.error('Database connection test failed:', error)
      return false
    }

    console.log('Database connection successful')
    return true
  } catch (error) {
    console.error('Database connection test failed:', error)
    return false
  }
}