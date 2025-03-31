import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';

const NavBar: React.FC = () => {
  const location = useLocation();
  
  // 导航链接数据
  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/map', label: 'World Map' },
    { path: '/comparison', label: 'Comparison' },
    { path: '/trend', label: 'Trend Analysis' }
  ];

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Military Power Visualization
        </Typography>
        <Box sx={{ display: 'flex' }}>
          {navLinks.map((link) => (
            <Button
              key={link.path}
              component={Link}
              to={link.path}
              color="inherit"
              sx={{
                fontWeight: location.pathname === link.path ? 'bold' : 'normal',
                borderBottom: location.pathname === link.path ? '2px solid white' : 'none',
                borderRadius: 0,
                mx: 1
              }}
            >
              {link.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar; 