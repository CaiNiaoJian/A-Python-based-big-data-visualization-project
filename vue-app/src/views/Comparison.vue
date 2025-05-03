<template>
  <div class="comparison-view">
    <van-nav-bar title="国家军力对比" left-arrow @click-left="$router.back()" />
    
    <div class="container">
      <!-- 国家选择区域 -->
      <div class="selection-area">
        <h3>选择要对比的国家</h3>
        
        <div class="country-selector">
          <div class="country-select-item">
            <CountryFlag :country-name="country1" :iso-code="country1IsoCode" size="large" />
            <van-field
              v-model="country1"
              placeholder="选择国家1"
              readonly
              right-icon="arrow-down"
              @click="showCountry1Picker = true"
            />
          </div>
          
          <div class="vs-badge">对比</div>
          
          <div class="country-select-item">
            <CountryFlag :country-name="country2" :iso-code="country2IsoCode" size="large" />
            <van-field
              v-model="country2"
              placeholder="选择国家2"
              readonly
              right-icon="arrow-down"
              @click="showCountry2Picker = true"
            />
          </div>
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
        
        <van-button type="primary" block @click="performComparison">开始对比</van-button>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <van-loading type="spinner" size="24px" vertical>加载中...</van-loading>
      </div>
      
      <!-- 错误信息 -->
      <div v-else-if="error" class="error-container">
        <van-empty image="error" :description="error">
          <template #bottom>
            <van-button round type="primary" @click="performComparison">重试</van-button>
          </template>
        </van-empty>
      </div>
      
      <!-- 对比结果 -->
      <div v-else-if="comparisonData" class="comparison-results">
        <h3>对比结果</h3>
        
        <!-- 快速概览卡片 -->
        <div class="overview-cards">
          <div 
            class="overview-card"
            :style="{
              '--primary-color': getCountryColor(0),
              '--border-color': getCountryColor(0, 0.3)
            }"
          >
            <div class="country-header">
              <CountryFlag :country-name="country1" :iso-code="country1IsoCode" :background-color="getCountryColor(0)" />
              <div class="country-name">{{ country1 }}</div>
            </div>
            <div class="expenditure-value">{{ formatLargeNumber(latestExpenditures.country1) }}</div>
            <div class="expenditure-label">百万美元 ({{ endYear }})</div>
            <div class="rank-badge" v-if="latestRanks.country1">
              全球排名 #{{ latestRanks.country1 }}
            </div>
          </div>
          
          <div 
            class="overview-card"
            :style="{
              '--primary-color': getCountryColor(1),
              '--border-color': getCountryColor(1, 0.3)
            }"
          >
            <div class="country-header">
              <CountryFlag :country-name="country2" :iso-code="country2IsoCode" :background-color="getCountryColor(1)" />
              <div class="country-name">{{ country2 }}</div>
            </div>
            <div class="expenditure-value">{{ formatLargeNumber(latestExpenditures.country2) }}</div>
            <div class="expenditure-label">百万美元 ({{ endYear }})</div>
            <div class="rank-badge" v-if="latestRanks.country2">
              全球排名 #{{ latestRanks.country2 }}
            </div>
          </div>
        </div>
        
        <!-- 详细对比统计 -->
        <div class="comparison-stats">
          <div class="stats-card">
            <div class="stats-title">军费差距</div>
            <div class="stats-value">{{ formatLargeNumber(getDifference()) }}</div>
            <div class="stats-label">百万美元</div>
          </div>
          
          <div class="stats-card">
            <div class="stats-title">倍数关系</div>
            <div class="stats-value">{{ getRatio().toFixed(1) }}倍</div>
            <div class="stats-label">{{ getStrongerCountry() }}更高</div>
          </div>
          
          <div class="stats-card">
            <div class="stats-title">增长率对比</div>
            <div class="stats-value" :class="getHigherGrowthRate().className">
              {{ getHigherGrowthRate().country }}
            </div>
            <div class="stats-label">增长更快</div>
          </div>
        </div>
        
        <!-- 趋势对比图表 -->
        <div class="chart-section">
          <h4>军费支出趋势对比</h4>
          <div class="chart-type-toggle">
            <van-button 
              size="small" 
              :type="trendChartType === 'line' ? 'primary' : 'default'"
              @click="trendChartType = 'line'"
            >
              折线图
            </van-button>
            <van-button 
              size="small" 
              :type="trendChartType === 'bar' ? 'primary' : 'default'"
              @click="trendChartType = 'bar'"
            >
              柱状图
            </van-button>
          </div>
          <MilitaryChart 
            :type="trendChartType" 
            :data="trendChartData" 
            height="300px"
          />
        </div>
        
        <!-- 占比饼图 -->
        <div class="chart-section">
          <h4>{{ endYear }}年军费占比对比</h4>
          <MilitaryChart 
            type="pie" 
            :data="pieChartData" 
            height="300px"
          />
        </div>
        
        <!-- 历年数据表格 -->
        <div class="data-table">
          <h4>历年军费支出数据</h4>
          <van-tabs v-model="activeYearTab">
            <van-tab title="按年份">
              <van-cell-group>
                <van-cell v-for="year in visibleYears" :key="year" :title="`${year}年`">
                  <template #value>
                    <div class="year-data-cell">
                      <div class="country-data">
                        <span class="country-dot" :style="{'background-color': getCountryColor(0)}"></span>
                        <span>{{ country1 }}:</span>
                        <span class="expenditure">{{ formatYearData(year, 'country1') }}</span>
                      </div>
                      <div class="country-data">
                        <span class="country-dot" :style="{'background-color': getCountryColor(1)}"></span>
                        <span>{{ country2 }}:</span>
                        <span class="expenditure">{{ formatYearData(year, 'country2') }}</span>
                      </div>
                    </div>
                  </template>
                </van-cell>
              </van-cell-group>
            </van-tab>
            <van-tab :title="country1">
              <van-cell-group>
                <van-cell v-for="item in country1Data" :key="item.year" :title="`${item.year}年`">
                  <template #value>
                    <span class="expenditure">{{ formatNumber(item.expenditure) }}百万美元</span>
                  </template>
                </van-cell>
              </van-cell-group>
            </van-tab>
            <van-tab :title="country2">
              <van-cell-group>
                <van-cell v-for="item in country2Data" :key="item.year" :title="`${item.year}年`">
                  <template #value>
                    <span class="expenditure">{{ formatNumber(item.expenditure) }}百万美元</span>
                  </template>
                </van-cell>
              </van-cell-group>
            </van-tab>
          </van-tabs>
        </div>
      </div>
      
      <!-- 国家选择器弹出层 -->
      <van-popup v-model="showCountry1Picker" position="bottom">
        <van-picker
          show-toolbar
          title="选择国家"
          :columns="countries"
          @confirm="onCountry1Selected"
          @cancel="showCountry1Picker = false"
          value-key="text"
        />
      </van-popup>
      
      <van-popup v-model="showCountry2Picker" position="bottom">
        <van-picker
          show-toolbar
          title="选择国家"
          :columns="countries"
          @confirm="onCountry2Selected"
          @cancel="showCountry2Picker = false"
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
  compareCountries, 
  getCountryMetadata,
  getCountryComparisonStats,
  getAllYears
} from '@/utils/jsonDataService'

