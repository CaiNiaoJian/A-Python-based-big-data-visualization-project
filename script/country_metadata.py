#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
国家元数据生成脚本
生成包含ISO代码和地理坐标的国家元数据
用于前端可视化
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any


def get_project_root() -> Path:
    """
    获取项目根目录
    
    Returns:
        项目根目录的Path对象
    """
    script_path = Path(os.path.abspath(__file__))
    return script_path.parent.parent


def load_military_data(json_file: str) -> pd.DataFrame:
    """
    加载已转换的军事数据JSON文件
    
    Args:
        json_file: JSON文件路径
    
    Returns:
        包含数据的DataFrame
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        print(f"成功加载JSON数据: {json_file}, 形状: {df.shape}")
        return df
    except Exception as e:
        print(f"加载JSON数据 {json_file} 失败: {e}")
        return pd.DataFrame()


def generate_country_codes() -> Dict[str, str]:
    """
    生成国家名称到ISO代码的映射
    
    Returns:
        国家名称到ISO代码的字典映射
    """
    # 常用国家名称到ISO代码的映射
    # 这里只包含一部分主要国家，实际应用中可能需要更完整的映射
    return {
        "United States": "USA",
        "China": "CHN",
        "Russia": "RUS",
        "United Kingdom": "GBR",
        "UK": "GBR",
        "India": "IND",
        "France": "FRA",
        "Germany": "DEU",
        "Japan": "JPN",
        "South Korea": "KOR",
        "Korea, South": "KOR",
        "North Korea": "PRK",
        "Korea, North": "PRK",
        "Italy": "ITA",
        "Brazil": "BRA",
        "Canada": "CAN",
        "Australia": "AUS",
        "Spain": "ESP",
        "Turkey": "TUR",
        "Israel": "ISR",
        "Iran": "IRN",
        "Indonesia": "IDN",
        "Pakistan": "PAK",
        "Saudi Arabia": "SAU",
        "Poland": "POL",
        "Ukraine": "UKR",
        "Egypt": "EGY",
        "Thailand": "THA",
        "Colombia": "COL",
        "Mexico": "MEX",
        "Malaysia": "MYS",
        "Netherlands": "NLD",
        "Argentina": "ARG",
        "Sweden": "SWE",
        "Switzerland": "CHE",
        "Belgium": "BEL",
        "Norway": "NOR",
        "Vietnam": "VNM",
        "Portugal": "PRT",
        "Romania": "ROU",
        "Bangladesh": "BGD",
        "Greece": "GRC",
        "Czech Republic": "CZE",
        "Denmark": "DNK",
        "Finland": "FIN",
        "Austria": "AUT",
        "New Zealand": "NZL",
        "Singapore": "SGP",
        "South Africa": "ZAF",
        "Algeria": "DZA",
        "Chile": "CHL",
        "Hungary": "HUN",
        "Iraq": "IRQ",
        "Peru": "PER",
        "Philippines": "PHL",
        "Kazakhstan": "KAZ",
        "Morocco": "MAR"
        # 实际应用中应该添加更多国家
    }


def generate_country_coordinates() -> Dict[str, Dict[str, float]]:
    """
    生成国家名称到地理坐标的映射
    
    Returns:
        国家名称到地理坐标的字典映射
    """
    # 常用国家的大致地理坐标（经纬度）
    # 实际应用中可能需要更精确的坐标
    return {
        "United States": {"lat": 37.0902, "lon": -95.7129},
        "China": {"lat": 35.8617, "lon": 104.1954},
        "Russia": {"lat": 61.5240, "lon": 105.3188},
        "United Kingdom": {"lat": 55.3781, "lon": -3.4360},
        "UK": {"lat": 55.3781, "lon": -3.4360},
        "India": {"lat": 20.5937, "lon": 78.9629},
        "France": {"lat": 46.6034, "lon": 1.8883},
        "Germany": {"lat": 51.1657, "lon": 10.4515},
        "Japan": {"lat": 36.2048, "lon": 138.2529},
        "South Korea": {"lat": 35.9078, "lon": 127.7669},
        "Korea, South": {"lat": 35.9078, "lon": 127.7669},
        "North Korea": {"lat": 40.3399, "lon": 127.5101},
        "Korea, North": {"lat": 40.3399, "lon": 127.5101},
        "Italy": {"lat": 41.8719, "lon": 12.5674},
        "Brazil": {"lat": -14.2350, "lon": -51.9253},
        "Canada": {"lat": 56.1304, "lon": -106.3468},
        "Australia": {"lat": -25.2744, "lon": 133.7751},
        "Spain": {"lat": 40.4637, "lon": -3.7492},
        "Turkey": {"lat": 38.9637, "lon": 35.2433},
        "Israel": {"lat": 31.0461, "lon": 34.8516},
        "Iran": {"lat": 32.4279, "lon": 53.6880},
        "Indonesia": {"lat": -0.7893, "lon": 113.9213},
        "Pakistan": {"lat": 30.3753, "lon": 69.3451},
        "Saudi Arabia": {"lat": 23.8859, "lon": 45.0792},
        "Poland": {"lat": 51.9194, "lon": 19.1451},
        "Ukraine": {"lat": 48.3794, "lon": 31.1656},
        "Egypt": {"lat": 26.8206, "lon": 30.8025},
        "Thailand": {"lat": 15.8700, "lon": 100.9925},
        "Colombia": {"lat": 4.5709, "lon": -74.2973},
        "Mexico": {"lat": 23.6345, "lon": -102.5528}
        # 实际应用中应该添加更多国家
    }


def load_countries_from_data(data_dir: str) -> List[str]:
    """
    从已转换的数据中加载所有国家名称
    
    Args:
        data_dir: 数据目录
    
    Returns:
        国家名称列表
    """
    # 尝试从所有军事数据文件中加载国家
    all_data_file = os.path.join(data_dir, "all_military_data.json")
    if os.path.exists(all_data_file):
        df = load_military_data(all_data_file)
        if not df.empty and 'Country' in df.columns:
            return df['Country'].unique().tolist()
    
    # 如果没有找到合并数据，尝试从年份数据中加载
    year_file = os.path.join(data_dir, "year_2020.json")  # 使用2020年作为示例
    if os.path.exists(year_file):
        df = load_military_data(year_file)
        if not df.empty and 'Country' in df.columns:
            return df['Country'].unique().tolist()
    
    return []


def generate_country_metadata():
    """
    生成国家元数据并保存为JSON
    """
    project_root = get_project_root()
    
    # 输出目录
    output_dir = os.path.join(project_root, "web", "public", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载从军事数据中提取的国家列表
    countries = load_countries_from_data(output_dir)
    
    # 获取国家代码和坐标映射
    country_codes = generate_country_codes()
    country_coordinates = generate_country_coordinates()
    
    # 创建元数据字典
    metadata = {}
    for country in countries:
        metadata[country] = {
            "iso_code": country_codes.get(country, ""),
            "coordinates": country_coordinates.get(country, {"lat": 0, "lon": 0})
        }
    
    # 保存元数据
    output_file = os.path.join(output_dir, "country_metadata.json")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f"成功保存国家元数据: {output_file}")
    except Exception as e:
        print(f"保存国家元数据失败: {e}")


def main():
    """
    主函数
    """
    print("开始生成国家元数据...")
    generate_country_metadata()
    print("生成完成！")


if __name__ == "__main__":
    main() 