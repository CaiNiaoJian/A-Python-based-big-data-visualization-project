import axios from 'axios';

// 设置基础URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 定义数据类型
export interface CountryData {
  country: string;
  expenditure: number;
  year: number;
}

export interface GlobalData {
  total: number;
  year: number;
  topCountries: {
    country: string;
    expenditure: number;
  }[];
}

export interface ComparisonData {
  country: string;
  years: {
    year: number;
    expenditure: number;
  }[];
}

// API服务
export const apiService = {
  // 获取全球军费数据
  getGlobalData: async (year: number): Promise<GlobalData> => {
    try {
      // TODO: 连接真实API
      // const response = await api.get(`/global/${year}`);
      // return response.data;
      
      // 模拟数据
      return {
        total: 2113000,
        year,
        topCountries: [
          { country: 'United States', expenditure: 877000 },
          { country: 'China', expenditure: 292000 },
          { country: 'Russia', expenditure: 86400 },
          { country: 'UK', expenditure: 68500 },
          { country: 'India', expenditure: 83000 }
        ]
      };
    } catch (error) {
      console.error('Error fetching global data:', error);
      throw error;
    }
  },

  // 获取世界地图数据
  getMapData: async (year: number): Promise<CountryData[]> => {
    try {
      // TODO: 连接真实API
      // const response = await api.get(`/map/${year}`);
      // return response.data;
      
      // 模拟数据
      return [
        { country: 'United States', expenditure: 877000, year },
        { country: 'China', expenditure: 292000, year },
        { country: 'Russia', expenditure: 86400, year },
        { country: 'UK', expenditure: 68500, year },
        { country: 'India', expenditure: 83000, year },
        { country: 'France', expenditure: 55300, year },
        { country: 'Germany', expenditure: 56000, year },
        { country: 'Japan', expenditure: 49400, year }
      ];
    } catch (error) {
      console.error('Error fetching map data:', error);
      throw error;
    }
  },

  // 获取国家比较数据
  getComparisonData: async (countries: string[], startYear: number, endYear: number): Promise<ComparisonData[]> => {
    try {
      // TODO: 连接真实API
      // const response = await api.get('/comparison', {
      //   params: { countries: countries.join(','), startYear, endYear }
      // });
      // return response.data;
      
      // 模拟数据
      return countries.map(country => ({
        country,
        years: Array.from({ length: endYear - startYear + 1 }, (_, index) => ({
          year: startYear + index,
          expenditure: Math.floor(Math.random() * 500000) + 50000
        }))
      }));
    } catch (error) {
      console.error('Error fetching comparison data:', error);
      throw error;
    }
  },

  // 获取趋势数据
  getTrendData: async (startYear: number, endYear: number): Promise<{ year: number; expenditure: number }[]> => {
    try {
      // TODO: 连接真实API
      // const response = await api.get('/trend', {
      //   params: { startYear, endYear }
      // });
      // return response.data;
      
      // 模拟数据
      return Array.from({ length: endYear - startYear + 1 }, (_, index) => ({
        year: startYear + index,
        expenditure: Math.floor(Math.random() * 2000000) + 1000000
      }));
    } catch (error) {
      console.error('Error fetching trend data:', error);
      throw error;
    }
  }
};

export default api; 