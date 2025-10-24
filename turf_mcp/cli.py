"""
Turf-MCP 命令行接口模块
"""
import os
import sys
import argparse
from turf_mcp.main import setup

# 添加当前目录到 Python 路径，以便可以导入 turf_mcp 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def main():
    """主命令行入口"""
    parser = argparse.ArgumentParser(description="Turf-MCP 地理空间分析工具")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('-t', '--transport', default='stdio', choices=['stdio', 'http', 'sse'],  help='mcp服务传输模式 stdio http sse')
    parser.add_argument('-p', '--port', default=8000, type=int,  help='当使用HTTP或SSE模式启用的端口')

    # 这里可以添加更多子命令
    args = parser.parse_args()

    setup(transport=args.transport, port=args.port)


if __name__ == '__main__':
    main()