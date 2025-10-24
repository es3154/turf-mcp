"""
Turf-MCP 包初始化模块
"""

import os

# 在模块导入时自动执行的代码
def _run_on_import():
    """在模块导入时运行的函数"""
    # 检查是否需要执行初始配置
    config_dir = os.path.expanduser("~/.turf-mcp")
    if not os.path.exists(config_dir):
        # 只有在首次导入且没有配置时才执行基础配置
        _run_initial_setup()

def _run_initial_setup():
    """执行初始设置"""
    try:
        # 创建配置目录
        config_dir = os.path.expanduser("~/.turf-mcp")
        os.makedirs(config_dir, exist_ok=True)
        
        # 创建标记文件表示已完成初始配置
        init_flag = os.path.join(config_dir, ".initialized")
        if not os.path.exists(init_flag):
            with open(init_flag, 'w') as f:
                f.write("Initial setup completed")
            
            # 这里可以添加任何你希望在首次导入时自动执行的代码
            print("Turf-MCP: 初始配置已完成")
    except Exception as e:
        # 避免因权限等问题导致导入失败
        pass

# 当包被导入时自动执行
_run_on_import()

# 导入主要功能
from .cli import main

# 定义包的公共API
__all__ = ['main']