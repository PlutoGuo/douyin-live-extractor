import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import html

from m3u8_generator import save_m3u8_playlist

def extract_stream_urls(html_content, live_url, Live_id=None):
    """
    从HTML内容中提取直播流URL
    """
    # 首先尝试解析播放器配置数据获取主播信息和直播状态
    print("🔎 解析主播信息和直播状态...")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 找出含有 data-config 的 <script> 标签（没有 id）
    script_tag = soup.find("script", attrs={"data-config": True})
    nickname = "未知主播"
    room_id = None 

    if script_tag:
        try:
            # 解码 HTML 实体
            data_config_str = html.unescape(script_tag.get("data-config"))
            data_anchor_info_str = html.unescape(script_tag.get("data-anchor-info", "{}"))
            data_room_info_str = html.unescape(script_tag.get("data-room-info", "{}"))

            config = json.loads(data_config_str)
            anchor_info = json.loads(data_anchor_info_str)
            room_info = json.loads(data_room_info_str)

            nickname = anchor_info.get("nickname", "未知主播")
            avatar = anchor_info.get("avatar")
            room_id = room_info.get("roomId")
            is_live_end = config.get("basicPlayerProps", {}).get("logOptions", {}).get("is_live_end", 1)

            print(f"📺 主播昵称: {nickname}")
            print(f"🏠 房间 ID: {room_id}")
            print(f"📡 直播状态: {'正在直播' if is_live_end == 0 else '直播已结束'}")
            if avatar:
                print(f"🖼️  头像地址: {avatar}")

        except json.JSONDecodeError as e:
            print(f"❌ 主播信息解析失败: {e}")
    else:
        print("⚠️ 未找到主播信息")

    # 查找包含流数据的JavaScript代码
    print("🔎 搜索直播流数据...")
    
    # 匹配 self.__pace_f.push([1, "JSON数据"])
    pattern = r'self\.__pace_f\.push\(\[1,\s*"({.*?data.*?})"\]\)'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    if not matches:
        print("❌ 主模式未找到直播流数据，尝试备用模式...")
        # 备用模式：直接匹配包含完整数据结构的JSON
        patterns = [
            r'self\.__pace_f\.push\(\[1,\s*"({.*?common.*?data.*?})"\]\)',
            r'"({.*?common.*?stream_name.*?data.*?})"',
            r'self\.__pace_f\.push\(\[1,\s*"([^"]*{.*?data.*?}[^"]*)"\]\)',
            r'"data":\s*({.*?"origin".*?})',
            r'streamData["\']?\s*[:=]\s*({.*?})',
            r'window\.__INITIAL_STATE__\s*=\s*({.*?});'
        ]
        
        for i, alt_pattern in enumerate(patterns):
            print(f"🔍 尝试模式 {i+1}/{len(patterns)}...")
            matches = re.findall(alt_pattern, html_content, re.DOTALL)
            if matches:
                print(f"✅ 模式 {i+1} 成功找到数据!")
                break
        
        if not matches:
            print("❌ 所有模式都未找到直播流数据")
            return
    
    # 解析找到的数据
    parse_stream_data(matches, nickname, room_id, live_url, Live_id)

