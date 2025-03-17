#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据分析模块
负责分析军事数据，计算统计指标和趋势
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from data.data_loader import DataLoader

class DataAnalyzer:
    """数据分析器类，负责分析军事数据"""
    
    def __init__(self, data_loader: DataLoader = None):
        """
        初始化数据分析器
        
        Args:
            data_loader: 数据加载器实例，如果为None则创建新实例
        """
        self.data_loader = data_loader if data_loader else DataLoader()
    
    def get_top_countries(self, year: int, top_n: int = 10) -> pd.DataFrame:
        """
        获取指定年份军费支出最高的国家
        
        Args:
            year: 年份
            top_n: 返回的国家数量
            
        Returns:
            包含前N个军费支出最高国家的DataFrame
        """
        all_data = self.data_loader.get_all_data()
        
        # 确保年份列存在
        if str(year) not in all_data.columns:
            raise ValueError(f"数据中不存在年份: {year}")
        
        # 选择国家列和指定年份列
        country_col = all_data.columns[0]
        year_data = all_data[[country_col, str(year)]].copy()
        
        # 删除缺失值
        year_data = year_data.dropna()
        
        # 确保数据类型为数值型
        year_data[str(year)] = pd.to_numeric(year_data[str(year)], errors='coerce')
        year_data = year_data.dropna()
        
        # 按军费支出降序排序
        year_data = year_data.sort_values(by=str(year), ascending=False)
        
        # 返回前N个国家
        return year_data.head(top_n)
    
    def calculate_growth_rate(self, country_name: str, start_year: int, end_year: int) -> float:
        """
        计算指定国家在给定时间段内的军费支出年均增长率
        
        Args:
            country_name: 国家名称
            start_year: 起始年份
            end_year: 结束年份
            
        Returns:
            年均增长率（百分比）
        """
        country_data = self.data_loader.get_country_data(country_name)
        
        # 确保年份列存在
        if str(start_year) not in country_data.columns or str(end_year) not in country_data.columns:
            raise ValueError(f"数据中不存在指定的年份范围: {start_year}-{end_year}")
        
        # 获取起始和结束年份的军费支出
        start_value = country_data[str(start_year)].values[0]
        end_value = country_data[str(end_year)].values[0]
        
        # 检查数据是否为缺失值
        if pd.isna(start_value) or pd.isna(end_value):
            raise ValueError(f"国家 {country_name} 在指定年份范围内存在缺失数据")
        
        # 计算年均增长率
        years = end_year - start_year
        if years <= 0:
            raise ValueError("结束年份必须大于起始年份")
            
        growth_rate = (end_value / start_value) ** (1 / years) - 1
        
        return growth_rate * 100  # 转换为百分比
    
    def compare_countries(self, countries: List[str], years: List[int]) -> pd.DataFrame:
        """
        比较多个国家在多个年份的军费支出
        
        Args:
            countries: 国家名称列表
            years: 年份列表
            
        Returns:
            包含多个国家在多个年份军费支出的DataFrame
        """
        all_data = self.data_loader.get_all_data()
        country_col = all_data.columns[0]
        
        # 过滤出指定的国家
        filtered_data = all_data[all_data[country_col].isin(countries)].copy()
        
        # 选择国家列和指定年份列
        year_cols = [str(year) for year in years if str(year) in filtered_data.columns]
        if not year_cols:
            raise ValueError("指定的年份在数据中不存在")
            
        return filtered_data[[country_col] + year_cols]
    
    def calculate_regional_total(self, continent: str, year: int) -> float:
        """
        计算特定大洲在指定年份的军费支出总和
        
        Args:
            continent: 大洲名称
            year: 年份
            
        Returns:
            军费支出总和
        """
        # 获取大洲数据
        continent_data = self.data_loader.get_continent_data(continent)
        
        # 确保年份列存在
        if str(year) not in continent_data.columns:
            raise ValueError(f"数据中不存在年份: {year}")
        
        # 确保数据类型为数值型
        continent_data[str(year)] = pd.to_numeric(continent_data[str(year)], errors='coerce')
        
        # 计算总和
        total = continent_data[str(year)].sum(skipna=True)
        
        return total
    
    def calculate_global_trend(self, start_year: int, end_year: int) -> pd.DataFrame:
        """
        计算全球军费支出趋势
        
        Args:
            start_year: 起始年份
            end_year: 结束年份
            
        Returns:
            包含全球军费支出趋势的DataFrame
        """
        all_data = self.data_loader.get_all_data()
        
        # 获取年份列
        year_cols = [str(year) for year in range(start_year, end_year + 1) if str(year) in all_data.columns]
        if not year_cols:
            raise ValueError("指定的年份范围在数据中不存在")
        
        # 计算每年的全球总和
        global_trend = {}
        for year in year_cols:
            global_trend[year] = all_data[year].sum(skipna=True)
        
        # 转换为DataFrame
        trend_df = pd.DataFrame(list(global_trend.items()), columns=['Year', 'Total Military Expenditure'])
        trend_df['Year'] = trend_df['Year'].astype(int)
        
        return trend_df.sort_values(by='Year') 