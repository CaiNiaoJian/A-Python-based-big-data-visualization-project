#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
国家比较视图组件
比较不同国家的军事数据
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

from data.data_loader import DataLoader
from data.data_analyzer import DataAnalyzer
from visualization.visualizer import Visualizer
from utils.helpers import figure_to_photoimage, save_figure, create_export_filename

class ComparisonView(ctk.CTkFrame):
    """国家比较视图组件类"""
    
    def __init__(self, master, data_loader: DataLoader, data_analyzer: DataAnalyzer, 
                 visualizer: Visualizer, **kwargs):
        """
        初始化国家比较视图
        
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
            text="国家军事力量比较",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 20), padx=20, anchor="w")
        
        # 控制面板
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # 国家选择
        self.countries_label = ctk.CTkLabel(
            self.control_frame, 
            text="选择国家:",
            font=ctk.CTkFont(size=14)
        )
        self.countries_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        
        # 获取所有国家列表
        try:
            self.all_countries = self.data_loader.get_countries_list()
            # 默认选择一些主要国家
            default_countries = ["China", "United States", "Russia", "India", "Japan"]
            # 确保默认国家在列表中
            self.default_countries = [c for c in default_countries if c in self.all_countries]
            if not self.default_countries:
                self.default_countries = self.all_countries[:5]
        except:
            self.all_countries = ["China", "United States", "Russia", "India", "Japan", "Germany", "United Kingdom", "France"]
            self.default_countries = ["China", "United States", "Russia", "India", "Japan"]
        
        # 国家下拉多选框
        self.countries_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.countries_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=10)
        
        # 创建国家选择框
        self.country_vars = {}
        self.country_checkboxes = {}
        
        # 创建滚动框架
        self.countries_scrollable_frame = ctk.CTkScrollableFrame(
            self.countries_frame,
            width=400,
            height=100
        )
        self.countries_scrollable_frame.pack(fill=tk.X, expand=True)
        
        # 添加国家复选框
        for i, country in enumerate(self.all_countries):
            var = tk.BooleanVar(value=country in self.default_countries)
            checkbox = ctk.CTkCheckBox(
                self.countries_scrollable_frame,
                text=country,
                variable=var,
                command=self._on_country_change
            )
            checkbox.grid(row=i//3, column=i%3, padx=10, pady=5, sticky="w")
            self.country_vars[country] = var
            self.country_checkboxes[country] = checkbox
        
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
            text="选择国家和年份范围后点击'更新图表'",
            font=ctk.CTkFont(size=16)
        )
        self.chart_label.pack(fill=tk.BOTH, expand=True)
        
        # 底部信息栏
        self.info_frame = ctk.CTkFrame(self, height=30)
        self.info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.info_label = ctk.CTkLabel(
            self.info_frame, 
            text="提示: 选择2-5个国家进行比较效果最佳。",
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
        """更新比较图表"""
        try:
            # 获取选中的国家
            selected_countries = [
                country for country, var in self.country_vars.items() 
                if var.get()
            ]
            
            if not selected_countries:
                messagebox.showinfo("提示", "请至少选择一个国家")
                return
            
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
            self._update_chart(selected_countries, start_year, end_year)
            
        except Exception as e:
            print(f"更新比较图表时发生错误: {e}")
            messagebox.showerror("错误", f"更新比较图表时发生错误: {str(e)}")
    
    def _update_chart(self, countries: List[str], start_year: int, end_year: int):
        """
        更新比较图表
        
        Args:
            countries: 国家列表
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
            
            # 获取年份列表
            years = list(range(start_year, end_year + 1))
            
            # 获取比较数据
            comparison_data = self.data_analyzer.compare_countries(countries, years)
            
            # 准备折线图数据
            line_data = pd.DataFrame()
            line_data['Year'] = years
            
            for country in countries:
                country_data = comparison_data[comparison_data.iloc[:, 0] == country]
                if not country_data.empty:
                    for year in years:
                        if str(year) in country_data.columns:
                            value = country_data[str(year)].values[0]
                            line_data.loc[line_data['Year'] == year, country] = value
            
            # 创建折线图
            fig = self.visualizer.create_line_chart(
                line_data,
                'Year',
                countries,
                f"{start_year}-{end_year}年各国军费支出比较",
                "年份",
                "军费支出 (百万美元)"
            )
            
            # 显示图表
            self.chart_label.pack_forget()
            
            chart_frame = FigureCanvasTkAgg(fig, self.chart_container)
            chart_frame.draw()
            chart_frame.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 缓存图表
            self.chart_cache['line_chart'] = {
                'figure': fig,
                'canvas': chart_frame
            }
            
            # 更新信息
            self.info_label.configure(text=f"显示 {len(countries)} 个国家在 {start_year}-{end_year} 年间的军费支出比较")
            
        except Exception as e:
            print(f"生成比较图表时发生错误: {e}")
            self.chart_label.configure(text=f"生成比较图表时发生错误: {str(e)}")
    
    def _on_country_change(self):
        """国家选择变化回调函数"""
        # 获取选中的国家数量
        selected_count = sum(var.get() for var in self.country_vars.values())
        
        # 如果选中的国家太多，显示警告
        if selected_count > 10:
            self.info_label.configure(text="警告: 选择太多国家可能导致图表不易读。")
        else:
            self.info_label.configure(text=f"已选择 {selected_count} 个国家。")
    
    def _on_save_chart(self):
        """保存图表处理函数"""
        if 'line_chart' in self.chart_cache and 'figure' in self.chart_cache['line_chart']:
            # 创建文件名
            filename = create_export_filename("countries_comparison", "png")
            
            # 选择保存路径
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG图像", "*.png"), ("PDF文档", "*.pdf"), ("SVG图像", "*.svg"), ("所有文件", "*.*")],
                title="保存比较图表",
                initialfile=filename
            )
            
            if file_path:
                try:
                    # 保存图表
                    fig = self.chart_cache['line_chart']['figure']
                    fig.savefig(file_path, dpi=300, bbox_inches='tight')
                    messagebox.showinfo("保存成功", f"图表已成功保存到: {file_path}")
                except Exception as e:
                    messagebox.showerror("保存失败", f"保存图表时发生错误: {str(e)}")
        else:
            messagebox.showinfo("提示", "没有可保存的图表")
    
    def export_data(self):
        """导出数据"""
        try:
            # 获取选中的国家
            selected_countries = [
                country for country, var in self.country_vars.items() 
                if var.get()
            ]
            
            if not selected_countries:
                messagebox.showinfo("提示", "请至少选择一个国家")
                return
            
            # 获取年份范围
            try:
                start_year = int(self.start_year_var.get())
                end_year = int(self.end_year_var.get())
            except ValueError:
                messagebox.showinfo("提示", "请输入有效的年份")
                return
            
            # 获取比较数据
            years = list(range(start_year, end_year + 1))
            comparison_data = self.data_analyzer.compare_countries(selected_countries, years)
            
            # 导出到CSV
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
                title="导出国家比较数据"
            )
            
            if file_path:
                comparison_data.to_csv(file_path, index=False)
                messagebox.showinfo("导出成功", f"数据已成功导出到: {file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出数据时发生错误: {str(e)}") 