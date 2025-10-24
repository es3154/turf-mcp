#!/usr/bin/env python3
"""
Node.js 环境检测和安装脚本
仅适用于 Linux 环境
"""

import subprocess
import sys
import os
import platform
import argparse

from turf_mcp.main import setup


def check_node_installed():
    """检查 Node.js 是否已安装"""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Node.js 已安装，版本: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js 未安装")
        return False


def detect_linux_distro():
    """检测 Linux 发行版"""
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read()
        
        distro_info = {}
        for line in content.split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                distro_info[key] = value.strip('"')
        
        distro_id = distro_info.get('ID', '').lower()
        distro_id_like = distro_info.get('ID_LIKE', '').lower()
        
        print(f"检测到系统: {distro_info.get('NAME', 'Unknown')}")
        print(f"发行版 ID: {distro_id}")
        
        return distro_id, distro_id_like
    except Exception as e:
        print(f"❌ 无法检测 Linux 发行版: {e}")
        return None, None


def install_nodejs_debian_based():
    """在 Debian/Ubuntu 系统上安装 Node.js"""
    print("🔧 在 Debian/Ubuntu 系统上安装 Node.js...")
    
    try:
        # 更新包列表
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        
        # 安装 curl 和 gnupg（如果未安装）
        subprocess.run(['sudo', 'apt', 'install', '-y', 'curl', 'gnupg'], check=True)
        
        # 添加 NodeSource 仓库
        node_setup_script = 'https://deb.nodesource.com/setup_18.x'
        subprocess.run(['curl', '-fsSL', node_setup_script], 
                      check=True, stdout=subprocess.PIPE)
        
        # 执行安装脚本
        curl_cmd = ['curl', '-fsSL', node_setup_script]
        setup_script = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        
        # 使用 sudo 执行安装脚本
        subprocess.run(['sudo', '-E', 'bash', '-c', setup_script.stdout], check=True)
        
        # 安装 Node.js
        subprocess.run(['sudo', 'apt', 'install', '-y', 'nodejs'], check=True)
        
        print("✅ Node.js 安装成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        return False


def install_nodejs_redhat_based():
    """在 RHEL/CentOS/Fedora 系统上安装 Node.js"""
    print("🔧 在 RHEL/CentOS/Fedora 系统上安装 Node.js...")
    
    try:
        # 安装 curl（如果未安装）
        subprocess.run(['sudo', 'yum', 'install', '-y', 'curl'], check=True)
        
        # 添加 NodeSource 仓库
        node_setup_script = 'https://rpm.nodesource.com/setup_18.x'
        
        # 执行安装脚本
        curl_cmd = ['curl', '-fsSL', node_setup_script]
        setup_script = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        
        # 使用 sudo 执行安装脚本
        subprocess.run(['sudo', '-E', 'bash', '-c', setup_script.stdout], check=True)
        
        # 安装 Node.js
        subprocess.run(['sudo', 'yum', 'install', '-y', 'nodejs'], check=True)
        
        print("✅ Node.js 安装成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        return False


def install_nodejs_fallback():
    """使用包管理器的默认仓库安装 Node.js（备用方案）"""
    print("🔧 使用备用方案安装 Node.js...")
    
    try:
        # 尝试使用常见的包管理器
        package_managers = [
            ['apt', 'install', '-y', 'nodejs', 'npm'],
            ['yum', 'install', '-y', 'nodejs', 'npm'],
            ['dnf', 'install', '-y', 'nodejs', 'npm'],
            ['zypper', 'install', '-y', 'nodejs', 'npm'],
            ['pacman', '-S', '--noconfirm', 'nodejs', 'npm']
        ]
        
        for pkg_cmd in package_managers:
            try:
                subprocess.run(['sudo'] + pkg_cmd, check=True)
                print("✅ Node.js 安装成功（使用备用方案）")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
                
        print("❌ 所有安装方法都失败了")
        return False
        
    except Exception as e:
        print(f"❌ 备用安装方案失败: {e}")
        return False


def install_nodejs():
    """根据 Linux 发行版安装 Node.js"""
    distro_id, distro_id_like = detect_linux_distro()
    
    if not distro_id:
        print("❌ 无法确定 Linux 发行版，尝试备用安装方案")
        return install_nodejs_fallback()
    
    # Debian/Ubuntu 系列
    if distro_id in ['debian', 'ubuntu'] or any(like in distro_id_like for like in ['debian', 'ubuntu']):
        if install_nodejs_debian_based():
            return True
    
    # RHEL/CentOS/Fedora 系列
    elif distro_id in ['rhel', 'centos', 'fedora'] or any(like in distro_id_like for like in ['rhel', 'fedora']):
        if install_nodejs_redhat_based():
            return True
    
    # 其他发行版尝试备用方案
    print(f"⚠️  不支持的发行版: {distro_id}，尝试备用安装方案")
    return install_nodejs_fallback()


def main():
    """主函数"""
    
    # 检查操作系统
    if platform.system() != 'Linux':
        print("❌ 此脚本仅适用于 Linux 环境")
        sys.exit(1)
    
    # 检查当前用户权限
    if os.geteuid() != 0:
        print("⚠️  建议使用 sudo 运行此脚本以获得安装权限")
    
    print("🔍 检查 Node.js 环境...")
    
    # 检查是否已安装 Node.js
    if check_node_installed() :
        print("✅ Node.js 环境就绪")

    else:
        # 安装 Node.js
        print("🚀 开始安装 Node.js...")
        if install_nodejs():
            # 验证安装
            if check_node_installed():
                print("🎉 Node.js 环境配置完成！")
            else:
                print("❌ 安装后验证失败")
                sys.exit(1)
        else:
            print("❌ Node.js 安装失败")
            sys.exit(1)

    setup("http")


if __name__ == '__main__':
    main()
