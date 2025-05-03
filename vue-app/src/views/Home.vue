<template>
  <div class="home">
    <van-nav-bar title="军事力量可视化" />
    
    <div class="container">
      <div class="header">
        <h1>全球军事力量数据可视化</h1>
        <p>探索世界各国军事数据的趋势和对比</p>
      </div>
      
      <van-grid :column-num="2" :gutter="10">
        <van-grid-item icon="chart-trending-o" text="全球趋势" to="/trends" />
        <van-grid-item icon="bar-chart-o" text="国家对比" to="/comparison" />
        <van-grid-item icon="world-o" text="全球地图" to="/map" />
        <van-grid-item icon="setting-o" text="设置" to="/settings" />
      </van-grid>
      
      <div class="section">
        <h2>军费开支排名前10国家</h2>
        <div v-if="loading" class="loading">
          <van-loading type="spinner" />
        </div>
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        <div v-else>
          <van-cell v-for="(item, index) in topCountries" :key="item.country" :title="`${index + 1}. ${item.country}`" :label="`军费开支: ${item.expenditure.toFixed(2)} 百万美元`" :to="`/country/${item.country}`" is-link />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTopCountriesByYear } from '@/utils/dataProcessor'

const loading = ref(true)
const error = ref(null)
const topCountries = ref([])
const selectedYear = ref(2022)

async function fetchData() {
  try {
    loading.value = true
    topCountries.value = await getTopCountriesByYear(selectedYear.value, 10)
    loading.value = false
  } catch (err) {
    console.error('获取数据失败:', err)
    error.value = '加载数据失败，请稍后重试'
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.home {
  min-height: 100%;
}

.container {
  padding: 16px;
}

.header {
  margin-bottom: 24px;
  text-align: center;
}

.header h1 {
  font-size: 24px;
  margin-bottom: 8px;
}

.header p {
  font-size: 14px;
  color: #666;
}

.section {
  margin-top: 24px;
}

.section h2 {
  font-size: 18px;
  margin-bottom: 16px;
}

.loading, .error {
  padding: 30px 0;
  text-align: center;
}

.error {
  color: #f44;
}
</style> 