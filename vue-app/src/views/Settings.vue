<template>
  <div class="settings-view">
    <van-nav-bar title="设置" left-arrow @click-left="$router.back()" />
    
    <div class="container">
      <van-cell-group title="应用设置">
        <van-cell title="语言" is-link :value="language" @click="showLanguagePicker = true" />
        <van-cell title="夜间模式">
          <template #right-icon>
            <van-switch v-model="darkMode" size="24" />
          </template>
        </van-cell>
        <van-cell title="数据缓存" is-link value="清除" @click="clearCache" />
      </van-cell-group>
      
      <van-cell-group title="关于" class="margin-top">
        <van-cell title="应用版本" value="1.0.0" />
        <van-cell title="数据来源" is-link @click="showDataSourceInfo = true" />
        <van-cell title="关于项目" is-link @click="showAboutInfo = true" />
      </van-cell-group>
      
      <div class="about-section">
        <h3>军事力量可视化</h3>
        <p>本应用致力于提供全球军事力量数据的可视化展示，帮助用户了解全球军事发展趋势。</p>
      </div>
    </div>
    
    <!-- 语言选择 -->
    <van-popup v-model="showLanguagePicker" position="bottom">
      <van-picker
        show-toolbar
        :columns="languages"
        @confirm="onLanguageSelected"
        @cancel="showLanguagePicker = false"
      />
    </van-popup>
    
    <!-- 数据来源弹窗 -->
    <van-popup
      v-model="showDataSourceInfo"
      closeable
      round
      position="bottom"
      :style="{ height: '50%' }"
    >
      <div class="popup-title">数据来源</div>
      <div class="popup-content">
        <p>本应用使用的数据主要来源于：</p>
        <ul>
          <li>斯德哥尔摩国际和平研究所 (SIPRI)</li>
          <li>世界银行公开数据</li>
          <li>联合国统计数据库</li>
        </ul>
        <p>数据时间范围：1960-2022年</p>
        <p>数据更新频率：每年</p>
        <p>最后更新时间：2023年3月</p>
      </div>
    </van-popup>
    
    <!-- 关于项目弹窗 -->
    <van-popup
      v-model="showAboutInfo"
      closeable
      round
      position="bottom"
      :style="{ height: '50%' }"
    >
      <div class="popup-title">关于项目</div>
      <div class="popup-content">
        <p>军事力量可视化应用是一个开源项目，旨在以直观的方式展示全球军事力量数据。</p>
        <p>主要功能：</p>
        <ul>
          <li>全球军事力量分布地图</li>
          <li>国家军事力量对比</li>
          <li>军事力量历史趋势分析</li>
          <li>军费支出排名</li>
        </ul>
        <p>技术栈：Vue.js, Vant UI, XLSX</p>
        <p>开源协议：MIT</p>
        <p>项目地址：<a href="https://github.com/example/military-visualization">GitHub</a></p>
        <p>欢迎贡献代码和提交问题反馈。</p>
      </div>
    </van-popup>
  </div>
</template>

<script>
export default {
  name: 'SettingsView',
  data() {
    return {
      language: '简体中文',
      darkMode: false,
      showLanguagePicker: false,
      showDataSourceInfo: false,
      showAboutInfo: false,
      languages: ['简体中文', '繁體中文', 'English']
    }
  },
  methods: {
    onLanguageSelected(language) {
      this.language = language
      this.showLanguagePicker = false
      // 实际项目中，这里会存储语言偏好并应用
      this.$toast(`语言已设置为：${language}`)
    },
    clearCache() {
      this.$dialog.confirm({
        title: '清除缓存',
        message: '确认要清除应用缓存吗？这将清除所有离线数据。',
      }).then(() => {
        // 实际项目中，这里会清理缓存
        localStorage.clear()
        this.$toast('缓存已清除')
      }).catch(() => {
        // 取消操作
      })
    }
  },
  watch: {
    darkMode(newValue) {
      // 实际项目中，这里会切换应用主题
      this.$toast(`夜间模式：${newValue ? '开启' : '关闭'}`)
    }
  }
}
</script>

<style scoped>
.settings-view {
  min-height: 100%;
}

.container {
  padding: 16px;
}

.about-section {
  margin-top: 32px;
  text-align: center;
  padding: 16px;
}

.about-section h3 {
  font-size: 18px;
  margin-bottom: 8px;
}

.about-section p {
  color: #666;
  font-size: 14px;
}

.margin-top {
  margin-top: 24px;
}

.popup-title {
  font-size: 18px;
  font-weight: bold;
  padding: 16px;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.popup-content {
  padding: 16px;
  overflow-y: auto;
  max-height: calc(100% - 50px);
}

.popup-content p {
  margin-bottom: 12px;
}

.popup-content ul {
  padding-left: 20px;
  margin-bottom: 12px;
}

.popup-content li {
  margin-bottom: 8px;
}
</style> 