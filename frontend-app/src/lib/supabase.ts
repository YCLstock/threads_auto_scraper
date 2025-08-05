import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-key'

// 檢查是否為 placeholder 值
const isValidConfig = 
  supabaseUrl !== 'https://your-project.supabase.co' && 
  supabaseUrl !== 'https://placeholder.supabase.co' &&
  supabaseAnonKey !== 'your-anon-key-here' && 
  supabaseAnonKey !== 'placeholder-key'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// 導出配置狀態
export const isSupabaseConfigured = isValidConfig

// 數據庫類型定義
export interface RawPost {
  post_id: string
  username: string
  content: string
  timestamp: string
  likes: number
  replies: number
  reposts: number
  images?: string[]
  post_url?: string
  scraped_at: string
  created_at: string
  updated_at: string
}

export interface ProcessedPostMetric {
  id: number
  post_id: string
  total_interactions: number
  heat_density: number
  freshness_score: number
  engagement_rate: number
  viral_potential: number
  processed_at: string
  created_at: string
}

export interface ProcessedTopicSummary {
  topic_id: number
  topic_keywords: string[]
  topic_name: string
  post_count: number
  average_heat_density: number
  total_interactions: number
  dominant_sentiment: 'positive' | 'negative' | 'neutral'
  trending_score: number
  processed_at: string
  created_at: string
  updated_at: string
}

export interface ProcessedKeywordTrend {
  id: number
  keyword: string
  date: string
  post_count: number
  total_interactions: number
  average_sentiment: number
  momentum_score: number
  processed_at: string
  created_at: string
}