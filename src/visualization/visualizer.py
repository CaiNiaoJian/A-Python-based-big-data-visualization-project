#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
可视化模块
负责生成各种军事数据可视化图表
"""

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any
import io
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 设置中文字体支持
try:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
except:
    print("警告: 无法设置中文字体，图表中的中文可能无法正确显示")

# 设置苹果风格的颜色主题
APPLE_COLORS = {
    'blue': '#007AFF',
    'green': '#34C759',
    'indigo': '#5856D6',
    'orange': '#FF9500',
    'pink': '#FF2D55',
    'purple': '#AF52DE',
    'red': '#FF3B30',
    'teal': '#5AC8FA',
    'yellow': '#FFCC00',
    'gray': '#8E8E93',
    'background': '#F2F2F7',
    'text': '#000000'
}

class Visualizer:
    """可视化器类，负责生成各种军事数据可视化图表"""
    
    def __init__(self, theme: str = 'apple'):
        """
        初始化可视化器
        
        Args:
            theme: 主题名称，目前支持'apple'
        """
        self.theme = theme
        
        # 设置主题
        if theme == 'apple':
            sns.set_style("whitegrid")
            sns.set_palette([
                APPLE_COLORS['blue'], 
                APPLE_COLORS['green'],
                APPLE_COLORS['orange'],
                APPLE_COLORS['purple'],
                APPLE_COLORS['red'],
                APPLE_COLORS['teal'],
                APPLE_COLORS['yellow'],
                APPLE_COLORS['indigo'],
                APPLE_COLORS['pink'],
                APPLE_COLORS['gray']
            ])
    
    def create_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str, 
                         title: str, x_label: str, y_label: str, 
                         figsize: Tuple[int, int] = (10, 6)) -> Figure:
        """
        创建柱状图
        
        Args:
            data: 包含数据的DataFrame
            x_col: X轴列名
            y_col: Y轴列名
            title: 图表标题
            x_label: X轴标签
            y_label: Y轴标签
            figsize: 图表大小
            
        Returns:
            matplotlib Figure对象
        """
        # 确保数据类型正确
        data = data.copy()
        if y_col in data.columns:
            data[y_col] = pd.to_numeric(data[y_col], errors='coerce')
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # 创建柱状图
        bars = ax.bar(data[x_col], data[y_col], color=APPLE_COLORS['blue'])
        
        # 设置标题和标签
        ax.set_title(title, fontsize=16, pad=20)
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        
        # 设置网格线
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # 美化
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        return fig
    
    def create_line_chart(self, data: pd.DataFrame, x_col: str, y_cols: List[str], 
                          title: str, x_label: str, y_label: str,
                          figsize: Tuple[int, int] = (10, 6)) -> Figure:
        """
        创建折线图
        
        Args:
            data: 包含数据的DataFrame
            x_col: X轴列名
            y_cols: Y轴列名列表（可以是多条线）
            title: 图表标题
            x_label: X轴标签
            y_label: Y轴标签
            figsize: 图表大小
            
        Returns:
            matplotlib Figure对象
        """
        # 确保数据类型正确
        data = data.copy()
        if x_col in data.columns:
            data[x_col] = pd.to_numeric(data[x_col], errors='coerce')
        
        for col in y_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # 获取颜色列表
        colors = list(APPLE_COLORS.values())[:len(y_cols)]
        
        # 创建折线图
        for i, y_col in enumerate(y_cols):
            if y_col in data.columns:
                ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, 
                       color=colors[i], label=y_col)
        
        # 设置标题和标签
        ax.set_title(title, fontsize=16, pad=20)
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        
        # 设置网格线
        ax.grid(linestyle='--', alpha=0.7)
        
        # 美化
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # 添加图例
        if len(y_cols) > 1:
            ax.legend(frameon=True, fancybox=True, shadow=True)
        
        plt.tight_layout()
        
        return fig
    
    def create_pie_chart(self, data: pd.DataFrame, value_col: str, label_col: str,
                         title: str, figsize: Tuple[int, int] = (10, 8)) -> Figure:
        """
        创建饼图
        
        Args:
            data: 包含数据的DataFrame
            value_col: 值列名
            label_col: 标签列名
            title: 图表标题
            figsize: 图表大小
            
        Returns:
            matplotlib Figure对象
        """
        # 确保数据类型正确
        data = data.copy()
        if value_col in data.columns:
            data[value_col] = pd.to_numeric(data[value_col], errors='coerce')
        
        # 删除缺失值
        data = data.dropna(subset=[value_col])
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # 获取颜色列表
        colors = list(APPLE_COLORS.values())[:len(data)]
        
        # 创建饼图
        wedges, texts, autotexts = ax.pie(
            data[value_col], 
            labels=data[label_col],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            shadow=False,
            wedgeprops={'edgecolor': 'w', 'linewidth': 1}
        )
        
        # 设置标题
        ax.set_title(title, fontsize=16, pad=20)
        
        # 设置文本样式
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=12)
        
        # 添加图例
        ax.legend(wedges, data[label_col],
                  title="国家",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        
        return fig
    
    def create_map_chart(self, data: pd.DataFrame, country_col: str, value_col: str,
                         title: str) -> Any:
        """
        创建世界地图可视化
        
        Args:
            data: 包含数据的DataFrame
            country_col: 国家列名
            value_col: 值列名
            title: 图表标题
            
        Returns:
            plotly Figure对象
        """
        # 确保数据类型正确
        data = data.copy()
        if value_col in data.columns:
            data[value_col] = pd.to_numeric(data[value_col], errors='coerce')
        
        # 删除缺失值
        data = data.dropna(subset=[value_col])
        
        # 创建世界地图
        fig = px.choropleth(
            data,
            locations=data[country_col],  # 国家名称
            locationmode='country names',  # 使用国家名称作为位置
            color=data[value_col],  # 颜色映射的值
            color_continuous_scale=px.colors.sequential.Blues,  # 颜色映射
            title=title,
            labels={value_col: '军费支出'},
            hover_name=data[country_col]
        )
        
        # 设置布局
        fig.update_layout(
            title_font_size=20,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            ),
            margin={"r":0,"t":40,"l":0,"b":0},
            coloraxis_colorbar=dict(
                title='军费支出',
                thicknessmode="pixels", thickness=20,
                lenmode="pixels", len=300,
                yanchor="top", y=1,
                ticks="outside"
            )
        )
        
        return fig
    
    def create_radar_chart(self, data: pd.DataFrame, categories: List[str], 
                           title: str) -> Any:
        """
        创建雷达图
        
        Args:
            data: 包含数据的DataFrame，每行是一个国家，列是不同类别的军事指标
            categories: 雷达图的类别名称列表
            title: 图表标题
            
        Returns:
            plotly Figure对象
        """
        # 确保数据类型正确
        data = data.copy()
        for cat in categories:
            if cat in data.columns:
                data[cat] = pd.to_numeric(data[cat], errors='coerce')
        
        # 创建雷达图
        fig = go.Figure()
        
        # 获取颜色列表
        colors = list(APPLE_COLORS.values())[:len(data)]
        
        # 为每个国家添加一条雷达线
        for i, row in data.iterrows():
            country_name = row.iloc[0]  # 假设第一列是国家名称
            values = []
            
            # 获取每个类别的值，确保是数值
            for cat in categories:
                try:
                    val = float(row[cat])
                    values.append(val)
                except (ValueError, TypeError):
                    values.append(0)  # 如果无法转换为数值，使用0
            
            # 闭合雷达图
            values.append(values[0])
            categories_closed = categories + [categories[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories_closed,
                fill='toself',
                name=country_name,
                line_color=colors[i % len(colors)]
            ))
        
        # 设置布局
        fig.update_layout(
            title=title,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, data[categories].max().max() * 1.1]
                )
            ),
            showlegend=True
        )
        
        return fig
    
    def create_stacked_area_chart(self, data: pd.DataFrame, x_col: str, y_cols: List[str],
                                 title: str, x_label: str, y_label: str) -> Any:
        """
        创建堆叠面积图
        
        Args:
            data: 包含数据的DataFrame
            x_col: X轴列名
            y_cols: Y轴列名列表（多个区域）
            title: 图表标题
            x_label: X轴标签
            y_label: Y轴标签
            
        Returns:
            plotly Figure对象
        """
        # 确保数据类型正确
        data = data.copy()
        data[x_col] = pd.to_numeric(data[x_col], errors='coerce')
        for col in y_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # 创建堆叠面积图
        fig = go.Figure()
        
        # 获取颜色列表
        colors = list(APPLE_COLORS.values())[:len(y_cols)]
        
        # 为每个区域添加一个面积
        for i, y_col in enumerate(y_cols):
            if y_col in data.columns:
                fig.add_trace(go.Scatter(
                    x=data[x_col], 
                    y=data[y_col],
                    mode='lines',
                    line=dict(width=0.5, color=colors[i]),
                    stackgroup='one',
                    name=y_col
                ))
        
        # 设置布局
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        return fig
    
    def create_bubble_chart(self, data: pd.DataFrame, x_col: str, y_col: str, 
                           size_col: str, color_col: str, hover_col: str,
                           title: str, x_label: str, y_label: str) -> Any:
        """
        创建气泡图
        
        Args:
            data: 包含数据的DataFrame
            x_col: X轴列名
            y_col: Y轴列名
            size_col: 气泡大小列名
            color_col: 气泡颜色列名
            hover_col: 悬停信息列名
            title: 图表标题
            x_label: X轴标签
            y_label: Y轴标签
            
        Returns:
            plotly Figure对象
        """
        # 确保数据类型正确
        data = data.copy()
        if x_col in data.columns:
            data[x_col] = pd.to_numeric(data[x_col], errors='coerce')
        if y_col in data.columns:
            data[y_col] = pd.to_numeric(data[y_col], errors='coerce')
        if size_col in data.columns:
            data[size_col] = pd.to_numeric(data[size_col], errors='coerce')
        
        # 创建气泡图
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            size=size_col,
            color=color_col,
            hover_name=hover_col,
            title=title,
            labels={
                x_col: x_label,
                y_col: y_label,
                size_col: '军费支出',
                color_col: '大洲'
            },
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        # 设置布局
        fig.update_layout(
            title_font_size=20,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        return fig 