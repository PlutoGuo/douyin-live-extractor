import time
import os
from datetime import datetime

from config import get_save_directory, set_save_directory
from ui import clear_screen, print_banner, get_user_input, show_help
from file_utils import ensure_directory_exists, open_current_directory, show_directory_files
from network import request_douyin_live
from cookie_manager import manage_cookies
from streamer_manager import get_streamers_list, remove_streamer_record, format_time_ago, clean_old_records
from iina_player import open_streamer_file, open_with_player, find_streamer_m3u8_file
from interactive_menu import create_menu
from simple_menu import create_menu as create_simple_menu_manager

def main_menu():
    """主菜单"""
    # 初始化时确保默认目录存在
    ensure_directory_exists(get_save_directory())
    
    menu = create_simple_menu_manager()
    
    while True:
        clear_screen()
        print_banner()
        
        # 菜单选项
        options = [
            "🎯 提取直播流URL",
            "🎭 查看提取过的主播", 
            "💾 文件存储设置",
            "🍪 Cookie管理",
            "❓ 使用帮助"
        ]
        
        choice = menu.show_menu("📋 主菜单", options)
        
        if choice == -1:  # 用户按q退出
            print("\n👋 感谢使用抖音直播流URL提取器!")
            break
        elif choice == 0:  # 提取直播流URL
            url, live_id = get_user_input()
            if url:
                print(f"\n🚀 开始处理: {url}")
                response = request_douyin_live(url,live_id)
                
                if response:
                    print("\n✅ 处理完成!")
                else:
                    print("\n❌ 处理失败!")
                
                input("\n按回车键继续...")
                
        elif choice == 1:  # 查看主播列表
            show_streamers_list()
            
        elif choice == 2:  # 文件存储设置
            show_storage_settings()
            
        elif choice == 3:  # Cookie管理
            manage_cookies()
            
        elif choice == 4:  # 使用帮助
            show_help()
            input("\n按回车键返回主菜单...")

def show_streamers_list():
    """显示提取过的主播列表"""
    menu = create_simple_menu_manager()
    
    while True:
        clear_screen()
        print("🎭 提取过的主播列表")
        print("=" * 50)
        
        # 获取主播列表
        streamers = get_streamers_list()
        
        if not streamers:
            print("📝 暂无提取过的主播记录")
            print("\n💡 提示: 提取直播流后，主播信息将自动记录在此")
            input("\n按回车键返回...")
            return
        
        print(f"📊 共记录了 {len(streamers)} 位主播:")
        print()
        
        # 显示主播列表
        for i, streamer in enumerate(streamers, 1):
            nickname = streamer['nickname']
            last_time = format_time_ago(streamer['last_extract_time'])
            success_rate = streamer['success_rate']
            total_extracts = streamer['total_extracts']
            
            # 状态图标
            if success_rate >= 80:
                status_icon = "✅"
            elif success_rate >= 50:
                status_icon = "⚠️"
            else:
                status_icon = "❌"
            
            print(f"  {i:2d}. {status_icon} {nickname}")
            print(f"      🕒 最后提取: {last_time}")
            print(f"      📊 成功率: {success_rate:.0f}% ({streamer['successful_extracts']}/{total_extracts})")
            if streamer['room_id']:
                print(f"      🏠 直播间ID: {streamer['room_id']}")
            print()
        
        # 创建简化的主播选择菜单
        streamer_options = []
        for i, streamer in enumerate(streamers):
            nickname = streamer['nickname']
            last_time = format_time_ago(streamer['last_extract_time'])
            success_rate = streamer['success_rate']
            
            # 状态图标
            if success_rate >= 80:
                status_icon = "✅"
            elif success_rate >= 50:
                status_icon = "⚠️"
            else:
                status_icon = "❌"
            
            streamer_options.append(f"{status_icon} {nickname} ({last_time})")
        
        # 添加管理选项
        management_options = [
            "🧹 清理30天前的旧记录",
            "🗑️ 删除指定主播记录", 
            "🔄 刷新列表",
            "🔙 返回主菜单"
        ]
        
        all_options = streamer_options + management_options
        choice = menu.show_menu("📋 选择操作", all_options)
        
        if choice == -1 or choice == len(all_options) - 1:  # 返回主菜单
            break
        elif choice == len(all_options) - 2:  # 刷新列表
            continue
        elif choice == len(all_options) - 3:  # 删除主播记录
            delete_streamer_record(streamers)
        elif choice == len(all_options) - 4:  # 清理旧记录
            clean_old_streamers()
        else:
            # 处理主播操作 - 显示二级菜单
            if 0 <= choice < len(streamers):
                show_streamer_actions(streamers[choice])

