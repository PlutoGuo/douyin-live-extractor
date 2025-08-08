#!/bin/bash

# 抖音直播流提取器启动脚本
# Douyin Live Stream Extractor Startup Script

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="抖音直播流提取器"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}    $1${NC}"
    echo -e "${PURPLE}================================${NC}"
}

# 检查Python环境
check_python() {
    print_info "检查Python环境..."
    
    # 检查python3是否存在
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version)
        print_success "找到Python: $PYTHON_VERSION"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version)
        print_success "找到Python: $PYTHON_VERSION"
    else
        print_error "未找到Python环境"
        echo "请安装Python 3.7或更高版本"
        echo "下载地址: https://www.python.org/downloads/"
        exit 1
    fi
}

# 检查依赖包
check_dependencies() {
    print_info "检查依赖包..."
    
    # 检查requests模块
    if $PYTHON_CMD -c "import requests" &> /dev/null; then
        print_success "requests模块已安装"
    else
        print_warning "requests模块未安装，正在安装..."
        $PYTHON_CMD -m pip install requests
        if [ $? -eq 0 ]; then
            print_success "requests模块安装成功"
        else
            print_error "requests模块安装失败"
            exit 1
        fi
    fi
}

# 检查项目文件
check_project_files() {
    print_info "检查项目文件..."
    
    required_files=(
        "app.py"
        "src/main.py"
        "src/parser.py"
        "src/m3u8_generator.py"
        "src/network.py"
        "src/config.py"
        "src/iina_player.py"
        "src/streamer_manager.py"
    )
    
    missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            print_success "✓ $file"
        else
            print_error "✗ $file (缺失)"
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        print_error "缺失关键文件，无法启动"
        exit 1
    fi
}

# 检查网络连接
check_network() {
    print_info "检查网络连接..."
    
    if ping -c 1 www.douyin.com &> /dev/null; then
        print_success "网络连接正常"
    else
        print_warning "无法连接到抖音服务器，请检查网络"
    fi
}

# 检查IINA播放器
check_iina() {
    print_info "检查IINA播放器..."
    
    if [ -d "/Applications/IINA.app" ]; then
        print_success "IINA播放器已安装"
    else
        print_warning "未找到IINA播放器"
        echo "建议安装IINA播放器以获得更好的播放体验"
        echo "下载地址: https://iina.io"
    fi
}

# 创建保存目录
create_directories() {
    print_info "创建必要目录..."
    
    # 创建下载目录
    DOWNLOADS_DIR="/Users/plutoguo/Documents/直播源/抖音直播源"
    if [ ! -d "$DOWNLOADS_DIR" ]; then
        mkdir -p "$DOWNLOADS_DIR"
        print_success "创建下载目录: $DOWNLOADS_DIR"
    fi
}

# 显示项目信息
show_project_info() {
    print_header "$PROJECT_NAME"
    echo ""
    echo -e "${BLUE}项目目录:${NC} $SCRIPT_DIR"
    echo -e "${BLUE}Python版本:${NC} $PYTHON_VERSION"
    echo -e "${BLUE}启动时间:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo -e "${CYAN}功能特性:${NC}"
    echo "  • 提取抖音直播流URL"
    echo "  • 生成m3u8播放列表文件"
    echo "  • 主播管理和历史记录"
    echo "  • 多播放器支持 (IINA/VLC/QuickTime)"
    echo "  • 流有效性检测"
    echo ""
}

# 显示使用说明
show_usage() {
    echo -e "${YELLOW}使用说明:${NC}"
    echo "  1. 输入抖音直播间URL或分享链接"
    echo "  2. 选择直播质量"
    echo "  3. 生成m3u8文件并选择播放器"
    echo "  4. 管理提取过的主播记录"
    echo ""
    echo -e "${YELLOW}快捷键:${NC}"
    echo "  Ctrl+C  - 退出程序"
    echo "  Enter   - 确认选择"
    echo ""
}

# 主启动函数
start_application() {
    print_info "启动应用程序..."
    
    cd "$SCRIPT_DIR"
    
    # 启动主程序
    $PYTHON_CMD app.py
    
    exit_code=$?
    
    echo ""
    if [ $exit_code -eq 0 ]; then
        print_success "程序正常退出"
    else
        print_error "程序异常退出 (退出码: $exit_code)"
    fi
}

# 清理函数
cleanup() {
    echo ""
    print_info "正在清理..."
    exit 0
}

# 捕获Ctrl+C信号
trap cleanup SIGINT

# 主流程
main() {
    clear
    
    # 显示项目信息
    show_project_info
    
    # 执行检查
    check_python
    check_dependencies
    check_project_files
    check_network
    check_iina
    create_directories
    
    echo ""
    print_success "所有检查完成，准备启动..."
    
    # 显示使用说明
    show_usage
    
    # 等待用户确认
    echo -e "${CYAN}按回车键启动程序，或按Ctrl+C退出...${NC}"
    read -r
    
    # 启动应用
    start_application
}

# 执行主函数
main "$@"
