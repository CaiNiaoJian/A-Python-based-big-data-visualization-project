import React, { useState, useEffect } from 'react';
import { 
  Typography, 
  Box, 
  Paper, 
  CircularProgress, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel,
  SelectChangeEvent,
  Card,
  CardContent,
  Divider,
  useTheme
} from '@mui/material';
import axios from 'axios';

// 定义类型
interface CountryExpenditure {
  Country: string;
  Continent: string;
  Expenditure: number;
}

interface YearSummary {
  total_countries: number;
  file: string;
  total_expenditure: number;
}

interface YearsSummary {
  [key: string]: YearSummary;
}

const Dashboard: React.FC = () => {
  const theme = useTheme();
  
  // 状态
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedYear, setSelectedYear] = useState<number>(2022); // 默认最新年份
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [yearData, setYearData] = useState<CountryExpenditure[]>([]);
  const [yearsSummary, setYearsSummary] = useState<YearsSummary>({});
  
  // 格式化数字为易读形式，如1,234,567
  const formatNumber = (num: number): string => {
    return new Intl.NumberFormat('en-US').format(Math.round(num));
  };
  
  // 将数字转换为带有单位的字符串，如1.2M, 3.4B
  const formatCurrency = (num: number): string => {
    if (num >= 1_000_000_000) {
      return `${(num / 1_000_000_000).toFixed(1)}B`;
    } else if (num >= 1_000_000) {
      return `${(num / 1_000_000).toFixed(1)}M`;
    } else if (num >= 1_000) {
      return `${(num / 1_000).toFixed(1)}K`;
    } else {
      return num.toString();
    }
  };
  
  // 加载年份摘要数据
  useEffect(() => {
    const fetchYearsSummary = async () => {
      try {
        const response = await axios.get<YearsSummary>('/data/years_summary.json');
        setYearsSummary(response.data);
        
        // 提取可用年份并按降序排序（最新年份在前）
        const years = Object.keys(response.data)
          .map(year => parseInt(year))
          .sort((a, b) => b - a);
        
        setAvailableYears(years);
        
        // 默认选择最新年份
        if (years.length > 0 && !selectedYear) {
          setSelectedYear(years[0]);
        }
        
      } catch (err) {
        console.error('Error fetching years summary:', err);
        setError('无法加载年份数据。请稍后再试。');
      }
    };
    
    fetchYearsSummary();
  }, []);
  
  // 加载特定年份的数据
  useEffect(() => {
    if (selectedYear) {
      const fetchYearData = async () => {
        setLoading(true);
        try {
          const response = await axios.get<CountryExpenditure[]>(`/data/year_${selectedYear}.json`);
          setYearData(response.data);
          setError(null);
        } catch (err) {
          console.error(`Error fetching data for year ${selectedYear}:`, err);
          setError(`无法加载${selectedYear}年的数据。请稍后再试。`);
          setYearData([]);
        } finally {
          setLoading(false);
        }
      };
      
      fetchYearData();
    }
  }, [selectedYear]);
  
  // 处理年份切换
  const handleYearChange = (event: SelectChangeEvent<number>) => {
    setSelectedYear(event.target.value as number);
  };
  
  // 获取前N个军费支出最高的国家
  const getTopCountries = (count: number = 10): CountryExpenditure[] => {
    return [...yearData]
      .sort((a, b) => b.Expenditure - a.Expenditure)
      .slice(0, count);
  };
  
  // 获取军费支出占总支出的百分比
  const getPercentageOfTotal = (expenditure: number): number => {
    const total = yearsSummary[selectedYear.toString()]?.total_expenditure || 0;
    return total > 0 ? (expenditure / total) * 100 : 0;
  };
  
  // 计算按大洲的总军费开支
  const getExpenditureByContinent = (): {[key: string]: number} => {
    const continentTotals: {[key: string]: number} = {};
    
    yearData.forEach(country => {
      if (!continentTotals[country.Continent]) {
        continentTotals[country.Continent] = 0;
      }
      continentTotals[country.Continent] += country.Expenditure;
    });
    
    return continentTotals;
  };
  
  // 获取不同颜色的大洲
  const getContinentColor = (continent: string): string => {
    const colors: {[key: string]: string} = {
      'african': theme.palette.error.main,
      'american': theme.palette.primary.main,
      'aisan': theme.palette.warning.main,
      'europen': theme.palette.success.main,
      'easternasian': theme.palette.info.main
    };
    
    return colors[continent] || theme.palette.grey[500];
  };
  
  // 渲染主要指标卡片
  const renderStatsCard = (title: string, value: string, subValue?: string) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          {title}
        </Typography>
        <Typography variant="h3" component="div" sx={{ mb: 1 }}>
          {value}
        </Typography>
        {subValue && (
          <Typography variant="body2" color="text.secondary">
            {subValue}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
  
  // 渲染前五国家卡片
  const renderTopCountriesCard = () => {
    const topCountries = getTopCountries(5);
    
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            军费开支前五国家
          </Typography>
          <Box sx={{ mt: 2 }}>
            {topCountries.map((country, index) => (
              <Box key={country.Country} sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="body1" fontWeight="medium">
                    {index + 1}. {country.Country}
                  </Typography>
                  <Typography variant="body1" fontWeight="medium">
                    ${formatCurrency(country.Expenditure)}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Box 
                    sx={{ 
                      height: 6, 
                      width: `${getPercentageOfTotal(country.Expenditure)}%`, 
                      bgcolor: theme.palette.primary.main,
                      borderRadius: 1
                    }} 
                  />
                  <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                    {getPercentageOfTotal(country.Expenditure).toFixed(1)}%
                  </Typography>
                </Box>
              </Box>
            ))}
          </Box>
        </CardContent>
      </Card>
    );
  };
  
  // 渲染按大洲支出卡片
  const renderContinentCard = () => {
    const continentTotals = getExpenditureByContinent();
    const total = yearsSummary[selectedYear.toString()]?.total_expenditure || 0;
    
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            按大洲军费支出
          </Typography>
          <Box sx={{ mt: 2 }}>
            {Object.entries(continentTotals)
              .sort(([, a], [, b]) => b - a)  // 按支出降序排序
              .map(([continent, expenditure]) => (
                <Box key={continent} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body1" fontWeight="medium">
                      {continent.charAt(0).toUpperCase() + continent.slice(1)}
                    </Typography>
                    <Typography variant="body1" fontWeight="medium">
                      ${formatCurrency(expenditure)}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box 
                      sx={{ 
                        height: 6, 
                        width: `${total > 0 ? (expenditure / total) * 100 : 0}%`, 
                        bgcolor: getContinentColor(continent),
                        borderRadius: 1
                      }} 
                    />
                    <Typography variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                      {total > 0 ? ((expenditure / total) * 100).toFixed(1) : 0}%
                    </Typography>
                  </Box>
                </Box>
              ))}
          </Box>
        </CardContent>
      </Card>
    );
  };
  
  return (
    <Box sx={{ py: 4 }}>
      {/* 标题和年份选择 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          全球军事实力概览 {selectedYear}
        </Typography>
        
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel id="year-select-label">年份</InputLabel>
          <Select
            labelId="year-select-label"
            id="year-select"
            value={selectedYear}
            label="年份"
            onChange={handleYearChange}
          >
            {availableYears.map(year => (
              <MenuItem key={year} value={year}>{year}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      
      {/* 加载中状态 */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}
      
      {/* 错误状态 */}
      {error && (
        <Paper sx={{ p: 3, bgcolor: 'error.light', color: 'error.contrastText', my: 2 }}>
          <Typography>{error}</Typography>
        </Paper>
      )}
      
      {/* 主要内容 */}
      {!loading && !error && (
        <>
          {/* 主要指标 */}
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
            <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '30%' } }}>
              {renderStatsCard(
                '全球军费开支总额',
                `$${formatCurrency(yearsSummary[selectedYear.toString()]?.total_expenditure || 0)}`,
                '单位: 美元'
              )}
            </Box>
            <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '30%' } }}>
              {renderStatsCard(
                '有数据的国家数量',
                formatNumber(yearsSummary[selectedYear.toString()]?.total_countries || 0),
                '包含在统计中的国家'
              )}
            </Box>
            <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '30%' } }}>
              {renderStatsCard(
                '人均军费开支',
                `$${formatNumber(
                  yearData.length > 0 
                    ? (yearsSummary[selectedYear.toString()]?.total_expenditure || 0) / 
                      (yearsSummary[selectedYear.toString()]?.total_countries || 1) 
                    : 0
                )}`,
                '按国家平均计算'
              )}
            </Box>
          </Box>
          
          {/* 详细数据 */}
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
            <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '45%' } }}>
              {renderTopCountriesCard()}
            </Box>
            <Box sx={{ flex: 1, minWidth: { xs: '100%', md: '45%' } }}>
              {renderContinentCard()}
            </Box>
          </Box>
          
          {/* 数据说明 */}
          <Paper sx={{ p: 3, mt: 4, bgcolor: 'background.paper' }}>
            <Typography variant="body2" color="text.secondary">
              数据来源: 斯德哥尔摩国际和平研究所(SIPRI)军费开支数据库
            </Typography>
            <Typography variant="body2" color="text.secondary">
              注意: 实际军费开支可能高于公开数据，部分国家的数据可能不完整或缺失。
            </Typography>
          </Paper>
        </>
      )}
    </Box>
  );
};

export default Dashboard; 