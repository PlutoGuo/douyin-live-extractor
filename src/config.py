import os

# 全局配置
CONFIG = {
    'save_directory': os.path.expanduser('~/Documents/直播源/抖音直播源'),
    'cookie_file': os.path.expanduser('~/Documents/直播源/抖音直播源/cookies.txt'),
    'custom_cookie': None
}

def get_save_directory():
    """获取当前保存目录"""
    return CONFIG['save_directory']

def set_save_directory(directory):
    """设置保存目录"""
    from file_utils import ensure_directory_exists
    expanded_dir = os.path.expanduser(directory)
    if ensure_directory_exists(expanded_dir):
        CONFIG['save_directory'] = expanded_dir
        return True
    return False

def get_current_cookie():
    """获取当前使用的Cookie"""

    return CONFIG.get('custom_cookie')


def set_custom_cookie(cookie):
    """设置自定义Cookie"""
    CONFIG['custom_cookie'] = cookie