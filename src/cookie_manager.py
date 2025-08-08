import os
import time
from datetime import datetime

from config import CONFIG, get_current_cookie, set_custom_cookie
from file_utils import ensure_directory_exists
from ui import clear_screen
from simple_menu import create_simple_menu

def manage_cookies():
    """Cookie管理菜单"""
    while True:
        clear_screen()
        print("🍪 Cookie管理")
        print("=" * 50)
        
        # 显示当前Cookie状态
        current_cookie = get_current_cookie()
        if current_cookie:
            print(f"📄 当前Cookie状态: ✅ 已设置 ({len(current_cookie)} 字符)")
            if len(current_cookie) > 100:
                print(f"📝 Cookie预览: {current_cookie[:50]}...{current_cookie[-50:]}")
            else:
                print(f"📝 Cookie内容: {current_cookie}")
        else:
            print("📄 当前Cookie状态: ❌ 未设置 (使用默认Cookie)")
        
        # 检查Cookie文件
        cookie_file = CONFIG['cookie_file']
        if os.path.exists(cookie_file):
            file_size = os.path.getsize(cookie_file)
            mod_time = datetime.fromtimestamp(os.path.getmtime(cookie_file))
            print(f"📁 Cookie文件: ✅ 存在 ({file_size} bytes, {mod_time.strftime('%Y-%m-%d %H:%M')})")
        else:
            print("📁 Cookie文件: ❌ 不存在")
        
        print("\n📋 操作选项:")
        options = [
            "✏️  手动输入Cookie",
            "📁 从文件导入Cookie", 
            "💾 保存当前Cookie到文件",
            "🔧 使用Cookie文件中的Cookie",
            "🧹 清除当前Cookie",
            "❓ Cookie获取帮助",
            "🔙 返回主菜单"
        ]
        
        choice_index = create_simple_menu(options, "请选择操作")
        if choice_index is None:
            break
            
        if choice_index == 0:
            input_cookie_manually()
        elif choice_index == 1:
            import_cookie_from_file()
        elif choice_index == 2:
            save_cookie_to_file()
        elif choice_index == 3:
            load_cookie_from_file()
        elif choice_index == 4:
            clear_current_cookie()
        elif choice_index == 5:
            show_cookie_help()
        elif choice_index == 6:
            break

def input_cookie_manually():
    """手动输入Cookie - 多种输入方式"""
    print("\n✏️ 手动输入Cookie")
    print("=" * 40)
    print("💡 选择输入方式:")
    
    options = [
        "🔗 临时文件输入",
        "📋 剪贴板导入 (需要pyperclip)",
        "🖥️  文本编辑器输入",
        "🔙 返回"
    ]
    
    choice_index = create_simple_menu(options, "请选择输入方式")
    if choice_index is None:
        return
        
    if choice_index == 0:
        input_cookie_by_temp_file()
    elif choice_index == 1:
        input_cookie_by_clipboard()
    elif choice_index == 2:
        input_cookie_by_editor()
    elif choice_index == 3:
        return

# 其他Cookie相关函数实现...
# [此处省略了其他Cookie功能函数，如: input_cookie_by_segments(), validate_cookie(), 等]
# 完整实现请参考原代码

