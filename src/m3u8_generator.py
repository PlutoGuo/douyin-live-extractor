import os
import subprocess
from datetime import datetime

from config import get_save_directory
from file_utils import ensure_directory_exists
from iina_player import open_with_player

def save_m3u8_playlist(m3u8_urls, nickname, live_url, Live_id):
    """
    保存m3u8播放列表到指定目录
    """
    # 确保保存目录存在
    save_dir = get_save_directory()
    if not ensure_directory_exists(save_dir):
        print("❌ 无法创建保存目录，使用当前目录")
        save_dir = '.'
    
    # 清理主播名，移除不能用于文件名的字符
    safe_nickname = "".join(c for c in nickname if c.isalnum() or c in (' ', '-', '_')).strip()
    if not safe_nickname:
        safe_nickname = "未知主播"
    
    # 生成文件名：主播名.m3u8
    filename = f'{safe_nickname}.m3u8'
    filepath = os.path.join(save_dir, filename)
    
    # 检查是否存在同名文件
    file_exists = os.path.exists(filepath)
    if file_exists:
        print(f"📝 发现同名文件，将覆盖更新: {filename}")
    else:
        print(f"📄 创建新文件: {filename}")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write("#EXT-X-VERSION:3\n")
            f.write(f"# 抖音直播流 - {nickname}\n")
            f.write(f"# 主播: {nickname}\n")
            if live_url:
                f.write(f"# 直播间URL: {live_url}\n")
            if Live_id:
                f.write(f"# 直播间ID: {Live_id}\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 质量等级: {len(m3u8_urls)}个\n")
            f.write(f"# 保存目录: {save_dir}\n\n")
            
            for description, url in m3u8_urls:
                # 添加流信息
                f.write(f"#EXTINF:-1,{description}\n")
                f.write(f"{url}\n\n")
        
        print(f"\n💾 m3u8播放列表已保存到:")
        print(f"   📁 目录: {save_dir}")
        print(f"   📄 文件: {filename}")
        print(f"   📱 包含 {len(m3u8_urls)} 个直播流")
        if file_exists:
            print(f"   🔄 文件已覆盖更新")
        else:
            print(f"   ✨ 新建文件")
        
        # 保存主播记录
        try:
            from streamer_manager import add_streamer_record
            add_streamer_record(nickname, Live_id, live_url, success=True)
            print(f"   📝 已更新主播记录: {nickname}")
        except Exception as e:
            print(f"   ⚠️ 记录主播信息失败: {e}")
        
        # 询问是否播放
        print("\n🎬 m3u8文件已生成完成！")
        open_with_player(filepath)
        
        return filepath
        
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")
        
        # 记录失败的主播信息
        try:
            from streamer_manager import add_streamer_record
            add_streamer_record(nickname, Live_id, live_url, success=False)
        except:
            pass
        
        # 尝试保存到当前目录作为备用
        try:
            fallback_path = filename
            with open(fallback_path, 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n")
                f.write("#EXT-X-VERSION:3\n")
                f.write(f"# 抖音直播流 - {nickname}\n")
                f.write(f"# 主播: {nickname}\n")
                if Live_id:
                    f.write(f"# 直播间ID: {Live_id}\n")
                if live_url:
                    f.write(f"# 直播间URL: {live_url}\n")
                f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for description, url in m3u8_urls:
                    f.write(f"#EXTINF:-1,{description}\n")
                    f.write(f"{url}\n\n")
            
            print(f"✅ 已保存到当前目录: {fallback_path}")
            return fallback_path
        except Exception as backup_e:
            print(f"❌ 备用保存也失败: {backup_e}")
            return None