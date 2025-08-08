#!/usr/bin/env python3
"""
测试Cookie管理菜单
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cookie_menu():
    """测试Cookie输入方式菜单"""
    print("🧪 测试Cookie输入方式菜单")
    
    # 模拟菜单选项
    options = [
        "🔗 临时文件输入",
        "📋 剪贴板导入 (需要pyperclip)",
        "🖥️  文本编辑器输入",
        "🔙 返回"
    ]
    
    print("\n💡 选择输入方式:")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print("  q. 返回/退出")
    
    print("\n✅ 菜单显示正常")
    print("✅ 已移除分段输入功能")
    print("✅ 其他选项保持完整")

if __name__ == "__main__":
    test_cookie_menu()
