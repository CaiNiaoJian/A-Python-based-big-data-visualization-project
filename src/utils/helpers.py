#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
辅助工具模块
提供各种辅助函数
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import io
import base64
from datetime import datetime

def figure_to_image(fig: Figure) -> Image.Image:
    """
    将matplotlib图表转换为PIL图像
    
    Args:
        fig: matplotlib Figure对象
        
    Returns:
        PIL Image对象
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    return img

def figure_to_photoimage(fig: Figure) -> Any:
    """
    将matplotlib图表转换为Tkinter PhotoImage
    
    Args:
        fig: matplotlib Figure对象
        
    Returns:
        Tkinter PhotoImage对象
    """
    img = figure_to_image(fig)
    photo = ImageTk.PhotoImage(img)
    return photo

def save_figure(fig: Figure, filename: str, directory: str = None) -> str:
    """
    保存matplotlib图表为图像文件
    
    Args:
        fig: matplotlib Figure对象
        filename: 文件名
        directory: 保存目录，默认为当前目录
        
    Returns:
        保存的文件路径
    """
    if directory is None:
        directory = os.getcwd()
    
    # 确保目录存在
    os.makedirs(directory, exist_ok=True)
    
    # 确保文件名有扩展名
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.pdf')):
        filename += '.png'
    
    # 构建完整路径
    filepath = os.path.join(directory, filename)
    
    # 保存图表
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    
    return filepath

def format_number(num: float, precision: int = 1) -> str:
    """
    格式化数字，对于大数使用K, M, B等后缀
    
    Args:
        num: 要格式化的数字
        precision: 小数位数
        
    Returns:
        格式化后的字符串
    """
    if pd.isna(num):
        return "N/A"
    
    if num == 0:
        return "0"
        
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    
    # 添加符号
    if magnitude == 0:
        return f"{num:.{precision}f}"
    elif magnitude == 1:
        return f"{num:.{precision}f}K"
    elif magnitude == 2:
        return f"{num:.{precision}f}M"
    elif magnitude == 3:
        return f"{num:.{precision}f}B"
    else:
        return f"{num:.{precision}f}T"

def get_year_range(start_year: int = 1960, end_year: int = 2023) -> List[int]:
    """
    获取年份范围列表
    
    Args:
        start_year: 起始年份
        end_year: 结束年份
        
    Returns:
        年份列表
    """
    return list(range(start_year, end_year + 1))

def create_export_filename(prefix: str, extension: str = 'png') -> str:
    """
    创建导出文件名，包含时间戳
    
    Args:
        prefix: 文件名前缀
        extension: 文件扩展名
        
    Returns:
        文件名
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def plotly_to_image(fig: Any) -> Image.Image:
    """
    将plotly图表转换为PIL图像
    
    Args:
        fig: plotly Figure对象
        
    Returns:
        PIL Image对象
    """
    try:
        # 首先尝试使用kaleido引擎导出
        img_bytes = fig.to_image(format="png", engine="kaleido")
        img = Image.open(io.BytesIO(img_bytes))
        return img
    except Exception as e:
        print(f"使用kaleido导出图像失败: {e}")
        
        try:
            # 尝试将Plotly图表保存为HTML并使用普通方式导出
            buffer = io.BytesIO()
            fig.write_image(buffer, format="png")
            buffer.seek(0)
            return Image.open(buffer)
        except Exception as e2:
            print(f"使用write_image导出图像失败: {e2}")
            
            # 创建一个空白图像作为后备
            width, height = 800, 600
            img = Image.new('RGB', (width, height), color='white')
            
            # 尝试从matplotlib创建一个简单的后备图像
            try:
                import matplotlib.pyplot as plt
                fig_fallback, ax = plt.subplots(figsize=(10, 6))
                title = "无法加载地图视图"
                if hasattr(fig, 'layout') and hasattr(fig.layout, 'title') and fig.layout.title.text:
                    title = f"无法加载: {fig.layout.title.text}"
                ax.text(0.5, 0.5, f"{title}\n\n数据连接错误: 无法获取地图数据\n请检查网络连接后重试", 
                       horizontalalignment='center', verticalalignment='center', fontsize=14)
                ax.set_axis_off()
                plt.tight_layout()
                
                # 将matplotlib图表转换为PIL图像
                buf = io.BytesIO()
                fig_fallback.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                buf.seek(0)
                img = Image.open(buf)
                plt.close(fig_fallback)
            except Exception as e3:
                print(f"创建后备图像失败: {e3}")
                # 如果matplotlib也失败，则显示纯文本错误消息
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(img)
                try:
                    # 尝试加载字体，失败则使用默认字体
                    font = ImageFont.truetype("arial.ttf", 16)
                except:
                    font = ImageFont.load_default()
                
                message = "无法加载地图视图\n\n数据连接错误: 无法获取地图数据\n请检查网络连接后重试"
                draw.text((width/2, height/2), message, fill="black", font=font, anchor="mm", align="center")
            
            return img

def get_continent_for_country(country_name: str) -> str:
    """
    获取国家所属的大洲
    
    Args:
        country_name: 国家名称
        
    Returns:
        大洲名称
    """
    # 这里使用一个简化的映射，实际应用中可能需要更完整的数据
    continent_map = {
        'China': 'Asia',
        'United States': 'North America',
        'Russia': 'Europe',
        'India': 'Asia',
        'Japan': 'Asia',
        'Germany': 'Europe',
        'United Kingdom': 'Europe',
        'France': 'Europe',
        'Italy': 'Europe',
        'Brazil': 'South America',
        # 可以根据需要添加更多国家
    }
    
    return continent_map.get(country_name, 'Unknown')

def normalize_data(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    对数据进行归一化处理
    
    Args:
        data: 包含数据的DataFrame
        columns: 要归一化的列名列表
        
    Returns:
        归一化后的DataFrame
    """
    result = data.copy()
    
    for column in columns:
        if column in result.columns:
            min_val = result[column].min()
            max_val = result[column].max()
            
            # 避免除以零
            if max_val > min_val:
                result[column] = (result[column] - min_val) / (max_val - min_val)
            else:
                result[column] = 0
    
    return result 