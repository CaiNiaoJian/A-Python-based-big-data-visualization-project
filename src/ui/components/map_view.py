#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
世界地图视图组件
显示世界各国军事数据的地图可视化
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from typing import Dict, List, Any, Callable
import pandas as pd
import numpy as np
import os
import io
import webbrowser
from PIL import Image, ImageTk

from data.data_loader import DataLoader
from data.data_analyzer import DataAnalyzer
from visualization.visualizer import Visualizer
from utils.helpers import plotly_to_image, create_export_filename

class MapView(ctk.CTkFrame):
    """世界地图视图组件类"""
    
    def __init__(self, master, data_loader: DataLoader, data_analyzer: DataAnalyzer, 
                 visualizer: Visualizer, **kwargs):
        """
        初始化世界地图视图
        
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
        self.map_image = None
        self.map_photo = None
        
        # 创建视图内容
        self._create_widgets()
    
    def _create_widgets(self):
        """创建视图组件"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self, 
            text="世界军事力量地图",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 20), padx=20, anchor="w")
        
        # 控制面板
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # 年份选择
        self.year_label = ctk.CTkLabel(
            self.control_frame, 
            text="选择年份:",
            font=ctk.CTkFont(size=14)
        )
        self.year_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        
        self.year_var = tk.StringVar(value="2022")
        self.year_menu = ctk.CTkOptionMenu(
            self.control_frame,
            values=["2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2010", "2005", "2000", "1995", "1990", "1985", "1980", "1975", "1970", "1965", "1960"],
            variable=self.year_var,
            command=self._on_year_change,
            width=100
        )
        self.year_menu.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # 视图类型选择
        self.view_type_label = ctk.CTkLabel(
            self.control_frame, 
            text="视图类型:",
            font=ctk.CTkFont(size=14)
        )
        self.view_type_label.pack(side=tk.LEFT, padx=(20, 10), pady=10)
        
        self.view_type_var = tk.StringVar(value="军费支出")
        self.view_type_menu = ctk.CTkOptionMenu(
            self.control_frame,
            values=["军费支出", "军费占GDP比例", "人均军费支出"],
            variable=self.view_type_var,
            command=self._on_view_type_change,
            width=150
        )
        self.view_type_menu.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # 保存按钮
        self.save_button = ctk.CTkButton(
            self.control_frame,
            text="保存地图",
            command=self._on_save_map,
            width=100
        )
        self.save_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        # 地图容器
        self.map_container = ctk.CTkFrame(self)
        self.map_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 地图标签
        self.map_label = ctk.CTkLabel(
            self.map_container,
            text="加载中...",
            font=ctk.CTkFont(size=16)
        )
        self.map_label.pack(fill=tk.BOTH, expand=True)
        
        # 底部信息栏
        self.info_frame = ctk.CTkFrame(self, height=30)
        self.info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.info_label = ctk.CTkLabel(
            self.info_frame, 
            text="提示: 地图加载可能需要一些时间，请耐心等待。",
            font=ctk.CTkFont(size=12)
        )
        self.info_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 加载初始地图
        self.update()
    
    def update(self):
        """更新地图数据"""
        try:
            # 获取选中的年份和视图类型
            year = int(self.year_var.get())
            view_type = self.view_type_var.get()
            
            # 更新地图
            self._update_map(year, view_type)
            
        except Exception as e:
            print(f"更新地图时发生错误: {e}")
            messagebox.showerror("错误", f"更新地图时发生错误: {str(e)}")
    
    def _update_map(self, year: int, view_type: str):
        """
        更新地图
        
        Args:
            year: 年份
            view_type: 视图类型
        """
        # 显示加载信息
        self.map_label.configure(text="正在加载地图，请稍候...")
        self.update_idletasks()
        
        try:
            # 获取数据
            all_data = self.data_loader.get_all_data()
            
            # 选择国家列和指定年份列
            country_col = all_data.columns[0]
            
            # 根据视图类型选择数据
            if view_type == "军费支出":
                value_col = str(year)
                title = f"{year}年世界各国军费支出"
            elif view_type == "军费占GDP比例":
                # 这里假设我们有GDP数据，实际应用中需要加载真实数据
                # 这里简化处理，随机生成一些比例数据
                all_data['GDP_Ratio'] = all_data[str(year)].astype(float) / np.random.uniform(100, 1000, len(all_data))
                value_col = 'GDP_Ratio'
                title = f"{year}年世界各国军费占GDP比例"
            elif view_type == "人均军费支出":
                # 这里假设我们有人口数据，实际应用中需要加载真实数据
                # 这里简化处理，随机生成一些人均数据
                all_data['Per_Capita'] = all_data[str(year)].astype(float) / np.random.uniform(1, 100, len(all_data))
                value_col = 'Per_Capita'
                title = f"{year}年世界各国人均军费支出"
            
            # 过滤掉缺失值
            map_data = all_data[[country_col, value_col]].dropna()
            
            # 创建地图
            fig = self.visualizer.create_map_chart(
                map_data,
                country_col,
                value_col,
                title
            )
            
            # 将plotly图表转换为PIL图像
            self.map_image = plotly_to_image(fig)
            
            # 调整图像大小以适应容器
            container_width = self.map_container.winfo_width()
            container_height = self.map_container.winfo_height()
            
            if container_width > 100 and container_height > 100:
                self.map_image = self.map_image.resize(
                    (container_width, container_height),
                    Image.LANCZOS
                )
            
            # 转换为PhotoImage
            self.map_photo = ImageTk.PhotoImage(self.map_image)
            
            # 更新地图标签
            self.map_label.configure(text="", image=self.map_photo)
            
            # 更新信息
            self.info_label.configure(text=f"显示 {len(map_data)} 个国家的数据")
            
        except Exception as e:
            print(f"生成地图时发生错误: {e}")
            self.map_label.configure(text=f"生成地图时发生错误: {str(e)}")
    
    def _on_year_change(self, value):
        """
        年份变化回调函数
        
        Args:
            value: 选中的年份
        """
        self.update()
    
    def _on_view_type_change(self, value):
        """
        视图类型变化回调函数
        
        Args:
            value: 选中的视图类型
        """
        self.update()
    
    def _on_save_map(self):
        """保存地图处理函数"""
        if self.map_image:
            # 创建文件名
            filename = create_export_filename("world_map", "png")
            
            # 选择保存路径
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG图像", "*.png"), ("所有文件", "*.*")],
                title="保存地图图像",
                initialfile=filename
            )
            
            if file_path:
                try:
                    # 保存图像
                    self.map_image.save(file_path)
                    messagebox.showinfo("保存成功", f"地图已成功保存到: {file_path}")
                except Exception as e:
                    messagebox.showerror("保存失败", f"保存地图时发生错误: {str(e)}")
        else:
            messagebox.showinfo("提示", "没有可保存的地图")
    
    def export_data(self):
        """导出数据"""
        try:
            # 获取选中的年份
            year = int(self.year_var.get())
            
            # 获取数据
            all_data = self.data_loader.get_all_data()
            
            # 选择国家列和指定年份列
            country_col = all_data.columns[0]
            export_data = all_data[[country_col, str(year)]].dropna()
            
            # 导出到CSV
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")],
                title="导出军费支出数据"
            )
            
            if file_path:
                export_data.to_csv(file_path, index=False)
                messagebox.showinfo("导出成功", f"数据已成功导出到: {file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出数据时发生错误: {str(e)}") 