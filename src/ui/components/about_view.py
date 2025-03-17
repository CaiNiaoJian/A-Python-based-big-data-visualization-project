#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
关于视图组件
显示应用程序的相关信息
"""

import tkinter as tk
import customtkinter as ctk
from typing import Dict, List, Any, Callable
import webbrowser
import os
from PIL import Image, ImageTk

class AboutView(ctk.CTkFrame):
    """关于视图组件类"""
    
    def __init__(self, master, **kwargs):
        """
        初始化关于视图
        
        Args:
            master: 父组件
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        
        # 创建视图内容
        self._create_widgets()
    
    def _create_widgets(self):
        """创建视图组件"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self, 
            text="关于应用程序&课程作业",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 20), padx=20, anchor="w")
        
        # 主内容区域
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # 应用信息
        self.app_info_frame = ctk.CTkFrame(self.content_frame)
        self.app_info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 应用标题
        self.app_title = ctk.CTkLabel(
            self.app_info_frame, 
            text="世界军事力量可视化",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.app_title.pack(pady=(20, 10))
        
        # 应用版本
        self.app_version = ctk.CTkLabel(
            self.app_info_frame, 
            text="版本 1.0.0",
            font=ctk.CTkFont(size=14)
        )
        self.app_version.pack(pady=(0, 20))
        
        # 应用描述
        self.app_description = ctk.CTkLabel(
            self.app_info_frame, 
            text="这是一个用于可视化世界各国军事力量数据的应用程序。\n"
                 "数据来源于斯德哥尔摩国际和平研究所(SIPRI)的军费开支数据库。",
            font=ctk.CTkFont(size=14),
            wraplength=600,
            justify="center"
        )
        self.app_description.pack(pady=(0, 20))
        
        # 数据来源信息
        self.data_source_frame = ctk.CTkFrame(self.app_info_frame)
        self.data_source_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.data_source_label = ctk.CTkLabel(
            self.data_source_frame, 
            text="数据来源:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.data_source_label.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        self.data_source_link = ctk.CTkButton(
            self.data_source_frame,
            text="SIPRI军费开支数据库",
            command=lambda: webbrowser.open("https://www.sipri.org/databases/milex"),
            fg_color="transparent",
            text_color=("#0066CC", "#3B8ED0"),
            hover=False
        )
        self.data_source_link.pack(side=tk.LEFT, padx=0, pady=10)
        
        # 开发者信息
        self.developer_frame = ctk.CTkFrame(self.app_info_frame)
        self.developer_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.developer_label = ctk.CTkLabel(
            self.developer_frame, 
            text="开发者:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.developer_label.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        self.developer_name = ctk.CTkLabel(
            self.developer_frame, 
            text="CaiNiaoJian @github.com/CaiNiaoJian 2025.03.17",
            font=ctk.CTkFont(size=14)
        )
        self.developer_name.pack(side=tk.LEFT, padx=0, pady=10)
        
        # 技术栈信息
        self.tech_frame = ctk.CTkFrame(self.app_info_frame)
        self.tech_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.tech_label = ctk.CTkLabel(
            self.tech_frame, 
            text="技术栈:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.tech_label.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        self.tech_info = ctk.CTkLabel(
            self.tech_frame, 
            text="Python, Tkinter, CustomTkinter, Matplotlib, Pandas, NumPy, Plotly",
            font=ctk.CTkFont(size=14)
        )
        self.tech_info.pack(side=tk.LEFT, padx=0, pady=10)
        
        # 版权信息
        self.copyright_label = ctk.CTkLabel(
            self.app_info_frame, 
            text="© 2025 军事数据可视化，CaiNiaoJian. 保留所有权利。",
            font=ctk.CTkFont(size=12)
        )
        self.copyright_label.pack(pady=(20, 10))
        
        # 免责声明
        self.disclaimer_label = ctk.CTkLabel(
            self.app_info_frame, 
            text="免责声明: 本应用程序仅用于教育和研究目的。\n"
                 "数据的准确性和完整性取决于原始数据源。",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            wraplength=600,
            justify="center"
        )
        self.disclaimer_label.pack(pady=(0, 20)) 