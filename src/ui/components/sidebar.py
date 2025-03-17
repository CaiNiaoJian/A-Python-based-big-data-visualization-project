#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
侧边栏组件
提供应用程序的导航功能
"""

import tkinter as tk
import customtkinter as ctk
from typing import Callable, Dict, Any
from PIL import Image, ImageTk
import os

class Sidebar(ctk.CTkFrame):
    """侧边栏组件类"""
    
    def __init__(self, master, on_view_change: Callable[[str], None], **kwargs):
        """
        初始化侧边栏
        
        Args:
            master: 父组件
            on_view_change: 视图切换回调函数
            **kwargs: 其他参数
        """
        super().__init__(master, **kwargs)
        
        self.on_view_change = on_view_change
        
        # 创建侧边栏内容
        self._create_widgets()
    
    def _create_widgets(self):
        """创建侧边栏组件"""
        # 标题
        self.title_label = ctk.CTkLabel(
            self, 
            text="导航菜单",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.pack(pady=(20, 20), padx=10)
        
        # 菜单按钮
        self.buttons = {}
        
        # 仪表盘按钮
        self.buttons['dashboard'] = self._create_menu_button(
            "仪表盘", 
            lambda: self.on_view_change('dashboard')
        )
        
        # 世界地图按钮
        self.buttons['map'] = self._create_menu_button(
            "世界地图", 
            lambda: self.on_view_change('map')
        )
        
        # 国家比较按钮
        self.buttons['comparison'] = self._create_menu_button(
            "国家比较", 
            lambda: self.on_view_change('comparison')
        )
        
        # 趋势分析按钮
        self.buttons['trend'] = self._create_menu_button(
            "趋势分析", 
            lambda: self.on_view_change('trend')
        )
        
        # 分隔线
        self.separator = ctk.CTkFrame(self, height=1, fg_color="gray75")
        self.separator.pack(fill=tk.X, padx=10, pady=(10, 10))
        
        # 关于按钮
        self.buttons['about'] = self._create_menu_button(
            "关于", 
            lambda: self.on_view_change('about')
        )
    
    def _create_menu_button(self, text: str, command: Callable[[], None]) -> ctk.CTkButton:
        """
        创建菜单按钮
        
        Args:
            text: 按钮文本
            command: 按钮点击回调函数
            
        Returns:
            创建的按钮
        """
        button = ctk.CTkButton(
            self,
            text=text,
            command=command,
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            height=40,
            corner_radius=0,
            font=ctk.CTkFont(size=14)
        )
        button.pack(fill=tk.X, padx=0, pady=(0, 5))
        
        return button
    
    def set_active(self, view_name: str):
        """
        设置活动视图
        
        Args:
            view_name: 视图名称
        """
        # 重置所有按钮
        for name, button in self.buttons.items():
            if name == view_name:
                button.configure(
                    fg_color=("gray75", "gray25"),
                    text_color=("gray10", "gray90")
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=("gray10", "gray90")
                ) 