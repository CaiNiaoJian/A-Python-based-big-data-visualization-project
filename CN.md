## 要求：
1. 科学性：引入一个真实的开源数据集，以反映真实情况
2. 技术性：Python：GUI+Tkinter+Matplotlib+SQLite或Manim
3. 工程性：用户友好的安装、使用和文档
4. 桌面应用程序
---
## 🏮
## 技术栈

![版本](https://img.shields.io/badge/版本-1.0.0-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.0-orange) ![状态](https://img.shields.io/badge/状态-完成-success) ![许可证](https://img.shields.io/badge/许可证-MIT-blueviolet) ![数据源](https://img.shields.io/badge/数据源-SIPRI-informational)

![NumPy](https://img.shields.io/badge/NumPy-≥1.20.0-013243?logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-≥1.3.0-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-≥3.4.0-11557c?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-≥5.3.0-3F4F75?logo=plotly&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-≥4.6.0-4B8BBE?logo=python&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-≥9.0.0-FFD43B?logo=python&logoColor=black)
![Seaborn](https://img.shields.io/badge/Seaborn-≥0.11.0-76B7B2?logo=python&logoColor=white)

![数据可视化](https://img.shields.io/badge/功能-数据可视化-brightgreen)
![军事数据](https://img.shields.io/badge/领域-军事数据-red)
![跨平台](https://img.shields.io/badge/特性-跨平台-blueviolet)

## 世界各国军事实力可视化应用（1960-2024）
我认为这对军迷来讲，一定是一个非常有趣的项目想法！创建一个展示1960-2024年世界各国军事实力变化的可视化应用完全符合这次项目要求。以下是一些具体建议：

## 数据来源
公开数据源：

- 斯德哥尔摩国际和平研究所(SIPRI) - 提供军费开支数据
- 全球火力指数(Global Firepower Index) - 提供综合军事实力排名
- 世界银行开放数据(World Bank Open Data) - 提供相关经济和人口数据
- 我们的数据世界(Our World in Data) - 提供历史军事数据
- 乌普萨拉冲突数据计划(Uppsala Conflict Data Program) - 提供冲突数据

## 可视化方案
1. 交互式世界地图：
   
   - 使用颜色深浅表示军事实力强弱
   - 点击国家可显示详细信息

2. 时间轴滑块：
   
   - 拖动滑块可以看到不同年份的全球军事格局变化
   - 可以添加播放按钮，自动展示随时间变化的动画效果

3. 多维度比较图表：
   
   - 柱状图比较不同国家的军费开支
   - 雷达图比较军事力量的不同维度（陆军、海军、空军等）
   - 折线图展示军事实力随时间的变化趋势
## 更多

## 中文版本

```markdown
## 开始使用

### 环境设置

1. 克隆仓库：
```bash
git clone https://github.com/CaiNiaoJian/A-Python-based-big-data-visualization-project.git
cd A-Python-based-big-data-visualization-project

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows系统
venv\Scripts\activate
# macOS/Linux系统
# source venv/bin/activate

# 升级pip到最新版本
python -m pip install --upgrade pip

# 安装所需包
pip install -r requirements.txt

```
# 项目使用的库总结

这个军事力量可视化项目使用了多种Python库来实现数据处理、可视化和用户界面功能。以下是主要使用的库：

## 核心数据处理库
- **pandas**：用于数据加载、处理和分析，处理Excel数据文件
- **numpy**：用于数值计算和数组操作，支持数据分析功能

## 可视化库
- **matplotlib**：创建基础图表（柱状图、折线图、饼图等）
- **plotly**：创建交互式图表（世界地图、堆叠面积图、雷达图等）
- **seaborn**：基于matplotlib的统计数据可视化

## 用户界面库
- **tkinter**：Python标准GUI库，提供基础界面组件
- **customtkinter**：tkinter的现代化扩展，提供美观的UI组件
- **PIL/Pillow**：处理图像，支持图表转换为图像显示

## 文件处理库
- **openpyxl**：用于读取Excel文件的库，pandas的依赖

## 其他辅助库
- **kaleido**：用于将plotly图表导出为静态图像
- **webbrowser**：用于打开网页链接（在"关于"页面中使用）
- **os**：处理文件路径和目录操作
- **io**：处理内存中的二进制数据流
- **datetime**：处理日期和时间，用于创建导出文件名

这些库共同构成了一个完整的数据可视化应用程序，实现了从数据加载、分析到可视化展示的全流程功能。项目采用了模块化设计，将数据处理、可视化和用户界面分离，使代码结构清晰，便于维护和扩展。


## 数据

SIPRI军费开支数据库包含173个国家1949-2023年期间的数据。该数据库最近进行了扩展，此前仅涵盖1988年开始的时期。不过，各国数据的时间跨度差异很大。大多数当时存在的国家至少有1960年代以来的数据。

有关SIPRI数据的来源和方法的信息，包括从财政年度数据计算日历年数据的方法、计算恒定价格美元数字的方法，以及作为世界和区域总计的一部分估算国家缺失数据的方法，请参见https://www.sipri.org/databases/milex/sources-and-methods。

本工作簿包括以下工作表：

1) 以恒定价格(2022年)美元(十亿)计算的世界、区域和次区域总额估计。
2) 按各国财政年度，以当前价格本地货币计算的各国军费开支数据。
3) 按日历年，以当前价格本地货币计算的各国军费开支数据。
4) 按日历年，以恒定价格(2022年)美元(百万)计算的各国军费开支数据，以及2023年以当前美元(百万)计算的数据。
5) 按日历年，以当前美元(百万)计算的各国军费开支数据。
6) 按日历年，以占GDP比例计算的各国军费开支数据。
7) 按日历年，以当前美元计算的人均军费开支数据。(仅1988-2023年)
8) 军费开支占一般政府支出的百分比数据。(仅1988-2023年)

本文档中的信息是SIPRI的知识产权。根据SIPRI的"合理使用"政策，这些数据可以免费用于非商业目的，包括研究、新闻报道、评论、不作商业销售的教育材料制作等，前提是：a) 引用SIPRI作为数据来源，引用格式为："SIPRI军费开支数据库2024，https://www.sipri.org/databases/milex"，以及b) 复制的数据不超过整个数据集的10%。

任何数据的商业使用(无论是否超过数据集的10%)，或任何超过整个数据集10%的复制，都需要获得SIPRI的特别许可，通常会根据生成数据的成本收取费用。欲了解更多信息，请联系milex@sipri.org。

就上述目的而言，SIPRI军费开支数据库的10%被定义为包含3,500个单独的数据单元，其中一个数据单元由一个国家在一年中的军费开支数字组成，可以是以当前价格本地货币计算(财政年度或日历年)、恒定(2022年)美元、当前美元，或占GDP的份额，每种情况下都包括该国家和年份的相关括号信息、特殊注释指标和脚注；或者是以恒定(2022年)美元或当前美元计算的世界或区域总额估计，以及该数字任何括号中包含的信息。

## 错误处理和备用机制

本应用程序实现了一个健壮的错误处理系统，特别是针对可能面临网络相关挑战的地图可视化组件：

1. **增强的plotly_to_image函数**：
   - 多层错误处理逻辑
   - 当第一种方式失败时，尝试替代方法来获取图像
   - 最终情况下，创建一个带有错误消息的图像，而不是抛出异常

2. **强大的地图可视化**：
   - 使用try-except块来捕获地图创建错误
   - 当地图创建失败时，提供替代可视化方案：
     - 显示前20个国家数据的条形图
     - 作为最后手段的简单表格视图

3. **用户友好的错误消息**：
   - 清晰解释发生了什么的错误消息
   - 提供替代视图或解决方案的建议
   - 引导用户完成恢复选项的状态更新

当用户遇到世界地图问题（例如，加载`world_110m.json`的错误）时，应用程序会：
1. 首先尝试标准的choropleth地图创建
2. 如果失败，尝试创建条形图来显示同样的数据
3. 如果条形图也失败，则显示简单的表格
4. 如果所有Plotly渲染都失败，则生成一个带有错误消息的图像

这个解决方案保持了代码结构的一致性，同时大大提高了应用程序的鲁棒性。

**注意**：世界地图库的成功使用需要网络访问Plotly的CDN服务器。由于这些服务器位于国际上，用户可能需要在某些网络环境中配置网络代理设置才能成功加载地图。在中国大陆使用时，可能需要借助网络代理工具才能正常显示世界地图。