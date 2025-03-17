#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据加载模块
负责从Excel文件中读取军事数据
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple

class DataLoader:
    """数据加载器类，负责读取和处理军事数据"""
    
    def __init__(self, data_dir: str = None):
        """
        初始化数据加载器
        
        Args:
            data_dir: 数据目录路径，默认为项目根目录下的rbdata
        """
        if data_dir is None:
            # 获取项目根目录
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.data_dir = os.path.join(root_dir, 'rbdata')
        else:
            self.data_dir = data_dir
            
        # 数据缓存
        self._data_cache = {}
        self._continents = ['african', 'american', 'aisan', 'europen', 'easternasian']
        
        # 设置默认年份范围（1960-2022）
        self._default_years = list(range(1960, 2023))
        
    def get_continent_data(self, continent: str) -> pd.DataFrame:
        """
        获取特定大洲的数据
        
        Args:
            continent: 大洲名称，可选值为'african', 'american', 'aisan', 'europen', 'easternasian'
            
        Returns:
            包含该大洲所有国家军事数据的DataFrame
        """
        if continent not in self._continents:
            raise ValueError(f"不支持的大洲: {continent}，可选值为: {', '.join(self._continents)}")
            
        # 检查缓存
        if continent in self._data_cache:
            return self._data_cache[continent]
            
        # 读取数据
        file_path = os.path.join(self.data_dir, f"{continent}.xlsx")
        df = pd.read_excel(file_path, header=None)  # 指定没有表头
        
        # 手动设置列名
        # 第一列是国家名称，后面的列是费用数据
        # 由于没有年份标签，我们使用默认年份范围作为列名
        column_names = ['Country']
        for i in range(1, len(df.columns)):
            # 确保年份索引不超出范围
            year_idx = i - 1
            if year_idx < len(self._default_years):
                column_names.append(str(self._default_years[year_idx]))
            else:
                # 如果列数超过预设年份数，使用索引作为列名
                column_names.append(f"Column_{i}")
        
        df.columns = column_names
        
        # 处理缺失值
        df.replace("...", np.nan, inplace=True)
        df.replace("xx", np.nan, inplace=True)
        
        # 将年份列的数据转换为数值类型
        for col in df.columns[1:]:
            if str(col).isdigit():
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 缓存数据
        self._data_cache[continent] = df
        
        return df
    
    def get_all_data(self) -> pd.DataFrame:
        """
        获取所有大洲的数据并合并
        
        Returns:
            包含所有国家军事数据的DataFrame
        """
        # 尝试直接读取合并后的数据文件
        try:
            file_path = os.path.join(self.data_dir, "current_data.xlsx")
            df = pd.read_excel(file_path, header=None)  # 指定没有表头
            
            # 手动设置列名
            column_names = ['Country']
            for i in range(1, len(df.columns)):
                year_idx = i - 1
                if year_idx < len(self._default_years):
                    column_names.append(str(self._default_years[year_idx]))
                else:
                    column_names.append(f"Column_{i}")
            
            df.columns = column_names
            
            # 处理缺失值
            df.replace("...", np.nan, inplace=True)
            df.replace("xx", np.nan, inplace=True)
            
            # 将年份列的数据转换为数值类型
            for col in df.columns[1:]:
                if str(col).isdigit():
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
        except Exception as e:
            print(f"读取合并数据文件失败: {e}，尝试合并各大洲数据...")
        
        # 合并各大洲数据
        dfs = []
        for continent in self._continents:
            dfs.append(self.get_continent_data(continent))
        
        return pd.concat(dfs, ignore_index=True)
    
    def get_country_data(self, country_name: str) -> pd.DataFrame:
        """
        获取特定国家的数据
        
        Args:
            country_name: 国家名称
            
        Returns:
            包含该国家军事数据的DataFrame行
        """
        all_data = self.get_all_data()
        country_data = all_data[all_data.iloc[:, 0] == country_name]
        
        if country_data.empty:
            raise ValueError(f"未找到国家: {country_name}")
            
        return country_data
    
    def get_countries_list(self) -> List[str]:
        """
        获取所有国家的列表
        
        Returns:
            所有国家名称的列表
        """
        all_data = self.get_all_data()
        return all_data.iloc[:, 0].unique().tolist()
    
    def get_years_list(self) -> List[int]:
        """
        获取所有年份的列表
        
        Returns:
            所有年份的列表
        """
        all_data = self.get_all_data()
        # 返回除第一列外的所有列名（应该是年份）
        years = []
        for col in all_data.columns[1:]:
            if str(col).isdigit():
                years.append(int(col))
        return years
    
    def get_data_by_year_range(self, start_year: int, end_year: int) -> pd.DataFrame:
        """
        获取特定年份范围的数据
        
        Args:
            start_year: 起始年份
            end_year: 结束年份
            
        Returns:
            包含指定年份范围数据的DataFrame
        """
        all_data = self.get_all_data()
        
        # 获取年份列
        year_cols = [col for col in all_data.columns if str(col).isdigit() and int(col) >= start_year and int(col) <= end_year]
        
        # 如果没有找到年份列，返回空DataFrame
        if not year_cols:
            return pd.DataFrame()
            
        # 返回国家列和年份列
        return all_data.loc[:, [all_data.columns[0]] + year_cols] 