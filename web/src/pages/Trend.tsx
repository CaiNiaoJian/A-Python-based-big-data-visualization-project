import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  SelectChangeEvent,
  CircularProgress, 
  Alert,
  Button,
  Card,
  CardContent,
  Tabs,
  Tab,
  useTheme
} from '@mui/material';
import ReactECharts from 'echarts-for-react';
import axios from 'axios';

// 定义数据接口
interface CountryData {
  Country: string;
  Continent: string;
  Expenditure: number;
}

interface YearData {
  [year: string]: CountryData[];
}

interface YearsSummary {
  [key: string]: {
    total_countries: number;
    file: string;
    total_expenditure: number;
  };
}

interface TrendData {
  year: number;
  value: number;
}

interface ContinentTrend {
  continent: string;
  data: TrendData[];
}

// 格式化数字显示
const formatCurrency = (value: number): string => {
  if (value >= 1000000) {
    return `$${(value / 1000000).toFixed(1)}M`;
  } else if (value >= 1000) {
    return `$${(value / 1000).toFixed(1)}K`;
  }
  return `$${value.toFixed(1)}`;
};

// 定义大洲颜色
const continentColors: { [key: string]: string } = {
  'Africa': '#8C564B',
  'Americas': '#E377C2',
  'Asia': '#FF7F0E',
  'Europe': '#1F77B4',
  'Oceania': '#2CA02C'
};

