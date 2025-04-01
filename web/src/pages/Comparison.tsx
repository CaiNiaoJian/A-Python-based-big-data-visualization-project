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
  SelectChangeEvent,
  Autocomplete,
  TextField,
  Button,
  Chip,
  Card,
  CardContent,
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

interface YearlyData {
  [year: string]: CountryData[];
}

interface YearsSummary {
  [key: string]: {
    total_countries: number;
    file: string;
    total_expenditure: number;
  };
}

interface CountryExpenditureByYear {
  country: string;
  continent: string;
  data: {
    year: number;
    expenditure: number;
  }[];
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

const Comparison: React.FC = () => {
  const theme = useTheme();
  
  // 状态
  const [loading, setLoading] = useState<boolean>(true);
  const [initialLoading, setInitialLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [startYear, setStartYear] = useState<number>(2000);
  const [endYear, setEndYear] = useState<number>(2022);
  const [allCountries, setAllCountries] = useState<string[]>([]);
  const [selectedCountries, setSelectedCountries] = useState<string[]>([]);
  const [countryInput, setCountryInput] = useState<string>('');
  const [comparisonData, setComparisonData] = useState<CountryExpenditureByYear[]>([]);
  const [yearlyData, setYearlyData] = useState<YearlyData>({});
  const [chartType, setChartType] = useState<string>('line');
  
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
        setStartYear(years[Math.floor(years.length / 2)]); // 默认从中间年份开始
        setEndYear(years[years.length - 1]); // 默认到最新年份结束
      } catch (err) {
        console.error('Error fetching years summary:', err);
        setError('无法加载年份数据。请稍后再试。');
      }
    };
    
