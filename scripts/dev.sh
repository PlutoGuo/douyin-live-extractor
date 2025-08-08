#!/bin/bash

# 抖音直播流提取器 - 开发者工具脚本
# Developer utility script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# 显示可用命令
show_commands() {
    echo "可用命令:"
    echo ""
    echo "  启动相关:"
    echo "    run         - 运行程序"
    echo "    quick       - 快速启动"
    echo "    debug       - 调试模式启动"
    echo ""
    echo "  环境管理:"
    echo "    install     - 安装依赖"
    echo "    check       - 检查环境"
    echo "    clean       - 清理临时文件"
    echo "    reset       - 重置所有配置"
    echo ""
    echo "  开发工具:"
    echo "    lint        - 代码检查"
    echo "    test        - 运行测试"
    echo "    backup      - 备份项目"
    echo "    package     - 打包项目"
    echo ""
    echo "  帮助:"
    echo "    help        - 显示此帮助"
    echo "    version     - 显示版本信息"
    echo ""
    echo "用法: $0 <命令>"
}

# 运行程序
run_app() {
    print_header "启动程序"
    cd "$SCRIPT_DIR"
    if command -v python3 &> /dev/null; then
        python3 app.py
    else
        python app.py
    fi
}

# 快速启动
quick_start() {
    print_header "快速启动"
    ./quick_start.sh
}

# 调试模式
debug_mode() {
    print_header "调试模式"
    cd "$SCRIPT_DIR"
    echo "启用调试模式..."
    export DEBUG=1
    if command -v python3 &> /dev/null; then
        python3 -u app.py
    else
        python -u app.py
    fi
}

# 安装依赖
install_deps() {
    print_header "安装依赖"
    
    if command -v pip3 &> /dev/null; then
        pip3 install requests urllib3 beautifulsoup4
        print_success "依赖安装完成"
    else
        print_error "pip3不可用"
    fi
}

# 检查环境
check_env() {
    print_header "环境检查"
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        print_success "Python3: $(python3 --version)"
    else
        print_error "Python3未安装"
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3可用"
    else
        print_warning "pip3不可用"
    fi
    
    # 检查模块
    if python3 -c "import requests" &> /dev/null; then
        print_success "requests模块已安装"
    else
        print_error "requests模块未安装"
    fi
    
    # 检查项目文件
    required_files=("app.py" "src/parser.py" "src/m3u8_generator.py" "src/network.py")
    for file in "${required_files[@]}"; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            print_success "文件存在: $file"
        else
            print_error "文件缺失: $file"
        fi
    done
}

# 清理临时文件
clean_temp() {
    print_header "清理临时文件"
    
    cd "$SCRIPT_DIR"
    
    # 清理Python缓存
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # 清理日志文件
    rm -f startup.log
    
    # 清理临时下载文件
    rm -f *.tmp
    
    print_success "临时文件已清理"
}

# 重置配置
reset_config() {
    print_header "重置配置"
    
    echo "这将删除所有配置和历史记录，是否继续? (y/N)"
    read -r confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        rm -f streamers_history.json
        rm -f cookies.txt
        rm -f startup.log
        print_success "配置已重置"
    else
        print_warning "操作已取消"
    fi
}

# 代码检查
lint_code() {
    print_header "代码检查"
    
    # 检查Python语法
    python_files=(*.py)
    for file in "${python_files[@]}"; do
        if [ -f "$file" ]; then
            if python3 -m py_compile "$file" 2>/dev/null; then
                print_success "语法检查通过: $file"
            else
                print_error "语法错误: $file"
            fi
        fi
    done
}

# 运行测试
run_tests() {
    print_header "运行测试"
    
    # 简单的功能测试
    cd "$SCRIPT_DIR"
    
    echo "测试模块导入..."
    if python3 -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
try:
    import parser
    import m3u8_generator
    import network
    import config
    print('✓ 所有模块导入成功')
except ImportError as e:
    print(f'✗ 模块导入失败: {e}')
    exit(1)
"; then
        print_success "模块测试通过"
    else
        print_error "模块测试失败"
    fi
}

# 备份项目
backup_project() {
    print_header "备份项目"
    
    backup_dir="$HOME/Desktop/douyin_backup_$(date +%Y%m%d_%H%M%S)"
    
    # 创建备份目录
    mkdir -p "$backup_dir"
    
    # 复制项目文件
    cp -r "$SCRIPT_DIR"/* "$backup_dir/"
    
    # 排除不必要的文件
    rm -rf "$backup_dir/__pycache__"
    rm -f "$backup_dir"/*.log
    rm -f "$backup_dir"/*.tmp
    
    print_success "项目已备份到: $backup_dir"
}

# 打包项目
package_project() {
    print_header "打包项目"
    
    package_name="douyin_live_extractor_$(date +%Y%m%d).tar.gz"
    
    cd "$(dirname "$SCRIPT_DIR")"
    
    tar -czf "$package_name" \
        --exclude="__pycache__" \
        --exclude="*.log" \
        --exclude="*.tmp" \
        --exclude=".git" \
        "$(basename "$SCRIPT_DIR")"
    
    print_success "项目已打包: $package_name"
}

# 显示版本
show_version() {
    echo "抖音直播流提取器 v2.0"
    echo "最后更新: $(date '+%Y-%m-%d')"
}

# 主函数
main() {
    case "${1:-help}" in
        "run")
            run_app
            ;;
        "quick")
            quick_start
            ;;
        "debug")
            debug_mode
            ;;
        "install")
            install_deps
            ;;
        "check")
            check_env
            ;;
        "clean")
            clean_temp
            ;;
        "reset")
            reset_config
            ;;
        "lint")
            lint_code
            ;;
        "test")
            run_tests
            ;;
        "backup")
            backup_project
            ;;
        "package")
            package_project
            ;;
        "version")
            show_version
            ;;
        "help"|*)
            show_commands
            ;;
    esac
}

# 执行主函数
main "$@"