const Trend: React.FC = () => {
  const theme = useTheme();
  
  // 状态
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [startYear, setStartYear] = useState<number>(1990);
  const [endYear, setEndYear] = useState<number>(2022);
  const [yearlyData, setYearlyData] = useState<YearData>({});
  const [globalTrend, setGlobalTrend] = useState<TrendData[]>([]);
  const [continentTrends, setContinentTrends] = useState<ContinentTrend[]>([]);
  const [topCountryTrends, setTopCountryTrends] = useState<any[]>([]);
  const [tabValue, setTabValue] = useState<number>(0);
  const [animationActive, setAnimationActive] = useState<boolean>(false);
  
  const chartRef = useRef<ReactECharts>(null);
  
  // 加载年份数据
  useEffect(() => {
    const fetchYearsSummary = async () => {
      try {
        const response = await axios.get<YearsSummary>('/data/years_summary.json');
        
        // 提取可用年份并按升序排序
        const years = Object.keys(response.data)
          .map(year => parseInt(year))
          .sort((a, b) => a - b);
        
        setAvailableYears(years);
        
        // 默认从1990年开始，到最新年份结束
        const defaultStartYear = Math.max(1990, years[0]);
        setStartYear(defaultStartYear);
        setEndYear(years[years.length - 1]);
      } catch (err) {
        console.error('Error fetching years summary:', err);
        setError('无法加载年份数据。请稍后再试。');
      }
    };
    
    fetchYearsSummary();
  }, []);
  
  // 加载年度数据
  useEffect(() => {
    const loadYearlyData = async () => {
      if (availableYears.length === 0) return;
      
      setLoading(true);
      setError(null);
      
      const data: YearData = {};
      const years = availableYears.filter(year => year >= startYear && year <= endYear);
      
      try {
        for (const year of years) {
          const response = await axios.get<CountryData[]>(`/data/year_${year}.json`);
          data[year.toString()] = response.data;
        }
        
        setYearlyData(data);
        
        // 计算全球趋势
        calculateGlobalTrend(data);
        
        // 计算大洲趋势
        calculateContinentTrends(data);
        
        // 计算主要国家趋势
        calculateTopCountryTrends(data);
        
        setLoading(false);
      } catch (err) {
        console.error('Error loading yearly data:', err);
        setError('加载年度数据时出错。请稍后再试。');
        setLoading(false);
      }
    };
    
    loadYearlyData();
  }, [availableYears, startYear, endYear]);
  
  // 计算全球趋势
  const calculateGlobalTrend = (data: YearData) => {
    const trend: TrendData[] = [];
    
    Object.entries(data).forEach(([year, countryData]) => {
      const totalExpenditure = countryData.reduce((sum, country) => sum + country.Expenditure, 0);
      trend.push({
        year: parseInt(year),
        value: totalExpenditure
      });
    });
    
    // 按年份排序
    trend.sort((a, b) => a.year - b.year);
    setGlobalTrend(trend);
  };
  
  // 计算大洲趋势
  const calculateContinentTrends = (data: YearData) => {
    const continents = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania'];
    const trends: ContinentTrend[] = continents.map(continent => ({
      continent,
      data: []
    }));
    
    Object.entries(data).forEach(([year, countryData]) => {
      // 按大洲分组计算总军费
      const continentData: { [key: string]: number } = {};
      
      countryData.forEach(country => {
        const continent = country.Continent || 'Unknown';
        if (!continentData[continent]) {
          continentData[continent] = 0;
        }
        continentData[continent] += country.Expenditure;
      });
      
      // 更新每个大洲的趋势数据
      trends.forEach(trend => {
        trend.data.push({
          year: parseInt(year),
          value: continentData[trend.continent] || 0
        });
      });
    });
    
    // 按年份排序每个大洲的数据
    trends.forEach(trend => {
      trend.data.sort((a, b) => a.year - b.year);
    });
    
    setContinentTrends(trends);
  };
  
  // 计算主要国家趋势
  const calculateTopCountryTrends = (data: YearData) => {
    if (Object.keys(data).length === 0) return;
    
    // 获取最新年份的数据
    const latestYear = Math.max(...Object.keys(data).map(Number));
    const latestData = data[latestYear.toString()];
    
    // 排序并获取军费支出最高的10个国家
    const topCountries = latestData
      .sort((a, b) => b.Expenditure - a.Expenditure)
      .slice(0, 10)
      .map(country => country.Country);
    
    // 为每个国家创建趋势数据
    const countryTrends: any[] = topCountries.map(country => {
      const countryData: TrendData[] = [];
      
      Object.entries(data).forEach(([year, yearData]) => {
        const countryYear = yearData.find(c => c.Country === country);
        if (countryYear) {
          countryData.push({
            year: parseInt(year),
            value: countryYear.Expenditure
          });
        } else {
          countryData.push({
            year: parseInt(year),
            value: 0
          });
        }
      });
      
      // 按年份排序
      countryData.sort((a, b) => a.year - b.year);
      
      return {
        country,
        data: countryData
      };
    });
    
    setTopCountryTrends(countryTrends);
  };
  
  // 处理开始年份变更
  const handleStartYearChange = (event: SelectChangeEvent<number>) => {
    const value = Number(event.target.value);
    setStartYear(value);
    
    // 确保结束年份不早于开始年份
    if (value > endYear) {
      setEndYear(value);
    }
  };
  
  // 处理结束年份变更
  const handleEndYearChange = (event: SelectChangeEvent<number>) => {
    const value = Number(event.target.value);
    setEndYear(value);
    
    // 确保开始年份不晚于结束年份
    if (value < startYear) {
      setStartYear(value);
    }
  };
  
  // 处理标签页变化
  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };
  
  // 处理动画开始/暂停
  const handleAnimationToggle = () => {
    setAnimationActive(prev => !prev);
  };
  
  // 获取全球趋势图表配置
  const getGlobalTrendOption = () => {
    return {
      title: {
        text: '全球军费支出趋势 (1990-2022)',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const param = params[0];
          return `${param.name}年: ${formatCurrency(param.value)}`;
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '10%',
        top: '15%',
        containLabel: true
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        data: globalTrend.map(item => item.year),
        name: '年份',
        nameLocation: 'middle',
        nameGap: 30,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        nameLocation: 'middle',
        nameGap: 50,
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000000 ? `${(value / 1000000).toFixed(0)}M` : 
                  value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      series: [
        {
          name: '全球军费支出',
          type: 'line',
          data: globalTrend.map(item => item.value),
          smooth: true,
          lineStyle: {
            width: 4
          },
          itemStyle: {
            color: '#1F77B4'
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                {
                  offset: 0,
                  color: 'rgba(31, 119, 180, 0.7)'
                },
                {
                  offset: 1,
                  color: 'rgba(31, 119, 180, 0.1)'
                }
              ]
            }
          },
          markPoint: {
            data: [
              { type: 'max', name: '最大值' },
              { type: 'min', name: '最小值' }
            ]
          },
          markLine: {
            data: [
              { type: 'average', name: '平均值' }
            ]
          }
        }
      ],
      // 添加动画效果
      animationDuration: 2000,
      animationEasing: 'elasticOut',
      animationDelay: function(idx: number) {
        return idx * 200;
      }
    };
  };
  
  // 获取大洲趋势图表配置
  const getContinentTrendOption = () => {
    return {
      title: {
        text: '各大洲军费支出趋势',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: continentTrends.map(trend => trend.continent),
        bottom: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        top: '15%',
        containLabel: true
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: continentTrends.length > 0 ? continentTrends[0].data.map(item => item.year) : [],
        name: '年份',
        nameLocation: 'middle',
        nameGap: 30,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        nameLocation: 'middle',
        nameGap: 50,
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000000 ? `${(value / 1000000).toFixed(0)}M` : 
                   value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      series: continentTrends.map(trend => ({
        name: trend.continent,
        type: 'line',
        stack: '总量',
        areaStyle: {},
        emphasis: {
          focus: 'series'
        },
        data: trend.data.map(item => item.value),
        itemStyle: {
          color: continentColors[trend.continent] || '#5470C6'
        }
      }))
    };
  };
  
  // 获取国家趋势图表配置
  const getCountryTrendOption = () => {
    return {
      title: {
        text: '主要国家军费支出趋势',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: topCountryTrends.map(trend => trend.country),
        type: 'scroll',
        bottom: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        top: '15%',
        containLabel: true
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: topCountryTrends.length > 0 ? topCountryTrends[0].data.map((item: TrendData) => item.year) : [],
        name: '年份',
        nameLocation: 'middle',
        nameGap: 30,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        nameLocation: 'middle',
        nameGap: 50,
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000000 ? `${(value / 1000000).toFixed(0)}M` : 
                   value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      series: topCountryTrends.map((trend, index) => ({
        name: trend.country,
        type: 'line',
        data: trend.data.map((item: TrendData) => item.value),
        emphasis: {
          focus: 'series'
        },
        lineStyle: {
          width: index < 3 ? 3 : 2 // 前三个国家线条更粗
        }
      }))
    };
  };
  
  // 获取占比图表配置
  const getShareChartOption = () => {
    // 处理数据，计算每个大洲的占比
    const years = globalTrend.map(item => item.year);
    const selectedYears = [
      years[0], 
      years[Math.floor(years.length / 3)], 
      years[Math.floor(years.length * 2 / 3)], 
      years[years.length - 1]
    ];
    
    // 准备数据
    const seriesData = continentTrends.map(trend => {
      return {
        name: trend.continent,
        type: 'bar',
        stack: '总量',
        emphasis: {
          focus: 'series'
        },
        data: selectedYears.map(year => {
          const yearData = trend.data.find(item => item.year === year);
          return yearData ? yearData.value : 0;
        }),
        itemStyle: {
          color: continentColors[trend.continent] || '#5470C6'
        }
      };
    });
    
    return {
      title: {
        text: '各大洲军费支出占比变化',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: continentTrends.map(trend => trend.continent),
        bottom: 0
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        top: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: selectedYears.map(year => `${year}年`)
      },
      yAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000000 ? `${(value / 1000000).toFixed(0)}M` : 
                   value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      series: seriesData
    };
  };
  
  // 获取动态赛跑图表配置
  const getRaceChartOption = () => {
    // 准备数据
    const years = globalTrend.map(item => item.year);
    
    // 如果还没有选定年份或动画未激活，显示最后一年
    const currentYear = animationActive ? 
      years[Math.floor((Date.now() / 1000) % years.length)] : 
      years[years.length - 1];
    
    // 获取当前年份的数据
    const yearData = yearlyData[currentYear.toString()] || [];
    
    // 获取排名前10的国家
    const topCountries = yearData
      .sort((a, b) => b.Expenditure - a.Expenditure)
      .slice(0, 10);
    
    return {
      title: {
        text: `${currentYear}年全球军费支出前10名`,
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '20%',
        right: '15%',
        bottom: '3%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000000 ? `${(value / 1000000).toFixed(0)}M` : 
                   value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      yAxis: {
        type: 'category',
        data: topCountries.map(country => country.Country),
        inverse: true,
        animationDuration: 300,
        animationDurationUpdate: 300
      },
      series: [
        {
          realtimeSort: true,
          name: '军费支出',
          type: 'bar',
          data: topCountries.map(country => country.Expenditure),
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => {
              return formatCurrency(params.value);
            }
          },
          itemStyle: {
            color: function(params: any) {
              const colors = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570'];
              return colors[params.dataIndex % colors.length];
            }
          }
        }
      ],
      animationDuration: 3000,
      animationDurationUpdate: 3000
    };
  };
  
  // 根据当前标签页获取图表配置
  const getChartOption = () => {
    switch (tabValue) {
      case 0: // 全球趋势
        return getGlobalTrendOption();
      case 1: // 大洲趋势
        return getContinentTrendOption();
      case 2: // 国家趋势
        return getCountryTrendOption();
      case 3: // 占比变化
        return getShareChartOption();
      case 4: // 动态赛跑
        return getRaceChartOption();
      default:
        return getGlobalTrendOption();
    }
  };
  
  // 处理图表更新（用于动画）
  useEffect(() => {
    if (!animationActive || tabValue !== 4) return;
    
    const timer = setInterval(() => {
      // 触发图表更新
      if (chartRef.current) {
        chartRef.current.getEchartsInstance().setOption(getRaceChartOption());
      }
    }, 1000);
    
    return () => clearInterval(timer);
  }, [animationActive, tabValue, yearlyData]);
  
  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        军费支出趋势分析
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          {/* 年份范围选择 */}
          <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '200px' } }}>
            <FormControl fullWidth>
              <InputLabel id="start-year-label">起始年份</InputLabel>
              <Select
                labelId="start-year-label"
                id="start-year"
                value={startYear}
                label="起始年份"
                onChange={handleStartYearChange}
                disabled={loading}
              >
                {availableYears.map(year => (
                  <MenuItem key={`start-${year}`} value={year}>{year}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
          
          <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '200px' } }}>
            <FormControl fullWidth>
              <InputLabel id="end-year-label">结束年份</InputLabel>
              <Select
                labelId="end-year-label"
                id="end-year"
                value={endYear}
                label="结束年份"
                onChange={handleEndYearChange}
                disabled={loading}
              >
                {availableYears.filter(year => year >= startYear).map(year => (
                  <MenuItem key={`end-${year}`} value={year}>{year}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
          
          {/* 动画控制按钮，仅在动态赛跑标签页显示 */}
          {tabValue === 4 && (
            <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '200px' }, display: 'flex', alignItems: 'center' }}>
              <Button 
                variant="contained" 
                color={animationActive ? "error" : "primary"}
                onClick={handleAnimationToggle}
                fullWidth
              >
                {animationActive ? "暂停动画" : "开始动画"}
              </Button>
            </Box>
          )}
        </Box>
      </Paper>
      
      {/* 加载中状态 */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}
      
      {/* 错误状态 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
      )}
      
      {/* 标签页切换 */}
      {!loading && !error && (
        <>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange}
              variant="scrollable"
              scrollButtons="auto"
            >
              <Tab label="全球趋势" />
              <Tab label="大洲趋势" />
              <Tab label="国家趋势" />
              <Tab label="占比变化" />
              <Tab label="动态排名" />
            </Tabs>
          </Box>
          
          {/* 图表展示 */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <ReactECharts 
                ref={chartRef}
                option={getChartOption()} 
                style={{ height: '500px', width: '100%' }}
                opts={{ renderer: 'svg' }}
              />
            </CardContent>
          </Card>
          
          {/* 图表说明 */}
          <Paper sx={{ p: 3, bgcolor: 'background.paper' }}>
            <Typography variant="body2" color="text.secondary">
              {tabValue === 0 && "全球趋势图展示了全球各国军费支出总额随时间的变化趋势，可以观察到全球军事投入的整体走向。"}
              {tabValue === 1 && "大洲趋势图展示了各大洲的军费支出随时间的变化，以堆叠面积图的形式直观展示各洲在全球军费中的比重。"}
              {tabValue === 2 && "国家趋势图展示了军费支出最高的十个国家随时间的变化趋势，可以观察各主要军事大国的支出变化。"}
              {tabValue === 3 && "占比变化图展示了不同时间点各大洲军费支出的绝对值和相对占比，直观比较各大洲间的军事投入差异。"}
              {tabValue === 4 && "动态排名以赛跑图的形式展示各年度军费支出排名前十的国家，可以动态观察排名变化。"}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              数据说明: 所有军费支出数据均以百万美元计，来源于斯德哥尔摩国际和平研究所(SIPRI)军费开支数据库。
            </Typography>
          </Paper>
        </>
      )}
    </Box>
  );
};

export default Trend; 