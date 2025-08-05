'use client'

import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface StatsCardProps {
  title: string
  value: string
  change: string
  trend: 'up' | 'down'
  icon: React.ReactNode
  color: 'blue' | 'green' | 'purple' | 'orange' | 'red'
}

const colorVariants = {
  blue: {
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    iconBg: 'bg-blue-100',
    iconText: 'text-blue-600',
    accent: 'text-blue-600'
  },
  green: {
    bg: 'bg-green-50',
    border: 'border-green-200', 
    iconBg: 'bg-green-100',
    iconText: 'text-green-600',
    accent: 'text-green-600'
  },
  purple: {
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    iconBg: 'bg-purple-100', 
    iconText: 'text-purple-600',
    accent: 'text-purple-600'
  },
  orange: {
    bg: 'bg-orange-50',
    border: 'border-orange-200',
    iconBg: 'bg-orange-100',
    iconText: 'text-orange-600', 
    accent: 'text-orange-600'
  },
  red: {
    bg: 'bg-red-50',
    border: 'border-red-200',
    iconBg: 'bg-red-100',
    iconText: 'text-red-600',
    accent: 'text-red-600'
  }
}

export default function StatsCard({ title, value, change, trend, icon, color }: StatsCardProps) {
  const colors = colorVariants[color]
  
  return (
    <motion.div
      whileHover={{ y: -5, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`${colors.bg} ${colors.border} border-2 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300`}
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`${colors.iconBg} p-3 rounded-lg`}>
          <div className={colors.iconText}>
            {icon}
          </div>
        </div>
        <div className={`flex items-center space-x-1 ${trend === 'up' ? 'text-green-600' : 'text-red-500'}`}>
          {trend === 'up' ? (
            <TrendingUp className="h-4 w-4" />
          ) : (
            <TrendingDown className="h-4 w-4" />
          )}
          <span className="text-sm font-medium">{change}</span>
        </div>
      </div>
      
      <div>
        <h3 className="text-gray-600 text-sm font-medium mb-1">{title}</h3>
        <p className={`text-3xl font-bold ${colors.accent}`}>{value}</p>
      </div>
      
      {/* 装饰性动画条 */}
      <div className="mt-4 h-1 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: '75%' }}
          transition={{ duration: 2, delay: 0.5, ease: 'easeOut' }}
          className={`h-full rounded-full ${colors.accent.replace('text', 'bg')}`}
        />
      </div>
    </motion.div>
  )
}