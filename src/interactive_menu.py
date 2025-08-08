"""
交互式菜单系统
支持键盘上下键选择和鼠标点击（在支持的终端中）
"""

import sys
import os
import termios
import tty
import select
from typing import List, Any, Optional, Callable

class InteractiveMenu:
    """交互式菜单类"""
    
    def __init__(self):
        self.selected_index = 0
        self.options = []
        self.title = ""
        self.show_numbers = True
        
    def show_menu(self, title: str, options: List[str], show_numbers: bool = True, 
                  callbacks: Optional[List[Callable]] = None) -> int:
        """
        显示交互式菜单
        
        Args:
            title: 菜单标题
            options: 选项列表
            show_numbers: 是否显示编号
            callbacks: 选项对应的回调函数列表
            
        Returns:
            选中的选项索引
        """
        self.title = title
        self.options = options
        self.show_numbers = show_numbers
        self.selected_index = 0
        
        if not options:
            return -1
            
        while True:
            self._render_menu()
            key = self._get_key()
            
            if key == 'up' and self.selected_index > 0:
                self.selected_index -= 1
            elif key == 'down' and self.selected_index < len(options) - 1:
                self.selected_index += 1
            elif key == 'enter':
                return self.selected_index
            elif key == 'escape' or key == 'q':
                return -1
            elif key.isdigit():
                # 支持数字键快速选择
                num = int(key) - 1
                if 0 <= num < len(options):
                    self.selected_index = num
                    return num
                    
    def _render_menu(self):
        """渲染菜单"""
        # 清屏
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # 显示标题
        print(f"\n{self.title}")
        print("=" * len(self.title))
        print()
        
        # 显示选项
        for i, option in enumerate(self.options):
            prefix = ""
            if self.show_numbers:
                prefix = f"{i + 1:2d}. "
            
            if i == self.selected_index:
                # 高亮选中项
                print(f"\033[7m  ▶ {prefix}{option}\033[0m")
            else:
                print(f"    {prefix}{option}")
        
        print()
        print("💡 使用方式:")
        print("  ↑↓ 上下键选择")
        print("  Enter 确认选择")
        print("  数字键 快速选择")
        print("  ESC/Q 返回")
        
    def _get_key(self):
        """获取按键输入"""
        try:
            # 保存终端设置
            old_settings = termios.tcgetattr(sys.stdin)
            tty.cbreak(sys.stdin.fileno())
            
            # 读取按键
            ch = sys.stdin.read(1)
            
            # 处理特殊键
            if ch == '\x1b':  # ESC序列
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A':
                        return 'up'
                    elif ch3 == 'B':
                        return 'down'
                    elif ch3 == 'C':
                        return 'right'
                    elif ch3 == 'D':
                        return 'left'
                return 'escape'
            elif ch == '\r' or ch == '\n':
                return 'enter'
            elif ch == '\x03':  # Ctrl+C
                raise KeyboardInterrupt
            else:
                return ch.lower()
                
        except Exception:
            return ''
        finally:
            # 恢复终端设置
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            except:
                pass

class SimpleMenu:
    """简化的菜单类，适用于不支持termios的环境"""
    
    @staticmethod
    def show_menu(title: str, options: List[str], show_numbers: bool = True) -> int:
        """显示简单菜单"""
        print(f"\n{title}")
        print("=" * len(title))
        print()
        
        for i, option in enumerate(options):
            prefix = f"{i + 1}. " if show_numbers else ""
            print(f"  {prefix}{option}")
        
        print()
        
        while True:
            try:
                choice = input(f"请选择 (1-{len(options)}, q退出): ").strip().lower()
                
                if choice == 'q':
                    return -1
                
                index = int(choice) - 1
                if 0 <= index < len(options):
                    return index
                else:
                    print("❌ 无效选择，请重试")
                    
            except ValueError:
                print("❌ 请输入有效数字")
            except KeyboardInterrupt:
                return -1

def create_menu() -> InteractiveMenu:
    """创建菜单实例，自动检测终端能力"""
    try:
        # 检查是否支持termios
        if hasattr(sys.stdin, 'fileno') and os.isatty(sys.stdin.fileno()):
            import termios
            return InteractiveMenu()
    except (ImportError, OSError):
        pass
    
    # 返回简单菜单
    return SimpleMenu()
