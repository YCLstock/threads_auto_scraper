import { Metadata } from 'next'
import Dashboard from '@/components/Dashboard'

export const metadata: Metadata = {
  title: 'Threads 趋势仪表板',
  description: '视觉化分析 Threads 平台的热门贴文、趋势关键字与主题分布',
}

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <Dashboard />
    </main>
  )
}
