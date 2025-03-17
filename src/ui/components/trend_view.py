#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
趋势分析视图组件
显示军事数据的历史趋势
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from typing import Dict, List, Any, Callable
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.graph_objects as go

from data.data_loader import DataLoader
from data.data_analyzer import DataAnalyzer
from visualization.visualizer import Visualizer
from utils.helpers import figure_to_photoimage, save_figure, create_export_filename, plotly_to_image

class TrendView(ctk.CTkFrame):
    """趋势视图组件类"""
    
    def __init__(self, master, data_loader: DataLoader, data_analyzer: DataAnalyzer, 
                 visualizer: Visualizer, **kwargs):
        """
        初始化趋势视图
        
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
        
        # 创建视图内容
        self._create_widgets()
    
    def _create_widgets(self):
        """创建视图组件"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self, 
            text="军事力量趋势分析",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 20), padx=20, anchor="w")
        
        # 控制面板
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # 趋势类型选择
        self.trend_type_label = ctk.CTkLabel(
            self.control_frame, 
            text="趋势类型:",
            font=ctk.CTkFont(size=14)
        )
        self.trend_type_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        
        self.trend_type_var = tk.StringVar(value="全球趋势")
        self.trend_type_menu = ctk.CTkOptionMenu(
            self.control_frame,
            values=["全球趋势", "大洲趋势", "主要国家趋势"],
            variable=self.trend_type_var,
            command=self._on_trend_type_change,
            width=150
        )
        self.trend_type_menu.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # 年份范围选择
        self.year_range_label = ctk.CTkLabel(
            self.control_frame, 
            text="年份范围:",
            font=ctk.CTkFont(size=14)
        )
        self.year_range_label.pack(side=tk.LEFT, padx=(20, 10), pady=10)
        
        self.year_range_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.year_range_frame.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        self.start_year_var = tk.StringVar(value="2000")
        self.start_year_entry = ctk.CTkEntry(
            self.year_range_frame,
            width=60,
            textvariable=self.start_year_var
        )
        self.start_year_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        self.year_range_separator = ctk.CTkLabel(
            self.year_range_frame, 
            text="至",
            font=ctk.CTkFont(size=14)
        )
        self.year_range_separator.pack(side=tk.LEFT, padx=5)
        
        self.end_year_var = tk.StringVar(value="2022")
        self.end_year_entry = ctk.CTkEntry(
            self.year_range_frame,
            width=60,
            textvariable=self.end_year_var
        )
        self.end_year_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # 更新按钮
        self.update_button = ctk.CTkButton(
            self.control_frame,
            text="更新图表",
            command=self.update,
            width=100
        )
        self.update_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        # 图表容器
        self.chart_container = ctk.CTkFrame(self)
        self.chart_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 图表标签
        self.chart_label = ctk.CTkLabel(
            self.chart_container,
            text="选择趋势类型和年份范围后点击'更新图表'",
            font=ctk.CTkFont(size=16)
        )
        self.chart_label.pack(fill=tk.BOTH, expand=True)
        
        # 底部信息栏
        self.info_frame = ctk.CTkFrame(self, height=30)
        self.info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.info_label = ctk.CTkLabel(
            self.info_frame, 
            text="提示: 选择合适的年份范围以获得更好的趋势展示。",
            font=ctk.CTkFont(size=12)
        )
        self.info_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 保存按钮
        self.save_button = ctk.CTkButton(
            self.info_frame,
            text="保存图表",
            command=self._on_save_chart,
            width=100
        )
        self.save_button.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def update(self):
        """更新趋势图表"""
        try:
            # 获取趋势类型
            trend_type = self.trend_type_var.get()
            
            # 获取年份范围
            try:
                start_year = int(self.start_year_var.get())
                end_year = int(self.end_year_var.get())
                
                if start_year > end_year:
                    messagebox.showinfo("提示", "起始年份不能大于结束年份")
                    return
            except ValueError:
                messagebox.showinfo("提示", "请输入有效的年份")
                return
            
            # 更新图表
            self._update_chart(trend_type, start_year, end_year)
            
        except Exception as e:
            print(f"更新趋势图表时发生错误: {e}")
            messagebox.showerror("错误", f"更新趋势图表时发生错误: {str(e)}")
    
    def _update_chart(self, trend_type: str, start_year: int, end_year: int):
        """
        更新趋势图表
        
        Args:
            trend_type: 趋势类型
            start_year: 起始年份
            end_year: 结束年份
        """
        # 显示加载信息
        self.chart_label.configure(text="正在加载图表，请稍候...")
        self.update_idletasks()
        
        try:
            # 清除旧图表
            for widget in self.chart_container.winfo_children():
                if widget != self.chart_label:
                    widget.destroy()
            
            # 根据趋势类型选择不同的图表
            if trend_type == "全球趋势":
                self._create_global_trend_chart(start_year, end_year)
            elif trend_type == "大洲趋势":
                self._create_continent_trend_chart(start_year, end_year)
            elif trend_type == "主要国家趋势":
                self._create_major_countries_trend_chart(start_year, end_year)
            
        except Exception as e:
            print(f"生成趋势图表时发生错误: {e}")
            self.chart_label.configure(text=f"生成趋势图表时发生错误: {str(e)}")
    
    def _create_global_trend_chart(self, start_year: int, end_year: int):
        """
        创建全球趋势图表
        
        Args:
            start_year: 起始年份
            end_year: 结束年份
        """
        # 获取全球趋势数据
        global_trend = self.data_analyzer.calculate_global_trend(start_year, end_year)
        
        # 创建折线图
        fig = self.visualizer.create_line_chart(
            global_trend,
            'Year',
            ['Total Military Expenditure'],
            f"{start_year}-{end_year}年全球军费支出趋势",
            "年份",
            "军费支出 (百万美元)"
        )
        
        # 显示图表
        self.chart_label.pack_forget()
        
        chart_frame = FigureCanvasTkAgg(fig, self.chart_container)
        chart_frame.draw()
        chart_frame.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 缓存图表
        self.chart_cache['trend_chart'] = {
            'figure': fig,
            'canvas': chart_frame
        }
        
        # 更新信息
        self.info_label.configure(text=f"显示 {start_year}-{end_year} 年间的全球军费支出趋势")
    
    def _create_continent_trend_chart(self, start_year: int, end_year: int):
        """
        创建大洲趋势图表
        
        Args:
            start_year: 起始年份
            end_year: 结束年份
        """
        # 获取各大洲数据
        continents = ['african', 'american', 'aisan', 'europen', 'easternasian']
        continent_names = ['非洲', '美洲', '亚洲', '欧洲', '东亚']
        
        # 准备数据
        years = list(range(start_year, end_year + 1))
        trend_data = pd.DataFrame()
        trend_data['Year'] = years
        
        for continent, name in zip(continents, continent_names):
            values = []
            for year in years:
                try:
                    value = self.data_analyzer.calculate_regional_total(continent, year)
                    values.append(float(value))  # 确保值为浮点数
                except Exception as e:
                    print(f"获取{continent}在{year}年的数据时出错: {e}")
                    values.append(np.nan)
            trend_data[name] = values
        
        # 确保所有数据列都是数值类型
        for col in trend_data.columns:
            if col != 'Year':
                trend_data[col] = pd.to_numeric(trend_data[col], errors='coerce')
        
        # 创建堆叠面积图
        fig = self.visualizer.create_stacked_area_chart(
            trend_data,
            'Year',
            continent_names,
            f"{start_year}-{end_year}年各大洲军费支出趋势",
            "年份",
            "军费支出 (百万美元)"
        )
        
        # 将plotly图表转换为PIL图像
        chart_image = plotly_to_image(fig)
        
        # 调整图像大小以适应容器
        container_width = self.chart_container.winfo_width()
        container_height = self.chart_container.winfo_height()
        
        if container_width > 100 and container_height > 100:
            chart_image = chart_image.resize(
                (container_width, container_height),
                Image.LANCZOS
            )
        
        # 转换为PhotoImage
        chart_photo = ImageTk.PhotoImage(chart_image)
        
        # 显示图表
        self.chart_label.pack_forget()
        
        chart_label = ctk.CTkLabel(
            self.chart_container,
            text="",
            image=chart_photo
        )
        chart_label.pack(fill=tk.BOTH, expand=True)
        
        # 缓存图表
        self.chart_cache['trend_chart'] = {
            'figure': fig,
            'image': chart_image,
            'photo': chart_photo,
            'label': chart_label
        }
        
        # 更新信息
        self.info_label.configure(text=f"显示 {start_year}-{end_year} 年间的各大洲军费支出趋势")
    
    def _create_major_countries_trend_chart(self, start_year: int, end_year: int):
        """
        创建主要国家趋势图表
        
        Args:
            start_year: 起始年份
            end_year: 结束年份
        """
        # 选择主要国家
        major_countries = ["China", "United States", "Russia", "India", "Japan"]
        
        # 获取年份列表
        years = list(range(start_year, end_year + 1))
        
        # 获取比较数据
        try:
            comparison_data = self.data_analyzer.compare_countries(major_countries, years)
            
            # 准备折线图数据
            line_data = pd.DataFrame()
            line_data['Year'] = years
            
            for country in major_countries:
                country_data = comparison_data[comparison_data.iloc[:, 0] == country]
                if not country_data.empty:
                    for year in years:
                        if str(year) in country_data.columns:
                            try:
                                value = float(country_data[str(year)].values[0])  # 确保值为浮点数
                                line_data.loc[line_data['Year'] == year, country] = value
                            except (ValueError, TypeError) as e:
                                print(f"转换{country}在{year}年的数据时出错: {e}")
            
            # 确保所有数据列都是数值类型
            for col in line_data.columns:
                if col != 'Year':
                    line_data[col] = pd.to_numeric(line_data[col], errors='coerce')
            
            # 创建折线图
            fig = self.visualizer.create_line_chart(
                line_data,
                'Year',
                major_countries,
                f"{start_year}-{end_year}年主要国家军费支出趋势",
                "年份",
                "军费支出 (百万美元)"
            )
            
            # 显示图表
            self.chart_label.pack_forget()
            
            chart_frame = FigureCanvasTkAgg(fig, self.chart_container)
            chart_frame.draw()
            chart_frame.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 缓存图表
            self.chart_cache['trend_chart'] = {
                'figure': fig,
                'canvas': chart_frame
            }
            
            # 更新信息
            self.info_label.configure(text=f"显示 {start_year}-{end_year} 年间的主要国家军费支出趋势")
            
        except Exception as e:
            print(f"创建主要国家趋势图表时发生错误: {e}")
            self.chart_label.configure(text=f"创建主要国家趋势图表时发生错误: {str(e)}")
    
    def _on_trend_type_change(self, value):
        """
        趋势类型变化回调函数
        
        Args:
            value: 选中的趋势类型
        """
        # 根据趋势类型调整年份范围
        if value == "全球趋势":
            self.start_year_var.set("1960")
            self.end_year_var.set("2023")
        elif value == "大洲趋势":
            self.start_year_var.set("1980")
            self.end_year_var.set("2023")
        elif value == "主要国家趋势":
            self.start_year_var.set("1990")
            self.end_year_var.set("2023")
    
    def _on_save_chart(self):
        """保存图表处理函数"""
        if 'trend_chart' in self.chart_cache:
            # 创建文件名
            trend_type = self.trend_type_var.get()
            filename = create_export_filename(f"{trend_type.replace(' ', '_')}_trend", "png")
            
            # 选择保存路径
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG图像", "*.png"), ("PDF文档", "*.pdf"), ("SVG图像", "*.svg"), ("所有文件", "*.*")],
                title="保存趋势图表",
                initialfile=filename
            )
            
            if file_path:
                try:
                    # 保存图表
                    if 'figure' in self.chart_cache['trend_chart'] and 'canvas' in self.chart_cache['trend_chart']:
                        # Matplotlib图表
                        fig = self.chart_cache['trend_chart']['figure']
                        fig.savefig(file_path, dpi=300, bbox_inches='tight')
                    elif 'image' in self.chart_cache['trend_chart']:
                        # Plotly图表
                        self.chart_cache['trend_chart']['image'].save(file_path)
                    
                    messagebox.showinfo("保存成功", f"图表已成功保存到: {file_path}")
                except Exception as e:
                    messagebox.showerror("保存失败", f"保存图表时发生错误: {str(e)}")
        else:
            messagebox.showinfo("提示", "没有可保存的图表")
    
    def export_data(self):
        """导出数据"""
        try:
            # 获取趋势类型
            trend_type = self.trend_type_var.get()
            
            # 获取年份范围
            try:
                start_year = int(self.start_year_var.get())
                end_year = int(self.end_year_var.get())
            except ValueError:
                messagebox.showinfo("提示", "请输入有效的年份")
                return
            
            # 根据趋势类型导出不同的数据
            if trend_type == "全球趋势":
                # 获取全球趋势数据
                export_data = self.data_analyzer.calculate_global_trend(start_year, end_year)
            elif trend_type == "大洲趋势":
                # 获取各大洲数据
                continents = ['african', 'american', 'aisan', 'europen', 'easternasian']
                continent_names = ['非洲', '美洲', '亚洲', '欧洲', '东亚']
                
                # 准备数据
                years = list(range(start_year, end_year + 1))
                export_data = pd.DataFrame()
                export_data['Year'] = years
                
                for continent, name in zip(continents, continent_names):
                    values = []
                    for year in years:
                        try:
                            value = self.data_analyzer.calculate_regional_total(continent, year)
                            values.append(value)
                        except:
                            values.append(np.nan)
                    export_data[name] = values
            elif trend_type == "主要国家趋势":
                # 选择主要国家
                major_countries = ["China", "United States", "Russia", "India", "Japan"]
                
                # 获取年份列表
                years = list(range(start_year, end_year + 1))
                
                # 获取比较数据
                comparison_data = self.data_analyzer.compare_countries(major_countries, years)
                
                # 准备数据
                export_data = comparison_data
            
            # 导出到CSV
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
                title="导出趋势数据"
            )
            
            if file_path:
                export_data.to_csv(file_path, index=False)
                messagebox.showinfo("导出成功", f"数据已成功导出到: {file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出数据时发生错误: {str(e)}") 