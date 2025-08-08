import os
from datetime import datetime

def ensure_directory_exists(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ 已创建目录: {directory}")
            return True
        except Exception as e:
            print(f"❌ 创建目录失败: {e}")
            return False
    return True

def open_current_directory(directory):
    """打开指定目录"""
    if not os.path.exists(directory):
        ensure_directory_exists(directory)
    
    try:
        os.system(f'open "{directory}"')  # macOS
        print(f"✅ 已打开目录: {directory}")
        return True
    except Exception as e:
        print(f"❌ 打开目录失败: {e}")
        return False

def show_directory_files(directory):
    """显示目录中的文件"""
    if not os.path.exists(directory):
        print("❌ 目录不存在")
        return False
    
    print(f"\n📁 目录文件列表: {directory}")
    print("=" * 60)
    
    files = [f for f in os.listdir(directory) if f.endswith('.m3u8')]
    
    if not files:
        print("📝 目录中暂无m3u8文件")
    else:
        print(f"\n📺 找到 {len(files)} 个m3u8文件:")
        for i, file in enumerate(files, 1):
            file_path = os.path.join(directory, file)
            file_size = os.path.getsize(file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"  {i}. {file}")
            print(f"     📊 大小: {file_size} bytes")
            print(f"     🕒 修改时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
    
    return True