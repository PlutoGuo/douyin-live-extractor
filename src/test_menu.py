#!/usr/bin/env python3
"""
测试简单菜单系统
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simple_menu import create_simple_menu, SimpleMenuManager

def test_simple_menu():
    """测试简单菜单"""
    print("🧪 测试简单菜单系统")
    
    options = [
        "选项1",
        "选项2", 
        "选项3",
        "退出"
    ]
    
    result = create_simple_menu(options, "测试菜单")
    print(f"用户选择: {result}")
    
    if result is not None:
        print(f"选择了: {options[result]}")

def test_menu_manager():
    """测试菜单管理器"""
    print("🧪 测试菜单管理器")
    
    manager = SimpleMenuManager()
    options = [
        "🎯 功能1",
        "🎭 功能2",
        "💾 功能3",
        "🚪 退出"
    ]
    
    result = manager.show_menu("主菜单", options)
    print(f"菜单管理器返回: {result}")
    
    if result >= 0:
        print(f"选择了: {options[result]}")

if __name__ == "__main__":
    print("选择测试模式:")
    print("1. 测试简单菜单")
    print("2. 测试菜单管理器")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        test_simple_menu()
    elif choice == "2":
        test_menu_manager()
    else:
        print("无效选择")
