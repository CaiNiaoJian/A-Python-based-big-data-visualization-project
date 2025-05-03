<template>
  <div id="app">
    <div class="content">
      <router-view />
    </div>
    <van-tabbar v-model="active" route>
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="world-o" to="/map">地图</van-tabbar-item>
      <van-tabbar-item icon="bar-chart-o" to="/comparison">对比</van-tabbar-item>
      <van-tabbar-item icon="chart-trending-o" to="/trends">趋势</van-tabbar-item>
      <van-tabbar-item icon="setting-o" to="/settings">设置</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const active = ref(0)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: 'PingFang SC', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f7f8fa;
}

.content {
  padding-bottom: 50px;
  height: 100%;
  overflow-y: auto;
}
</style>
