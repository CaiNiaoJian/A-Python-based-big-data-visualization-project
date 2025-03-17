#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
军事力量可视化应用程序
主UI应用类
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any, Callable
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.graph_objects as go
import webbrowser

# 导入项目模块
from data.data_loader import DataLoader
from data.data_analyzer import DataAnalyzer
from visualization.visualizer import Visualizer, APPLE_COLORS
from utils.helpers import (
    figure_to_photoimage, save_figure, format_number, 
    get_year_range, create_export_filename, plotly_to_image
)

# 导入UI组件
from ui.components.sidebar import Sidebar
from ui.components.dashboard import Dashboard
from ui.components.map_view import MapView
from ui.components.comparison_view import ComparisonView
from ui.components.trend_view import TrendView
from ui.components.about_view import AboutView

class MilitaryPowerApp:
    """军事力量可视化应用程序主类"""
    
    def __init__(self):
        """初始化应用程序"""
        # 设置应用程序主题
        ctk.set_appearance_mode("light")  # 苹果风格使用浅色主题
        ctk.set_default_color_theme("blue")  # 使用蓝色主题，接近苹果的蓝色
        
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("世界军事力量可视化")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 设置图标（如果有）
        # self.root.iconbitmap("path/to/icon.ico")
        
        # 初始化数据相关对象
        self.data_loader = DataLoader()
        self.data_analyzer = DataAnalyzer(self.data_loader)
        self.visualizer = Visualizer(theme='apple')
        
        # 创建UI布局
        self._create_layout()
        
        # 绑定事件
        self._bind_events()
        
        # 加载初始数据
        self._load_initial_data()
    
    def _create_layout(self):
        """创建应用程序布局"""
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建顶部标题栏
        self._create_title_bar()
        
        # 创建内容区域
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(10, 0))
        
        # 创建侧边栏
        self.sidebar = Sidebar(
            self.content_frame, 
            on_view_change=self._on_view_change,
            width=200
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 创建主内容区域
        self.main_content = ctk.CTkFrame(self.content_frame)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建各个视图
        self.views = {}
        
        # 仪表盘视图
        self.views['dashboard'] = Dashboard(
            self.main_content,
            self.data_loader,
            self.data_analyzer,
            self.visualizer
        )
        
        # 世界地图视图
        self.views['map'] = MapView(
            self.main_content,
            self.data_loader,
            self.data_analyzer,
            self.visualizer
        )
        
        # 国家比较视图
        self.views['comparison'] = ComparisonView(
            self.main_content,
            self.data_loader,
            self.data_analyzer,
            self.visualizer
        )
        
        # 趋势分析视图
        self.views['trend'] = TrendView(
            self.main_content,
            self.data_loader,
            self.data_analyzer,
            self.visualizer
        )
        
        # 关于视图
        self.views['about'] = AboutView(
            self.main_content
        )
        
        # 默认显示仪表盘视图
        self._on_view_change('dashboard')
        
        # 创建底部状态栏
        self._create_status_bar()
    
    def _create_title_bar(self):
        """创建顶部标题栏"""
        self.title_bar = ctk.CTkFrame(self.main_frame, height=50)
        self.title_bar.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        # 应用标题
        self.title_label = ctk.CTkLabel(
            self.title_bar, 
            text="世界军事力量可视化 (1960-2023)",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # 右侧工具栏
        self.toolbar = ctk.CTkFrame(self.title_bar, fg_color="transparent")
        self.toolbar.pack(side=tk.RIGHT, padx=10)
        
        # 导出按钮
        self.export_button = ctk.CTkButton(
            self.toolbar,
            text="导出数据",
            command=self._on_export_data,
            width=100,
            height=32
        )
        self.export_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 设置按钮
        self.settings_button = ctk.CTkButton(
            self.toolbar,
            text="设置",
            command=self._on_settings,
            width=80,
            height=32
        )
        self.settings_button.pack(side=tk.RIGHT, padx=(5, 0))
    
    def _create_status_bar(self):
        """创建底部状态栏"""
        self.status_bar = ctk.CTkFrame(self.main_frame, height=30)
        self.status_bar.pack(fill=tk.X, padx=0, pady=(10, 0))
        
        # 状态信息
        self.status_label = ctk.CTkLabel(
            self.status_bar, 
            text="就绪",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # 数据来源信息
        self.data_source_label = ctk.CTkLabel(
            self.status_bar, 
            text="数据来源: SIPRI军费开支数据库 (1948-2023)",
            font=ctk.CTkFont(size=12)
        )
        self.data_source_label.pack(side=tk.RIGHT, padx=10)
    
    def _bind_events(self):
        """绑定事件处理函数"""
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # 窗口大小改变事件
        self.root.bind("<Configure>", self._on_resize)
    
    def _load_initial_data(self):
        """加载初始数据"""
        try:
            # 更新状态栏
            self.status_label.configure(text="正在加载数据...")
            self.root.update()
            
            # 加载数据
            countries = self.data_loader.get_countries_list()
            years = self.data_loader.get_years_list()
            
            # 更新状态栏
            self.status_label.configure(text=f"已加载 {len(countries)} 个国家的数据")
        except Exception as e:
            messagebox.showerror("数据加载错误", f"加载数据时发生错误: {str(e)}")
            self.status_label.configure(text="数据加载失败")
    
    def _on_view_change(self, view_name: str):
        """
        切换视图
        
        Args:
            view_name: 视图名称
        """
        # 隐藏所有视图
        for view in self.views.values():
            view.pack_forget()
        
        # 显示选定的视图
        if view_name in self.views:
            self.views[view_name].pack(fill=tk.BOTH, expand=True)
            
            # 更新视图（如果视图有update方法）
            if hasattr(self.views[view_name], 'update'):
                self.views[view_name].update()
    
    def _on_export_data(self):
        """导出数据处理函数"""
        # 获取当前视图
        current_view = None
        for view_name, view in self.views.items():
            if view.winfo_ismapped():
                current_view = view
                break
        
        if current_view and hasattr(current_view, 'export_data'):
            current_view.export_data()
        else:
            messagebox.showinfo("导出", "当前视图不支持数据导出")
    
    def _on_settings(self):
        """设置处理函数"""
        # 创建设置对话框
        settings_dialog = ctk.CTkToplevel(self.root)
        settings_dialog.title("设置")
        settings_dialog.geometry("400x300")
        settings_dialog.resizable(False, False)
        settings_dialog.grab_set()  # 模态对话框
        
        # 设置对话框内容
        settings_frame = ctk.CTkFrame(settings_dialog)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 主题设置
        theme_label = ctk.CTkLabel(
            settings_frame, 
            text="外观主题:",
            font=ctk.CTkFont(size=14)
        )
        theme_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        
        theme_var = tk.StringVar(value="light")
        theme_light = ctk.CTkRadioButton(
            settings_frame, 
            text="浅色",
            variable=theme_var,
            value="light",
            command=lambda: ctk.set_appearance_mode("light")
        )
        theme_light.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 5))
        
        theme_dark = ctk.CTkRadioButton(
            settings_frame, 
            text="深色",
            variable=theme_var,
            value="dark",
            command=lambda: ctk.set_appearance_mode("dark")
        )
        theme_dark.grid(row=0, column=2, sticky="w", padx=10, pady=(10, 5))
        
        # 语言设置
        language_label = ctk.CTkLabel(
            settings_frame, 
            text="语言:",
            font=ctk.CTkFont(size=14)
        )
        language_label.grid(row=1, column=0, sticky="w", padx=10, pady=(10, 5))
        
        language_var = tk.StringVar(value="zh_CN")
        language_zh = ctk.CTkRadioButton(
            settings_frame, 
            text="中文",
            variable=language_var,
            value="zh_CN"
        )
        language_zh.grid(row=1, column=1, sticky="w", padx=10, pady=(10, 5))
        
        language_en = ctk.CTkRadioButton(
            settings_frame, 
            text="英文",
            variable=language_var,
            value="en_US"
        )
        language_en.grid(row=1, column=2, sticky="w", padx=10, pady=(10, 5))
        
        # 数据设置
        data_label = ctk.CTkLabel(
            settings_frame, 
            text="数据设置:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        data_label.grid(row=2, column=0, sticky="w", padx=10, pady=(20, 5))
        
        # 年份范围
        year_range_label = ctk.CTkLabel(
            settings_frame, 
            text="默认年份范围:",
            font=ctk.CTkFont(size=14)
        )
        year_range_label.grid(row=3, column=0, sticky="w", padx=10, pady=(10, 5))
        
        year_range_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        year_range_frame.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        
        start_year_var = tk.StringVar(value="1960")
        start_year_entry = ctk.CTkEntry(
            year_range_frame,
            width=60,
            textvariable=start_year_var
        )
        start_year_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        year_range_separator = ctk.CTkLabel(
            year_range_frame, 
            text="至",
            font=ctk.CTkFont(size=14)
        )
        year_range_separator.pack(side=tk.LEFT, padx=5)
        
        end_year_var = tk.StringVar(value="2022")
        end_year_entry = ctk.CTkEntry(
            year_range_frame,
            width=60,
            textvariable=end_year_var
        )
        end_year_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # 按钮
        button_frame = ctk.CTkFrame(settings_dialog, fg_color="transparent")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="取消",
            command=settings_dialog.destroy,
            width=100
        )
        cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_button = ctk.CTkButton(
            button_frame,
            text="保存",
            command=lambda: self._save_settings(
                theme_var.get(),
                language_var.get(),
                start_year_var.get(),
                end_year_var.get(),
                settings_dialog
            ),
            width=100
        )
        save_button.pack(side=tk.RIGHT)
    
    def _save_settings(self, theme: str, language: str, start_year: str, end_year: str, dialog: ctk.CTkToplevel):
        """
        保存设置
        
        Args:
            theme: 主题
            language: 语言
            start_year: 起始年份
            end_year: 结束年份
            dialog: 设置对话框
        """
        # 这里可以保存设置到配置文件
        # 简单起见，这里只是关闭对话框
        dialog.destroy()
        
        # 显示保存成功消息
        messagebox.showinfo("设置", "设置已保存")
    
    def _on_resize(self, event):
        """窗口大小改变事件处理函数"""
        # 这里可以处理窗口大小改变事件
        pass
    
    def _on_close(self):
        """窗口关闭事件处理函数"""
        # 询问是否确定退出
        if messagebox.askyesno("退出", "确定要退出应用程序吗？"):
            self.root.destroy()
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()