def input_cookie_by_temp_file():
    """通过临时文件输入Cookie"""
    print("\n🔗 临时文件输入Cookie")
    print("-" * 30)
    
    # 创建临时文件路径
    temp_dir = os.path.expanduser('~/Documents/直播源/抖音直播源/temp')
    ensure_directory_exists(temp_dir)
    temp_file = os.path.join(temp_dir, 'temp_cookie_input.txt')
    
    try:
        # 创建临时文件并写入说明
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("# 请将Cookie内容粘贴到下面这行\n")
            f.write("# 删除本行注释，然后粘贴完整的Cookie\n")
            f.write("\n")
        
        print(f"📁 临时文件已创建: {temp_file}")
        print("\n💡 操作步骤:")
        print("  1. 程序将自动打开临时文件")
        print("  2. 删除文件中的注释行")
        print("  3. 粘贴完整的Cookie内容")
        print("  4. 保存文件并关闭编辑器")
        print("  5. 回到此界面按回车继续")
        
        # 打开文件编辑器
        try:
            os.system(f'open -t "{temp_file}"')  # macOS TextEdit
        except:
            try:
                os.system(f'nano "{temp_file}"')  # 终端编辑器
            except:
                print(f"❌ 无法自动打开编辑器，请手动编辑文件: {temp_file}")
        
        input("\n⏳ 编辑完成后按回车键继续...")
        
        # 读取文件内容
        if os.path.exists(temp_file):
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # 解析内容
            cookie_str = parse_cookie_file_content(content)
            
            if cookie_str:
                print(f"✅ 从临时文件读取成功!")
                print(f"📊 Cookie长度: {len(cookie_str)} 字符")
                validate_and_save_cookie(cookie_str)
            else:
                print("❌ 临时文件中未找到有效的Cookie内容")
                input("按回车键继续...")
            
            # 清理临时文件
            try:
                os.remove(temp_file)
                print("🧹 临时文件已清理")
            except:
                print(f"⚠️ 请手动删除临时文件: {temp_file}")
        else:
            print("❌ 临时文件不存在")
            input("按回车键继续...")
            
    except Exception as e:
        print(f"❌ 临时文件操作失败: {e}")
        input("按回车键继续...")

def input_cookie_by_clipboard():
    """从剪贴板导入Cookie"""
    print("\n📋 剪贴板导入Cookie")
    print("-" * 30)
    
    try:
        import pyperclip
        
        print("💡 操作步骤:")
        print("  1. 复制完整的Cookie到剪贴板")
        print("  2. 按回车键从剪贴板读取")
        
        input("📋 准备好后按回车键...")
        
        # 从剪贴板读取
        clipboard_content = pyperclip.paste()
        
        if clipboard_content and len(clipboard_content.strip()) > 10:
            cookie_str = clipboard_content.strip()
            print(f"✅ 从剪贴板读取成功!")
            print(f"📊 Cookie长度: {len(cookie_str)} 字符")
            print(f"📄 内容预览: {cookie_str[:50]}...{cookie_str[-50:]}")
            
            validate_and_save_cookie(cookie_str)
        else:
            print("❌ 剪贴板内容为空或过短")
            input("按回车键继续...")
            
    except ImportError:
        print("❌ 未安装pyperclip库")
        print("💡 安装方法: pip install pyperclip")
        print("🔄 或选择其他输入方式")
        input("按回车键继续...")
    except Exception as e:
        print(f"❌ 剪贴板操作失败: {e}")
        input("按回车键继续...")