export default {
  name: 'ComparisonView',
  components: {
    CountryFlag,
    MilitaryChart
  },
  data() {
    return {
      // 基础数据状态
      countries: [],
      loading: false,
      error: '',
      countryMetadata: {},
      allYears: [],
      minYear: 1960,
      maxYear: 2022,
      
      // 选择状态
      country1: '',
      country2: '',
      showCountry1Picker: false,
      showCountry2Picker: false,
      yearRange: [2010, 2022],
      startYear: 2010,
      endYear: 2022,
      
      // 对比数据
      comparisonData: null,
      latestComparisonStats: null,
      country1Data: [],
      country2Data: [],
      latestExpenditures: { country1: 0, country2: 0 },
      latestRanks: { country1: null, country2: null },
      trendChartType: 'line',
      activeYearTab: 0
    }
  },
  computed: {
    // ISO 代码
    country1IsoCode() {
      if (!this.countryMetadata[this.country1]) return ''
      return this.countryMetadata[this.country1].iso_code || ''
    },
    
    country2IsoCode() {
      if (!this.countryMetadata[this.country2]) return ''
      return this.countryMetadata[this.country2].iso_code || ''
    },
    
    // 可见的年份列表（用于表格展示）
    visibleYears() {
      return Array.from({ length: this.endYear - this.startYear + 1 }, (_, i) => this.startYear + i).reverse()
    },
    
    // 图表数据计算
    trendChartData() {
      if (!this.comparisonData) return { xAxis: [], series: [] }
      
      // 构造X轴数据（年份）
      const xAxis = Array.from(
        { length: this.endYear - this.startYear + 1 }, 
        (_, i) => this.startYear + i
      )
      
      // 构造国家1的数据系列
      const country1Series = {
        name: this.country1,
        type: this.trendChartType,
        data: xAxis.map(year => {
          const item = this.country1Data.find(d => d.year === year)
          return item ? item.expenditure : null
        }),
        itemStyle: {
          color: this.getCountryColor(0)
        }
      }
      
      // 构造国家2的数据系列
      const country2Series = {
        name: this.country2,
        type: this.trendChartType,
        data: xAxis.map(year => {
          const item = this.country2Data.find(d => d.year === year)
          return item ? item.expenditure : null
        }),
        itemStyle: {
          color: this.getCountryColor(1)
        }
      }
      
      return {
        xAxis,
        series: [country1Series, country2Series]
      }
    },
    
    // 饼图数据
    pieChartData() {
      if (!this.latestComparisonStats) return { legend: [], series: [] }
      
      const country1Value = this.latestExpenditures.country1
      const country2Value = this.latestExpenditures.country2
      
      return {
        name: '军费占比',
        legend: [this.country1, this.country2],
        series: [
          {
            name: this.country1,
            value: country1Value || 0,
            itemStyle: { color: this.getCountryColor(0) }
          },
          {
            name: this.country2,
            value: country2Value || 0,
            itemStyle: { color: this.getCountryColor(1) }
          }
        ].filter(item => item.value > 0) // 过滤掉值为0的数据
      }
    }
  },
  async mounted() {
    try {
      // 从路由参数中获取预选国家
      const { country1: routeCountry1, country2: routeCountry2 } = this.$route.query
      
      // 加载国家列表和元数据
      const [countriesList, metadata, yearsData] = await Promise.all([
        getCountryList(),
        getCountryMetadata(),
        getAllYears()
      ])
      
      // 格式化国家列表为对象数组，适配Vant选择器
      this.countries = countriesList.map(country => ({
        text: country,
        value: country
      }))
      
      this.countryMetadata = metadata
      this.allYears = yearsData
      
      // 设置年份范围限制
      if (yearsData.length > 0) {
        this.minYear = Math.min(...yearsData)
        this.maxYear = Math.max(...yearsData)
      }
      
      // 设置默认国家为美国和中国
      const defaultCountry1 = routeCountry1 || '美国'
      const defaultCountry2 = routeCountry2 || '中国'
      
      if (countriesList.includes(defaultCountry1)) {
        this.country1 = defaultCountry1
      } else if (countriesList.length > 0) {
        this.country1 = countriesList[0]
      }
      
      if (countriesList.includes(defaultCountry2)) {
        this.country2 = defaultCountry2
      } else if (countriesList.length > 1) {
        this.country2 = countriesList[1]
      }
      
      console.log('已设置默认国家:', this.country1, this.country2);
      
      // 确保默认执行对比
      setTimeout(() => {
        if (this.country1 && this.country2) {
          this.performComparison()
        }
      }, 300)
    } catch (err) {
      console.error('初始化数据失败:', err)
      this.error = '加载国家数据失败，请稍后重试'
    }
  },
  methods: {
    // 国家选择处理
    onCountry1Selected(value) {
      console.log('选择国家1:', value);
      if (typeof value === 'object') {
        this.country1 = value.value || value.text || '';
      } else {
        this.country1 = value;
      }
      this.showCountry1Picker = false;
    },
    
    onCountry2Selected(value) {
      console.log('选择国家2:', value);
      if (typeof value === 'object') {
        this.country2 = value.value || value.text || '';
      } else {
        this.country2 = value;
      }
      this.showCountry2Picker = false;
    },
    
    // 年份范围变化处理
    handleYearRangeChange(values) {
      this.startYear = values[0]
      this.endYear = values[1]
    },
    
    // 执行对比
    async performComparison() {
      if (!this.country1 || !this.country2) {
        this.error = '请选择两个要对比的国家'
        return
      }
      
      try {
        this.loading = true
        this.error = ''
        
        // 获取对比数据
        const comparison = await compareCountries(
          this.country1,
          this.country2,
          this.startYear,
          this.endYear
        )
        
        this.comparisonData = comparison
        this.country1Data = comparison.country1.data
        this.country2Data = comparison.country2.data
        
        // 获取最新年份的详细对比统计
        const latestStats = await getCountryComparisonStats(
          this.country1,
          this.country2,
          this.endYear
        )
        
        this.latestComparisonStats = latestStats
        
        if (latestStats) {
          this.latestExpenditures.country1 = latestStats.country1.expenditure
          this.latestExpenditures.country2 = latestStats.country2.expenditure
          this.latestRanks.country1 = latestStats.country1.rank
          this.latestRanks.country2 = latestStats.country2.rank
        }
        
        // 更新URL参数，方便分享
        this.$router.replace({
          query: { ...this.$route.query, country1: this.country1, country2: this.country2 }
        })
        
        this.loading = false
      } catch (err) {
        console.error('对比数据失败:', err)
        this.error = '加载对比数据失败，请稍后重试'
        this.loading = false
      }
    },
    
    // 辅助函数
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
    },
    
    formatYearData(year, countryKey) {
      if (!this.comparisonData) return '暂无数据'
      
      const data = this.comparisonData[countryKey].data.find(item => item.year === year)
      if (!data) return '暂无数据'
      
      return this.formatNumber(data.expenditure) + '百万美元'
    },
    
    // 获取国家代表色
    getCountryColor(index, opacity = 1) {
      const colors = ['#1989fa', '#ff6b6b', '#07c160', '#ff9800', '#8a2be2']
      if (opacity === 1) {
        return colors[index % colors.length]
      }
      
      // 创建半透明颜色
      const hexColor = colors[index % colors.length]
      // 将十六进制转为RGB
      const r = parseInt(hexColor.slice(1, 3), 16)
      const g = parseInt(hexColor.slice(3, 5), 16)
      const b = parseInt(hexColor.slice(5, 7), 16)
      
      return `rgba(${r}, ${g}, ${b}, ${opacity})`
    },
    
    // 计算差异值
    getDifference() {
      if (!this.latestComparisonStats) return 0
      return this.latestComparisonStats.difference
    },
    
    // 计算比率
    getRatio() {
      if (!this.latestComparisonStats) return 1
      return this.latestComparisonStats.ratio
    },
    
    // 获取军费更高的国家
    getStrongerCountry() {
      if (!this.latestComparisonStats) return ''
      
      if (this.latestExpenditures.country1 > this.latestExpenditures.country2) {
        return this.country1
      } else {
        return this.country2
      }
    },
    
    // 计算增长率并比较
    getHigherGrowthRate() {
      if (!this.comparisonData) {
        return { country: '暂无数据', className: '' }
      }
      
      const country1Start = this.country1Data.find(item => item.year === this.startYear)
      const country1End = this.country1Data.find(item => item.year === this.endYear)
      const country2Start = this.country2Data.find(item => item.year === this.startYear)
      const country2End = this.country2Data.find(item => item.year === this.endYear)
      
      if (!country1Start || !country1End || !country2Start || !country2End) {
        return { country: '数据不完整', className: '' }
      }
      
      const growth1 = ((country1End.expenditure - country1Start.expenditure) / country1Start.expenditure) * 100
      const growth2 = ((country2End.expenditure - country2Start.expenditure) / country2Start.expenditure) * 100
      
      if (growth1 > growth2) {
        return { 
          country: `${this.country1} +${growth1.toFixed(2)}%`, 
          className: 'positive'
        }
      } else {
        return { 
          country: `${this.country2} +${growth2.toFixed(2)}%`, 
          className: 'positive'
        }
      }
    }
  }
}
</script>

