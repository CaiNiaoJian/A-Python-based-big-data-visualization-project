<template>
  <div class="chart-container" ref="chartContainer"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'MilitaryChart',
  props: {
    type: {
      type: String,
      default: 'line',
      validator: (value) => ['line', 'bar', 'pie', 'radar', 'scatter'].includes(value)
    },
    data: {
      type: Object,
      required: true
    },
    theme: {
      type: String,
      default: ''
    },
    height: {
      type: String,
      default: '300px'
    },
    width: {
      type: String,
      default: '100%'
    },
    options: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      chart: null,
      isFirstRender: true
    }
  },
  methods: {
    // 初始化图表
    initChart() {
      if (!this.$refs.chartContainer) return
      
      // 确保DOM已经渲染完毕
      this.$nextTick(() => {
        if (this.chart) {
          this.chart.dispose()
        }
        
        this.chart = echarts.init(this.$refs.chartContainer, this.theme)
        
        // 设置响应式调整大小
        window.addEventListener('resize', this.resizeChart)
        
        // 首次更新前确保有效数据
        if (this.isValidData()) {
          this.updateChart()
          this.isFirstRender = false
        }
      })
    },
    
    // 检查数据是否有效
    isValidData() {
      if (!this.data) return false
      
      // 检查特定类型所需的数据
      switch (this.type) {
        case 'line':
        case 'bar':
          return Array.isArray(this.data.xAxis) && 
                this.data.xAxis.length > 0 && 
                Array.isArray(this.data.series);
          
        case 'pie':
          return Array.isArray(this.data.series) && 
                this.data.series.length > 0;
          
        case 'radar':
          return Array.isArray(this.data.indicator) && 
                this.data.indicator.length > 0 && 
                Array.isArray(this.data.series);
          
        case 'scatter':
          return Array.isArray(this.data.series);
          
        default:
          return false;
      }
    },
    
    // 更新图表数据
    updateChart() {
      if (!this.chart || !this.isValidData()) return
      
      let options = {}
      
      switch (this.type) {
        case 'line':
          options = this.getLineChartOptions()
          break
        case 'bar':
          options = this.getBarChartOptions()
          break
        case 'pie':
          options = this.getPieChartOptions()
          break
        case 'radar':
          options = this.getRadarChartOptions()
          break
        case 'scatter':
          options = this.getScatterChartOptions()
          break
        default:
          options = this.getLineChartOptions()
      }
      
      // 合并用户自定义选项
      const mergedOptions = { ...options, ...this.options }
      
      // 使用try-catch包装setOption调用
      try {
        this.chart.setOption(mergedOptions, true)
      } catch (error) {
        console.error('ECharts setOption error:', error)
      }
    },
    
    // 调整图表大小
    resizeChart() {
      if (this.chart) {
        try {
          this.chart.resize()
        } catch (error) {
          console.error('ECharts resize error:', error)
        }
      }
    },
    
    // 折线图配置
    getLineChartOptions() {
      return {
        tooltip: {
          trigger: 'axis',
          formatter: '{b}: {c} 百万美元'
        },
        xAxis: {
          type: 'category',
          data: this.data.xAxis || [],
          axisLabel: {
            interval: 'auto',
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '军费支出(百万美元)',
          nameLocation: 'middle',
          nameGap: 40,
          axisLine: {
            show: true
          },
          axisLabel: {
            formatter: (value) => {
              if (value >= 1000) {
                return (value / 1000).toFixed(1) + 'B'
              }
              return value
            }
          }
        },
        series: this.formatSeries(this.data.series || [])
      }
    },
    
    // 柱状图配置
    getBarChartOptions() {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: this.data.xAxis || [],
          axisLabel: {
            interval: 0,
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '军费支出(百万美元)',
          nameLocation: 'middle',
          nameGap: 40,
          axisLine: {
            show: true
          },
          axisLabel: {
            formatter: (value) => {
              if (value >= 1000) {
                return (value / 1000).toFixed(1) + 'B'
              }
              return value
            }
          }
        },
        series: this.formatSeries(this.data.series || [])
      }
    },
    
    // 饼图配置
    getPieChartOptions() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: this.data.legend || []
        },
        series: [
          {
            name: this.data.name || '数据分布',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.formatPieData(this.data.series || [])
          }
        ]
      }
    },
    
    // 雷达图配置
    getRadarChartOptions() {
      return {
        tooltip: {
          trigger: 'item'
        },
        radar: {
          indicator: this.data.indicator || []
        },
        series: [
          {
            type: 'radar',
            data: this.formatRadarData(this.data.series || [])
          }
        ]
      }
    },
    
    // 散点图配置
    getScatterChartOptions() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            return `${params.data.name || ''}: ${params.data.value?.[0] || 0}, ${params.data.value?.[1] || 0}`
          }
        },
        xAxis: {
          type: 'value',
          name: this.data.xName || '',
          nameLocation: 'middle',
          nameGap: 30
        },
        yAxis: {
          type: 'value',
          name: this.data.yName || '',
          nameLocation: 'middle',
          nameGap: 30
        },
        series: [
          {
            type: 'scatter',
            data: this.formatScatterData(this.data.series || []),
            symbolSize: (data) => {
              return this.data.symbolSize ? this.data.symbolSize(data) : 10
            }
          }
        ]
      }
    },
    
    // 格式化系列数据确保type属性存在
    formatSeries(series) {
      return series.map(item => {
        // 确保每个系列都有type属性
        return {
          ...item,
          type: item.type || this.type
        }
      })
    },
    
    // 格式化饼图数据
    formatPieData(data) {
      return data.map(item => {
        // 确保每个数据项有name和value
        if (typeof item === 'object') {
          return {
            name: item.name || '未命名',
            value: item.value || 0,
            ...item
          }
        }
        return { name: '未命名', value: 0 }
      })
    },
    
    // 格式化雷达图数据
    formatRadarData(data) {
      return data.map(item => {
        // 确保每个数据项有name和value
        if (typeof item === 'object') {
          return {
            name: item.name || '未命名',
            value: item.value || [],
            ...item
          }
        }
        return { name: '未命名', value: [] }
      })
    },
    
    // 格式化散点图数据
    formatScatterData(data) {
      return data.map(item => {
        // 确保每个数据项有name和value
        if (typeof item === 'object') {
          return {
            name: item.name || '未命名',
            value: item.value || [0, 0],
            ...item
          }
        }
        return { name: '未命名', value: [0, 0] }
      })
    }
  },
  mounted() {
    this.initChart()
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resizeChart)
    if (this.chart) {
      this.chart.dispose()
      this.chart = null
    }
  },
  watch: {
    data: {
      handler() {
        if (this.isFirstRender || this.isValidData()) {
          this.$nextTick(() => {
            this.updateChart()
            this.isFirstRender = false
          })
        }
      },
      deep: true
    },
    type() {
      this.$nextTick(() => {
        this.updateChart()
      })
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 300px;
}
</style> 