'use client'

import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import { motion } from 'framer-motion'

import { KeywordTrendData } from '@/lib/types';

interface TrendRiverChartProps {
  data: KeywordTrendData[];
}

interface RiverPath {
  key: string;
}

// Helper function to check if data is a specific data point from the trend
function isTooltipDataPoint(data: KeywordTrendData | (KeywordTrendData['data'][0] & { keyword: string, color: string })): data is (KeywordTrendData['data'][0] & { keyword: string, color: string }) {
  return 'date' in data && 'post_count' in data; 
}

export default function TrendRiverChart({ data }: TrendRiverChartProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null)
  const [tooltip, setTooltip] = useState<{ x: number; y: number; visible: boolean; data?: KeywordTrendData | (KeywordTrendData['data'][0] & { keyword: string, color: string }) }>({
    x: 0,
    y: 0,
    visible: false
  })

  useEffect(() => {
    if (!data || data.length === 0) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    // 设置图表尺寸
    const margin = { top: 40, right: 120, bottom: 60, left: 60 }
    const width = 900 - margin.left - margin.right
    const height = 400 - margin.top - margin.bottom

    // 创建主容器
    const container = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // 处理数据
    const allDates = Array.from(new Set(data.flatMap(d => d.data.map(item => item.date)))).sort()
    const parseDate = d3.timeParse('%Y-%m-%d')
    const formatDate = d3.timeFormat('%m/%d')

    // 创建比例尺
    const xScale = d3.scaleTime()
      .domain(d3.extent(allDates, d => parseDate(d)) as [Date, Date])
      .range([0, width])

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d3.max(d.data, item => item.post_count)) as number])
      .range([height, 0])

    // 创建堆叠数据
    const stackData = allDates.map(date => {
      const dateData: { date: Date | null; [key: string]: number | Date | null } = { date: parseDate(date) }
      data.forEach(keyword => {
        const found = keyword.data.find(item => item.date === date)
        dateData[keyword.keyword] = found ? found.post_count : 0
      })
      return dateData
    })

    const stack = d3.stack<typeof stackData[number], string>()
      .keys(data.map(d => d.keyword))
      .order(d3.stackOrderNone)
      .offset(d3.stackOffsetWiggle)

    const stackedData = stack(stackData)

    // 更新y比例尺以适应堆叠数据
    const yExtent = d3.extent(stackedData.flat().flat()) as [number, number]
    yScale.domain(yExtent).nice()

    // 创建区域生成器
    const area = d3.area<d3.SeriesPoint<{ date: Date | null; [key: string]: number | Date | null }>>()
      .x(d => xScale(d.data.date as Date))
      .y0(d => yScale(d[0]))
      .y1(d => yScale(d[1]))
      .curve(d3.curveBasis)

    // 创建渐变定义
    const defs = svg.append('defs')
    data.forEach(keyword => {
      const gradient = defs.append('linearGradient')
        .attr('id', `gradient-${keyword.keyword}`)
        .attr('gradientUnits', 'userSpaceOnUse')
        .attr('x1', 0).attr('y1', height)
        .attr('x2', 0).attr('y2', 0)

      gradient.append('stop')
        .attr('offset', '0%')
        .attr('stop-color', keyword.color)
        .attr('stop-opacity', 0.2)

      gradient.append('stop')
        .attr('offset', '100%')
        .attr('stop-color', keyword.color)
        .attr('stop-opacity', 0.8)
    })

    // 创建河流路径
    const paths = container.selectAll('.river-path')
      .data(stackedData)
      .enter()
      .append('path')
      .attr('class', 'river-path')
      .attr('d', area)
      .style('fill', (d, i) => `url(#gradient-${data[i].keyword})`)
      .style('stroke', (d, i) => data[i].color)
      .style('stroke-width', 1)
      .style('cursor', 'pointer')
      .style('opacity', d => selectedKeyword === null || selectedKeyword === d.key ? 1 : 0.3)

    // 路径动画
    const totalLength = paths.nodes().map(node => (node as SVGPathElement).getTotalLength())
    
    paths
      .style('stroke-dasharray', (d, i) => `${totalLength[i]} ${totalLength[i]}`)
      .style('stroke-dashoffset', (d, i) => totalLength[i])
      .transition()
      .duration(2000)
      .ease(d3.easeLinear)
      .style('stroke-dashoffset', 0)

    // 鼠标事件处理
    paths
      .on('mouseenter', function(event, d: d3.Series<{ date: Date | null; [key: string]: number | Date | null; }, string>) {
        const keywordIndex = stackedData.indexOf(d)
        const keyword = data[keywordIndex]
        const [x, y] = d3.pointer(event, document.body)
        
        setSelectedKeyword(keyword.keyword)
        setTooltip({ x, y, visible: true, data: keyword })

        // 高亮当前路径
        d3.selectAll('.river-path')
          .style('opacity', (path: RiverPath) => path.key === keyword.keyword ? 1 : 0.2)
      })
      .on('mouseleave', function() {
        setSelectedKeyword(null)
        setTooltip(prev => ({ ...prev, visible: false }))

        // 恢复所有路径透明度
        d3.selectAll('.river-path')
          .style('opacity', 1)
      })

    // 创建坐标轴
    const xAxis = d3.axisBottom(xScale)
      .tickFormat(formatDate)
      .ticks(d3.timeDay.every(1))

    const yAxis = d3.axisLeft(yScale)
      .ticks(6)

    container.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${height})`)
      .call(xAxis)
      .selectAll('text')
      .style('font-size', '12px')
      .style('fill', '#666')

    container.append('g')
      .attr('class', 'y-axis')
      .call(yAxis)
      .selectAll('text')
      .style('font-size', '12px')
      .style('fill', '#666')

    // 坐标轴标签
    container.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 0 - margin.left)
      .attr('x', 0 - height / 2)
      .attr('dy', '1em')
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('fill', '#666')
      .text('贴文数量')

    container.append('text')
      .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 10})`)
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('fill', '#666')
      .text('日期')

    // 创建图例
    const legend = container.append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${width + 20}, 20)`)

    const legendItems = legend.selectAll('.legend-item')
      .data(data)
      .enter()
      .append('g')
      .attr('class', 'legend-item')
      .attr('transform', (d, i) => `translate(0, ${i * 25})`)
      .style('cursor', 'pointer')

    legendItems.append('rect')
      .attr('width', 15)
      .attr('height', 15)
      .style('fill', d => d.color)
      .style('opacity', 0.8)

    legendItems.append('text')
      .attr('x', 20)
      .attr('y', 12)
      .style('font-size', '12px')
      .style('fill', '#333')
      .text(d => d.keyword)

    legendItems.append('text')
      .attr('x', 20)
      .attr('y', 25)
      .style('font-size', '10px')
      .style('fill', '#666')
      .text(d => `${d.total_mentions} 次提及`)

    // 图例交互
    legendItems
      .on('mouseenter', function(event, d) {
        setSelectedKeyword(d.keyword)
        d3.selectAll('.river-path')
          .style('opacity', (path: RiverPath) => path.key === d.keyword ? 1 : 0.2)
      })
      .on('mouseleave', function() {
        setSelectedKeyword(null)
        d3.selectAll('.river-path')
          .style('opacity', 1)
      })

    // 添加数据点
    data.forEach((keyword, keywordIndex) => {
      const points = container.selectAll(`.points-${keywordIndex}`)
        .data(keyword.data)
        .enter()
        .append('circle')
        .attr('class', `points-${keywordIndex}`)
        .attr('cx', d => xScale(parseDate(d.date) as Date))
        .attr('cy', d => {
          // 找到对应的堆叠数据点
          const stackPoint = stackedData[keywordIndex].find(s => 
            (s.data.date as Date).getTime() === (parseDate(d.date) as Date).getTime()
          )
          return stackPoint ? yScale((stackPoint[0] + stackPoint[1]) / 2) : yScale(0)
        })
        .attr('r', 0)
        .style('fill', keyword.color)
        .style('stroke', '#fff')
        .style('stroke-width', 2)
        .style('opacity', 0)

      // 点的动画
      points.transition()
        .delay((d, i) => i * 100 + keywordIndex * 200)
        .duration(600)
        .attr('r', d => Math.sqrt(d.momentum_score) * 3 + 2)
        .style('opacity', 0.8)

      points
        .on('mouseenter', function(event, d) {
          const [x, y] = d3.pointer(event, document.body)
          setTooltip({ 
            x, 
            y, 
            visible: true, 
            data: { ...d, keyword: keyword.keyword, color: keyword.color }
          })

          d3.select(this)
            .transition()
            .duration(200)
            .attr('r', Math.sqrt(d.momentum_score) * 3 + 5)
        })
        .on('mouseleave', function(event, d) {
          setTooltip(prev => ({ ...prev, visible: false }))
          
          d3.select(this)
            .transition()
            .duration(200)
            .attr('r', Math.sqrt(d.momentum_score) * 3 + 2)
        })
    })

  }, [data, selectedKeyword])

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
          className="fixed bg-gray-900 text-white p-3 rounded-lg shadow-xl z-50"
          style={{
            left: tooltip.x + 10,
            top: tooltip.y - 80,
            pointerEvents: 'none'
          }}
        >
          <div className="space-y-1">
            {tooltip.data.keyword && (
              <div className="font-bold" style={{ color: tooltip.data.color }}>
                {tooltip.data.keyword}
              </div>
            )}
            {isTooltipDataPoint(tooltip.data) && (
              <div className="text-sm text-gray-300">
                日期: {new Date(tooltip.data.date).toLocaleDateString()}
              </div>
            )}
            <div className="text-sm">
              贴文数: {isTooltipDataPoint(tooltip.data) ? tooltip.data.post_count : tooltip.data.total_mentions}
            </div>
            {isTooltipDataPoint(tooltip.data) && tooltip.data.total_interactions && (
              <div className="text-sm">
                互动数: {tooltip.data.total_interactions.toLocaleString()}
              </div>
            )}
            {isTooltipDataPoint(tooltip.data) && tooltip.data.momentum_score && (
              <div className="text-sm">
                动量分数: {tooltip.data.momentum_score.toFixed(2)}
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* 图表说明 */}
      <div className="mt-4 text-sm text-gray-600 space-y-1">
        <p>• 河流宽度代表关键词在该时间的热度</p>
        <p>• 河流颜色区分不同关键词</p>
        <p>• 圆点大小表示动量分数，悬停查看详细数据</p>
      </div>
    </div>
  )
}