<style scoped>
.comparison-view {
  min-height: 100%;
}

.container {
  padding: 16px;
}

.selection-area {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.selection-area h3 {
  margin-bottom: 16px;
  font-size: 18px;
  color: #323233;
}

.country-selector {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.country-select-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.vs-badge {
  width: 50px;
  height: 30px;
  line-height: 30px;
  margin: 0 8px;
  background-color: #f2f3f5;
  color: #969799;
  text-align: center;
  border-radius: 15px;
  font-size: 14px;
}

.year-range {
  margin: 20px 0;
}

.year-label {
  text-align: center;
  margin-bottom: 12px;
  color: #646566;
}

.loading-container, .error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}

.comparison-results {
  margin-top: 24px;
}

.comparison-results h3 {
  margin-bottom: 16px;
  font-size: 18px;
  color: #323233;
}

.overview-cards {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.overview-card {
  flex: 1;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: relative;
  border-left: 5px solid var(--border-color, #e8f3ff);
}

.country-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.country-name {
  font-size: 16px;
  font-weight: bold;
  color: #323233;
}

.expenditure-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-color, #1989fa);
  margin-bottom: 4px;
}

.expenditure-label {
  font-size: 12px;
  color: #969799;
  margin-bottom: 8px;
}

.rank-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background-color: #f2f3f5;
  color: #646566;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.comparison-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.stats-card {
  min-width: 110px;
  flex: 1;
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
}

.chart-type-toggle {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
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

.year-data-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.country-data {
  display: flex;
  align-items: center;
  gap: 8px;
}

.country-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.expenditure {
  color: #1989fa;
  font-weight: 500;
}
</style> 