def show_streamer_actions(streamer):
    """显示单个主播的操作菜单"""
    menu = create_simple_menu_manager()
    
    while True:
        clear_screen()
        print(f"🎭 主播操作 - {streamer['nickname']}")
        print("=" * 50)
        
        # 显示主播详细信息
        print(f"📺 主播昵称: {streamer['nickname']}")
        if streamer['room_id']:
            print(f"🏠 直播间ID: {streamer['room_id']}")
        print(f"🕒 最后提取: {format_time_ago(streamer['last_extract_time'])}")
        print(f"📊 成功率: {streamer['success_rate']:.0f}% ({streamer['successful_extracts']}/{streamer['total_extracts']})")
        print()
        
        # 操作选项
        action_options = [
            "🎯 重新提取直播流",
            "🎬 播放已保存的直播流",
            "🗑️ 删除此主播记录",
            "🔙 返回主播列表"
        ]
        
        action_choice = menu.show_menu("选择操作", action_options)
        
        if action_choice == -1 or action_choice == 3:  # 返回
            break
        elif action_choice == 0:  # 重新提取
            re_extract_streamer(streamer)
            break
        elif action_choice == 1:  # 播放
            play_streamer_file(streamer)
        elif action_choice == 2:  # 删除
            if delete_single_streamer(streamer):
                break  # 删除成功后返回主播列表

def delete_single_streamer(streamer):
    """删除单个主播记录"""
    menu = create_simple_menu_manager()
    
    confirm_options = [
        f"✅ 确认删除 '{streamer['nickname']}'",
        "❌ 取消"
    ]
    
    confirm_choice = menu.show_menu(f"确认删除主播 '{streamer['nickname']}' 吗？", confirm_options)
    
    if confirm_choice == 0:  # 确认删除
        if remove_streamer_record(streamer['room_id']):
            print(f"✅ 已删除主播 '{streamer['nickname']}' 的记录")
            input("按回车键继续...")
            return True
        else:
            print(f"❌ 删除失败")
            input("按回车键继续...")
    
    return False

def play_streamer_file(streamer):
    """播放指定主播的直播流文件"""
    print(f"\n🎬 播放主播: {streamer['nickname']}")
    
    save_dir = get_save_directory()
    filepath = find_streamer_m3u8_file(streamer['nickname'], save_dir)
    
    if not filepath:
        print(f"❌ 未找到主播 '{streamer['nickname']}' 的直播流文件")
        print("💡 提示: 请先提取该主播的直播流")
        input("按回车键继续...")
        return
    
    print(f"📁 找到文件: {os.path.basename(filepath)}")
    
    # 直接用IINA打开，不再询问
    if open_with_player(filepath):
        print(f"🎉 已启动播放: {streamer['nickname']}")
    
    input("\n按回车键继续...")

def re_extract_streamer(streamer):
    """重新提取指定主播的直播流"""
    print(f"\n🚀 开始重新提取主播: {streamer['nickname']}")
    
    live_url = streamer['live_url']
    room_id = streamer['room_id']
    if not live_url:
        print("❌ 该主播没有保存直播间URL，无法重新提取")
        input("按回车键继续...")
        return
    
    print(f"🔗 直播间URL: {live_url}")
    
    # 调用网络请求功能
    print(f"\n🌐 正在连接到直播间...")
    response = request_douyin_live(live_url, room_id)
    
    if response:
        print("\n✅ 重新提取完成!")
        print(f"📝 主播 {streamer['nickname']} 的记录已更新")
        
        # 询问是否要播放刚更新的文件
        play_choice = input("\n🎬 是否要播放刚更新的直播流? (y/n): ").lower()
        if play_choice in ['y', 'yes', '是', '']:
            save_dir = get_save_directory()
            filepath = find_streamer_m3u8_file(streamer['nickname'], save_dir)
            if filepath and open_with_player(filepath):
                print(f"🎉 已启动播放: {streamer['nickname']}")
    else:
        print("\n❌ 重新提取失败!")
        print("💡 可能的原因:")
        print("  • 主播当前未开播")
        print("  • 直播间URL已失效")
        print("  • 网络连接问题")
        print("  • Cookie需要更新")
        print("  • 网络连接问题")
        print("  • Cookie需要更新")
    
    input("\n按回车键继续...")

def clean_old_streamers():
    """清理旧的主播记录"""
    print("\n🧹 清理旧记录")
    print("-" * 30)
    
    confirm = input("❓ 确认删除30天前的主播记录吗? (y/n): ").lower()
    if confirm not in ['y', 'yes', '是']:
        print("🔄 操作已取消")
        input("按回车键继续...")
        return
    
    removed_count = clean_old_records(30)
    
    if removed_count > 0:
        print(f"✅ 已清理 {removed_count} 条旧记录")
    else:
        print("ℹ️ 没有找到需要清理的旧记录")
    
    input("按回车键继续...")

