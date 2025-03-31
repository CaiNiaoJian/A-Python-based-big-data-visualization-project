# 世界军事力量可视化平台 - Web前端

这是一个基于React和TypeScript的前端应用程序，用于可视化世界各国的军事力量数据。

## 技术栈

- **React**: 用于构建用户界面的JavaScript库
- **TypeScript**: JavaScript的超集，添加了静态类型定义
- **React Router**: 用于处理应用程序的路由
- **Material-UI**: 用于UI组件的React UI框架
- **Axios**: 用于进行HTTP请求的库

## 项目结构

```
src/
├── assets/         # 图像、图标等静态资源
├── components/     # 可复用组件
│   └── NavBar.tsx  # 导航栏组件
├── pages/          # 页面组件
│   ├── Home.tsx    # 首页
│   └── ...         # 其他页面组件
├── services/       # 服务和API调用
│   └── api.ts      # API服务
├── types/          # TypeScript类型定义
├── App.tsx         # 应用程序主组件
└── index.tsx       # 应用程序入口点
```

## 功能

- **首页**: 项目概览和快速导航
- **仪表板**: 全球军事数据概览
- **世界地图**: 军事力量的地理分布可视化
- **国家比较**: 不同国家的军事力量对比
- **趋势分析**: 军事支出随时间的变化趋势

## 安装和运行

### 前提条件

- Node.js (v14.0.0或更高版本)
- npm (v6.0.0或更高版本)

### 安装步骤

1. 克隆项目

```bash
git clone <repository-url>
cd web
```

2. 安装依赖

```bash
npm install
```

3. 运行开发服务器

```bash
npm start
```

应用将在 [http://localhost:3000](http://localhost:3000) 打开。

### 构建生产版本

```bash
npm run build
```

构建后的文件将位于 `build/` 目录中。

## 与后端连接

该前端应用程序默认连接到 `http://localhost:5000/api`。要更改API的URL，可以设置环境变量 `REACT_APP_API_URL`。

例如，创建一个 `.env` 文件：

```
REACT_APP_API_URL=https://your-api-url.com/api
```

## 数据来源

应用程序使用的数据来源于斯德哥尔摩国际和平研究所(SIPRI)的军费开支数据库。

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
