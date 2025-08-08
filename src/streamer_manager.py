import os
import json
from datetime import datetime
from config import get_save_directory
from file_utils import ensure_directory_exists

def get_streamers_db_path():
    """获取主播数据库文件路径"""
    save_dir = get_save_directory()
    ensure_directory_exists(save_dir)
    return os.path.join(save_dir, 'streamers_history.json')

def load_streamers_history():
    """加载主播历史记录"""
    db_path = get_streamers_db_path()
    
    if not os.path.exists(db_path):
        return {}
    
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 读取主播历史记录失败: {e}")
        return {}

def save_streamers_history(streamers_data):
    """保存主播历史记录"""
    db_path = get_streamers_db_path()
    
    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(streamers_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"⚠️ 保存主播历史记录失败: {e}")
        return False

def add_streamer_record(nickname, room_id, live_url, success=True):
    """添加主播提取记录"""
    streamers_data = load_streamers_history()
    
    # 使用room_id作为唯一标识
    streamer_key = room_id if room_id else nickname
    
    if streamer_key not in streamers_data:
        streamers_data[streamer_key] = {
            'nickname': nickname,
            'room_id': room_id,
            'live_url': live_url,
            'first_extract_time': datetime.now().isoformat(),
            'extract_history': []
        }
    
    # 更新基本信息（可能主播改名了）
    streamers_data[streamer_key]['nickname'] = nickname
    streamers_data[streamer_key]['live_url'] = live_url
    
    # 添加提取记录
    extract_record = {
        'timestamp': datetime.now().isoformat(),
        'success': success,
        'nickname': nickname
    }
    
    streamers_data[streamer_key]['extract_history'].append(extract_record)
    
    # 只保留最近10次记录
    if len(streamers_data[streamer_key]['extract_history']) > 10:
        streamers_data[streamer_key]['extract_history'] = streamers_data[streamer_key]['extract_history'][-10:]
    
    # 更新最后提取时间
    streamers_data[streamer_key]['last_extract_time'] = datetime.now().isoformat()
    
    save_streamers_history(streamers_data)
    
    return streamer_key

def get_streamers_list():
    """获取主播列表，按最后提取时间排序"""
    streamers_data = load_streamers_history()
    
    streamers_list = []
    for key, data in streamers_data.items():
        # 计算提取统计
        total_extracts = len(data.get('extract_history', []))
        successful_extracts = sum(1 for record in data.get('extract_history', []) if record.get('success', False))
        
        # 解析时间
        try:
            last_extract_time = datetime.fromisoformat(data.get('last_extract_time', data.get('first_extract_time', '')))
        except:
            last_extract_time = datetime.min
        
        try:
            first_extract_time = datetime.fromisoformat(data.get('first_extract_time', ''))
        except:
            first_extract_time = datetime.min
        
        streamer_info = {
            'key': key,
            'nickname': data.get('nickname', '未知'),
            'room_id': data.get('room_id', ''),
            'live_url': data.get('live_url', ''),
            'first_extract_time': first_extract_time,
            'last_extract_time': last_extract_time,
            'total_extracts': total_extracts,
            'successful_extracts': successful_extracts,
            'success_rate': (successful_extracts / total_extracts * 100) if total_extracts > 0 else 0
        }
        
        streamers_list.append(streamer_info)
    
    # 按最后提取时间排序（最新的在前）
    streamers_list.sort(key=lambda x: x['last_extract_time'], reverse=True)
    
    return streamers_list

def remove_streamer_record(streamer_key):
    """删除主播记录"""
    streamers_data = load_streamers_history()
    
    if streamer_key in streamers_data:
        del streamers_data[streamer_key]
        save_streamers_history(streamers_data)
        return True
    
    return False

def format_time_ago(dt):
    """格式化时间差"""
    if dt == datetime.min:
        return "未知"
    
    time_diff = datetime.now() - dt
    total_seconds = int(time_diff.total_seconds())
    
    if total_seconds < 60:
        return "刚刚"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes}分钟前"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours}小时前"
    elif total_seconds < 2592000:  # 30天
        days = total_seconds // 86400
        return f"{days}天前"
    else:
        return dt.strftime('%Y-%m-%d')

def clean_old_records(days_threshold=30):
    """清理旧记录"""
    streamers_data = load_streamers_history()
    threshold_date = datetime.now() - datetime.timedelta(days=days_threshold)
    
    to_remove = []
    for key, data in streamers_data.items():
        try:
            last_extract_time = datetime.fromisoformat(data.get('last_extract_time', data.get('first_extract_time', '')))
            if last_extract_time < threshold_date:
                to_remove.append(key)
        except:
            # 如果时间解析失败，也标记为删除
            to_remove.append(key)
    
    removed_count = 0
    for key in to_remove:
        del streamers_data[key]
        removed_count += 1
    
    if removed_count > 0:
        save_streamers_history(streamers_data)
    
    return removed_count
