<template>
  <div class="country-detail">
    <van-nav-bar
      :title="country"
      left-arrow
      @click-left="$router.back()"
      :right-text="isFavorite ? '取消收藏' : '收藏'"
      @click-right="toggleFavorite"
    />
    
    <div v-if="loading" class="loading">
      <van-loading type="spinner" />
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="countryData.length === 0" class="empty">
      没有找到 {{ country }} 的军事数据
    </div>
    <div v-else class="container">
      <!-- 国家基本信息 -->
      <div class="country-info">
        <div class="country-flag">
          <div class="flag-placeholder">
            {{ country.substr(0, 1) }}
          </div>
        </div>
        <div class="country-stats">
          <div class="country-name">{{ country }}</div>
          <div class="stats-row">
            <div class="stat-item">
              <div class="stat-value">{{ formatNumber(getLatestExpenditure()) }}</div>
              <div class="stat-label">最新军费支出（百万美元）</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ latestRank ? `第${latestRank}位` : '暂无' }}</div>
              <div class="stat-label">全球排名</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 军费支出趋势 -->
      <div class="section">
        <h3>军费支出趋势</h3>
        <div class="year-range">
          <van-slider
            v-model="yearRange"
            range
            :min="1960"
            :max="2022"
            :step="1"
            @change="handleYearRangeChange"
          />
          <div class="year-label">{{ startYear }} - {{ endYear }}</div>
        </div>
        
        <div class="chart-placeholder">
          <p>军费支出趋势图将在此处显示</p>
          <p>显示 {{ country }} 在 {{ startYear }}-{{ endYear }} 年间的军费支出变化</p>
        </div>
        
        <!-- 数据统计 -->
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
      </div>
      
      <!-- 历史数据表格 -->
      <div class="section">
        <h3>历史数据</h3>
        <van-search
          v-model="searchYear"
          placeholder="搜索年份"
          @input="filterData"
        />
        
        <van-cell-group>
          <van-cell v-for="item in filteredData" :key="item.year">
            <template #title>
              <span class="cell-year">{{ item.year }}年</span>
            </template>
            <template #default>
              <span class="cell-value">{{ formatNumber(item.expenditure) }}百万美元</span>
            </template>
            <template #label>
              <span class="cell-rank" v-if="item.rank">
                全球排名: 第{{ item.rank }}位
              </span>
            </template>
          </van-cell>
        </van-cell-group>
      </div>
      
      <!-- 对比推荐 -->
      <div class="section">
        <h3>推荐对比</h3>
        <div class="recommend-list">
          <van-cell
            v-for="rec in recommendations"
            :key="rec"
            :title="rec"
            is-link
            @click="goToCompare(rec)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getDataByCountry, loadCountries } from '@/utils/dataProcessor'