def input_cookie_by_editor():
    """使用系统文本编辑器输入Cookie"""
    print("\n🖥️ 文本编辑器输入Cookie")
    print("-" * 30)
    
    # 创建临时编辑文件
    temp_dir = os.path.expanduser('~/Documents/直播源/抖音直播源/temp')
    ensure_directory_exists(temp_dir)
    edit_file = os.path.join(temp_dir, 'cookie_editor.txt')
    
    try:
        # 创建编辑模板
        template = """# 抖音直播Cookie编辑器
# 请在下方粘贴完整的Cookie内容
# 删除所有注释行（以#开头的行）
# 保存文件后关闭编辑器

"""
        
        with open(edit_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"📝 编辑文件: {edit_file}")
        print("\n💡 支持的编辑器:")
        
        editor_options = [
            "🍎 macOS TextEdit (默认)",
            "🖥️  Visual Studio Code",
            "⚡ Vim/Nano (终端)",
            "📝 自定义编辑器"
        ]
        
        choice_index = create_simple_menu(editor_options, "选择编辑器")
        if choice_index is None:
            return
            
        if choice_index == 0:
            os.system(f'open -t "{edit_file}"')
        elif choice_index == 1:
            os.system(f'code "{edit_file}"')
        elif choice_index == 2:
            editor = input("输入编辑器命令 (vim/nano): ").strip()
            if editor in ['vim', 'nano']:
                os.system(f'{editor} "{edit_file}"')
            else:
                print("❌ 不支持的编辑器")
                return
        elif choice_index == 3:
            custom_cmd = input("输入自定义编辑器命令: ").strip()
            if custom_cmd:
                os.system(f'{custom_cmd} "{edit_file}"')
        else:
            print("❌ 无效选择，使用默认编辑器")
            os.system(f'open -t "{edit_file}"')
        
        input("\n⏳ 编辑完成后按回车继续...")
        
        # 读取编辑结果
        if os.path.exists(edit_file):
            with open(edit_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cookie_str = parse_cookie_file_content(content)
            
            if cookie_str:
                print(f"✅ 编辑器输入成功!")
                print(f"📊 Cookie长度: {len(cookie_str)} 字符")
                validate_and_save_cookie(cookie_str)
            else:
                print("❌ 编辑文件中未找到有效的Cookie内容")
                input("按回车键继续...")
            
            # 清理编辑文件
            cleanup_choice = input("🧹 是否删除编辑文件? (y/n): ").lower()
            if cleanup_choice in ['y', 'yes', '是']:
                try:
                    os.remove(edit_file)
                    print("✅ 编辑文件已删除")
                except:
                    print(f"⚠️ 请手动删除: {edit_file}")
        else:
            print("❌ 编辑文件不存在")
            input("按回车键继续...")
            
    except Exception as e:
        print(f"❌ 编辑器操作失败: {e}")
        input("按回车键继续...")

def validate_and_save_cookie(cookie_str):
    """验证并保存Cookie"""
    print(f"\n🔍 验证Cookie格式...")
    
    if validate_cookie(cookie_str):
        CONFIG['custom_cookie'] = cookie_str
        print(f"✅ Cookie验证成功并已设置!")
        print(f"📊 Cookie统计:")
        print(f"  • 长度: {len(cookie_str)} 字符")
        print(f"  • 包含 '=' 数量: {cookie_str.count('=')}")
        print(f"  • 包含 ';' 数量: {cookie_str.count(';')}")
        
        # 检查关键字段
        key_fields = ['UIFID', 'odin_tt', '__ac_nonce', 'passport_csrf_token']
        found_fields = [field for field in key_fields if field in cookie_str]
        print(f"  • 关键字段: {', '.join(found_fields) if found_fields else '无'}")
        
        # 询问是否保存到文件
        save_choice = input("\n💾 是否保存到文件以便下次使用? (y/n): ").lower()
        if save_choice in ['y', 'yes', '是']:
            save_cookie_to_file()
    else:
        print("❌ Cookie格式验证失败")
        print("💡 可能的问题:")
        print("  • Cookie格式不正确")
        print("  • 缺少必要的抖音字段")
        print("  • 内容被截断或损坏")
        
        # 提供调试选项
        debug_choice = input("\n🔧 是否查看详细调试信息? (y/n): ").lower()
        if debug_choice in ['y', 'yes', '是']:
            print(f"\n🔍 调试信息:")
            print(f"  • Cookie长度: {len(cookie_str)}")
            print(f"  • 前100字符: {cookie_str[:100]}")
            print(f"  • 后100字符: {cookie_str[-100:]}")
            print(f"  • 包含'='号: {'是' if '=' in cookie_str else '否'}")
            print(f"  • 包含抖音字段: {'是' if any(field in cookie_str for field in ['UIFID', 'odin_tt']) else '否'}")
    
    input("\n按回车键继续...")

def import_cookie_from_file():
    """从文件导入Cookie"""
    print("\n📁 从文件导入Cookie")
    print("=" * 40)
    print("💡 支持的文件格式:")
    print("  • .txt 文本文件")
    print("  • .json JSON格式")
    print("  • Netscape格式")
    print()
    
    file_path = input("📝 请输入Cookie文件路径: ").strip()
    
    if not file_path:
        print("❌ 文件路径不能为空")
        input("按回车键继续...")
        return
    
    # 展开用户目录
    file_path = os.path.expanduser(file_path)
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        input("按回车键继续...")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 尝试解析不同格式
        cookie_str = parse_cookie_file_content(content)
        
        if cookie_str and validate_cookie(cookie_str):
            CONFIG['custom_cookie'] = cookie_str
            print(f"\n✅ Cookie导入成功!")
            print(f"📊 Cookie长度: {len(cookie_str)} 字符")
            print(f"📁 源文件: {file_path}")
        else:
            print("❌ Cookie格式验证失败或文件内容无效")
            
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
    
    input("按回车键继续...")

def save_cookie_to_file():
    """保存当前Cookie到文件"""
    current_cookie = get_current_cookie()
    if not current_cookie:
        print("❌ 当前没有设置Cookie")
        input("按回车键继续...")
        return
    
    print("\n💾 保存Cookie到文件")
    print("=" * 30)
    
    # 确保保存目录存在
    cookie_dir = os.path.dirname(CONFIG['cookie_file'])
    ensure_directory_exists(cookie_dir)
    
    try:
        with open(CONFIG['cookie_file'], 'w', encoding='utf-8') as f:
            f.write(f"# 抖音直播Cookie\n")
            f.write(f"# 保存时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Cookie长度: {len(current_cookie)} 字符\n\n")
            f.write(current_cookie)
        
        print(f"✅ Cookie已保存到: {CONFIG['cookie_file']}")
        print(f"📊 文件大小: {len(current_cookie)} 字符")
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")
    
    input("按回车键继续...")

def load_cookie_from_file():
    """从默认文件加载Cookie"""
    cookie_file = CONFIG['cookie_file']
    
    if not os.path.exists(cookie_file):
        print(f"❌ Cookie文件不存在: {cookie_file}")
        input("按回车键继续...")
        return
    
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 解析文件内容
        cookie_str = parse_cookie_file_content(content)
        
        if cookie_str and validate_cookie(cookie_str):
            CONFIG['custom_cookie'] = cookie_str
            print(f"✅ Cookie加载成功!")
            print(f"📊 Cookie长度: {len(cookie_str)} 字符")
        else:
            print("❌ Cookie文件格式无效")
            
    except Exception as e:
        print(f"❌ 加载失败: {e}")
    
    input("按回车键继续...")

def clear_current_cookie():
    """清除当前Cookie"""
    if CONFIG['custom_cookie']:
        confirm = input("❓ 确认清除当前Cookie设置吗? (y/n): ").lower()
        if confirm in ['y', 'yes', '是']:
            CONFIG['custom_cookie'] = None
            print("✅ Cookie已清除，将使用默认Cookie")
        else:
            print("🔄 操作已取消")
    else:
        print("ℹ️ 当前没有自定义Cookie")
    
    input("按回车键继续...")

def show_cookie_help():
    """显示Cookie获取帮助"""
    clear_screen()
    print("❓ Cookie获取帮助")
    print("=" * 50)
    print("""
🍪 什么是Cookie?
  • Cookie是浏览器存储的用户身份验证信息
  • 用于访问需要登录的抖音直播间
  • 可以提高请求成功率和稳定性

🔧 如何获取Cookie?
  1. 使用Chrome浏览器打开抖音直播页面
  2. 按F12打开开发者工具
  3. 切换到Network(网络)标签
  4. 刷新页面，找到第一个请求
  5. 右键 → Copy → Copy as cURL
  6. 在cURL命令中找到 -H 'cookie: ...' 部分
  7. 复制引号内的完整Cookie内容

📝 Cookie格式示例:
  enter_pc_once=1; UIFID_TEMP=xxx; hevc_supported=true; ...

⚠️ 注意事项:
  • Cookie包含敏感信息，请勿泄露
  • Cookie有时效性，失效后需重新获取
  • 不同浏览器的Cookie可能不同
  • 建议保存到文件以便重复使用

🔍 故障排除:
  • 如果请求失败，尝试更新Cookie
  • 确保Cookie来源于相同的抖音域名
  • 检查Cookie是否完整，没有截断
    """)
    
    input("按回车键继续...")

def parse_cookie_file_content(content):
    """解析Cookie文件内容"""
    lines = content.split('\n')
    cookie_parts = []
    
    for line in lines:
        line = line.strip()
        # 跳过注释行和空行
        if not line or line.startswith('#'):
            continue
        
        # 如果看起来像Cookie格式
        if '=' in line and (';' in line or len(line) > 50):
            cookie_parts.append(line)
    
    # 拼接所有Cookie部分
    if cookie_parts:
        return ' '.join(cookie_parts)
    
    # 如果没找到明显的Cookie格式，返回去除注释的内容
    non_comment_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
    if non_comment_lines:
        return ' '.join(non_comment_lines)
    
    return None

def validate_cookie(cookie_str):
    """验证Cookie格式"""
    if not cookie_str or len(cookie_str) < 10:
        return False
    
    # 基本格式检查：应该包含key=value格式
    if '=' not in cookie_str:
        return False
    
    # 检查是否包含常见的抖音Cookie字段
    common_fields = ['UIFID', 'odin_tt', '__ac_nonce', 'passport_csrf_token']
    has_douyin_fields = any(field in cookie_str for field in common_fields)
    
    return has_douyin_fields

    """获取当前使用的Cookie"""
    return CONFIG.get('custom_cookie')

def get_request_headers_with_cookie():
    """获取包含Cookie的请求头"""
    headers = {
        'authority': 'live.douyin.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }
    
    # 使用自定义Cookie或默认Cookie
    current_cookie = get_current_cookie()
    if current_cookie:
        headers['cookie'] = current_cookie
        print(f"🍪 使用自定义Cookie ({len(current_cookie)} 字符)")
        print(f"📝 Cookie内容: {current_cookie[:50]}...{current_cookie[-50:]}")
    else:
        # 默认Cookie
        default_cookie = 'enter_pc_once=1; UIFID_TEMP=ecb38e5e86f1f8799c3256ca6c3446710d152cd7b76a2f92ca888d379e861b9eb284b4e9a0b949b27b20ca643d2a5f24b0303d07145fb5e8919e6002ee5d43e7ba9382138ae600570f556b83e0249eaa08781c54bd4c4f9a62c72eb99822b212f2423e8c5cf3097bc1ad79b95ccfd26d; hevc_supported=true; __security_mc_1_s_sdk_cert_key=341ff6c2-42d1-85dd; __security_mc_1_s_sdk_sign_data_key_web_protect=21916978-4623-ae6c; __security_mc_1_s_sdk_crypt_sdk=6addeff6-4dca-b655; bd_ticket_guard_client_web_domain=2; passport_csrf_token=4d713363889176dba46a4d28394acf2f; passport_csrf_token_default=4d713363889176dba46a4d28394acf2f; xgplayer_device_id=58452011698; xgplayer_user_id=392125239040; live_use_vvc=%22false%22; fpk1=U2FsdGVkX18v/bibN3Q9R546FaGOwlBjcMYXv87tt8FGIjXHxhtad7YnQNJsomkvt8ok1KDHeA9H0WC4vOynVQ==; fpk2=ce69b851c4edc7eebfb3998aa94a7157; is_dash_user=1; odin_tt=e0bcb4ad345d3ed6915b71cab9469cb459681b743f65d870cb52329adfa8792b80633cf01c31edd9cf4874b743daacc7b789efd1727202b7ed3f6e7059ce43a72f3358995fc8367000f0b42103a78d1b; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __live_version__=%221.1.3.6863%22; download_guide=%223%2F20250806%2F0%22; strategyABtestKey=%221754464113.446%22; SEARCH_RESULT_LIST_TYPE=%22single%22; volume_info=%7B%22volume%22%3A0.43%2C%22isMute%22%3Afalse%2C%22isUserMute%22%3Afalse%7D; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A150%7D%22; home_can_add_dy_2_desktop=%221%22; ttwid=1%7COnZEYGAxHABx6WRfArV8V0vfh1qUfP8AU2WYpG2ybdU%7C1754493043%7C867b28541b24aca9aec6379357aa2bff731e159fa7a804a767f575c8ff886639; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTDBEUUY2MzhCU3pad2ZWTytaenJ2UmpzWENnMDFPRjFOOXIwbXdUT1o4bUZVeHY4UXRqN1FnRkg2RmV0c1FnWDdJTWN0WGhpME43NTFiQ0dMZmxmZUU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; gulu_source_res=eyJwX2luIjoiNWRiODg4ZDk2OWY5MmIyYmRkNjBkMTk5NjFmM2EzM2M0MDE5MTQ4NjExYzMyZGJjNzllZGE3NTdkNTBmMGQwMyJ9; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e5927666d776a686028607d71606b766c6a6b3f2a2a646063606d616d61666c6c606a66646e636a677564646a696d6c756e667562662a666a6b71606b715a7666776c7571762a666a757c2b6f76592758272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f27313235333135363c3131303234272927676c715a75776a716a666a69273f2763646976602778; bit_env=Euo170FfXsKEzZJCgqupttxa8m_sf0klOSsAfK0mcUE-UJH6uA_0c7z8WJ3vIDRPbmh5lFzfdE5-MYjgkit8RHGmhY9vM0oYD0c0eCM0_Gb2xk65Snmo_7py5IQSYybh_nUixA9yALKY-ARhrFEZx8PSaGbCX-vU0KRSQqSGgv5nnzf8eQGUceUNDHkRE5PQTzb1AxvKj2xlh8DSUcifu2HH2xMQ-KzSAbJxyssoComL6Kjlv9WoCVTDhAut_byJWvSVsgqIeIq0YBRt09D9f2vsmqgNHIG5rOUXijAQOcvC6pw6P-YqmQDqXKcF9T3PjYvJWZVqYjjSEbFrALPav1xIsOHrpRCgj2Sj-qvwfrZvRY8ZMeMj9exj0Pu1itLuB05dCshbbaGa2ThZv_6qlzHPRakx6PsTVpsz2IIFwQLgpEkzejcPbPoZkEud18CTbvSqVNxuOUrRFJTRuagLiXRU6JuaK1uyjGplkSEB9z27NysWKbAtuYneIVbGXsuztn9IvA_XkhqM_qRHay2KNF99kFRabO_vB8znQ57lTxE%3D; passport_auth_mix_state=0n14tl9x0fx7kn66tkrfrj8rah4295g5; biz_trace_id=519f5d46; IsDouyinActive=false; __ac_nonce=06893707d00e64c4488d5; __ac_signature=_02B4Z6wo00f01m0zFcQAAIDDRDeLuhFSmo5tExFAAPPu88; xg_device_score=7.583871944698103; has_avx2=null; device_web_cpu_core=8; device_web_memory_size=8; live_can_add_dy_2_desktop=%220%22; csrf_session_id=571b9edd51990393b67f30b2e23fe9da'
        headers['cookie'] = default_cookie
        print("🍪 使用默认Cookie")
    
    return headers



    """获取包含Cookie的请求头"""
    headers = {
        'authority': 'live.douyin.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }
    
    # 使用自定义Cookie或默认Cookie
    current_cookie = get_current_cookie()
    if current_cookie:
        headers['cookie'] = current_cookie
        print(f"🍪 使用自定义Cookie ({len(current_cookie)} 字符)")
    else:
        # 默认Cookie
        default_cookie = 'enter_pc_once=1; UIFID_TEMP=ecb38e5e86f1f8799c3256ca6c3446710d152cd7b76a2f92ca888d379e861b9eb284b4e9a0b949b27b20ca643d2a5f24b0303d07145fb5e8919e6002ee5d43e7ba9382138ae600570f556b83e0249eaa08781c54bd4c4f9a62c72eb99822b212f2423e8c5cf3097bc1ad79b95ccfd26d; hevc_supported=true;'
        # 此处截断默认Cookie展示，实际使用时请使用完整Cookie
        headers['cookie'] = default_cookie
        print("🍪 使用默认Cookie")
    
    return headers