#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
军事力量可视化应用程序
主程序入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入，不使用src前缀
from ui.app import MilitaryPowerApp

if __name__ == "__main__":
    app = MilitaryPowerApp()
    app.run() 