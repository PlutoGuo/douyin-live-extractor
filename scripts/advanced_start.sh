#!/bin/bash

# 抖音直播流提取器 - 高级启动脚本
# Advanced startup script with additional features

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="抖音直播流提取器"
LOG_FILE="$SCRIPT_DIR/startup.log"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

print_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
    log "INFO: $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    log "SUCCESS: $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    log "WARNING: $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    log "ERROR: $1"
}

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -q, --quick    快速启动（跳过检查）"
    echo "  -c, --check    只执行环境检查"
    echo "  -l, --log      显示启动日志"
    echo "  -v, --version  显示版本信息"
    echo "  --install-deps 安装/更新依赖包"
    echo "  --reset        重置配置文件"
    echo ""
    echo "示例:"
    echo "  $0              # 正常启动"
    echo "  $0 -q           # 快速启动"
    echo "  $0 --check      # 只检查环境"
    echo ""
}

# 显示版本信息
show_version() {
    echo "$PROJECT_NAME v2.0"
    echo "构建时间: $(date '+%Y-%m-%d')"
    echo "Python版本要求: 3.7+"
    echo "作者: GitHub Copilot"
}

# 安装依赖
install_dependencies() {
    print_info "安装/更新依赖包..."
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3未找到，请安装pip"
        return 1
    fi
    
    # 更新pip
    print_info "更新pip..."
    pip3 install --upgrade pip
    
    # 安装requests
    print_info "安装requests..."
    pip3 install requests
    
    # 安装其他可选依赖
    print_info "安装可选依赖..."
    pip3 install urllib3 beautifulsoup4
    
    print_success "依赖包安装完成"
}

# 重置配置
reset_config() {
    print_warning "重置配置文件..."
    
    config_files=(
        "streamers_history.json"
        "cookies.txt"
        "startup.log"
    )
    
    for file in "${config_files[@]}"; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            mv "$SCRIPT_DIR/$file" "$SCRIPT_DIR/$file.backup.$(date +%s)"
            print_info "备份并重置: $file"
        fi
    done
    
    print_success "配置已重置，旧配置已备份"
}

# 环境检查
check_environment() {
    print_info "执行环境检查..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python环境: $PYTHON_VERSION"
    else
        print_error "Python3未安装"
        return 1
    fi
    
    # 检查依赖
    if python3 -c "import requests" &> /dev/null; then
        REQUESTS_VERSION=$(python3 -c "import requests; print(requests.__version__)")
        print_success "requests模块: v$REQUESTS_VERSION"
    else
        print_error "requests模块未安装"
        return 1
    fi
    
    # 检查项目文件
    if [ -f "$SCRIPT_DIR/app.py" ]; then
        print_success "项目文件完整"
    else
        print_error "项目文件缺失"
        return 1
    fi
    
    # 检查播放器
    if [ -d "/Applications/IINA.app" ]; then
        print_success "IINA播放器已安装"
    else
        print_warning "IINA播放器未安装（建议安装）"
    fi
    
    print_success "环境检查完成"
    return 0
}

# 显示启动日志
show_log() {
    if [ -f "$LOG_FILE" ]; then
        echo "=== 启动日志 ==="
        tail -20 "$LOG_FILE"
    else
        print_info "暂无启动日志"
    fi
}

# 主启动函数
start_application() {
    print_info "启动应用程序..."
    cd "$SCRIPT_DIR"
    
    # 确保Python命令可用
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python环境不可用"
        exit 1
    fi
    
    # 启动主程序
    $PYTHON_CMD app.py
    
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        print_success "程序正常退出"
    else
        print_error "程序异常退出 (退出码: $exit_code)"
    fi
    
    return $exit_code
}

# 解析命令行参数
QUICK_MODE=false
CHECK_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -q|--quick)
            QUICK_MODE=true
            shift
            ;;
        -c|--check)
            CHECK_ONLY=true
            shift
            ;;
        -l|--log)
            show_log
            exit 0
            ;;
        -v|--version)
            show_version
            exit 0
            ;;
        --install-deps)
            install_dependencies
            exit $?
            ;;
        --reset)
            reset_config
            exit 0
            ;;
        *)
            print_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 主流程
main() {
    # 初始化日志
    log "========== 启动会话开始 =========="
    
    # 显示标题
    echo -e "${PURPLE}🎬 $PROJECT_NAME${NC}"
    echo -e "${BLUE}================================${NC}"
    
    # 快速模式
    if [ "$QUICK_MODE" = true ]; then
        print_info "快速启动模式"
        start_application
        exit $?
    fi
    
    # 环境检查
    if ! check_environment; then
        print_error "环境检查失败"
        echo ""
        echo "建议执行以下命令修复："
        echo "  $0 --install-deps    # 安装依赖"
        echo "  $0 --help           # 查看帮助"
        exit 1
    fi
    
    # 仅检查模式
    if [ "$CHECK_ONLY" = true ]; then
        print_info "环境检查完成，退出"
        exit 0
    fi
    
    echo ""
    print_success "准备启动程序..."
    echo -e "${CYAN}按回车键继续，或按Ctrl+C退出...${NC}"
    read -r
    
    # 启动应用
    start_application
}

# 捕获信号
trap 'echo ""; print_info "用户中断"; exit 130' INT

# 执行主函数
main "$@"
