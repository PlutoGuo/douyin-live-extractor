import os
import subprocess
import requests
from datetime import datetime
from simple_menu import create_simple_menu

def check_m3u8_stream_validity(file_path):
    """
    检查m3u8文件中的流是否有效（增强版本）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取流URL
        stream_urls = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('http'):
                stream_urls.append(line)
        
        if not stream_urls:
            return False, "❌ 文件中未找到有效的流URL"
        
        print(f"🔍 找到 {len(stream_urls)} 个流URL，正在验证...")
        
        # 检查前几个流URL的有效性
        valid_count = 0
        total_checked = min(3, len(stream_urls))  # 最多检查3个URL
        
        for i, test_url in enumerate(stream_urls[:total_checked]):
            print(f"� 检查流 {i+1}/{total_checked}: {test_url[:60]}...")
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                }
                
                # 使用HEAD请求快速检查
                response = requests.head(test_url, headers=headers, timeout=8, allow_redirects=True)
                
                if response.status_code == 200:
                    print(f"   ✅ 流 {i+1} 有效 (状态码: {response.status_code})")
                    valid_count += 1
                elif response.status_code == 403:
                    print(f"   ❌ 流 {i+1} 访问被拒绝 (403)")
                elif response.status_code == 404:
                    print(f"   ❌ 流 {i+1} 不存在 (404)")
                else:
                    print(f"   ⚠️ 流 {i+1} 状态异常 ({response.status_code})")
                    
            except requests.exceptions.Timeout:
                print(f"   ⏰ 流 {i+1} 检查超时")
            except requests.exceptions.ConnectionError:
                print(f"   🔌 流 {i+1} 连接失败")
            except requests.exceptions.RequestException as e:
                print(f"   ❌ 流 {i+1} 检查失败: {str(e)[:50]}")
        
        # 根据有效流的数量判断整体状态
        if valid_count == 0:
            return False, f"❌ 所有检查的流都已失效 (0/{total_checked})"
        elif valid_count == total_checked:
            return True, f"✅ 所有检查的流都有效 ({valid_count}/{total_checked})"
        else:
            return True, f"⚠️ 部分流有效 ({valid_count}/{total_checked})，可尝试播放"
            
    except Exception as e:
        return False, f"❌ 文件读取失败: {str(e)}"

def get_file_age(file_path):
    """
    获取文件的创建时间信息
    """
    try:
        stat = os.stat(file_path)
        create_time = datetime.fromtimestamp(stat.st_mtime)
        age = datetime.now() - create_time
        
        if age.seconds < 3600:  # 1小时内
            age_str = f"{age.seconds // 60}分钟"
        elif age.days == 0:
            age_str = f"{age.seconds // 3600}小时"
        else:
            age_str = f"{age.days}天"
            
        return create_time, age_str
    except:
        return None, "未知"

def open_with_player(file_path):
    """
    使用播放器打开m3u8文件，支持多种播放器选择
    """
    print(f"🎬 准备播放: {os.path.basename(file_path)}")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 显示文件信息
    create_time, age_str = get_file_age(file_path)
    if create_time:
        print(f"📅 文件创建时间: {create_time.strftime('%Y-%m-%d %H:%M:%S')} ({age_str}前)")
    
    # 检查流有效性
    print("🔍 正在检查直播流有效性...")
    is_valid, check_message = check_m3u8_stream_validity(file_path)
    print(f"📊 检查结果: {check_message}")
    
    if not is_valid:
        print("\n⚠️ 直播流可能已失效，播放器可能会自动关闭")
        print("💡 建议:")
        print("  1. 重新提取该主播的直播流")
        print("  2. 确认主播当前是否在直播")
        
        continue_choice = input("\n❓ 是否仍要尝试播放? (y/n): ").lower()
        if continue_choice not in ['y', 'yes', '是']:
            return False
    
    # 询问播放器选择
    player_choice = ask_open_with_iina()
    
    if player_choice is None:
        print("🚫 已取消播放")
        return False
    elif player_choice == 'iina':
        return open_with_iina_simple(file_path)
    else:
        return open_with_alternative_player(file_path, player_choice)

def open_with_iina_simple(file_path):
    """
    使用IINA播放器打开文件（最优化版本）
    """
    try:
        print(f"🚀 正在启动IINA播放器...")
        
        # 使用最稳定的启动方式：open -a IINA
        try:
            print("📱 使用系统标准方式启动IINA...")
            
            # 使用 open -a 命令启动IINA，这是最稳定的方式
            result = subprocess.run([
                'open', '-a', 'IINA', file_path
            ], capture_output=True, text=True, timeout=8)
            
            if result.returncode == 0:
                print("✅ IINA启动命令执行成功")
                
                # 给IINA一些时间启动
                import time
                print("⏳ 等待IINA加载流...")
                time.sleep(2)
                
                # 检查IINA进程
                try:
                    check_process = subprocess.run([
                        'pgrep', '-f', 'IINA'
                    ], capture_output=True, text=True, timeout=3)
                    
                    if check_process.returncode == 0 and check_process.stdout.strip():
                        process_ids = check_process.stdout.strip().split('\n')
                        print(f"✅ IINA正在运行 (进程ID: {', '.join(process_ids)})")
                        
                        # 再等待一段时间检查是否自动退出
                        time.sleep(3)
                        check_again = subprocess.run([
                            'pgrep', '-f', 'IINA'
                        ], capture_output=True, text=True, timeout=3)
                        
                        if check_again.returncode == 0 and check_again.stdout.strip():
                            print("🎉 IINA正在正常播放")
                            print("💡 提示: 如果看不到画面，可能是流URL已失效")
                        else:
                            print("⚠️ IINA已自动退出")
                            print("💡 这通常表示:")
                            print("   • 直播流URL已失效或过期")
                            print("   • 主播已停止直播")
                            print("   • 网络连接问题")
                            print("🔄 建议重新提取该主播的直播流")
                    else:
                        print("⚠️ 未检测到IINA进程，可能启动失败")
                        
                except subprocess.TimeoutExpired:
                    print("⏰ 进程检查超时，但IINA可能正在运行")
                except Exception as check_error:
                    print(f"⚠️ 无法检查IINA状态: {check_error}")
                
                return True
                
            else:
                print(f"❌ IINA启动失败，返回码: {result.returncode}")
                if result.stderr:
                    print(f"错误信息: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ IINA启动超时，但可能正在后台运行")
            return True
            
        except FileNotFoundError:
            print("❌ 找不到 'open' 命令或IINA应用")
            print("💡 请确保IINA已正确安装到Applications文件夹")
            return False
            
        except Exception as e:
            print(f"❌ 启动IINA时出错: {e}")
            print("💡 可能的解决方案:")
            print("   • 重新安装IINA应用")
            print("   • 检查文件权限")
            print("   • 重启系统")
            return False
            
    except Exception as e:
        print(f"❌ 出现未知错误: {e}")
        return False

def ask_open_with_iina():
    """
    询问用户是否要用IINA打开文件
    """
    print("\n🎬 播放选项:")
    options = [
        "使用IINA播放器",
        "使用VLC播放器", 
        "使用QuickTime播放器",
        "复制文件路径到剪贴板",
        "不播放"
    ]
    
    choice_index = create_simple_menu(options, "请选择播放方式")
    if choice_index is None:
        return None
        
    player_map = ['iina', 'vlc', 'quicktime', 'copy', None]
    return player_map[choice_index]

def open_with_alternative_player(file_path, player_type):
    """
    使用其他播放器打开文件
    """
    try:
        if player_type == 'vlc':
            # 尝试VLC播放器
            vlc_paths = [
                '/Applications/VLC.app/Contents/MacOS/VLC',
                '/usr/bin/vlc'
            ]
            vlc_command = None
            for path in vlc_paths:
                if os.path.exists(path):
                    vlc_command = path
                    break
            
            if vlc_command:
                print("🎬 正在启动VLC播放器...")
                subprocess.run([vlc_command, file_path], capture_output=True)
                return True
            else:
                print("❌ 未找到VLC播放器")
                return False
                
        elif player_type == 'quicktime':
            # 使用QuickTime播放器
            print("🎬 正在启动QuickTime播放器...")
            subprocess.run(['open', '-a', 'QuickTime Player', file_path], capture_output=True)
            return True
            
        elif player_type == 'copy':
            # 复制路径到剪贴板
            try:
                subprocess.run(['pbcopy'], input=file_path.encode(), check=True)
                print(f"📋 文件路径已复制到剪贴板: {file_path}")
                print("💡 可以粘贴到任何支持m3u8的播放器中")
                return True
            except:
                print(f"📁 文件路径: {file_path}")
                print("💡 请手动复制上述路径到播放器中")
                return True
    except Exception as e:
        print(f"❌ 启动播放器失败: {e}")
        return False

def find_streamer_m3u8_file(nickname, save_dir):
    """
    查找主播对应的m3u8文件
    """
    # 清理主播名，移除不能用于文件名的字符
    safe_nickname = "".join(c for c in nickname if c.isalnum() or c in (' ', '-', '_')).strip()
    if not safe_nickname:
        safe_nickname = "未知主播"
    
    filename = f'{safe_nickname}.m3u8'
    filepath = os.path.join(save_dir, filename)
    
    if os.path.exists(filepath):
        return filepath
    return None

def open_streamer_file(nickname, save_dir):
    """
    打开指定主播的m3u8文件（增强版本）
    """
    filepath = find_streamer_m3u8_file(nickname, save_dir)
    
    if not filepath:
        print(f"❌ 未找到主播 '{nickname}' 的直播流文件")
        print(f"💡 文件应该位于: {save_dir}")
        return False
    
    print(f"📁 找到文件: {os.path.basename(filepath)}")
    print(f"📍 文件路径: {filepath}")
    
    # 显示文件基本信息
    try:
        file_size = os.path.getsize(filepath)
        print(f"📏 文件大小: {file_size} 字节")
        
        # 检查文件内容预览
        with open(filepath, 'r', encoding='utf-8') as f:
            first_lines = f.readlines()[:10]
            stream_count = sum(1 for line in first_lines if line.strip().startswith('http'))
            print(f"📺 预览: 文件前10行包含 {stream_count} 个流URL")
            
    except Exception as e:
        print(f"⚠️ 无法读取文件信息: {e}")
    
    print("\n" + "="*50)
    print(f"🎭 准备播放主播: {nickname}")
    print("="*50)
    
    success = open_with_player(filepath)
    
    if success:
        print(f"\n🎉 已启动播放: {nickname}")
    else:
        print(f"\n😞 播放启动失败: {nickname}")
        print("💡 可能的原因:")
        print("   • 直播流已过期失效")
        print("   • 播放器启动失败")
        print("   • 文件内容损坏")
    
    return success
