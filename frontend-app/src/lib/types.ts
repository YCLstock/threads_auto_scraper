
export interface HeatBubbleData {
  post_id: string;
  username: string;
  content: string;
  timestamp: string;
  total_interactions: number;
  heat_density: number;
  freshness_score: number;
  engagement_rate: number;
  viral_potential: number;
  post_url: string;
}

export interface KeywordTrendData {
  keyword: string;
  data: {
    date: string;
    post_count: number;
  }[];
  color: string;
  total_mentions: number;
}

export interface TopicTreemapData {
  topic_id: string;
  topic_name: string;
  topic_keywords: string[];
  post_count: number;
  average_heat_density: number;
  total_interactions: number;
  dominant_sentiment: string;
  trending_score: number;
  size: number;
  color: string;
  children: {
    name: string;
    value: number;
    sentiment: string;
    posts: number;
  }[];
}

export interface DashboardStats {
  total_posts: number;
  total_interactions: number;
  active_topics: number;
  trending_keywords: number;
  total_users: number;
  data_range: { start_date: string; end_date: string };
  last_updated: string;
}

export interface DashboardData {
  metadata: {
    generated_at: string;
    data_source?: string;
  };
  heat_bubble_data: HeatBubbleData[];
  keyword_trends_data: KeywordTrendData[];
  topic_treemap_data: TopicTreemapData[];
  dashboard_stats: DashboardStats & {
    top_trending_topics: { name: string; growth_rate: number; posts_today: number }[];
    top_users: { username: string; total_interactions: number; posts_count: number }[];
  };
}
