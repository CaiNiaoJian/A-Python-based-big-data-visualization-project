import React, { useState, useEffect, useRef } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  CircularProgress, 
  Alert, 
  Slider, 
  Card, 
  CardContent, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Tooltip,
  SelectChangeEvent,
  Tab,
  Tabs
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import ReactECharts from 'echarts-for-react';
// 引入完整的echarts而不是echarts/core
import * as echarts from 'echarts';
import axios from 'axios';

// 定义数据接口
interface CountryData {
  Country: string;
  Continent: string;
  Expenditure: number;
}

interface YearData {
  year: number;
  countries: CountryData[];
}

interface CountryMetadata {
  [country: string]: {
    iso_code: string;
    coordinates: {
      lat: number;
      lon: number;
    }
  }
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

// 获取大洲颜色
const getContinentColor = (continent: string): string => {
  const colors: {[key: string]: string} = {
    'Africa': '#FF5722',
    'Americas': '#2196F3',
    'Asia': '#4CAF50',
    'Europe': '#9C27B0',
    'Oceania': '#FFC107',
    'african': '#FF5722',
    'american': '#2196F3',
    'aisan': '#4CAF50',
    'europen': '#9C27B0',
    'easternasian': '#FFC107'
  };
  return colors[continent] || '#607D8B'; // 默认颜色
};

const Map: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedYear, setSelectedYear] = useState<number>(2022); // 默认显示最新年份
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [mapData, setMapData] = useState<CountryData[]>([]);
  const [selectedContinent, setSelectedContinent] = useState<string>('all');
  const [viewMode, setViewMode] = useState<number>(0); // 0: 表格视图, 1: 地图视图
  const [countryMetadata, setCountryMetadata] = useState<CountryMetadata>({});
  const [mapLoading, setMapLoading] = useState<boolean>(true);
  const [mapLoadError, setMapLoadError] = useState<string | null>(null);
  
  const chartRef = useRef<ReactECharts>(null);

  // 获取年份列表
  useEffect(() => {
    const fetchAvailableYears = async () => {
      try {
        // 获取1990年以后的数据，数据质量更好
        const years = Array.from({ length: 33 }, (_, i) => 1990 + i).reverse();
        setAvailableYears(years);
      } catch (err) {
        setError('加载年份数据失败');
        console.error(err);
      }
    };

    fetchAvailableYears();
  }, []);
  
  // 加载国家元数据
  useEffect(() => {
    const fetchCountryMetadata = async () => {
      setMapLoading(true);
      setMapLoadError(null);
      
      try {
        const response = await axios.get<CountryMetadata>('/data/country_metadata.json');
        setCountryMetadata(response.data);
        setMapLoading(false);
      } catch (err) {
        console.error('Error loading country metadata:', err);
        setMapLoadError('加载国家元数据失败，地图功能可能不完整');
        setMapLoading(false);
      }
    };
    
    fetchCountryMetadata();
  }, []);

  // 加载特定年份的数据
  useEffect(() => {
    const fetchYearData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/data/year_${selectedYear}.json`);
        
        if (!response.ok) {
          throw new Error(`加载${selectedYear}年数据失败`);
        }
        
        const data = await response.json();
        
        // 设置国家数据
        setMapData(data);
      } catch (err) {
        setError(`加载${selectedYear}年数据失败: ${err instanceof Error ? err.message : String(err)}`);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (selectedYear) {
      fetchYearData();
    }
  }, [selectedYear]);
  
  // 当echarts脚本加载完成时注册地图
  useEffect(() => {
    // 当视图切换到地图模式，确保地图自适应容器大小
    if (viewMode === 1 && chartRef.current) {
      const chart = chartRef.current.getEchartsInstance();
      setTimeout(() => {
        chart.resize();
      }, 200);
    }
  }, [viewMode]);

  // 处理年份变更
  const handleYearChange = (event: SelectChangeEvent<number>) => {
    setSelectedYear(Number(event.target.value));
  };

  // 使用滑块改变年份
  const handleSliderChange = (_event: Event, newValue: number | number[]) => {
    if (typeof newValue === 'number') {
      setSelectedYear(newValue);
    }
  };

  // 处理大洲选择变更
  const handleContinentChange = (event: SelectChangeEvent<string>) => {
    setSelectedContinent(event.target.value);
  };
  
  // 处理视图模式切换
  const handleViewModeChange = (_event: React.SyntheticEvent, newValue: number) => {
    setViewMode(newValue);
  };

  // 获取筛选后的数据
  const getFilteredData = (): CountryData[] => {
    if (selectedContinent === 'all') {
      return mapData;
    } else {
      return mapData.filter(country => country.Continent.toLowerCase() === selectedContinent);
    }
  };
  
  // 获取备用图表配置（当地图加载失败时使用）
  const getFallbackChartOption = () => {
    // 获取排名前20的国家数据
    const topCountries = getFilteredData()
      .sort((a, b) => b.Expenditure - a.Expenditure)
      .slice(0, 20);
      
    // 按大洲分组统计军费支出
    const continentData: {[key: string]: number} = {};
    getFilteredData().forEach(country => {
      if (!continentData[country.Continent]) {
        continentData[country.Continent] = 0;
      }
      continentData[country.Continent] += country.Expenditure;
    });
    
    // 准备饼图数据
    const pieData = Object.entries(continentData).map(([continent, value]) => ({
      name: continent,
      value,
      itemStyle: {
        color: getContinentColor(continent)
      }
    }));
    
    // 准备柱状图数据
    const barData = topCountries.map(country => ({
      name: country.Country,
      value: country.Expenditure,
      itemStyle: {
        color: getContinentColor(country.Continent)
      }
    }));
    
    return {
      title: [
        {
          text: `${selectedYear}年全球军费支出分布`,
          left: 'center',
          top: 0
        },
        {
          text: '按大洲分布',
          left: '25%',
          top: '50%',
          textAlign: 'center'
        },
        {
          text: '前20国家',
          left: '75%',
          top: '50%',
          textAlign: 'center'
        }
      ],
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          if (params.seriesType === 'pie') {
            return `${params.name}: ${formatCurrency(params.value)} (${params.percent}%)`;
          } else {
            return `${params.name}: ${formatCurrency(params.value)}`;
          }
        }
      },
      legend: {
        type: 'scroll',
        orient: 'vertical',
        right: 10,
        top: 50,
        bottom: 20,
      },
      grid: [
        {right: '50%', top: '55%', bottom: '10%', left: '10%'},
      ],
      xAxis: [
        {gridIndex: 0, type: 'value', name: '军费支出', axisLabel: {rotate: 30}},
      ],
      yAxis: [
        {
          gridIndex: 0, 
          type: 'category', 
          data: barData.map(item => item.name),
          axisLabel: {
            interval: 0,
            width: 100,
            overflow: 'truncate',
            fontSize: 10
          }
        },
      ],
      series: [
        // 饼图 - 按大洲分布
        {
          name: '大洲军费支出',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['25%', '75%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 16,
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: false
          },
          data: pieData
        },
        // 水平柱状图 - 前20国家
        {
          name: '前20国家军费支出',
          type: 'bar',
          xAxisIndex: 0,
          yAxisIndex: 0,
          data: barData.map(item => ({
            value: item.value,
            itemStyle: item.itemStyle
          }))
        }
      ]
    };
  };
  
  // 获取世界地图配置
  const getWorldMapOption = () => {
    // 准备地图数据
    const data = getFilteredData()
      .map(country => {
        const metadata = countryMetadata[country.Country];
        if (!metadata) return null;
        
        return {
          name: country.Country,
          value: country.Expenditure,
          continent: country.Continent,
          // 使用国家坐标
          coord: [metadata.coordinates.lon, metadata.coordinates.lat]
        };
      })
      .filter(item => item !== null) as any[];
    
    // 计算最大值和最小值，用于设置气泡大小范围
    const expenditures = data.map(item => item.value);
    const maxValue = Math.max(...expenditures);
    const minValue = Math.min(...expenditures);
    
    // 设置气泡大小范围 (最小5, 最大30)
    const symbolSizeScale = (value: number) => {
      if (maxValue === minValue) return 10;
      const normalizedValue = (value - minValue) / (maxValue - minValue);
      return 5 + normalizedValue * 25;
    };
    
    // 计算出与支出相对应的颜色 (红色渐变)
    const getColorByValue = (value: number) => {
      if (maxValue === minValue) return 'rgba(255, 0, 0, 0.7)';
      const intensity = (value - minValue) / (maxValue - minValue);
      // 从浅红色到深红色的渐变
      return `rgba(255, ${Math.round(200 - intensity * 200)}, ${Math.round(200 - intensity * 200)}, 0.7)`;
    };
    
    return {
      backgroundColor: '#F5F5F5',
      title: {
        text: `${selectedYear}年全球军费支出地图`,
        left: 'center',
        top: 10
      },
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          const { name, value, continent } = params.data;
          return `
            <div style="font-weight:bold;margin-bottom:5px;">${name}</div>
            <div>大洲: ${continent}</div>
            <div>军费支出: ${formatCurrency(value)}</div>
          `;
        }
      },
      visualMap: {
        min: minValue,
        max: maxValue,
        text: ['高', '低'],
        inRange: {
          color: ['#FFD700', '#FF4500']
        },
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '5%',
        formatter: (value: number) => formatCurrency(value)
      },
      geo: {
        map: 'world',
        roam: true,  // 允许缩放和平移
        zoom: 1.2,
        center: [0, 20],  // 地图中心点
        label: {
          show: false
        },
        itemStyle: {
          areaColor: '#eee',
          borderColor: '#ccc',
          emphasis: {
            areaColor: '#F5F5F5',
            shadowOffsetX: 0,
            shadowOffsetY: 0,
            shadowBlur: 20,
            borderWidth: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      },
      series: [
        {
          name: '军费支出',
          type: 'scatter',
          coordinateSystem: 'geo',
          data: data,
          symbolSize: (value: any) => symbolSizeScale(value[2]),
          itemStyle: {
            color: (params: any) => getColorByValue(params.data.value)
          },
          encode: {
            value: 2
          },
          zlevel: 1,
          emphasis: {
            label: {
              show: true,
              position: 'top',
              formatter: '{b}'
            }
          }
        },
        {
          name: '前10国家',
          type: 'effectScatter',
          coordinateSystem: 'geo',
          data: data
            .sort((a, b) => b.value - a.value)
            .slice(0, 10),
          symbolSize: (value: any) => symbolSizeScale(value[2]) * 1.2,
          showEffectOn: 'render',
          rippleEffect: {
            brushType: 'stroke'
          },
          hoverAnimation: true,
          itemStyle: {
            color: (params: any) => getColorByValue(params.data.value),
            shadowBlur: 10,
            shadowColor: '#333'
          },
          zlevel: 2,
          emphasis: {
            label: {
              show: true,
              position: 'top',
              formatter: '{b}'
            }
          }
        }
      ]
    };
  };
  
  // 准备ECharts实例
  const onChartReady = (chart: any) => {
    try {
      // 尝试注册地图
      fetch('/assets/world.json')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to load world map data');
          }
          return response.json();
        })
        .then(worldMap => {
          try {
            // 使用全局echarts对象注册地图
            if (echarts && typeof echarts.registerMap === 'function') {
              echarts.registerMap('world', worldMap);
              chart.setOption(getWorldMapOption());
            } else {
              console.error('echarts.registerMap is not available');
              setMapLoadError('地图功能不可用，显示备用图表');
              chart.setOption(getFallbackChartOption());
            }
          } catch (error) {
            console.error('Error rendering world map:', error);
            setMapLoadError('世界地图渲染失败，显示备用图表');
            // 显示备用图表
            chart.setOption(getFallbackChartOption());
          }
        })
        .catch(err => {
          console.error('Failed to load world map:', err);
          setMapLoadError('世界地图加载失败，显示备用图表');
          // 显示备用图表
          chart.setOption(getFallbackChartOption());
        });
    } catch (error) {
      console.error('Unexpected error in map initialization:', error);
      setMapLoadError('地图初始化过程中出现意外错误，显示备用图表');
      chart.setOption(getFallbackChartOption());
    }
  };

  return (
    <Box sx={{ py: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        世界军事支出地图
      </Typography>
      
      <Typography variant="subtitle1" gutterBottom align="center" sx={{ mb: 3 }}>
        按国家查看{selectedYear}年全球军费支出分布
      </Typography>

      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
          <Box sx={{ flex: 1 }}>
            <FormControl fullWidth>
              <InputLabel id="year-select-label">选择年份</InputLabel>
              <Select
                labelId="year-select-label"
                id="year-select"
                value={selectedYear}
                label="选择年份"
                onChange={handleYearChange}
                disabled={loading}
              >
                {availableYears.map(year => (
                  <MenuItem key={year} value={year}>{year}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
          
          <Box sx={{ flex: 2 }}>
            <Typography gutterBottom>年份滑块</Typography>
            <Slider
              value={selectedYear}
              min={1990}
              max={2022}
              marks={[
                { value: 1990, label: '1990' },
                { value: 2000, label: '2000' },
                { value: 2010, label: '2010' },
                { value: 2022, label: '2022' }
              ]}
              onChange={handleSliderChange}
              valueLabelDisplay="auto"
              disabled={loading}
            />
          </Box>

          <Box sx={{ flex: 1 }}>
            <FormControl fullWidth>
              <InputLabel id="continent-select-label">选择大洲</InputLabel>
              <Select
                labelId="continent-select-label"
                id="continent-select"
                value={selectedContinent}
                label="选择大洲"
                onChange={handleContinentChange}
                disabled={loading}
              >
                <MenuItem value="all">所有大洲</MenuItem>
                <MenuItem value="africa">非洲</MenuItem>
                <MenuItem value="americas">美洲</MenuItem>
                <MenuItem value="asia">亚洲</MenuItem>
                <MenuItem value="europe">欧洲</MenuItem>
                <MenuItem value="oceania">大洋洲</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>
      </Paper>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
      
      {/* 视图切换标签 */}
      <Paper elevation={3} sx={{ mb: 3 }}>
        <Tabs
          value={viewMode}
          onChange={handleViewModeChange}
          variant="fullWidth"
          centered
        >
          <Tab label="表格视图" />
          <Tab label="地图视图" />
        </Tabs>
      </Paper>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {/* 表格视图 */}
          {viewMode === 0 && (
            <Paper 
              elevation={3} 
              sx={{ 
                p: 3,
                mb: 3
              }}
            >
              <Typography variant="h6" gutterBottom display="flex" alignItems="center">
                {selectedYear}年军费支出排名前20的国家
                <Tooltip title="军费支出单位为百万美元">
                  <InfoIcon fontSize="small" sx={{ ml: 1 }} />
                </Tooltip>
              </Typography>
              
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>排名</TableCell>
                      <TableCell>国家</TableCell>
                      <TableCell>大洲</TableCell>
                      <TableCell align="right">军费支出</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {getFilteredData()
                      .sort((a, b) => b.Expenditure - a.Expenditure)
                      .slice(0, 20)
                      .map((country, index) => (
                        <TableRow 
                          key={country.Country}
                          sx={{ 
                            '&:nth-of-type(odd)': { backgroundColor: 'rgba(0, 0, 0, 0.03)' },
                            borderLeft: `4px solid ${getContinentColor(country.Continent)}`
                          }}
                        >
                          <TableCell>{index + 1}</TableCell>
                          <TableCell>{country.Country}</TableCell>
                          <TableCell>{country.Continent}</TableCell>
                          <TableCell align="right">{formatCurrency(country.Expenditure)}</TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          )}
          
          {/* 地图视图 */}
          {viewMode === 1 && (
            <Paper 
              elevation={3} 
              sx={{ 
                p: 3,
                mb: 3
              }}
            >
              {mapLoadError && (
                <Alert severity="warning" sx={{ mb: 3 }}>{mapLoadError}</Alert>
              )}
              
              {mapLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <Box sx={{ height: 600, position: 'relative' }}>
                  <ReactECharts
                    ref={chartRef}
                    style={{ height: '100%', width: '100%' }}
                    option={{}}
                    onChartReady={onChartReady}
                    opts={{ renderer: 'canvas' }}
                    onEvents={{
                      // 窗口大小改变时自动调整图表大小
                      resize: () => {
                        if (chartRef.current) {
                          chartRef.current.getEchartsInstance().resize();
                        }
                      }
                    }}
                  />
                  <Typography 
                    variant="caption" 
                    color="text.secondary" 
                    sx={{ 
                      position: 'absolute', 
                      bottom: 5, 
                      right: 10,
                      backgroundColor: 'rgba(255,255,255,0.7)',
                      padding: '2px 5px',
                      borderRadius: 1
                    }}
                  >
                    提示: 可使用鼠标滚轮缩放，按住左键拖动地图
                  </Typography>
                </Box>
              )}
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" gutterBottom>
                  <strong>地图说明：</strong> 
                </Typography>
                <Typography variant="body2">
                  • 气泡大小表示军费支出的相对数量，颜色深浅也反映了支出规模
                </Typography>
                <Typography variant="body2">
                  • 前10名国家以特效气泡突出显示
                </Typography>
                <Typography variant="body2">
                  • 鼠标悬停在气泡上可查看详细信息
                </Typography>
              </Box>
            </Paper>
          )}
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
            <Card sx={{ flex: 1, minWidth: { xs: '100%', md: '45%' } }}>
              <CardContent>
                <Typography variant="h6" gutterBottom display="flex" alignItems="center">
                  军费支出统计 ({selectedYear})
                  <Tooltip title="显示选定范围内的军费支出统计数据">
                    <InfoIcon fontSize="small" sx={{ ml: 1 }} />
                  </Tooltip>
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">总军费支出</Typography>
                  <Typography variant="h5">
                    {formatCurrency(getFilteredData().reduce((sum, country) => sum + country.Expenditure, 0))}
                  </Typography>
                </Box>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">国家数量</Typography>
                  <Typography variant="h5">{getFilteredData().length}</Typography>
                </Box>
                
                <Box>
                  <Typography variant="body2" color="text.secondary">平均军费支出</Typography>
                  <Typography variant="h5">
                    {formatCurrency(getFilteredData().reduce((sum, country) => sum + country.Expenditure, 0) / (getFilteredData().length || 1))}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
            
            <Card sx={{ flex: 1, minWidth: { xs: '100%', md: '45%' } }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  关于数据
                </Typography>
                <Typography paragraph>
                  此页面显示了{selectedYear}年各国的军事支出数据。数据来源于斯德哥尔摩国际和平研究所(SIPRI)的军费支出数据库。
                </Typography>
                <Typography paragraph>
                  数据以百万美元为单位，经过了适当处理和转换，以确保可比性。可以通过上方的年份选择器或滑块来查看不同年份的数据，也可以按大洲筛选。
                </Typography>
                <Typography>
                  表格左侧的彩色条纹表示不同大洲：
                  <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {[
                      { name: '非洲', color: getContinentColor('Africa') },
                      { name: '美洲', color: getContinentColor('Americas') },
                      { name: '亚洲', color: getContinentColor('Asia') },
                      { name: '欧洲', color: getContinentColor('Europe') },
                      { name: '大洋洲', color: getContinentColor('Oceania') }
                    ].map(continent => (
                      <Box 
                        key={continent.name}
                        sx={{ 
                          display: 'flex', 
                          alignItems: 'center',
                          mr: 2
                        }}
                      >
                        <Box sx={{ width: 16, height: 16, bgcolor: continent.color, mr: 0.5 }} />
                        <Typography variant="body2">{continent.name}</Typography>
                      </Box>
                    ))}
                  </Box>
                </Typography>
              </CardContent>
            </Card>
          </Box>
        </>
      )}
    </Box>
  );
};

export default Map; 