import React from 'react';
import { Typography, Paper, Box, Button, Card, CardContent, CardMedia } from '@mui/material';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  // 功能卡片数据
  const features = [
    {
      title: 'Dashboard',
      description: '全球军事数据概览，包括总体支出、前五国家等关键指标。',
      image: '/dashboard.jpg',
      path: '/dashboard'
    },
    {
      title: 'World Map',
      description: '通过交互式世界地图可视化全球军事力量分布。',
      image: '/map.jpg',
      path: '/map'
    },
    {
      title: 'Country Comparison',
      description: '比较不同国家的军事实力和军费支出数据。',
      image: '/comparison.jpg',
      path: '/comparison'
    },
    {
      title: 'Trend Analysis',
      description: '分析军事支出随时间的变化趋势。',
      image: '/trend.jpg',
      path: '/trend'
    }
  ];

  return (
    <Box sx={{ py: 4 }}>
      {/* 标题部分 */}
      <Paper elevation={0} sx={{ p: 4, mb: 4, bgcolor: '#f5f5f5', borderRadius: 2 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          世界军事力量可视化平台
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          探索1960-2024年间全球军事力量的变化和分布
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          size="large" 
          component={Link} 
          to="/dashboard"
          sx={{ mt: 2 }}
        >
          开始探索
        </Button>
      </Paper>

      {/* 数据来源部分 */}
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" gutterBottom>
          关于数据
        </Typography>
        <Typography variant="body1" paragraph>
          本平台的数据来源于斯德哥尔摩国际和平研究所(SIPRI)的军费开支数据库，包含173个国家从1949年至2023年的军事支出数据。
        </Typography>
        <Typography variant="body1">
          数据包括各国军费开支（以当地货币和美元计）、军费占GDP比例、人均军费开支等多个维度。
        </Typography>
      </Box>

      {/* 功能卡片部分 */}
      <Typography variant="h4" gutterBottom>
        主要功能
      </Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        {features.map((feature) => (
          <Box key={feature.title} sx={{ width: { xs: '100%', sm: '45%', md: '22%' }, mb: 3 }}>
            <Card 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                transition: '0.3s',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: 6
                }
              }}
            >
              <CardMedia
                component="div"
                sx={{
                  height: 140,
                  bgcolor: 'primary.light',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <Typography variant="h5" color="white">
                  {feature.title}
                </Typography>
              </CardMedia>
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
              <Box sx={{ p: 2 }}>
                <Button 
                  component={Link} 
                  to={feature.path} 
                  variant="outlined" 
                  size="small" 
                  fullWidth
                >
                  查看详情
                </Button>
              </Box>
            </Card>
          </Box>
        ))}
      </Box>
    </Box>
  );
};

export default Home; 