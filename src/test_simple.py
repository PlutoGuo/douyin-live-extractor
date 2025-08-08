#!/usr/bin/env python3
"""
简化的主程序测试
"""

import os
import sys

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🧪 测试简化主程序")
    
    try:
        from simple_menu import SimpleMenuManager
        print("✅ simple_menu 导入成功")
        
        manager = SimpleMenuManager()
        print("✅ 菜单管理器创建成功")
        
        options = ["选项1", "选项2", "退出"]
        print("✅ 准备显示菜单...")
        
        # 注释掉实际菜单显示避免交互
        # result = manager.show_menu("测试菜单", options)
        print("✅ 菜单系统准备就绪")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
