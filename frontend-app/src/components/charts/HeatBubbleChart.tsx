'use client'

import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { motion } from 'framer-motion'

import { HeatBubbleData } from '@/lib/types';

interface BubbleData extends HeatBubbleData {
  x?: number;
  y?: number;
  radius?: number;
  color?: string;
}

interface HeatBubbleChartProps {
  data: BubbleData[]
}

export default function HeatBubbleChart({ data }: HeatBubbleChartProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [selectedBubble, setSelectedBubble] = useState<BubbleData | null>(null)
  const [tooltip, setTooltip] = useState<{ x: number; y: number; visible: boolean }>({
    x: 0,
    y: 0,
    visible: false
  })

  useEffect(() => {
    if (!data || data.length === 0) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    // 设置图表尺寸
    const margin = { top: 20, right: 20, bottom: 20, left: 20 }
    const width = 800 - margin.left - margin.right
    const height = 600 - margin.top - margin.bottom

    // 创建主容器
    const container = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // 添加渐变定义
    const defs = svg.append('defs')
    const gradient = defs.append('radialGradient')
      .attr('id', 'bubbleGradient')
      .attr('cx', '30%')
      .attr('cy', '30%')

    gradient.append('stop')
      .attr('offset', '0%')
      .attr('stop-color', 'rgba(255,255,255,0.3)')

    gradient.append('stop')
      .attr('offset', '100%')
      .attr('stop-color', 'rgba(0,0,0,0.1)')

    // 创建比例尺
    const radiusScale = d3.scaleSqrt()
      .domain(d3.extent(data, d => d.total_interactions) as [number, number])
      .range([15, 60])

    const colorScale = d3.scaleSequential(d3.interpolateViridis)
      .domain(d3.extent(data, d => d.heat_density) as [number, number])

    // 力导向模拟
    const simulation = d3.forceSimulation(data as d3.SimulationNodeDatum[])
      .force('charge', d3.forceManyBody().strength(-50))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius((d: any) => radiusScale((d as BubbleData).total_interactions) + 2))
      .force('x', d3.forceX(width / 2).strength(0.1))
      .force('y', d3.forceY(height / 2).strength(0.1))

    // 创建气泡
    const bubbles = container.selectAll('.bubble')
      .data(data)
      .enter()
      .append('g')
      .attr('class', 'bubble')
      .style('cursor', 'pointer')

    // 添加气泡圆形
    const circles = bubbles.append('circle')
      .attr('r', 0)
      .attr('fill', d => colorScale(d.heat_density))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('filter', 'url(#bubbleGradient)')
      .style('opacity', 0.8)

    // 添加用户名标签
    const labels = bubbles.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '.3em')
      .style('font-size', '12px')
      .style('font-weight', 'bold')
      .style('fill', '#fff')
      .style('pointer-events', 'none')
      .style('opacity', 0)
      .text(d => `@${d.username}`)

    // 动画进入效果
    circles.transition()
      .duration(1000)
      .delay((d, i) => i * 50)
      .attr('r', d => radiusScale(d.total_interactions))
      .ease(d3.easeBounceOut)

    labels.transition()
      .duration(800)
      .delay((d, i) => i * 50 + 200)
      .style('opacity', 1)

    // 鼠标事件处理
    bubbles
      .on('mouseenter', function(event, d) {
        const [x, y] = d3.pointer(event, document.body)
        
        d3.select(this).select('circle')
          .transition()
          .duration(200)
          .attr('r', radiusScale(d.total_interactions) * 1.2)
          .style('opacity', 1)

        setTooltip({ x, y, visible: true })
        setSelectedBubble(d)
      })
      .on('mouseleave', function(d) {
        d3.select(this).select('circle')
          .transition()
          .duration(200)
          .attr('r', radiusScale(d.total_interactions))
          .style('opacity', 0.8)

        setTooltip(prev => ({ ...prev, visible: false }))
        setSelectedBubble(null)
      })
      .on('click', function(event, d) {
        // 点击时可以打开详细信息或跳转到原始链接
        window.open(d.post_url, '_blank')
      })

    // 力导向模拟更新
    simulation.on('tick', () => {
      bubbles
        .attr('transform', (d: BubbleData) => `translate(${d.x},${d.y})`)
    })

    // 添加图例
    const legend = container.append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${width - 150}, 20)`)

    // 热度颜色图例
    const legendHeight = 100
    const legendWidth = 20
    
    const legendScale = d3.scaleLinear()
      .domain(colorScale.domain())
      .range([legendHeight, 0])

    const legendAxis = d3.axisRight(legendScale)
      .ticks(5)
      .tickFormat(d3.format('.1f'))

    // 创建渐变条
    const legendGradient = defs.append('linearGradient')
      .attr('id', 'legend-gradient')
      .attr('x1', '0%')
      .attr('y1', '100%')
      .attr('x2', '0%')
      .attr('y2', '0%')

    const stops = d3.range(0, 1.1, 0.1)
    stops.forEach(t => {
      legendGradient.append('stop')
        .attr('offset', `${t * 100}%`)
        .attr('stop-color', colorScale(colorScale.domain()[0] + t * (colorScale.domain()[1] - colorScale.domain()[0])))
    })

    legend.append('rect')
      .attr('width', legendWidth)
      .attr('height', legendHeight)
      .style('fill', 'url(#legend-gradient)')
      .style('stroke', '#ccc')

    legend.append('g')
      .attr('transform', `translate(${legendWidth}, 0)`)
      .call(legendAxis)

    legend.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', -30)
      .attr('x', -legendHeight / 2)
      .style('text-anchor', 'middle')
      .style('font-size', '12px')
      .style('fill', '#666')
      .text('热度密度')

    // 大小图例
    const sizeLegend = container.append('g')
      .attr('class', 'size-legend')
      .attr('transform', `translate(50, ${height - 80})`)

    const sizeData = [
      { interactions: d3.min(data, d => d.total_interactions) || 0, label: '低互动' },
      { interactions: d3.median(data, d => d.total_interactions) || 0, label: '中等互动' },
      { interactions: d3.max(data, d => d.total_interactions) || 0, label: '高互动' }
    ]

    sizeData.forEach((d, i) => {
      const g = sizeLegend.append('g')
        .attr('transform', `translate(${i * 80}, 0)`)

      g.append('circle')
        .attr('r', radiusScale(d.interactions))
        .attr('fill', 'rgba(100, 100, 100, 0.3)')
        .attr('stroke', '#999')

      g.append('text')
        .attr('y', radiusScale(d.interactions) + 15)
        .attr('text-anchor', 'middle')
        .style('font-size', '10px')
        .style('fill', '#666')
        .text(d.label)
    })

    // 清理函数
    return () => {
      simulation.stop()
    }
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
      {tooltip.visible && selectedBubble && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          className="fixed bg-gray-900 text-white p-4 rounded-lg shadow-xl z-50 max-w-sm"
          style={{
            left: tooltip.x + 10,
            top: tooltip.y - 100,
            pointerEvents: 'none'
          }}
        >
          <div className="space-y-2">
            <div className="font-bold text-blue-300">@{selectedBubble.username}</div>
            <div className="text-sm text-gray-300 line-clamp-3">
              {selectedBubble.content.slice(0, 100)}...
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="text-gray-400">互动数:</span>
                <span className="ml-1 font-medium">{selectedBubble.total_interactions.toLocaleString()}</span>
              </div>
              <div>
                <span className="text-gray-400">热度:</span>
                <span className="ml-1 font-medium">{selectedBubble.heat_density.toFixed(1)}</span>
              </div>
              <div>
                <span className="text-gray-400">新鲜度:</span>
                <span className="ml-1 font-medium">{(selectedBubble.freshness_score * 100).toFixed(0)}%</span>
              </div>
              <div>
                <span className="text-gray-400">病毒潜力:</span>
                <span className="ml-1 font-medium">{(selectedBubble.viral_potential * 100).toFixed(0)}%</span>
              </div>
            </div>
            <div className="text-xs text-gray-400 border-t border-gray-700 pt-2">
              点击查看原贴文
            </div>
          </div>
        </motion.div>
      )}

      {/* 图表说明 */}
      <div className="mt-4 text-sm text-gray-600 space-y-1">
        <p>• 气泡大小代表互动数量（点赞 + 回复 + 转发）</p>
        <p>• 气泡颜色代表热度密度（考虑时间衰减和用户影响力）</p>
        <p>• 悬停查看详细信息，点击跳转原贴文</p>
      </div>
    </div>
  )
}