def delete_streamer_record(streamers):
    """删除指定主播记录"""
    menu = create_simple_menu_manager()
    
    print("\n🗑️ 删除主播记录")
    print("-" * 30)
    
    # 创建主播选择列表
    streamer_options = []
    for streamer in streamers:
        nickname = streamer['nickname']
        last_time = format_time_ago(streamer['last_extract_time'])
        streamer_options.append(f"🗑️ {nickname} (最后提取: {last_time})")
    
    streamer_options.append("🔙 取消删除")
    
    choice = menu.show_menu("选择要删除的主播", streamer_options)
    
    if choice == -1 or choice == len(streamers):  # 取消
        print("🔄 操作已取消")
        input("按回车键继续...")
        return
    
    if 0 <= choice < len(streamers):
        streamer = streamers[choice]
        
        print(f"\n📋 主播信息:")
        print(f"  👤 昵称: {streamer['nickname']}")
        print(f"  🏠 直播间ID: {streamer['room_id']}")
        print(f"  📊 提取次数: {streamer['total_extracts']}")
        print(f"  🕒 最后提取: {format_time_ago(streamer['last_extract_time'])}")
        
        # 确认删除
        confirm_options = [
            f"✅ 确认删除 '{streamer['nickname']}'",
            "❌ 取消删除"
        ]
        
        confirm_choice = menu.show_menu(f"确认删除主播 '{streamer['nickname']}' 吗？", confirm_options)
        
        if confirm_choice == 0:  # 确认删除
            if remove_streamer_record(streamer['key']):
                print(f"✅ 已删除主播 '{streamer['nickname']}' 的记录")
            else:
                print("❌ 删除失败")
        else:
            print("🔄 操作已取消")
    
    input("按回车键继续...")

def show_storage_settings():
    """显示存储设置菜单"""
    menu = create_simple_menu_manager()
    
    while True:
        clear_screen()
        print("💾 文件存储设置")
        print("=" * 50)
        print(f"\n📁 当前保存目录:")
        print(f"   {get_save_directory()}")
        
        # 检查目录是否存在
        if os.path.exists(get_save_directory()):
            print("   ✅ 目录存在")
        else:
            print("   ❌ 目录不存在 (将自动创建)")
        
        # 菜单选项
        options = [
            "🔧 修改保存目录",
            "📂 打开当前目录", 
            "🏠 重置为默认目录",
            "📝 查看目录中的文件",
            "🔙 返回主菜单"
        ]
        
        choice = menu.show_menu("📋 存储设置选项", options)
        
        if choice == -1 or choice == 4:  # 返回主菜单
            break
        elif choice == 0:  # 修改保存目录
            change_save_directory()
        elif choice == 1:  # 打开当前目录
            open_current_directory(get_save_directory())
            input("按回车键继续...")
        elif choice == 2:  # 重置为默认目录
            reset_default_directory()
        elif choice == 3:  # 查看目录文件
            show_directory_files(get_save_directory())
            input("按回车键继续...")

def change_save_directory():
    """修改保存目录"""
    print("\n🔧 修改保存目录")
    print("-" * 30)
    print(f"📁 当前目录: {get_save_directory()}")
    print("\n💡 提示:")
    print("  • 可使用 ~ 表示用户主目录")
    print("  • 例如: ~/Documents/MyStreams")
    print("  • 或绝对路径: /Users/username/Documents/MyStreams")
    
    new_directory = input("\n📝 请输入新的保存目录: ").strip()
    
    if not new_directory:
        print("❌ 目录不能为空")
        input("按回车键继续...")
        return
    
    if set_save_directory(new_directory):
        print(f"✅ 保存目录已更新为: {get_save_directory()}")
    else:
        print("❌ 设置目录失败")
    
    input("按回车键继续...")

def reset_default_directory():
    """重置为默认目录"""
    menu = create_simple_menu_manager()
    default_dir = os.path.expanduser('~/Documents/直播源/抖音直播源')
    
    print(f"\n🏠 重置为默认目录")
    print(f"默认目录: {default_dir}")
    
    options = [
        "✅ 确认重置为默认目录",
        "❌ 取消操作"
    ]
    
    choice = menu.show_menu("确认重置？", options)
    
    if choice == 0:  # 确认重置
        if set_save_directory(default_dir):
            print("✅ 已重置为默认目录")
        else:
            print("❌ 重置失败")
    else:
        print("🔄 操作已取消")
    
    input("按回车键继续...")

def run():
    """程序入口函数"""
    # 确保默认目录存在
    ensure_directory_exists(get_save_directory())
    
    # 打印欢迎横幅
    print_banner()
    
    # 进入主菜单
    main_menu()
    
    print("\n👋 程序已退出，感谢使用！")

if __name__ == "__main__":
    run()