def parse_stream_data(matches, nickname, room_id, live_url, Live_id):
    """解析直播流数据"""
    stream_data = None
    for match in matches:
        try:
            print(f"🔧 尝试解析JSON数据 (长度: {len(match)} 字符)...")
            
            # 处理转义字符
            json_str = match.replace('\\"', '"').replace('\\\\', '\\')
            
            # 尝试解析JSON
            parsed_data = json.loads(json_str)
            
            # 检查是否包含我们需要的数据结构
            if 'data' in parsed_data and isinstance(parsed_data['data'], dict):
                stream_data = parsed_data
                print("✅ 成功解析流数据!")
                break
            else:
                print("⚠️ 数据格式不匹配，尝试下一个...")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            # 如果解析失败，尝试清理数据
            try:
                # 移除可能的前缀/后缀
                cleaned = re.sub(r'^[^{]*', '', json_str)  # 移除开头非JSON字符
                cleaned = re.sub(r'[^}]*$', '', cleaned)   # 移除结尾非JSON字符
                parsed_data = json.loads(cleaned)
                if 'data' in parsed_data:
                    stream_data = parsed_data
                    print("✅ 清理后成功解析!")
                    break
            except:
                continue
    
    if not stream_data:
        print("❌ 未能解析出有效的流数据")
        return
    
    try:
        print("\n🎉 抖音直播流URL提取成功！")
        print("=" * 80)
        
        # 提取不同清晰度的流URL
        data = stream_data.get('data', {})
        
        # 更新清晰度描述，包含编码信息
        qualities = {
            'origin': '原画质',
            'uhd': '超高清 (1080p)', 
            'hd': '高清 (720p)',
            'sd': '标清',
            'ld': '流畅',
            'md': '极速',
            'ao': '纯音频'
        }
        
        m3u8_urls = extract_m3u8_urls(data, qualities)
        
        print(f"\n📊 总计找到 {len(m3u8_urls)} 个HLS流")
        
        if m3u8_urls:
            # 自动保存m3u8格式
            print("\n💾 正在保存m3u8播放列表...")
            # 优先使用解析出的room_id，如果没有则使用传入的Live_id
            final_room_id = room_id if room_id else Live_id
            save_m3u8_playlist(m3u8_urls, nickname, live_url, final_room_id)
        else:
            print("❌ 未找到HLS格式的直播流")
        
        # 显示通用信息
        common_info = stream_data.get('common', {})
        if common_info:
            print(f"\n📋 流信息:")
            print(f"  🆔 流ID: {common_info.get('stream', 'unknown')}")
            print(f"  📡 会话ID: {common_info.get('session_id', 'unknown')}")
            print(f"  🕒 时间戳: {common_info.get('ts', 'unknown')}")
            if 'stream_name' in common_info:
                print(f"  📺 流名称: {common_info['stream_name']}")
        
    except Exception as e:
        print(f"❌ 提取流URL时出错: {e}")
        
        # 提供调试选项
        debug_choice = input("\n🔧 是否保存原始数据用于调试? (y/n): ")
        if debug_choice.lower() in ['y', 'yes', '是']:
            debug_file = f'debug_raw_data_{datetime.now().strftime("%H%M%S")}.txt'
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write("=== 匹配到的数据 ===\n")
                for i, match in enumerate(matches):
                    f.write(f"\n--- 匹配 {i+1} ---\n")
                    f.write(match)
            print(f"✅ 调试数据已保存到 {debug_file}")

def extract_m3u8_urls(data, qualities):
    """从数据中提取不同清晰度的m3u8 URL"""
    available_qualities = []
    m3u8_urls = []
    
    for quality, description in qualities.items():
        if quality in data:
            quality_data = data[quality]
            
            # 获取技术参数
            sdk_params_str = quality_data.get('main', {}).get('sdk_params', '{}')
            try:
                sdk_params = json.loads(sdk_params_str.replace('\\', ''))
                vcodec = sdk_params.get('VCodec', 'unknown')
                resolution = sdk_params.get('resolution', 'unknown')
                fps = sdk_params.get('fps', 'unknown')
                bitrate = sdk_params.get('vbitrate', 0)
                
                # 获取实时信息
                template_info = quality_data.get('main', {}).get('templateRealTimeInfo', {})
                real_bitrate = template_info.get('bitrateKbps', 0)
                
                # 构建详细描述
                detail_parts = [description]
                if resolution != 'unknown' and resolution:
                    detail_parts.append(f"{resolution}")
                if fps not in ['unknown', 0]:
                    detail_parts.append(f"{fps}fps")
                if vcodec != 'unknown':
                    detail_parts.append(f"{vcodec.upper()}")
                if real_bitrate > 0:
                    detail_parts.append(f"{real_bitrate}kbps")
                
                full_description = " ".join(detail_parts)
                
            except:
                full_description = description
            
            available_qualities.append((quality, full_description))
            print(f"\n📺 {full_description}")
            
            # 主线路
            if 'main' in quality_data:
                main_data = quality_data['main']
                print("  🔸 主线路:")
                
                if main_data.get('hls'):
                    hls_url = main_data['hls']
                    print(f"    HLS: {hls_url}")
                    m3u8_urls.append((full_description, hls_url))
                
                if main_data.get('flv'):
                    flv_url = main_data['flv']
                    print(f"    FLV: {flv_url}")
            
            # 备用线路
            if 'backup' in quality_data:
                backup_data = quality_data['backup']
                print("  🔹 备用线路:")
                if backup_data.get('hls'):
                    backup_hls = backup_data['hls']
                    print(f"    HLS: {backup_hls}")
                    m3u8_urls.append((f"{full_description} (备用)", backup_hls))
    
    return m3u8_urls