    fetchYearsSummary();
  }, []);
  
  // 加载国家列表
  useEffect(() => {
    const fetchCountries = async () => {
      try {
        // 使用最新年份的数据获取所有国家列表
        if (availableYears.length > 0) {
          const latestYear = Math.max(...availableYears);
          const response = await axios.get<CountryData[]>(`/data/year_${latestYear}.json`);
          
          // 提取国家列表并排序
          const countries = response.data
            .map(item => item.Country)
            .sort((a, b) => a.localeCompare(b));
          
          setAllCountries(countries);
          
          // 默认选择前5个军费支出最高的国家
          const topCountries = response.data
            .sort((a, b) => b.Expenditure - a.Expenditure)
            .slice(0, 5)
            .map(item => item.Country);
          
          setSelectedCountries(topCountries);
          setInitialLoading(false);
        }
      } catch (err) {
        console.error('Error fetching countries:', err);
        setError('无法加载国家列表。请稍后再试。');
        setInitialLoading(false);
      }
    };
    
    if (availableYears.length > 0) {
      fetchCountries();
    }
  }, [availableYears]);
  
  // 预加载所有年份的数据
  useEffect(() => {
    const loadYearlyData = async () => {
      setLoading(true);
      setError(null);
      
      const data: YearlyData = {};
      const years = availableYears.filter(year => year >= startYear && year <= endYear);
      
      try {
        for (const year of years) {
          const response = await axios.get<CountryData[]>(`/data/year_${year}.json`);
          data[year.toString()] = response.data;
        }
        
        setYearlyData(data);
        setLoading(false);
      } catch (err) {
        console.error('Error loading yearly data:', err);
        setError('加载年度数据时出错。请稍后再试。');
        setLoading(false);
      }
    };
    
    if (startYear && endYear && !initialLoading) {
      loadYearlyData();
    }
  }, [startYear, endYear, availableYears, initialLoading]);
  
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
  
  // 处理图表类型变更
  const handleChartTypeChange = (event: SelectChangeEvent<string>) => {
    setChartType(event.target.value);
  };
  
  // 处理国家添加
  const handleAddCountry = () => {
    if (countryInput && !selectedCountries.includes(countryInput)) {
      setSelectedCountries([...selectedCountries, countryInput]);
      setCountryInput('');
    }
  };
  
  // 处理国家删除
  const handleDeleteCountry = (countryToDelete: string) => {
    setSelectedCountries(selectedCountries.filter(country => country !== countryToDelete));
  };
  
  // 处理国家列表清空
  const handleClearCountries = () => {
    setSelectedCountries([]);
  };
  
  // 处理数据比较
  useEffect(() => {
    if (Object.keys(yearlyData).length > 0 && selectedCountries.length > 0) {
      const years = Object.keys(yearlyData).map(Number).sort((a, b) => a - b);
      
      const result: CountryExpenditureByYear[] = selectedCountries.map(country => {
        const countryData = {
          country,
          continent: '',
          data: years.map(year => ({
            year,
            expenditure: 0
          }))
        };
        
        // 填充每年的数据
        years.forEach((year, index) => {
          const yearData = yearlyData[year.toString()];
          const countryYearData = yearData.find(item => item.Country === country);
          
          if (countryYearData) {
            countryData.data[index].expenditure = countryYearData.Expenditure;
            if (!countryData.continent && countryYearData.Continent) {
              countryData.continent = countryYearData.Continent;
            }
          }
        });
        
        return countryData;
      });
      
      setComparisonData(result);
    } else {
      setComparisonData([]);
    }
  }, [yearlyData, selectedCountries]);
  
  // 获取折线图配置
  const getLineChartOption = () => {
    const years = comparisonData.length > 0
      ? comparisonData[0].data.map(d => d.year)
      : [];
    
    const series = comparisonData.map(country => ({
      name: country.country,
      type: 'line',
      data: country.data.map(d => d.expenditure),
      smooth: true,
      emphasis: {
        focus: 'series'
      },
      lineStyle: {
        width: 3
      }
    }));
    
    return {
      title: {
        text: '军费支出趋势比较',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          let tooltip = `<div style="font-weight:bold;margin-bottom:5px;">${params[0].axisValue}年</div>`;
          params.forEach((param: any) => {
            tooltip += `<div style="display:flex;align-items:center;margin:3px 0;">
              <span style="display:inline-block;width:10px;height:10px;background:${param.color};margin-right:5px;"></span>
              <span>${param.seriesName}: ${formatCurrency(param.value)}</span>
            </div>`;
          });
          return tooltip;
        }
      },
      legend: {
        data: comparisonData.map(c => c.country),
        type: 'scroll',
        orient: 'horizontal',
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
        data: years,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      series
    };
  };
  
  // 获取柱状图配置
  const getBarChartOption = () => {
    const years = comparisonData.length > 0
      ? comparisonData[0].data.map(d => d.year)
      : [];
    
    const series = comparisonData.map(country => ({
      name: country.country,
      type: 'bar',
      data: country.data.map(d => d.expenditure),
      emphasis: {
        focus: 'series'
      }
    }));
    
    return {
      title: {
        text: '军费支出对比',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: (params: any) => {
          let tooltip = `<div style="font-weight:bold;margin-bottom:5px;">${params[0].axisValue}年</div>`;
          params.forEach((param: any) => {
            tooltip += `<div style="display:flex;align-items:center;margin:3px 0;">
              <span style="display:inline-block;width:10px;height:10px;background:${param.color};margin-right:5px;"></span>
              <span>${param.seriesName}: ${formatCurrency(param.value)}</span>
            </div>`;
          });
          return tooltip;
        }
      },
      legend: {
        data: comparisonData.map(c => c.country),
        type: 'scroll',
        orient: 'horizontal',
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
        data: years,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      series
    };
  };
  
  // 获取堆叠区域图配置
  const getStackedAreaChartOption = () => {
    const years = comparisonData.length > 0
      ? comparisonData[0].data.map(d => d.year)
      : [];
    
    const series = comparisonData.map(country => ({
      name: country.country,
      type: 'line',
      stack: '总量',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: country.data.map(d => d.expenditure)
    }));
    
    return {
      title: {
        text: '军费支出累计对比',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          let tooltip = `<div style="font-weight:bold;margin-bottom:5px;">${params[0].axisValue}年</div>`;
          params.forEach((param: any) => {
            tooltip += `<div style="display:flex;align-items:center;margin:3px 0;">
              <span style="display:inline-block;width:10px;height:10px;background:${param.color};margin-right:5px;"></span>
              <span>${param.seriesName}: ${formatCurrency(param.value)}</span>
            </div>`;
          });
          return tooltip;
        }
      },
      legend: {
        data: comparisonData.map(c => c.country),
        type: 'scroll',
        orient: 'horizontal',
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
        data: years,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '军费支出 (百万美元)',
        axisLabel: {
          formatter: (value: number) => {
            return value >= 1000 ? `${(value / 1000).toFixed(0)}K` : value;
          }
        }
      },
      series
    };
  };
  
  // 获取雷达图配置
  const getRadarChartOption = () => {
    if (comparisonData.length === 0) return {};
    
    // 雷达图只展示最近10年数据，避免过于复杂
    const recentYears = comparisonData[0].data
      .slice(-10)
      .map(d => d.year);
    
    const indicator = recentYears.map(year => ({
      name: `${year}`,
      max: Math.max(...comparisonData.map(country => {
        const yearData = country.data.find(d => d.year === year);
        return yearData ? yearData.expenditure : 0;
      })) * 1.2 // 最大值增加20%的空间
    }));
    
    const series = [{
      type: 'radar',
      data: comparisonData.map(country => ({
        value: recentYears.map(year => {
          const yearData = country.data.find(d => d.year === year);
          return yearData ? yearData.expenditure : 0;
        }),
        name: country.country,
        areaStyle: {
          opacity: 0.3
        },
        lineStyle: {
          width: 2
        }
      }))
    }];
    
    return {
      title: {
        text: '最近10年军费支出雷达图',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        data: comparisonData.map(c => c.country),
        type: 'scroll',
        orient: 'horizontal',
        bottom: 0
      },
      grid: {
        bottom: '15%'
      },
      radar: {
        indicator,
        splitNumber: 4,
        axisName: {
          formatter: '{value}'
        }
      },
      series
    };
  };
  
  // 获取当前图表配置
  const getChartOption = () => {
    switch (chartType) {
      case 'line':
        return getLineChartOption();
      case 'bar':
        return getBarChartOption();
      case 'area':
        return getStackedAreaChartOption();
      case 'radar':
        return getRadarChartOption();
      default:
        return getLineChartOption();
    }
  };
  
  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        国家军费支出比较
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
                disabled={loading || initialLoading}
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
                disabled={loading || initialLoading}
              >
                {availableYears.filter(year => year >= startYear).map(year => (
                  <MenuItem key={`end-${year}`} value={year}>{year}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
          
          <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '200px' } }}>
            <FormControl fullWidth>
              <InputLabel id="chart-type-label">图表类型</InputLabel>
              <Select
                labelId="chart-type-label"
                id="chart-type"
                value={chartType}
                label="图表类型"
                onChange={handleChartTypeChange}
                disabled={loading || initialLoading}
              >
                <MenuItem value="line">折线图</MenuItem>
                <MenuItem value="bar">柱状图</MenuItem>
                <MenuItem value="area">堆叠面积图</MenuItem>
                <MenuItem value="radar">雷达图</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>
        
        {/* 国家选择 */}
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            选择比较国家
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'flex-start' }}>
            <Autocomplete
              id="country-selector"
              options={allCountries.filter(country => !selectedCountries.includes(country))}
              sx={{ width: 300 }}
              renderInput={(params) => <TextField {...params} label="搜索国家" />}
              value={countryInput}
              onChange={(_, newValue) => setCountryInput(newValue || '')}
              disabled={loading || initialLoading}
            />
            
            <Button 
              variant="contained" 
              onClick={handleAddCountry}
              disabled={!countryInput || loading || initialLoading}
            >
              添加国家
            </Button>
            
            <Button 
              variant="outlined" 
              color="error"
              onClick={handleClearCountries}
              disabled={selectedCountries.length === 0 || loading || initialLoading}
            >
              清空所有
            </Button>
          </Box>
          
          {/* 已选国家列表 */}
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 2 }}>
            {selectedCountries.map(country => (
              <Chip
                key={country}
                label={country}
                onDelete={() => handleDeleteCountry(country)}
                color="primary"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>
      </Paper>
      
      {/* 加载中状态 */}
      {(loading || initialLoading) && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}
      
      {/* 错误状态 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
      )}
      
      {/* 图表展示 */}
      {!loading && !initialLoading && !error && comparisonData.length > 0 && (
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
      )}
      
      {/* 无数据提示 */}
      {!loading && !initialLoading && !error && comparisonData.length === 0 && (
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary">
            请选择至少一个国家进行比较
          </Typography>
        </Paper>
      )}
      
      {/* 数据说明 */}
      <Paper sx={{ p: 3, bgcolor: 'background.paper' }}>
        <Typography variant="body2" color="text.secondary">
          数据说明: 所有军费支出数据均以百万美元计，来源于斯德哥尔摩国际和平研究所(SIPRI)军费开支数据库。
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          通过选择不同的图表类型，可以从不同角度分析国家间的军费支出情况。折线图展示趋势变化，柱状图直观对比各年度支出，堆叠面积图显示累计情况，雷达图则提供多维度比较。
        </Typography>
      </Paper>
    </Box>
  );
};

export default Comparison; 