'use client'

import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { motion } from 'framer-motion'

interface TopicData {
  topic_id: number
  topic_name: string
  topic_keywords: string[]
  post_count: number
  average_heat_density: number
  total_interactions: number
  dominant_sentiment: string
  trending_score: number
  size: number
  color: string
  children?: {
    name: string
    value: number
    sentiment: string
    posts: number
  }[]
}

interface TopicTreemapProps {
  data: TopicData[]
}

interface HierarchyData {
    name: string;
    value?: number;
    data?: TopicData;
    children?: HierarchyData[];
}

export default function TopicTreemap({ data }: TopicTreemapProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [tooltip, setTooltip] = useState<{ x: number; y: number; visible: boolean; data?: TopicData }>({
    x: 0,
    y: 0,
    visible: false
  })

  useEffect(() => {
    if (!data || data.length === 0) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    // 设置图表尺寸
    const width = 800
    const height = 500
    const padding = 2

    svg.attr('width', width).attr('height', height)

    // 准备层次数据
    const hierarchyData: HierarchyData = {
      name: "主题",
      children: data.map(topic => ({
        name: topic.topic_name,
        value: topic.size,
        data: topic,
        children: topic.children || []
      }))
    }

    // 创建层次结构
    const root = d3.hierarchy(hierarchyData)
      .sum(d => d.value || 0)
      .sort((a, b) => (b.value || 0) - (a.value || 0))

    // 创建树图布局
    const treemap = d3.treemap<HierarchyData>()
      .size([width, height])
      .padding(padding)
      .round(true)

    treemap(root)

    // 情感颜色映射
    const sentimentColors = {
      'positive': '#10b981',
      'negative': '#ef4444', 
      'neutral': '#6b7280'
    }

    // 创建渐变定义
    const defs = svg.append('defs')
    
    data.forEach(topic => {
      const gradient = defs.append('linearGradient')
        .attr('id', `gradient-${topic.topic_id}`)
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '100%')
        .attr('y2', '100%')

      gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', topic.color)
        .attr('stop-opacity', 0.8)

      gradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', d3.color(topic.color)?.darker(0.5) || topic.color)
        .attr('stop-opacity', 1)
    })

    // 创建主要矩形
    const leaves = root.leaves()
    
    const cells = svg.selectAll('.cell')
      .data(leaves)
      .enter()
      .append('g')
      .attr('class', 'cell')
      .attr('transform', d => `translate(${d.x0},${d.y0})`)
      .style('cursor', 'pointer')

    // 主矩形
    const rects = cells.append('rect')
      .attr('width', d => Math.max(0, d.x1 - d.x0))
      .attr('height', d => Math.max(0, d.y1 - d.y0))
      .attr('fill', d => `url(#gradient-${(d.data.data as TopicData).topic_id})`)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('opacity', 0)

    // 动画效果
    rects.transition()
      .duration(1000)
      .delay((d, i) => i * 100)
      .style('opacity', 0.9)
      .ease(d3.easeBackOut)

    // 主题名称标签
    const labels = cells.append('text')
      .attr('x', d => (d.x1 - d.x0) / 2)
      .attr('y', 20)
      .attr('text-anchor', 'middle')
      .style('font-size', d => {
        const width = d.x1 - d.x0
        const height = d.y1 - d.y0
        const area = width * height
        return `${Math.min(16, Math.max(10, Math.sqrt(area) / 10))}px`
      })
      .style('font-weight', 'bold')
      .style('fill', '#fff')
      .style('text-shadow', '1px 1px 2px rgba(0,0,0,0.7)')
      .style('opacity', 0)
      .text(d => d.data.name)

    // 标签动画
    labels.transition()
      .duration(800)
      .delay((d, i) => i * 100 + 300)
      .style('opacity', 1)

    // 统计信息标签
    const statsLabels = cells.append('text')
      .attr('x', d => (d.x1 - d.x0) / 2)
      .attr('y', d => (d.y1 - d.y0) / 2 + 10)
      .attr('text-anchor', 'middle')
      .style('font-size', '12px')
      .style('fill', '#fff')
      .style('text-shadow', '1px 1px 2px rgba(0,0,0,0.7)')
      .style('opacity', 0)
      .text(d => `${(d.data.data as TopicData).post_count} 篇`)

    const interactionLabels = cells.append('text')
      .attr('x', d => (d.x1 - d.x0) / 2)
      .attr('y', d => (d.y1 - d.y0) / 2 + 25)
      .attr('text-anchor', 'middle')
      .style('font-size', '11px')
      .style('fill', '#fff')
      .style('text-shadow', '1px 1px 2px rgba(0,0,0,0.7)')
      .style('opacity', 0)
      .text(d => `${(d.data.data as TopicData).total_interactions.toLocaleString()} 互动`)

    // 统计标签动画
    statsLabels.transition()
      .duration(600)
      .delay((d, i) => i * 100 + 600)
      .style('opacity', 0.9)

    interactionLabels.transition()
      .duration(600)
      .delay((d, i) => i * 100 + 700)
      .style('opacity', 0.8)

    // 情感指示器
    const sentimentIndicators = cells.append('circle')
      .attr('cx', d => (d.x1 - d.x0) - 15)
      .attr('cy', 15)
      .attr('r', 6)
      .attr('fill', d => sentimentColors[(d.data.data as TopicData).dominant_sentiment as keyof typeof sentimentColors] || sentimentColors.neutral)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('opacity', 0)

    sentimentIndicators.transition()
      .duration(500)
      .delay((d, i) => i * 100 + 800)
      .style('opacity', 0.9)

    // 趋势指示器（小三角形）
    const trendIndicators = cells.append('path')
      .attr('d', d => {
        const x = (d.x1 - d.x0) - 30
        const y = 15
        const size = 5
        const trend = (d.data.data as TopicData).trending_score
        if (trend > 0.7) {
          // 向上箭头
          return `M${x},${y+size} L${x+size},${y-size} L${x-size},${y-size} Z`
        } else if (trend < 0.3) {
          // 向下箭头
          return `M${x},${y-size} L${x+size},${y+size} L${x-size},${y+size} Z`
        } else {
          // 水平线
          return `M${x-size},${y} L${x+size},${y}`
        }
      })
      .attr('fill', d => {
        const trend = (d.data.data as TopicData).trending_score
        return trend > 0.7 ? '#10b981' : trend < 0.3 ? '#ef4444' : '#6b7280'
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 1)
      .style('opacity', 0)

    trendIndicators.transition()
      .duration(500)
      .delay((d, i) => i * 100 + 900)
      .style('opacity', 0.8)

    // 子主题显示
    cells.each(function(d) {
      if (d.data.children && d.data.children.length > 0) {
        const cellWidth = d.x1 - d.x0
        const cellHeight = d.y1 - d.y0
        
        if (cellWidth > 120 && cellHeight > 80) {
          const subTopics = d.data.children.slice(0, 3) // 最多显示3个子主题
          
          subTopics.forEach((child, i) => {
            d3.select(this).append('text')
              .attr('x', 10)
              .attr('y', cellHeight - 40 + i * 12)
              .style('font-size', '9px')
              .style('fill', '#fff')
              .style('text-shadow', '1px 1px 1px rgba(0,0,0,0.8)')
              .style('opacity', 0)
              .text(`• ${child.name}`)
              .transition()
              .duration(400)
              .delay(1000 + i * 100)
              .style('opacity', 0.7)
          })
        }
      }
    })

    // 鼠标事件处理
    cells
      .on('mouseenter', function(event, d: d3.HierarchyRectangularNode<HierarchyData>) {
        const [x, y] = d3.pointer(event, document.body)
        
        d3.select(this).select('rect')
          .transition()
          .duration(200)
          .style('opacity', 1)
          .attr('stroke-width', 3)

        d3.select(this)
          .transition()
          .duration(200)
          .attr('transform', 
            `translate(${d.x0},${d.y0}) scale(1.02) translate(${-(d.x1-d.x0)*0.01},${-(d.y1-d.y0)*0.01})`
          )

        setTooltip({ x, y, visible: true, data: d.data.data })
      })
      .on('mouseleave', function(event, d: d3.HierarchyRectangularNode<HierarchyData>) {
        d3.select(this).select('rect')
          .transition()
          .duration(200)
          .style('opacity', 0.9)
          .attr('stroke-width', 2)

        d3.select(this)
          .transition()
          .duration(200)
          .attr('transform', `translate(${d.x0},${d.y0})`)

        setTooltip(prev => ({ ...prev, visible: false }))
      })
      .on('click', function(event, d: d3.HierarchyRectangularNode<HierarchyData>) {
        // 点击时可以展开详细信息或进行钻取
        console.log('Topic clicked:', d.data.data)
      })

    // 标题
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', 20)
      .attr('text-anchor', 'middle')
      .style('font-size', '18px')
      .style('font-weight', 'bold')
      .style('fill', '#333')
      .text('主题分布矩阵树图')

  }, [data])

  return (
    <div className="relative">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full flex justify-center"
      >
        <svg
          ref={svgRef}
          className="border border-gray-200 rounded-lg bg-white shadow-sm"
        />
      </motion.div>

      {/* 工具提示 */}
      {tooltip.visible && tooltip.data && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          className="fixed bg-gray-900 text-white p-4 rounded-lg shadow-xl z-50 max-w-sm"
          style={{
            left: Math.min(tooltip.x + 10, window.innerWidth - 250),
            top: tooltip.y - 150,
            pointerEvents: 'none'
          }}
        >
          <div className="space-y-2">
            <div className="font-bold text-lg" style={{ color: tooltip.data.color }}>
              {tooltip.data.topic_name}
            </div>
            
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="text-gray-400">贴文数:</span>
                <span className="ml-1 font-medium">{tooltip.data.post_count}</span>
              </div>
              <div>
                <span className="text-gray-400">互动数:</span>
                <span className="ml-1 font-medium">{tooltip.data.total_interactions.toLocaleString()}</span>
              </div>
              <div>
                <span className="text-gray-400">平均热度:</span>
                <span className="ml-1 font-medium">{tooltip.data.average_heat_density.toFixed(1)}</span>
              </div>
              <div>
                <span className="text-gray-400">趋势分数:</span>
                <span className="ml-1 font-medium">{(tooltip.data.trending_score * 100).toFixed(0)}%</span>
              </div>
            </div>
            
            <div>
              <span className="text-gray-400">情感倾向:</span>
              <span className={`ml-1 font-medium ${
                tooltip.data.dominant_sentiment === 'positive' ? 'text-green-400' :
                tooltip.data.dominant_sentiment === 'negative' ? 'text-red-400' : 'text-gray-400'
              }`}>
                {tooltip.data.dominant_sentiment === 'positive' ? '积极' :
                 tooltip.data.dominant_sentiment === 'negative' ? '消极' : '中性'}
              </span>
            </div>
            
            <div>
              <span className="text-gray-400">关键词:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {tooltip.data.topic_keywords.slice(0, 4).map((keyword: string, i: number) => (
                  <span key={i} className="bg-gray-700 px-2 py-1 rounded text-xs">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* 图例 */}
      <div className="mt-4 flex flex-wrap justify-center gap-4">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-green-500 rounded-full"></div>
          <span className="text-sm text-gray-600">积极情感</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-red-500 rounded-full"></div>
          <span className="text-sm text-gray-600">消极情感</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-gray-500 rounded-full"></div>
          <span className="text-sm text-gray-600">中性情感</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-0 h-0 border-l-2 border-r-2 border-b-4 border-l-transparent border-r-transparent border-b-green-500"></div>
          <span className="text-sm text-gray-600">上升趋势</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-0 h-0 border-l-2 border-r-2 border-t-4 border-l-transparent border-r-transparent border-t-red-500"></div>
          <span className="text-sm text-gray-600">下降趋势</span>
        </div>
      </div>

      {/* 图表说明 */}
      <div className="mt-4 text-sm text-gray-600 space-y-1">
        <p>• 矩形大小代表主题的互动数量</p>
        <p>• 矩形颜色区分不同主题类别</p>
        <p>• 右上角圆点表示情感倾向，三角形表示趋势方向</p>
        <p>• 悬停查看详细信息，点击可进行更深入分析</p>
      </div>
    </div>
  )
}
