#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
军事数据转换批处理脚本
按顺序运行所有数据转换脚本
"""

import os
import sys
import time
import subprocess
from pathlib import Path


def get_script_dir() -> Path:
    """
    获取脚本目录
    
    Returns:
        脚本目录的Path对象
    """
    return Path(os.path.dirname(os.path.abspath(__file__)))


def run_script(script_name: str) -> bool:
    """
    运行指定的Python脚本
    
    Args:
        script_name: 脚本文件名
    
    Returns:
        脚本是否成功运行
    """
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, script_name)
    
    if not os.path.exists(script_path):
        print(f"错误: 脚本 {script_path} 不存在！")
        return False
    
    print(f"\n{'='*60}")
    print(f"正在运行脚本: {script_name}")
    print(f"{'='*60}\n")
    
    try:
        # 使用当前Python解释器运行脚本
        python_executable = sys.executable
        result = subprocess.run([python_executable, script_path], check=True)
        
        if result.returncode == 0:
            print(f"\n脚本 {script_name} 成功运行完成！")
            return True
        else:
            print(f"\n错误: 脚本 {script_name} 运行失败，返回码: {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"\n错误: 脚本 {script_name} 运行失败: {e}")
        return False
    except Exception as e:
        print(f"\n错误: 运行脚本 {script_name} 时发生异常: {e}")
        return False


def main():
    """
    主函数
    """
    start_time = time.time()
    
    print("开始批量转换军事数据...")
    
    # 要运行的脚本列表（按顺序）
    scripts = [
        "data_converter.py",
        "country_metadata.py"
    ]
    
    # 运行所有脚本
    success_count = 0
    failed_scripts = []
    
    for script in scripts:
        if run_script(script):
            success_count += 1
        else:
            failed_scripts.append(script)
    
    # 输出摘要
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n" + "="*60)
    print(f"批处理执行完毕！")
    print(f"总运行时间: {elapsed_time:.2f} 秒")
    print(f"成功: {success_count}/{len(scripts)} 个脚本")
    
    if failed_scripts:
        print("\n失败的脚本:")
        for script in failed_scripts:
            print(f"- {script}")
    
    print("="*60)


if __name__ == "__main__":
    main() 