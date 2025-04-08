# Mobile App
这是一个安卓（或者华为鸿蒙）移动端的app，继承src和web的项目数据集，继续开发一个军事力量可视化app

## 要求

### 1. 功能需求
- 继承桌面端和Web端的数据集和可视化功能
- 支持离线数据访问
- 提供响应式设计，适配不同尺寸的移动设备
- 实现以下核心功能：
  - 世界地图军事力量可视化
  - 国家间军事力量对比
  - 时间序列分析
  - 数据筛选和搜索
  - 收藏和分享功能

### 2. 技术栈
- 开发语言：![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white) ![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=java&logoColor=white)
- UI框架：![Jetpack Compose](https://img.shields.io/badge/Jetpack_Compose-4285F4?style=flat-square&logo=jetpackcompose&logoColor=white)
- 数据存储：![Room Database](https://img.shields.io/badge/Room-3DDC84?style=flat-square&logo=android&logoColor=white)
- 网络请求：![Retrofit](https://img.shields.io/badge/Retrofit-48B983?style=flat-square&logo=square&logoColor=white)
- 图表库：![MPAndroidChart](https://img.shields.io/badge/MPAndroidChart-3DDC84?style=flat-square&logo=android&logoColor=white)
- 地图组件：![Google Maps](https://img.shields.io/badge/Google_Maps-4285F4?style=flat-square&logo=google-maps&logoColor=white) ![高德地图](https://img.shields.io/badge/高德地图-FF0000?style=flat-square&logo=autonavi&logoColor=white)

### 3. 性能要求
- 应用启动时间 < 2秒
- 页面切换流畅，无卡顿
- 离线数据加载时间 < 1秒
- 内存占用 < 100MB
- 支持Android 8.0及以上版本

### 4. 安全要求
- 实现数据加密存储
- 支持用户认证
- 保护用户隐私数据
- 遵循Google Play安全规范

### 5. 用户体验
- 简洁直观的界面设计
- 支持深色模式
- 手势操作支持
- 多语言支持（中英文）
- 无障碍功能支持

### 6. 开发规范
- 遵循MVVM架构模式
- 使用Kotlin协程处理异步任务
- 实现单元测试和UI测试
- 代码注释率 > 30%
- 遵循Google官方开发规范

### 7. 发布要求
- 通过Google Play审核
- 支持应用内更新
- 提供错误报告机制
- 定期更新数据源

## 项目结构
```
mobile-app/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── com/
│   │   │   │       └── military/
│   │   │   │           ├── data/
│   │   │   │           ├── di/
│   │   │   │           ├── ui/
│   │   │   │           ├── utils/
│   │   │   │           └── MilitaryApp.kt
│   │   │   └── res/
│   │   └── test/
│   ├── build.gradle
│   └── proguard-rules.pro
├── gradle/
├── build.gradle
└── settings.gradle
```

## 开发计划
1. 需求分析和设计（1周）
2. 基础架构搭建（1周）
3. 核心功能开发（3周）
4. UI/UX优化（1周）
5. 测试和调试（1周）
6. 发布准备（1周）

## 注意事项
- 确保与桌面端和Web端数据格式保持一致
- 定期同步更新数据源
- 关注用户反馈，持续优化
- 遵守相关法律法规
