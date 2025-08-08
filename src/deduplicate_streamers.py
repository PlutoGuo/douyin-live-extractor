#!/usr/bin/env python3
"""
主播数据去重工具
"""

import json
import os
from datetime import datetime

def get_streamers_db_path():
    """获取主播数据库文件路径"""
    from config import get_save_directory
    save_dir = get_save_directory()
    return os.path.join(save_dir, 'streamers_history.json')

def deduplicate_streamers():
    """去重主播记录"""
    db_path = get_streamers_db_path()
    
    if not os.path.exists(db_path):
        print("❌ 主播数据库文件不存在")
        return
    
    # 读取现有数据
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            streamers_data = json.load(f)
    except Exception as e:
        print(f"❌ 读取数据失败: {e}")
        return
    
    print(f"📊 原始记录数: {len(streamers_data)}")
    
    # 按昵称去重，保留最新的记录
    nickname_to_key = {}
    unique_streamers = {}
    
    for key, data in streamers_data.items():
        nickname = data.get('nickname', '未知')
        
        # 解析最后提取时间
        try:
            last_time = datetime.fromisoformat(data.get('last_extract_time', data.get('first_extract_time', '')))
        except:
            last_time = datetime.min
        
        # 如果这个昵称已经存在
        if nickname in nickname_to_key:
            existing_key = nickname_to_key[nickname]
            existing_data = unique_streamers[existing_key]
            
            try:
                existing_time = datetime.fromisoformat(existing_data.get('last_extract_time', existing_data.get('first_extract_time', '')))
            except:
                existing_time = datetime.min
            
            # 保留时间更新的记录
            if last_time > existing_time:
                print(f"🔄 更新主播记录: {nickname} (新key: {key}, 旧key: {existing_key})")
                del unique_streamers[existing_key]
                unique_streamers[key] = data
                nickname_to_key[nickname] = key
            else:
                print(f"⏭️  跳过重复记录: {nickname} (key: {key})")
        else:
            # 新的昵称，直接添加
            unique_streamers[key] = data
            nickname_to_key[nickname] = key
    
    print(f"📊 去重后记录数: {len(unique_streamers)}")
    
    # 备份原文件
    backup_path = db_path + '.backup'
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(streamers_data, f, ensure_ascii=False, indent=2)
        print(f"💾 原数据已备份到: {backup_path}")
    except Exception as e:
        print(f"⚠️ 备份失败: {e}")
    
    # 保存去重后的数据
    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(unique_streamers, f, ensure_ascii=False, indent=2)
        print("✅ 去重完成，数据已保存")
    except Exception as e:
        print(f"❌ 保存失败: {e}")

if __name__ == "__main__":
    print("🧹 主播数据去重工具")
    print("=" * 40)
    
    # 确认操作
    confirm = input("⚠️  这将修改主播历史数据，是否继续? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 操作已取消")
        exit()
    
    deduplicate_streamers()
    print("\n🎉 去重操作完成！")
