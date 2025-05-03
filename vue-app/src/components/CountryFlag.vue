<template>
  <div 
    class="country-flag"
    :class="{ 'circle': isCircle, 'small': size === 'small', 'large': size === 'large' }"
    :style="{'background-color': backgroundColor}"
  >
    <span v-if="!hasFlagImage" class="country-initial">
      {{ getInitial(countryName) }}
    </span>
    <img v-else :src="flagUrl" :alt="countryName" class="flag-image" />
  </div>
</template>

<script>
export default {
  name: 'CountryFlag',
  props: {
    countryName: {
      type: String,
      required: true
    },
    isoCode: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    isCircle: {
      type: Boolean,
      default: true
    },
    backgroundColor: {
      type: String,
      default: '#1989fa'
    }
  },
  computed: {
    // 获取国旗图片URL
    flagUrl() {
      if (!this.isoCode) return ''
      return `https://flagcdn.com/w80/${this.isoCode.toLowerCase()}.png`
    },
    
    // 检查是否有国旗图片
    hasFlagImage() {
      return !!this.isoCode
    }
  },
  methods: {
    // 获取首字母
    getInitial(name) {
      if (!name) return '?'
      return name.charAt(0).toUpperCase()
    }
  }
}
</script>

<style scoped>
.country-flag {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--background-color, #1989fa);
  color: white;
  font-weight: bold;
  overflow: hidden;
  width: 48px;
  height: 48px;
}

.circle {
  border-radius: 50%;
}

.small {
  width: 32px;
  height: 32px;
  font-size: 14px;
}

.large {
  width: 64px;
  height: 64px;
  font-size: 24px;
}

.country-initial {
  font-size: 20px;
}

.small .country-initial {
  font-size: 14px;
}

.large .country-initial {
  font-size: 28px;
}

.flag-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style> 