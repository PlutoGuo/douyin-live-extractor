from re import U
from pydantic_core import Url
import requests
from datetime import datetime

from ui import show_progress
from cookie_manager import get_request_headers_with_cookie
from parser import extract_stream_urls

def request_douyin_live(url, room_id):
    """
    请求抖音直播页面
    """
    try:
        print(f"\n🌐 正在连接到: {url}")
        show_progress("建立连接中", 1)
        
        # 获取包含Cookie的请求头
        headers = get_request_headers_with_cookie()
        
        # 添加会话管理
        session = requests.Session()
        session.headers.update(headers)
        
        print("📡 发送HTTP请求...")
        response = session.get(url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        
        print(f"✅ 状态码: {response.status_code}")
        print(f"📊 页面内容长度: {len(response.text):,} 字符")
        print(f"🔤 响应编码: {response.encoding}")
        
        # 检查内容是否正确解码
        if response.text and len(response.text) > 100:
            
            # 提取直播流URL
            print("\n🔍 开始解析直播流数据...")
            show_progress("解析中", 2)
            extract_stream_urls(response.text, url, room_id)

        else:
            print("❌ 响应内容为空或解码失败")
            
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        print("\n💡 可能的解决方案:")
        print("   1. 检查网络连接")
        print("   2. 确认直播间是否正在直播")
        print("   3. 尝试更新Cookie")
        print("   4. 稍后重试")
        return None