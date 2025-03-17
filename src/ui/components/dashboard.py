#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
仪表盘视图组件
显示军事数据的概览信息
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from typing import Dict, List, Any, Callable
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
from PIL import Image, ImageTk

from data.data_loader import DataLoader
from data.data_analyzer import DataAnalyzer
from visualization.visualizer import Visualizer, APPLE_COLORS
from utils.helpers import figure_to_photoimage, format_number

class Dashboard(ctk.CTkFrame):
    """仪表盘视图组件类"""
    
    def __init__(self, master, data_loader: DataLoader, data_analyzer: DataAnalyzer, 
                 visualizer: Visualizer, **kwargs):
        """
        初始化仪表盘视图
        
        Args:
            master: 父组件
            data_loader: 数据加载器
            data_analyzer: 数据分析器
            visualizer: 可视化器
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        
        self.data_loader = data_loader
        self.data_analyzer = data_analyzer
        self.visualizer = visualizer
        
        # 图表缓存
        self.chart_cache = {}
        
        # 创建仪表盘内容
        self._create_widgets()
        
        # 加载数据
        self.update()
    
    def _create_widgets(self):
        """创建仪表盘组件"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self, 
            text="军事力量数据仪表盘",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 20), padx=20, anchor="w")
        
        # 年份选择框架
        self.year_frame = ctk.CTkFrame(self)
        self.year_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.year_label = ctk.CTkLabel(
            self.year_frame, 
            text="选择年份:",
            font=ctk.CTkFont(size=14)
        )
        self.year_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        
        # 使用2022年作为默认年份
        self.year_var = tk.StringVar(value="2022")
        self.year_menu = ctk.CTkOptionMenu(
            self.year_frame,
            values=["2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2010", "2005", "2000", "1995", "1990", "1985", "1980", "1975", "1970", "1965", "1960"],
            variable=self.year_var,
            command=self._on_year_change,
            width=100
        )
        self.year_menu.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # 创建主内容区域（两列布局）
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 左侧列 - 统计卡片
        self.left_column = ctk.CTkFrame(self.content_frame)
        self.left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=0)
        
        # 右侧列 - 图表
        self.right_column = ctk.CTkFrame(self.content_frame)
        self.right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=0)
        
        # 创建统计卡片
        self._create_stat_cards()
        
        # 创建图表区域
        self._create_chart_areas()
    
    def _create_stat_cards(self):
        """创建统计卡片"""
        # 全球军费支出卡片
        self.global_card = StatCard(
            self.left_column,
            title="全球军费支出",
            icon=None,
            value="加载中...",
            unit="百万美元",
            trend="+2.3%",
            trend_up=True
        )
        self.global_card.pack(fill=tk.X, padx=10, pady=10)
        
        # 前五国家卡片
        self.top5_card = TopCountriesCard(
            self.left_column,
            title="军费支出前五国家",
            data=[]
        )
        self.top5_card.pack(fill=tk.X, padx=10, pady=10)
        
        # 大洲分布卡片
        self.continent_card = StatCard(
            self.left_column,
            title="亚洲军费支出",
            icon=None,
            value="加载中...",
            unit="百万美元",
            trend="+3.5%",
            trend_up=True
        )
        self.continent_card.pack(fill=tk.X, padx=10, pady=10)
    
    def _create_chart_areas(self):
        """创建图表区域"""
        # 顶部图表 - 柱状图
        self.top_chart_frame = ctk.CTkFrame(self.right_column)
        self.top_chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        self.top_chart_label = ctk.CTkLabel(
            self.top_chart_frame, 
            text="军费支出前10国家",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.top_chart_label.pack(pady=(10, 0), padx=10, anchor="w")
        
        self.top_chart_canvas = ctk.CTkFrame(self.top_chart_frame)
        self.top_chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 底部图表 - 饼图
        self.bottom_chart_frame = ctk.CTkFrame(self.right_column)
        self.bottom_chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        self.bottom_chart_label = ctk.CTkLabel(
            self.bottom_chart_frame, 
            text="各大洲军费支出占比",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.bottom_chart_label.pack(pady=(10, 0), padx=10, anchor="w")
        
        self.bottom_chart_canvas = ctk.CTkFrame(self.bottom_chart_frame)
        self.bottom_chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update(self):
        """更新仪表盘数据"""
        try:
            # 获取选中的年份
            year = int(self.year_var.get())
            
            # 更新全球军费支出
            self._update_global_stat(year)
            
            # 更新前五国家
            self._update_top_countries(year)
            
            # 更新大洲分布
            self._update_continent_stat(year)
            
            # 更新图表
            self._update_charts(year)
            
        except Exception as e:
            print(f"更新仪表盘时发生错误: {e}")
    
    def _update_global_stat(self, year: int):
        """
        更新全球军费支出统计
        
        Args:
            year: 年份
        """
        try:
            # 获取全球军费支出
            all_data = self.data_loader.get_all_data()
            global_expenditure = all_data[str(year)].sum(skipna=True)
            
            # 计算同比增长率
            if str(year-1) in all_data.columns:
                prev_expenditure = all_data[str(year-1)].sum(skipna=True)
                growth_rate = (global_expenditure / prev_expenditure - 1) * 100
                trend_up = growth_rate > 0
            else:
                growth_rate = 0
                trend_up = True
            
            # 更新卡片
            self.global_card.update_value(
                format_number(global_expenditure, 1),
                f"{growth_rate:.1f}%",
                trend_up
            )
        except Exception as e:
            print(f"更新全球军费支出时发生错误: {e}")
    
    def _update_top_countries(self, year: int):
        """
        更新前五国家统计
        
        Args:
            year: 年份
        """
        try:
            # 获取前五国家
            top_countries = self.data_analyzer.get_top_countries(year, 5)
            
            # 准备数据
            data = []
            for i, (country, value) in enumerate(zip(top_countries.iloc[:, 0], top_countries.iloc[:, 1])):
                data.append({
                    "rank": i + 1,
                    "country": country,
                    "value": format_number(value, 1)
                })
            
            # 更新卡片
            self.top5_card.update_data(data)
        except Exception as e:
            print(f"更新前五国家时发生错误: {e}")
    
    def _update_continent_stat(self, year: int):
        """
        更新大洲分布统计
        
        Args:
            year: 年份
        """
        try:
            # 获取亚洲军费支出
            asia_expenditure = self.data_analyzer.calculate_regional_total('aisan', year)
            
            # 计算同比增长率
            try:
                prev_asia_expenditure = self.data_analyzer.calculate_regional_total('aisan', year-1)
                growth_rate = (asia_expenditure / prev_asia_expenditure - 1) * 100
                trend_up = growth_rate > 0
            except:
                growth_rate = 0
                trend_up = True
            
            # 更新卡片
            self.continent_card.update_value(
                format_number(asia_expenditure, 1),
                f"{growth_rate:.1f}%",
                trend_up
            )
        except Exception as e:
            print(f"更新大洲分布时发生错误: {e}")
    
    def _update_charts(self, year: int):
        """
        更新图表
        
        Args:
            year: 年份
        """
        # 更新柱状图
        self._update_bar_chart(year)
        
        # 更新饼图
        self._update_pie_chart(year)
    
    def _update_bar_chart(self, year: int):
        """
        更新柱状图
        
        Args:
            year: 年份
        """
        try:
            # 清除旧图表
            for widget in self.top_chart_canvas.winfo_children():
                widget.destroy()
            
            # 获取前10国家
            top_countries = self.data_analyzer.get_top_countries(year, 10)
            
            # 创建柱状图
            fig = self.visualizer.create_bar_chart(
                top_countries,
                top_countries.columns[0],
                str(year),
                f"{year}年军费支出前10国家",
                "国家",
                "军费支出 (百万美元)"
            )
            
            # 显示图表
            chart_frame = FigureCanvasTkAgg(fig, self.top_chart_canvas)
            chart_frame.draw()
            chart_frame.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 缓存图表
            self.chart_cache['bar_chart'] = chart_frame
        except Exception as e:
            print(f"更新柱状图时发生错误: {e}")
    
    def _update_pie_chart(self, year: int):
        """
        更新饼图
        
        Args:
            year: 年份
        """
        try:
            # 清除旧图表
            for widget in self.bottom_chart_canvas.winfo_children():
                widget.destroy()
            
            # 获取各大洲数据
            continents = ['african', 'american', 'aisan', 'europen', 'easternasian']
            continent_names = ['非洲', '美洲', '亚洲', '欧洲', '东亚']
            
            # 计算各大洲军费支出
            expenditures = []
            for continent in continents:
                try:
                    expenditure = self.data_analyzer.calculate_regional_total(continent, year)
                    expenditures.append(expenditure)
                except:
                    expenditures.append(0)
            
            # 创建数据框
            pie_data = pd.DataFrame({
                'Continent': continent_names,
                'Expenditure': expenditures
            })
            
            # 创建饼图
            fig = self.visualizer.create_pie_chart(
                pie_data,
                'Expenditure',
                'Continent',
                f"{year}年各大洲军费支出占比"
            )
            
            # 显示图表
            chart_frame = FigureCanvasTkAgg(fig, self.bottom_chart_canvas)
            chart_frame.draw()
            chart_frame.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 缓存图表
            self.chart_cache['pie_chart'] = chart_frame
        except Exception as e:
            print(f"更新饼图时发生错误: {e}")
    
    def _on_year_change(self, value):
        """
        年份变化回调函数
        
        Args:
            value: 选中的年份
        """
        self.update()
    
    def export_data(self):
        """导出数据"""
        # 获取选中的年份
        year = int(self.year_var.get())
        
        # 获取前10国家
        top_countries = self.data_analyzer.get_top_countries(year, 10)
        
        # 导出到CSV
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
            title="导出前10国家军费支出数据"
        )
        
        if file_path:
            top_countries.to_csv(file_path, index=False)
            messagebox.showinfo("导出成功", f"数据已成功导出到: {file_path}")


class StatCard(ctk.CTkFrame):
    """统计卡片组件类"""
    
    def __init__(self, master, title: str, icon: Any = None, value: str = "0", 
                 unit: str = "", trend: str = "0%", trend_up: bool = True, **kwargs):
        """
        初始化统计卡片
        
        Args:
            master: 父组件
            title: 卡片标题
            icon: 图标
            value: 统计值
            unit: 单位
            trend: 趋势值
            trend_up: 趋势是否上升
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        
        # 设置圆角和阴影
        self.configure(corner_radius=10, fg_color=("white", "gray25"))
        
        # 创建卡片内容
        self._create_widgets(title, icon, value, unit, trend, trend_up)
    
    def _create_widgets(self, title: str, icon: Any, value: str, unit: str, trend: str, trend_up: bool):
        """创建卡片组件"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self, 
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(pady=(15, 5), padx=15, anchor="w")
        
        # 值
        self.value_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.value_frame.pack(fill=tk.X, padx=15, pady=(5, 5))
        
        self.value_label = ctk.CTkLabel(
            self.value_frame, 
            text=value,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.value_label.pack(side=tk.LEFT)
        
        self.unit_label = ctk.CTkLabel(
            self.value_frame, 
            text=unit,
            font=ctk.CTkFont(size=12)
        )
        self.unit_label.pack(side=tk.LEFT, padx=(5, 0), anchor="s")
        
        # 趋势
        self.trend_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.trend_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        trend_color = APPLE_COLORS['green'] if trend_up else APPLE_COLORS['red']
        trend_prefix = "↑ " if trend_up else "↓ "
        
        self.trend_label = ctk.CTkLabel(
            self.trend_frame, 
            text=trend_prefix + trend,
            text_color=trend_color,
            font=ctk.CTkFont(size=12)
        )
        self.trend_label.pack(side=tk.LEFT)
        
        self.trend_text = ctk.CTkLabel(
            self.trend_frame, 
            text="相比去年",
            font=ctk.CTkFont(size=12)
        )
        self.trend_text.pack(side=tk.LEFT, padx=(5, 0))
    
    def update_value(self, value: str, trend: str, trend_up: bool):
        """
        更新卡片值
        
        Args:
            value: 新的统计值
            trend: 新的趋势值
            trend_up: 趋势是否上升
        """
        self.value_label.configure(text=value)
        
        trend_color = APPLE_COLORS['green'] if trend_up else APPLE_COLORS['red']
        trend_prefix = "↑ " if trend_up else "↓ "
        
        self.trend_label.configure(
            text=trend_prefix + trend,
            text_color=trend_color
        )


class TopCountriesCard(ctk.CTkFrame):
    """前五国家卡片组件类"""
    
    def __init__(self, master, title: str, data: List[Dict[str, Any]], **kwargs):
        """
        初始化前五国家卡片
        
        Args:
            master: 父组件
            title: 卡片标题
            data: 国家数据列表
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        
        # 设置圆角和阴影
        self.configure(corner_radius=10, fg_color=("white", "gray25"))
        
        # 创建卡片内容
        self._create_widgets(title, data)
    
    def _create_widgets(self, title: str, data: List[Dict[str, Any]]):
        """创建卡片组件"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self, 
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(pady=(15, 10), padx=15, anchor="w")
        
        # 国家列表
        self.countries_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.countries_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # 创建国家项
        self.country_items = []
        for i in range(5):
            item = self._create_country_item(i + 1, "加载中...", "0")
            item.pack(fill=tk.X, pady=(0, 5))
            self.country_items.append(item)
        
        # 更新数据
        self.update_data(data)
    
    def _create_country_item(self, rank: int, country: str, value: str) -> ctk.CTkFrame:
        """
        创建国家项
        
        Args:
            rank: 排名
            country: 国家名称
            value: 军费支出值
            
        Returns:
            国家项框架
        """
        item = ctk.CTkFrame(self.countries_frame, fg_color="transparent")
        
        # 排名
        rank_label = ctk.CTkLabel(
            item, 
            text=f"{rank}",
            width=25,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        rank_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 国家名称
        country_label = ctk.CTkLabel(
            item, 
            text=country,
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        country_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 军费支出值
        value_label = ctk.CTkLabel(
            item, 
            text=value,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        value_label.pack(side=tk.RIGHT)
        
        # 保存标签引用
        item.rank_label = rank_label
        item.country_label = country_label
        item.value_label = value_label
        
        return item
    
    def update_data(self, data: List[Dict[str, Any]]):
        """
        更新国家数据
        
        Args:
            data: 国家数据列表
        """
        # 确保数据长度不超过项数
        data = data[:len(self.country_items)]
        
        # 更新现有数据
        for i, item in enumerate(self.country_items):
            if i < len(data):
                item.country_label.configure(text=data[i]["country"])
                item.value_label.configure(text=data[i]["value"])
            else:
                item.country_label.configure(text="--")
                item.value_label.configure(text="--") 