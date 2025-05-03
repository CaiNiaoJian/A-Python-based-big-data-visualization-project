<template>
  <div class="map-view">
    <van-nav-bar title="全球军力地图" left-arrow @click-left="$router.back()" />
    
    <div class="container">
      <div class="year-selector">
        <van-slider
          v-model="selectedYear"
          :min="1960"
          :max="2022"
          :step="1"
          @change="fetchData"
        />
        <div class="year-display">{{ selectedYear }} 年</div>
      </div>
      
      <div v-if="loading" class="loading">
        <van-loading type="spinner" />
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else class="map-container">
        <div class="map-placeholder">
          <p>地图视图将在此处显示</p>
          <p>当前数据: {{ selectedYear }}年军费开支数据</p>
          <p>数据数量: {{ yearData.length }} 条</p>
        </div>
        
        <div class="continent-data">
          <h3>大洲数据</h3>
          <van-grid :column-num="2" :gutter="10">
            <van-grid-item v-for="(item, index) in continentData" :key="index">
              <div class="continent-card">
                <div class="continent-name">{{ item.continent }}</div>
                <div class="continent-value">{{ formatNumber(item.total) }}</div>
                <div class="continent-label">百万美元</div>
              </div>
            </van-grid-item>
          </van-grid>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getDataByYear } from '@/utils/dataProcessor'

export default {
  name: 'MapView',
  data() {
    return {
      loading: true,
      error: null,
      selectedYear: 2020,
      yearData: [],
      continentData: []
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        this.loading = true
        this.error = null
        
        this.yearData = await getDataByYear(this.selectedYear)
        
        // 计算大洲数据
        const continentMap = {}
        this.yearData.forEach(item => {
          if (!continentMap[item.continent]) {
            continentMap[item.continent] = 0
          }
          continentMap[item.continent] += item.expenditure
        })
        
        this.continentData = Object.keys(continentMap).map(continent => ({
          continent,
          total: continentMap[continent]
        })).sort((a, b) => b.total - a.total)
        
        this.loading = false
      } catch (error) {
        console.error('获取数据失败:', error)
        this.error = '加载数据失败，请稍后重试'
        this.loading = false
      }
    },
    formatNumber(num) {
      return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    }
  }
}
</script>

<style scoped>
.map-view {
  min-height: 100%;
}

.container {
  padding: 16px;
}

.year-selector {
  margin-bottom: 24px;
}

.year-display {
  text-align: center;
  margin-top: 12px;
  font-size: 18px;
  font-weight: bold;
}

.map-container {
  margin-top: 16px;
}

.map-placeholder {
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

.loading, .error {
  padding: 30px 0;
  text-align: center;
}

.error {
  color: #f44;
}

.continent-data {
  margin-top: 24px;
}

.continent-data h3 {
  margin-bottom: 16px;
  font-size: 18px;
}

.continent-card {
  padding: 16px;
  border-radius: 8px;
  background-color: #f7f8fa;
  text-align: center;
}

.continent-name {
  font-size: 16px;
  margin-bottom: 8px;
}

.continent-value {
  font-size: 18px;
  font-weight: bold;
  color: #1989fa;
  margin-bottom: 4px;
}

.continent-label {
  font-size: 12px;
  color: #999;
}
</style> 