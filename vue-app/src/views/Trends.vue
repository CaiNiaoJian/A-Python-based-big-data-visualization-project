<template>
  <div class="trends-view">
    <van-nav-bar title="军事力量趋势" left-arrow @click-left="$router.back()" />
    
    <div class="container">
      <div class="filters-panel">
        <h3>趋势分析控制面板</h3>
        
        <div class="filter-group">
          <div class="country-selector">
            <van-field
              v-model="selectedCountry"
              label="选择国家"
              placeholder="点击此处选择要分析的国家"
              readonly
              class="country-selector-field"
              @click="showCountryPicker = true"
            >
              <template #right-icon>
                <div class="selector-icon-container">
                  <CountryFlag 
                    v-if="selectedCountry" 
                    :country-name="selectedCountry" 
                    :iso-code="countryIsoCode" 
                    size="small" 
                    class="selector-flag-inline"
                  />
                  <van-icon name="arrow-down" size="18" color="#1989fa" />
                </div>
              </template>
            </van-field>
          </div>
          
          <div class="year-range">
            <div class="year-label">年份范围: {{ startYear }} - {{ endYear }}</div>
            <van-slider
              v-model="yearRange"
              range
              :min="minYear"
              :max="maxYear"
              :step="1"
              @change="handleYearRangeChange"
            />
          </div>
          
          <div class="chart-type-selector">
            <span class="selector-label">图表类型:</span>
            <div class="button-group">
              <van-button 
                size="small" 
                :type="chartType === 'line' ? 'primary' : 'default'"
                @click="chartType = 'line'"
              >折线图</van-button>
              <van-button 
                size="small" 
                :type="chartType === 'bar' ? 'primary' : 'default'"
                @click="chartType = 'bar'"
              >柱状图</van-button>
              <van-button 
                size="small" 
                :type="chartType === 'area' ? 'primary' : 'default'"
                @click="chartType = 'area'"
              >面积图</van-button>
            </div>
          </div>
          
          <van-button type="primary" block @click="fetchTrend">分析趋势</van-button>
        </div>
      </div>
      
      <div v-if="loading" class="loading-container">
        <van-loading type="spinner" vertical>加载中...</van-loading>
      </div>
      <div v-else-if="error" class="error-container">
        <van-empty image="error" :description="error">
          <template #bottom>
            <van-button round type="primary" @click="fetchTrend">重试</van-button>
          </template>
        </van-empty>
      </div>
      <div v-else-if="trendData.length > 0" class="trend-data">
        <div class="trend-header">
          <CountryFlag :country-name="selectedCountry" :iso-code="countryIsoCode" size="large" />
          <h3>{{ selectedCountry }} 军费支出趋势分析</h3>
          <div class="year-badge">{{ startYear }}-{{ endYear }}</div>
        </div>
        
        <div class="stats-cards">
          <div class="stats-card">
            <div class="stats-title">平均年度支出</div>
            <div class="stats-value">{{ formatLargeNumber(getAverageExpenditure()) }}</div>
            <div class="stats-label">百万美元/年</div>
          </div>
          
          <div class="stats-card">
            <div class="stats-title">累计总支出</div>
            <div class="stats-value">{{ formatLargeNumber(getTotalExpenditure()) }}</div>
            <div class="stats-label">百万美元</div>
          </div>
          
          <div class="stats-card">
            <div class="stats-title">年均增长率</div>
            <div class="stats-value" :class="getGrowthRate() >= 0 ? 'positive' : 'negative'">
              {{ getGrowthRate() >= 0 ? '+' : '' }}{{ getGrowthRate().toFixed(2) }}%
            </div>
            <div class="stats-label">{{ startYear }} - {{ endYear }}</div>
          </div>
          
          <div class="stats-card">
            <div class="stats-title">峰值支出年份</div>
            <div class="stats-value">{{ getPeakYear() }}年</div>
            <div class="stats-label">{{ formatLargeNumber(getPeakExpenditure()) }}百万美元</div>
          </div>
        </div>
        
        <div class="chart-section">
          <h4>军费支出历年变化趋势</h4>
          <MilitaryChart 
            :type="getChartType()" 
            :data="getChartData()" 
            height="350px"
            :options="getChartOptions()"
          />
        </div>
        
        <div class="insights-section">
          <h4>趋势洞察分析</h4>
          <div class="insight-cards">
            <div class="insight-card">
              <van-icon name="chart-trending-o" size="24" />
              <div class="insight-content">
                <h5>整体趋势</h5>
                <p>{{ getTrendInsight() }}</p>
              </div>
            </div>
            
            <div class="insight-card">
              <van-icon name="increase" size="24" />
              <div class="insight-content">
                <h5>增长分析</h5>
                <p>{{ getGrowthInsight() }}</p>
              </div>
            </div>
            
            <div class="insight-card">
              <van-icon name="bar-chart-o" size="24" />
              <div class="insight-content">
                <h5>波动特征</h5>
                <p>{{ getVolatilityInsight() }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="data-table">
          <h4>历年数据明细</h4>
          <van-cell-group>
            <van-cell v-for="item in sortedTrendData" :key="item.year" :title="item.year + '年'" :value="formatNumber(item.expenditure) + '百万美元'" />
          </van-cell-group>
        </div>
      </div>
      
      <van-popup v-model="showCountryPicker" position="bottom">
        <van-picker
          show-toolbar
          title="选择要分析的国家"
          :columns="countries"
          @confirm="onCountrySelected"
          @cancel="showCountryPicker = false"
          value-key="text"
        />
      </van-popup>
    </div>
  </div>
</template>

<script>
import CountryFlag from '@/components/CountryFlag.vue'
import MilitaryChart from '@/components/MilitaryChart.vue'
import { 
  getCountryList, 
  getCountryHistoricalData,
  getCountryMetadata,
  getYearData
} from '@/utils/jsonDataService'

export default {
  name: 'TrendsView',
  components: {
    CountryFlag,
    MilitaryChart
  },
  data() {
    return {
      loading: false,
      error: null,
      countries: [],
      countryMetadata: {},
      selectedCountry: '',
      showCountryPicker: false,
      yearRange: [2010, 2022],
      startYear: 2010,
      endYear: 2022,
      minYear: 1960,
      maxYear: 2022,
      trendData: [],
      chartType: 'line' // 默认图表类型
    }
  },
  computed: {
    countryIsoCode() {
      if (!this.countryMetadata[this.selectedCountry]) return ''
      return this.countryMetadata[this.selectedCountry].iso_code || ''
    },
    sortedTrendData() {
      return [...this.trendData].sort((a, b) => b.year - a.year)
    }
  },
  async mounted() {
    try {
      // 加载国家列表和元数据
      const [countriesList, metadata] = await Promise.all([
        getCountryList(),
        getCountryMetadata()
      ])
      
      // 格式化国家列表为对象数组，适配Vant选择器
      this.countries = countriesList.map(country => ({
        text: country,
        value: country
      }))
      
      this.countryMetadata = metadata
      
      // 强制设置默认国家为中国
      this.selectedCountry = '中国'
      console.log('默认选择中国进行趋势分析')
      
      // 确保中国存在于数据集中
      const yearData = await getYearData(2022) // 获取最新年份数据
      const chinaExists = yearData.some(country => country.Country === '中国')
      
      if (!chinaExists) {
        console.warn('数据集中不存在中国数据，尝试使用列表中的第一个国家')
        if (countriesList.length > 0) {
          this.selectedCountry = countriesList[0]
        }
      }
      
      // 立即执行趋势分析
      this.fetchTrend()
    } catch (error) {
      console.error('加载国家数据失败:', error)
      this.error = '加载国家数据失败，请稍后重试'
    }
  },
  methods: {
    onCountrySelected(value) {
      console.log('选择国家:', value);
      if (typeof value === 'object') {
        this.selectedCountry = value.value || value.text || ''
      } else {
        this.selectedCountry = value
      }
      this.showCountryPicker = false
      
      // 选择国家后立即进行趋势分析
      this.fetchTrend()
    },
    
    handleYearRangeChange(values) {
      this.startYear = values[0]
      this.endYear = values[1]
      
      // 年份范围变化后自动更新数据
      if (this.trendData.length > 0) {
        this.fetchTrend()
      }
    },
    
    async fetchTrend() {
      if (!this.selectedCountry) {
        this.error = '请选择要查看趋势的国家'
        return
      }
      
      try {
        this.loading = true
        this.error = null
        
        console.log(`开始加载${this.selectedCountry}的历史数据...`)
        const historyData = await getCountryHistoricalData(this.selectedCountry)
        console.log(`成功获取${historyData.length}条历史数据记录`)
        
        // 筛选年份范围内的数据
        this.trendData = historyData.filter(
          item => item.year >= this.startYear && item.year <= this.endYear
        )
        console.log(`筛选${this.startYear}-${this.endYear}年范围内的数据，共${this.trendData.length}条记录`)
        
        this.loading = false
        
        if (this.trendData.length === 0) {
          this.error = `未找到${this.selectedCountry}在${this.startYear}-${this.endYear}年范围内的数据`
        }
      } catch (error) {
        console.error('获取趋势数据失败:', error)
        this.error = '加载趋势数据失败，请稍后重试'
        this.loading = false
      }
    },
    
    // 图表相关方法
    getChartType() {
      // 如果是面积图，使用line类型，然后在options中设置areaStyle
      return this.chartType === 'area' ? 'line' : this.chartType
    },
    
    getChartData() {
      // 确保有数据可用
      if (this.trendData.length === 0) {
        return { xAxis: [], series: [] };
      }
      
      // 按年份排序数据
      const sortedData = [...this.trendData].sort((a, b) => a.year - b.year);
      
      const years = sortedData.map(item => item.year);
      const expenditures = sortedData.map(item => item.expenditure);
      
      return {
        xAxis: years,
        series: [
          {
            name: this.selectedCountry,
            type: this.getChartType(), // 确保设置类型
            data: expenditures
          }
        ]
      };
    },
    
    getChartOptions() {
      const options = {
        tooltip: {
          trigger: 'axis',
          formatter: params => {
            const param = params[0]
            return `${param.name}年<br/>${param.seriesName}: ${this.formatNumber(param.value)}百万美元`
          }
        },
        grid: {
          left: '5%',
          right: '5%',
          bottom: '10%',
          containLabel: true
        }
      }
      
      // 如果是面积图，添加areaStyle属性
      if (this.chartType === 'area') {
        options.series = [
          {
            type: 'line',
            areaStyle: {
              opacity: 0.3
            }
          }
        ]
      }
      
      return options
    },
    
    // 统计分析方法
    getAverageExpenditure() {
      if (this.trendData.length === 0) return 0
      const sum = this.trendData.reduce((total, item) => total + item.expenditure, 0)
      return sum / this.trendData.length
    },
    
    getTotalExpenditure() {
      if (this.trendData.length === 0) return 0
      return this.trendData.reduce((total, item) => total + item.expenditure, 0)
    },
    
    getGrowthRate() {
      if (this.trendData.length < 2) return 0
      
      // 按年份排序
      const sortedData = [...this.trendData].sort((a, b) => a.year - b.year)
      
      // 找到开始年份和结束年份的数据
      const firstYearData = sortedData[0]
      const lastYearData = sortedData[sortedData.length - 1]
      
      if (!firstYearData || !lastYearData) return 0
      
      const firstValue = firstYearData.expenditure
      const lastValue = lastYearData.expenditure
      
      if (firstValue === 0) return 0
      
      // 计算年复合增长率 CAGR
      const years = lastYearData.year - firstYearData.year
      if (years === 0) return 0
      
      const cagr = (Math.pow(lastValue / firstValue, 1 / years) - 1) * 100
      return cagr
    },
    
    getPeakYear() {
      if (this.trendData.length === 0) return '--'
      
      const peakData = this.trendData.reduce((max, item) => 
        item.expenditure > max.expenditure ? item : max, 
        this.trendData[0]
      )
      
      return peakData.year
    },
    
    getPeakExpenditure() {
      if (this.trendData.length === 0) return 0
      
      const peakData = this.trendData.reduce((max, item) => 
        item.expenditure > max.expenditure ? item : max, 
        this.trendData[0]
      )
      
      return peakData.expenditure
    },
    
    // 智能洞察分析
    getTrendInsight() {
      if (this.trendData.length < 2) return '数据不足，无法分析趋势。'
      
      // 按年份排序
      const sortedData = [...this.trendData].sort((a, b) => a.year - b.year)
      
      // 检查增长趋势
      const firstValue = sortedData[0].expenditure
      const lastValue = sortedData[sortedData.length - 1].expenditure
      
      let trendType = ''
      if (lastValue > firstValue * 1.5) {
        trendType = '快速增长'
      } else if (lastValue > firstValue * 1.1) {
        trendType = '稳步增长'
      } else if (lastValue >= firstValue * 0.9) {
        trendType = '基本稳定'
      } else if (lastValue >= firstValue * 0.5) {
        trendType = '逐步下降'
      } else {
        trendType = '大幅下降'
      }
      
      return `${this.startYear}年至${this.endYear}年间，${this.selectedCountry}的军费支出呈${trendType}趋势，从${this.formatLargeNumber(firstValue)}百万美元变化到${this.formatLargeNumber(lastValue)}百万美元。`
    },
    
    getGrowthInsight() {
      if (this.trendData.length < 3) return '数据点不足，无法进行详细增长分析。'
      
      const growthRate = this.getGrowthRate()
      const avgExpenditure = this.getAverageExpenditure()
      
      let growthAnalysis = ''
      if (growthRate > 15) {
        growthAnalysis = '极高的增长速度，显示了军事投入的高度重视'
      } else if (growthRate > 8) {
        growthAnalysis = '高速增长，军事投入明显提升'
      } else if (growthRate > 3) {
        growthAnalysis = '稳定增长，军事投入持续加强'
      } else if (growthRate >= 0) {
        growthAnalysis = '缓慢增长，军事投入保持平稳'
      } else if (growthRate >= -3) {
        growthAnalysis = '轻微下降，可能受经济因素影响'
      } else if (growthRate >= -8) {
        growthAnalysis = '明显下降，军事投入减少'
      } else {
        growthAnalysis = '大幅下降，军事投入显著减少'
      }
      
      return `${this.selectedCountry}在该时期内军费年均增长率为${growthRate.toFixed(2)}%，平均每年投入约${this.formatLargeNumber(avgExpenditure)}百万美元，${growthAnalysis}。`
    },
    
    getVolatilityInsight() {
      if (this.trendData.length < 4) return '数据点不足，无法分析波动性。'
      
      // 按年份排序
      const sortedData = [...this.trendData].sort((a, b) => a.year - b.year)
      
      // 计算相邻年份变化率
      const changes = []
      for (let i = 1; i < sortedData.length; i++) {
        const prev = sortedData[i-1].expenditure
        const curr = sortedData[i].expenditure
        if (prev > 0) {
          changes.push((curr - prev) / prev * 100)
        }
      }
      
      // 计算变化率的标准差作为波动性指标
      const mean = changes.reduce((sum, val) => sum + val, 0) / changes.length
      const variance = changes.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / changes.length
      const volatility = Math.sqrt(variance)
      
      let volatilityDesc = ''
      if (volatility > 20) {
        volatilityDesc = '极高波动性，军费投入变化剧烈'
      } else if (volatility > 10) {
        volatilityDesc = '高波动性，军费投入变化明显'
      } else if (volatility > 5) {
        volatilityDesc = '中等波动性，军费投入有一定变化'
      } else {
        volatilityDesc = '低波动性，军费投入相对稳定'
      }
      
      // 寻找显著变化的年份
      const significantChanges = changes.map((change, i) => ({
        year: sortedData[i+1].year,
        change
      })).filter(item => Math.abs(item.change) > 15)
      
      let significantYears = ''
      if (significantChanges.length > 0) {
        significantYears = `特别是在${significantChanges.map(item => item.year).join('、')}年，军费投入有显著变化。`
      }
      
      return `${this.selectedCountry}的军费支出表现出${volatilityDesc}，年度变化率平均为${mean.toFixed(2)}%。${significantYears}`
    },
    
    // 格式化方法
    formatNumber(num) {
      if (num === null || num === undefined) return '暂无数据'
      return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    
    formatLargeNumber(num) {
      if (num === null || num === undefined) return '暂无数据'
      
      if (num >= 1000000) {
        return (num / 1000000).toFixed(2) + ' 万亿'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(2) + ' 十亿'
      } else {
        return num.toFixed(2) + ' 百万'
      }
    }
  }
}
</script>

<style scoped>
.trends-view {
  min-height: 100%;
  background-color: #f7f8fa;
}

.container {
  padding: 16px;
}

.filters-panel {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.filters-panel h3 {
  margin-bottom: 16px;
  font-size: 18px;
  color: #323233;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.year-range {
  margin: 8px 0;
}

.year-label {
  margin-bottom: 12px;
  color: #646566;
  text-align: center;
}

.chart-type-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 8px 0;
}

.selector-label {
  color: #646566;
}

.loading-container, .error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 40px 0;
}

.trend-data {
  margin-top: 24px;
}

.trend-header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.trend-header h3 {
  flex: 1;
  margin: 0;
  font-size: 18px;
  color: #323233;
}

.year-badge {
  padding: 4px 8px;
  background-color: #e8f3ff;
  color: #1989fa;
  border-radius: 4px;
  font-size: 14px;
}

.stats-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.stats-card {
  flex: 1;
  min-width: calc(50% - 16px);
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.stats-title {
  font-size: 14px;
  color: #646566;
  margin-bottom: 8px;
}

.stats-value {
  font-size: 18px;
  font-weight: bold;
  color: #1989fa;
  margin-bottom: 4px;
}

.stats-value.positive {
  color: #07c160;
}

.stats-value.negative {
  color: #ee0a24;
}

.stats-label {
  font-size: 12px;
  color: #969799;
}

.chart-section {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.chart-section h4 {
  margin-bottom: 16px;
  font-size: 16px;
  color: #323233;
  text-align: center;
}

.insights-section {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.insights-section h4 {
  margin-bottom: 16px;
  font-size: 16px;
  color: #323233;
}

.insight-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.insight-card {
  display: flex;
  gap: 16px;
  padding: 12px;
  background-color: #f7f8fa;
  border-radius: 8px;
}

.insight-card .van-icon {
  color: #1989fa;
  flex-shrink: 0;
  margin-top: 4px;
}

.insight-content {
  flex: 1;
}

.insight-content h5 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #323233;
}

.insight-content p {
  margin: 0;
  font-size: 14px;
  color: #646566;
  line-height: 1.5;
}

.data-table {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.data-table h4 {
  margin-bottom: 16px;
  font-size: 16px;
  color: #323233;
}

.country-selector {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.country-selector-field {
  flex: 1;
}

.selector-icon-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.selector-flag-inline {
  width: 24px;
  height: 24px;
  margin-right: 4px;
}

.button-group {
  display: flex;
  overflow: hidden;
  border-radius: 2px;
}

.button-group .van-button {
  margin: 0 !important;
  border-radius: 0;
}

.button-group .van-button:not(:first-child) {
  border-left: 0;
}

.button-group .van-button:first-child {
  border-top-left-radius: 2px;
  border-bottom-left-radius: 2px;
}

.button-group .van-button:last-child {
  border-top-right-radius: 2px;
  border-bottom-right-radius: 2px;
}

@media (max-width: 480px) {
  .stats-card {
    min-width: 100%;
  }
}
</style> 