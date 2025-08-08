"""
简化的菜单系统 - 稳定版本
避免 termios 相关的闪烁问题
"""

import os

class SimpleMenuManager:
    """简单菜单管理器"""
    
    def show_menu(self, title, options):
        """显示菜单并返回选择的索引"""
        while True:
            # 清屏
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print(f"\n{title}")
            print("=" * 50)
            print()
            
            # 显示选项
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
            
            print("  q. 返回/退出")
            
            # 获取用户输入
            try:
                choice = input(f"\n请选择 (1-{len(options)}, q): ").strip().lower()
                
                if choice == 'q':
                    return -1
                
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(options):
                        return index
                
                print("❌ 无效选择，请重试")
                input("按回车键继续...")
                
            except KeyboardInterrupt:
                return -1
            except Exception as e:
                print(f"❌ 输入错误: {e}")
                input("按回车键继续...")

def create_menu():
    """创建菜单管理器 - 兼容原有接口"""
    return SimpleMenuManager()

def create_simple_menu(options, title="请选择"):
    """
    创建简单的数字选择菜单 - 直接返回选择的索引
    """
    while True:
        # 清屏
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"\n{title}")
        print("=" * 50)
        print()
        
        # 显示选项
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        print("  q. 返回/退出")
        
        # 获取用户输入
        try:
            choice = input(f"\n请选择 (1-{len(options)}, q): ").strip().lower()
            
            if choice == 'q':
                return None
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(options):
                    return index
            
            print("❌ 无效选择，请重试")
            input("按回车键继续...")
            
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print(f"❌ 输入错误: {e}")
            input("按回车键继续...")
