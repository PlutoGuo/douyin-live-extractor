import os
import time
import re

def clear_screen():
    """清屏函数"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """打印程序横幅"""
    print("=" * 80)
    print("🎥 抖音直播流URL提取器 v2.0")
    print("=" * 80)
    print("✨ 功能: 自动提取抖音直播间的各清晰度流媒体URL")
    print("🔧 支持: m3u8 格式，多清晰度选择")
    print("=" * 80)

def show_progress(message, duration=2):
    """显示进度动画"""
    symbols = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for symbol in symbols:
            if time.time() >= end_time:
                break
            print(f"\r{symbol} {message}", end='', flush=True)
            time.sleep(0.1)
    print(f"\r✅ {message} - 完成!")

def get_user_input():
    """获取用户输入的直播间URL"""
    print("\n📝 请输入抖音直播间URL:")
    print("💡 示例1: https://live.douyin.com/143040673633")
    print("💡 示例2: https://www.douyin.com/follow/live/143040673633?r_id=fo_lh_143040673633&r_player=1")
    print("💡 或直接输入房间号: 143040673633")
    print("-" * 50)
    room_id = None
    while True:
        url_input = input("🔗 URL/房间号: ").strip()
        
        if not url_input:
            print("❌ 输入不能为空，请重新输入")
            continue
            
        # 如果只是数字，构造完整URL
        if url_input.isdigit():
            room_id = url_input
            url = f"https://live.douyin.com/{url_input}"
            print(f"✅ 已构造完整URL: {url}")
        elif url_input.startswith('https://live.douyin.com/'):
            url = url_input
            print(f"✅ 使用输入的URL: {url}")
        elif url_input.startswith('https://www.douyin.com/follow/live/'):
            # 提取房间号
            match = re.search(r'/follow/live/(\d+)', url_input)
            if match:
                room_id = match.group(1)
                url = f"https://live.douyin.com/{room_id}"
                print(f"✅ 已提取房间号并构造URL: {url}")
            else:
                print("❌ 无法从输入中提取房间号，请输入正确的URL")
                continue
        else:
            print("❌ 无效的URL格式，请输入正确的抖音直播间URL或房间号")
            continue
            
        # 直接返回解析出的URL和房间号
        return url, room_id

def show_help():
    """显示帮助信息"""
    clear_screen()
    print("❓ 使用帮助")
    print("=" * 50)
    print("""
🎯 程序功能:
  • 自动提取抖音直播间的m3u8流媒体URL
  • 支持多种清晰度 (原画质/超高清/高清/标清/流畅/极速)
  • 自动生成标准m3u8播放列表格式
  • 自动保存提取结果

🔧 使用步骤:
  1. 选择"提取直播流URL"
  2. 输入抖音直播间URL或房间号
  3. 等待程序自动解析
  4. 程序自动保存m3u8文件

💡 URL格式示例:
  • 完整URL: https://live.douyin.com/943807960472
  • 房间号: 943807960472

⚠️  注意事项:
  • 确保直播间正在直播
  • 网络连接稳定
  • 某些直播间可能有访问限制
  • 生成的m3u8文件可用于播放器播放

🔍 故障排除:
  • 如果提取失败，请检查直播状态
  • 如果连接超时，请检查网络
  • 可保存调试数据进行分析
    """)