export default {
  name: 'CountryDetail',
  props: {
    name: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      country: '',
      loading: true,
      error: null,
      countryData: [],
      filteredData: [],
      yearRange: [2010, 2022],
      startYear: 2010,
      endYear: 2022,
      searchYear: '',
      isFavorite: false,
      recommendations: [],
      latestRank: null
    }
  },
  created() {
    this.country = this.name
    this.fetchData()
    this.loadRecommendations()
    
    // 检查是否已收藏
    const favorites = JSON.parse(localStorage.getItem('favoriteCountries') || '[]')
    this.isFavorite = favorites.includes(this.country)
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true
        this.error = null
        
        const data = await getDataByCountry(this.country)
        if (!data || data.length === 0) {
          this.error = `没有找到${this.country}的军事数据`
          this.loading = false
          return
        }
        
        this.countryData = data.sort((a, b) => b.year - a.year)
        this.filterData()
        
        // 获取最新的排名
        const latestData = this.countryData[0]
        if (latestData && latestData.rank) {
          this.latestRank = latestData.rank
        }
        
        this.loading = false
      } catch (error) {
        console.error('获取国家数据失败:', error)
        this.error = '加载数据失败，请稍后重试'
        this.loading = false
      }
    },
    async loadRecommendations() {
      try {
        const countries = await loadCountries()
        // 从国家列表中随机选择3个不同于当前国家的国家
        const filteredCountries = countries
          .map(c => c.name)
          .filter(name => name !== this.country)
        
        // 随机选择3个国家
        this.recommendations = []
        while (this.recommendations.length < 3 && filteredCountries.length > 0) {
          const index = Math.floor(Math.random() * filteredCountries.length)
          this.recommendations.push(filteredCountries[index])
          filteredCountries.splice(index, 1)
        }
      } catch (error) {
        console.error('加载推荐国家失败:', error)
      }
    },
    filterData() {
      if (!this.searchYear) {
        this.filteredData = this.countryData
      } else {
        const searchTerm = this.searchYear.trim()
        this.filteredData = this.countryData.filter(item => 
          item.year.toString().includes(searchTerm)
        )
      }
    },
    handleYearRangeChange(values) {
      this.startYear = values[0]
      this.endYear = values[1]
    },
    getFilteredDataByYearRange() {
      return this.countryData.filter(
        item => item.year >= this.startYear && item.year <= this.endYear
      )
    },
    getAverageExpenditure() {
      const filteredData = this.getFilteredDataByYearRange()
      if (filteredData.length === 0) return 0
      
      const sum = filteredData.reduce((total, item) => total + item.expenditure, 0)
      return sum / filteredData.length
    },
    getTotalExpenditure() {
      const filteredData = this.getFilteredDataByYearRange()
      if (filteredData.length === 0) return 0
      
      return filteredData.reduce((total, item) => total + item.expenditure, 0)
    },
    getGrowthRate() {
      const filteredData = this.getFilteredDataByYearRange()
      if (filteredData.length < 2) return 0
      
      // 找到开始年份和结束年份的数据
      const firstYearData = filteredData.find(item => item.year === this.startYear)
      const lastYearData = filteredData.find(item => item.year === this.endYear)
      
      if (!firstYearData || !lastYearData) return 0
      
      const firstValue = firstYearData.expenditure
      const lastValue = lastYearData.expenditure
      
      if (firstValue === 0) return 0
      
      return ((lastValue - firstValue) / firstValue) * 100
    },
    getLatestExpenditure() {
      if (this.countryData.length === 0) return 0
      return this.countryData[0].expenditure
    },
    formatNumber(num) {
      return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    toggleFavorite() {
      const favorites = JSON.parse(localStorage.getItem('favoriteCountries') || '[]')
      
      if (this.isFavorite) {
        // 移除收藏
        const index = favorites.indexOf(this.country)
        if (index !== -1) {
          favorites.splice(index, 1)
        }
      } else {
        // 添加收藏
        if (!favorites.includes(this.country)) {
          favorites.push(this.country)
        }
      }
      
      localStorage.setItem('favoriteCountries', JSON.stringify(favorites))
      this.isFavorite = !this.isFavorite
      
      this.$toast(this.isFavorite ? '已添加到收藏' : '已从收藏中移除')
    },
    goToCompare(otherCountry) {
      this.$router.push({
        path: '/comparison',
        query: {
          country1: this.country,
          country2: otherCountry
        }
      })
    }
  }
}
</script>

<style scoped>
.country-detail {
  min-height: 100%;
}

.container {
  padding: 16px;
}

.loading, .error, .empty {
  padding: 30px 0;
  text-align: center;
}

.error {
  color: #f44;
}

.country-info {
  display: flex;
  margin-bottom: 24px;
  padding: 16px;
  background-color: #f7f8fa;
  border-radius: 8px;
}

.country-flag {
  width: 60px;
  height: 60px;
  margin-right: 16px;
}

.flag-placeholder {
  width: 100%;
  height: 100%;
  background-color: #1989fa;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  border-radius: 50%;
}

.country-stats {
  flex: 1;
}

.country-name {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stats-row {
  display: flex;
}

.stat-item {
  margin-right: 20px;
}

.stat-value {
  font-weight: bold;
  color: #1989fa;
}

.stat-label {
  font-size: 12px;
  color: #999;
}

.section {
  margin-bottom: 24px;
  background-color: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(100, 101, 102, 0.08);
}

.section h3 {
  margin-bottom: 16px;
  font-size: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.year-range {
  margin-bottom: 16px;
}

.year-label {
  text-align: center;
  margin-top: 8px;
  color: #666;
}

.chart-placeholder {
  background-color: #eee;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  margin-bottom: 16px;
  text-align: center;
}

.stats-cards {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.stats-card {
  width: 32%;
  padding: 12px;
  border-radius: 8px;
  background-color: #f7f8fa;
  text-align: center;
  margin-bottom: 8px;
}

.stats-title {
  font-size: 12px;
  margin-bottom: 4px;
}

.stats-value {
  font-size: 14px;
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
  font-size: 10px;
  color: #999;
}

.cell-year {
  font-weight: bold;
}

.cell-value {
  color: #1989fa;
}

.cell-rank {
  font-size: 12px;
  color: #999;
}
</style> 