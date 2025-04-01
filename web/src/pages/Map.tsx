import React, { useState, useEffect } from 'react';
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
  SelectChangeEvent
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

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

  // 获取筛选后的数据
  const getFilteredData = (): CountryData[] => {
    if (selectedContinent === 'all') {
      return mapData;
    } else {
      return mapData.filter(country => country.Continent === selectedContinent);
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
                <MenuItem value="african">非洲</MenuItem>
                <MenuItem value="american">美洲</MenuItem>
                <MenuItem value="aisan">亚洲</MenuItem>
                <MenuItem value="europen">欧洲</MenuItem>
                <MenuItem value="easternasian">东亚</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>
      </Paper>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
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
                      { name: '非洲', color: getContinentColor('african') },
                      { name: '美洲', color: getContinentColor('american') },
                      { name: '亚洲', color: getContinentColor('aisan') },
                      { name: '欧洲', color: getContinentColor('europen') },
                      { name: '东亚', color: getContinentColor('easternasian') }
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