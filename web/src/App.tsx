import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import './App.css';

// 导入组件
import NavBar from './components/NavBar';

// 导入页面组件
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Map from './pages/Map';
// import Comparison from './pages/Comparison';
// import Trend from './pages/Trend';

// 创建一个主题
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <NavBar />
          <Container maxWidth="lg" style={{ marginTop: '2rem' }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/map" element={<Map />} />
              <Route path="/comparison" element={<div>Comparison (待实现)</div>} />
              <Route path="/trend" element={<div>Trend Analysis (待实现)</div>} />
              <Route path="*" element={<div>404 - Not Found</div>} />
            </Routes>
          </Container>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
