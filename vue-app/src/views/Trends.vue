<template>
  <div class="trends-view">
    <van-nav-bar title="军事力量趋势" left-arrow @click-left="$router.back()" />
    
    <div class="container">
      <div class="filters">
        <h3>筛选条件</h3>
        
        <van-field
          v-model="selectedCountry"
          label="国家"
          placeholder="选择国家"
          readonly
          right-icon="arrow-down"
          @click="showCountryPicker = true"
        />
        
        <div class="year-range">
          <div class="year-label">年份范围: {{ startYear }} - {{ endYear }}</div>
          <van-slider
            v-model="yearRange"
            range
            :min="1960"
            :max="2022"
            :step="1"
            @change="handleYearRangeChange"
          />
        </div>
        
        <van-button type="primary" block @click="fetchTrend">查看趋势</van-button>
      </div>
      
      <div v-if="loading" class="loading">
        <van-loading type="spinner" />
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else-if="trendData.length > 0" class="trend-data">
        <h3>{{ selectedCountry }} 军费开支趋势 ({{ startYear }}-{{ endYear }})</h3>
        
        <div class="stats-cards">
          <div class="stats-card">
            <div class="stats-title">平均支出</div>
            <div class="stats-value">{{ formatNumber(getAverageExpenditure()) }}</div>
            <div class="stats-label">百万美元/年</div>
          </div>
          
          <div class="stats-card">
            <div class="stats-title">总支出</div>
            <div class="stats-value">{{ formatNumber(getTotalExpenditure()) }}</div>
            <div class="stats-label">百万美元</div>
          </div>
          
          <div class="stats-card">
            <div class="stats-title">增长率</div>
            <div class="stats-value" :class="getGrowthRate() >= 0 ? 'positive' : 'negative'">
              {{ getGrowthRate() >= 0 ? '+' : '' }}{{ getGrowthRate().toFixed(2) }}%
            </div>
            <div class="stats-label">{{ startYear }} - {{ endYear }}</div>
          </div>
        </div>
        
        <div class="chart-placeholder">
          <p>趋势图表将在此处显示</p>
          <p>显示 {{ selectedCountry }} 在 {{ startYear }}-{{ endYear }} 年间的军费开支趋势</p>
          <p>数据点数量: {{ trendData.length }}</p>
        </div>
        
        <div class="data-table">
          <h4>数据明细</h4>
          <van-cell-group>
            <van-cell v-for="item in trendData" :key="item.year" :title="item.year + '年'" :value="formatNumber(item.expenditure) + '百万美元'" />
          </van-cell-group>
        </div>
      </div>
      
      <van-popup v-model="showCountryPicker" position="bottom">
        <van-picker
          show-toolbar
          :columns="countries"
          @confirm="onCountrySelected"
          @cancel="showCountryPicker = false"
        />
      </van-popup>
    </div>
  </div>
</template>

<script>
import { loadCountries, getCountryTrend } from '@/utils/dataProcessor'

export default {
  name: 'TrendsView',
  data() {
    return {
      loading: false,
      error: null,
      countries: [],
      selectedCountry: '',
      showCountryPicker: false,
      yearRange: [2010, 2022],
      startYear: 2010,
      endYear: 2022,
      trendData: []
    }
  },
  async created() {
    try {
      const countryData = await loadCountries()
      this.countries = countryData.map(country => country.name)
      
      // 默认选择中国
      if (this.countries.includes('中国')) {
        this.selectedCountry = '中国'
        this.fetchTrend()
      }
    } catch (error) {
      console.error('加载国家数据失败:', error)
      this.error = '加载国家数据失败，请稍后重试'
    }
  },
  methods: {
    onCountrySelected(country) {
      this.selectedCountry = country
      this.showCountryPicker = false
    },
    handleYearRangeChange(values) {
      this.startYear = values[0]
      this.endYear = values[1]
    },
    async fetchTrend() {
      if (!this.selectedCountry) {
        this.error = '请选择要查看趋势的国家'
        return
      }
      
      try {
        this.loading = true
        this.error = null
        
        this.trendData = await getCountryTrend(
          this.selectedCountry,
          this.startYear,
          this.endYear
        )
        
        this.loading = false
      } catch (error) {
        console.error('获取趋势数据失败:', error)
        this.error = '加载趋势数据失败，请稍后重试'
        this.loading = false
      }
    },
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
      
      // 找到开始年份和结束年份的数据
      const firstYearData = this.trendData.find(item => item.year === this.startYear)
      const lastYearData = this.trendData.find(item => item.year === this.endYear)
      
      if (!firstYearData || !lastYearData) return 0
      
      const firstValue = firstYearData.expenditure
      const lastValue = lastYearData.expenditure
      
      if (firstValue === 0) return 0
      
      return ((lastValue - firstValue) / firstValue) * 100
    },
    formatNumber(num) {
      return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    }
  }
}
</script>

<style scoped>
.trends-view {
  min-height: 100%;
}

.container {
  padding: 16px;
}

.filters {
  margin-bottom: 24px;
}

.filters h3 {
  margin-bottom: 16px;
  font-size: 18px;
}

.year-range {
  margin: 16px 0 24px;
}

.year-label {
  margin-bottom: 12px;
}

.trend-data {
  margin-top: 24px;
}

.trend-data h3 {
  margin-bottom: 16px;
  font-size: 18px;
  text-align: center;
}

.stats-cards {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.stats-card {
  width: 32%;
  padding: 16px;
  border-radius: 8px;
  background-color: #f7f8fa;
  text-align: center;
  margin-bottom: 8px;
}

.stats-title {
  font-size: 14px;
  margin-bottom: 8px;
}

.stats-value {
  font-size: 16px;
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
  color: #999;
}

.chart-placeholder {
  background-color: #eee;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  margin-bottom: 24px;
  text-align: center;
}

.data-table {
  margin-top: 24px;
}

.data-table h4 {
  margin-bottom: 12px;
  font-size: 16px;
}

.loading, .error {
  padding: 30px 0;
  text-align: center;
}

.error {
  color: #f44;
}
</style> 