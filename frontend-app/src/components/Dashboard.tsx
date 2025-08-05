'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { BarChart3, TrendingUp, Hash, Activity, Users, MessageCircle, Database, Wifi, WifiOff } from 'lucide-react'

import HeatBubbleChart from '@/components/charts/HeatBubbleChart'
import TrendRiverChart from '@/components/charts/TrendRiverChart'
import TopicTreemap from '@/components/charts/TopicTreemap'
import StatsCard from '@/components/ui/StatsCard'
import mockData from '@/mock-data.json'
// Keep api imports for when we revert
import { 
  getHeatBubbleData, 
  getKeywordTrendsData, 
  getTopicTreemapData, 
  getDashboardStats,
  testConnection 
} from '@/lib/api'

interface DashboardData {
  metadata: any
  heat_bubble_data: any[]
  keyword_trends_data: any[]
  topic_treemap_data: any[]
  dashboard_stats: any
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [activeChart, setActiveChart] = useState<'bubble' | 'river' | 'treemap'>('bubble')
  const [isLoading, setIsLoading] = useState(true)
  // const [useRealData, setUseRealData] = useState(false) // Temporarily disabled for testing
  // const [connectionStatus, setConnectionStatus] = useState<'unknown' | 'connected' | 'failed'>('unknown') // Temporarily disabled for testing

  // Temporarily disabled for testing
  // const checkConnection = async () => {
  //   const isConnected = await testConnection()
  //   setConnectionStatus(isConnected ? 'connected' : 'failed')
  //   return isConnected
  // }

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true)
      
      // Forcing mock data for testing purposes
      console.log("Forcing mock data load for testing.");
      await new Promise(resolve => setTimeout(resolve, 800)) // 模擬加載延遲
      setData(mockData as DashboardData)
      
      setIsLoading(false)
    }

    loadData()
  }, []) // Empty dependency array to run only once

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="text-gray-600">加载数据中...</p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">数据加载失败</p>
      </div>
    )
  }

  const chartContainerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  }

  return (
    <div className="min-h-screen p-6">
      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mb-8"
      >
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                Threads 趋势仪表板
              </h1>
              <p className="text-gray-600">
                分析时间范围: {new Date(data.metadata.data_range.start_date).toLocaleDateString()} - {new Date(data.metadata.data_range.end_date).toLocaleDateString()}
              </p>
            </div>
            <div className="flex items-center space-x-4">
              {/* 數據源切換 - Temporarily disabled for testing */}
              
              <div className="text-sm text-gray-500">
                最后更新: {new Date().toLocaleTimeString()}
              </div>
              <div className={`h-3 w-3 rounded-full bg-blue-500`}></div>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Stats Cards */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="mb-8"
      >
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatsCard
              title="总贴文数"
              value={data.metadata.total_posts.toLocaleString()}
              change="+12.5%"
              trend="up"
              icon={<MessageCircle className="h-6 w-6" />}
              color="blue"
            />
            <StatsCard
              title="总互动数"
              value={data.metadata.total_interactions.toLocaleString()}
              change="+18.3%"
              trend="up"
              icon={<Activity className="h-6 w-6" />}
              color="green"
            />
            <StatsCard
              title="活跃用户"
              value={data.metadata.total_users.toString()}
              change="+5.2%"
              trend="up"
              icon={<Users className="h-6 w-6" />}
              color="purple"
            />
            <StatsCard
              title="热门话题"
              value={data.topic_treemap_data.length.toString()}
              change="+3.1%"
              trend="up"
              icon={<Hash className="h-6 w-6" />}
              color="orange"
            />
          </div>
        </div>
      </motion.section>

      {/* Chart Navigation */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="mb-8"
      >
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={() => setActiveChart('bubble')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all duration-300 ${
                activeChart === 'bubble'
                  ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                  : 'bg-white text-gray-700 hover:bg-blue-50 hover:text-blue-600 shadow-md'
              }`}
            >
              <BarChart3 className="h-5 w-5" />
              <span>热度气泡图</span>
            </button>
            <button
              onClick={() => setActiveChart('river')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all duration-300 ${
                activeChart === 'river'
                  ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                  : 'bg-white text-gray-700 hover:bg-blue-50 hover:text-blue-600 shadow-md'
              }`}
            >
              <TrendingUp className="h-5 w-5" />
              <span>趋势河流图</span>
            </button>
            <button
              onClick={() => setActiveChart('treemap')}
              className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all duration-300 ${
                activeChart === 'treemap'
                  ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                  : 'bg-white text-gray-700 hover:bg-blue-50 hover:text-blue-600 shadow-md'
              }`}
            >
              <Hash className="h-5 w-5" />
              <span>主题矩阵树图</span>
            </button>
          </div>
        </div>
      </motion.section>

      {/* Chart Display */}
      <motion.section
        key={activeChart}
        variants={chartContainerVariants}
        initial="hidden"
        animate="visible"
        className="mb-8"
      >
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-6">
            {activeChart === 'bubble' && (
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">热度气泡图</h3>
                <p className="text-gray-600 mb-6">
                  气泡大小代表互动数量，颜色深度代表热度密度，位置反映新鲜度
                </p>
                <HeatBubbleChart data={data.heat_bubble_data} />
              </div>
            )}
            
            {activeChart === 'river' && (
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">趋势河流图</h3>
                <p className="text-gray-600 mb-6">
                  展示关键词在时间轴上的热度变化趋势
                </p>
                <TrendRiverChart data={data.keyword_trends_data} />
              </div>
            )}
            
            {activeChart === 'treemap' && (
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">主题矩阵树图</h3>
                <p className="text-gray-600 mb-6">
                  通过矩形大小和颜色展示各主题的热度分布
                </p>
                <TopicTreemap data={data.topic_treemap_data} />
              </div>
            )}
          </div>
        </div>
      </motion.section>

      {/* Top Trending Topics */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* 热门话题 */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-red-500" />
                今日热门话题
              </h3>
              <div className="space-y-4">
                {data.dashboard_stats.top_trending_topics.map((topic: any, index: number) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">{topic.name}</h4>
                      <p className="text-sm text-gray-600">{topic.posts_today} 篇新贴文</p>
                    </div>
                    <div className="text-right">
                      <span className="text-green-600 font-medium">+{topic.growth_rate}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 活跃用户 */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                <Users className="h-5 w-5 mr-2 text-blue-500" />
                活跃用户排行
              </h3>
              <div className="space-y-4">
                {data.dashboard_stats.top_users.map((user: any, index: number) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                        <span className="text-blue-600 font-medium">{index + 1}</span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900">@{user.username}</h4>
                        <p className="text-sm text-gray-600">{user.posts_count} 篇贴文</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="text-gray-900 font-medium">{user.total_interactions.toLocaleString()}</span>
                      <p className="text-sm text-gray-600">总互动</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </motion.section>
    </div>
  )
}
