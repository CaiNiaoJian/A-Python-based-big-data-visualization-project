#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据转换脚本
将rbdata目录中的Excel军事数据转换为JSON格式
"""

import os
import sys
import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union


def get_project_root() -> Path:
    """
    获取项目根目录
    
    Returns:
        项目根目录的Path对象
    """
    script_path = Path(os.path.abspath(__file__))
    return script_path.parent.parent


def load_excel_data(file_path: str) -> pd.DataFrame:
    """
    加载Excel数据文件
    
    Args:
        file_path: Excel文件路径
    
    Returns:
        包含数据的DataFrame
    """
    try:
        df = pd.read_excel(file_path, header=None)
        print(f"成功加载文件: {file_path}, 形状: {df.shape}")
        return df
    except Exception as e:
        print(f"加载文件 {file_path} 失败: {e}")
        return pd.DataFrame()


def process_dataframe(df: pd.DataFrame, file_name: str) -> pd.DataFrame:
    """
    处理DataFrame数据
    
    Args:
        df: 原始DataFrame数据
        file_name: 文件名（用于确定大洲）
    
    Returns:
        处理后的DataFrame
    """
    if df.empty:
        return df
    
    # 根据README.md，第一列是国家名称，其余列是1948-2023年的军费开支数据
    # 设置列名
    continent = file_name.split('.')[0]
    
    # 使用1960-2022年的年份范围作为列名（与data_loader.py中一致）
    years = list(range(1960, 2023))
    column_names = ['Country'] + [str(year) for year in years]
    
    # 确保列数匹配（如果不匹配，进行调整）
    if len(df.columns) > len(column_names):
        # 截断额外的列
        df = df.iloc[:, :len(column_names)]
    elif len(df.columns) < len(column_names):
        # 补充缺失的列
        for i in range(len(df.columns), len(column_names)):
            df[i] = np.nan
    
    # 设置列名
    df.columns = column_names
    
    # 处理缺失值
    df.replace("...", np.nan, inplace=True)
    df.replace("xx", np.nan, inplace=True)
    
    # 将年份列的数据转换为数值类型
    for col in df.columns[1:]:
        if str(col).isdigit():
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 添加大洲信息列
    df['Continent'] = continent
    
    return df


def convert_to_json(df: pd.DataFrame, output_file: str, format_type: str = 'records'):
    """
    将DataFrame转换为JSON并保存
    
    Args:
        df: 要转换的DataFrame
        output_file: 输出文件路径
        format_type: JSON格式类型，可选值为'records'（默认）、'split'、'index'等
    """
    if df.empty:
        print(f"警告: DataFrame为空，未生成JSON文件: {output_file}")
        return
    
    try:
        # 转换为JSON
        if format_type == 'records':
            # 以记录形式输出，更适合前端使用
            json_data = df.to_json(orient=format_type, date_format='iso')
            # 解析并格式化JSON数据
            parsed_data = json.loads(json_data)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(parsed_data, f, ensure_ascii=False, indent=4)
        else:
            # 以其他形式输出
            df.to_json(output_file, orient=format_type, date_format='iso', indent=4)
        
        print(f"成功保存JSON文件: {output_file}")
    except Exception as e:
        print(f"保存JSON文件 {output_file} 失败: {e}")


def convert_single_file(input_file: str, output_dir: str):
    """
    转换单个Excel文件为JSON
    
    Args:
        input_file: 输入的Excel文件路径
        output_dir: 输出目录
    """
    # 获取文件名（不含扩展名）
    file_name = os.path.basename(input_file)
    file_base = os.path.splitext(file_name)[0]
    
    # 加载数据
    df = load_excel_data(input_file)
    if df.empty:
        return
    
    # 处理数据
    df = process_dataframe(df, file_name)
    if df.empty:
        return
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 转换为JSON并保存
    output_file = os.path.join(output_dir, f"{file_base}.json")
    convert_to_json(df, output_file)
    
    # 输出数据基本信息
    print(f"文件 {file_base} 统计信息:")
    print(f"- 国家数量: {len(df)}")
    print(f"- 年份范围: 1960-2022")
    print(f"- 输出JSON文件: {output_file}")
    print("-" * 50)


def convert_all_files():
    """
    转换所有Excel文件为JSON
    """
    project_root = get_project_root()
    
    # 输入目录
    input_dir = os.path.join(project_root, "rbdata")
    
    # 输出目录
    output_dir = os.path.join(project_root, "web", "public", "data")
    
    # 检查输入目录是否存在
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录 {input_dir} 不存在！")
        return
    
    # 获取所有Excel文件
    excel_files = [
        os.path.join(input_dir, f) for f in os.listdir(input_dir)
        if f.endswith(".xlsx") and not f.startswith("~")
    ]
    
    if not excel_files:
        print(f"警告: 在 {input_dir} 中未找到Excel文件！")
        return
    
    print(f"找到 {len(excel_files)} 个Excel文件:")
    for file in excel_files:
        print(f"- {os.path.basename(file)}")
    print("-" * 50)
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 合并所有数据
    all_dfs = []
    for file in excel_files:
        df = load_excel_data(file)
        if not df.empty:
            df = process_dataframe(df, os.path.basename(file))
            all_dfs.append(df)
    
    # 合并数据框
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        # 转换合并后的数据为JSON
        output_file = os.path.join(output_dir, "all_military_data.json")
        convert_to_json(combined_df, output_file)
        
        # 创建按年份组织的数据
        years_data = {}
        for year in range(1960, 2023):
            year_str = str(year)
            year_df = combined_df[['Country', 'Continent', year_str]].copy()
            year_df.rename(columns={year_str: 'Expenditure'}, inplace=True)
            year_df = year_df.dropna(subset=['Expenditure'])
            
            year_output_file = os.path.join(output_dir, f"year_{year}.json")
            convert_to_json(year_df, year_output_file)
            
            # 存储年份数据的摘要
            years_data[year] = {
                'total_countries': len(year_df),
                'file': f"year_{year}.json",
                'total_expenditure': float(year_df['Expenditure'].sum())
            }
        
        # 保存年份摘要数据
        years_summary_file = os.path.join(output_dir, "years_summary.json")
        with open(years_summary_file, 'w', encoding='utf-8') as f:
            json.dump(years_data, f, ensure_ascii=False, indent=4)
        print(f"成功保存年份摘要数据: {years_summary_file}")
    
    # 处理各个文件
    for file in excel_files:
        convert_single_file(file, output_dir)


def main():
    """
    主函数
    """
    print("开始转换军事数据为JSON格式...")
    convert_all_files()
    print("转换完成！")


if __name__ == "__main__":
    main() 