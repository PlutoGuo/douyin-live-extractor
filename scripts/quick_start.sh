#!/bin/bash

# 抖音直播流提取器 - 快速启动脚本
# 简化版本，适合日常使用

# 获取脚本目录的父目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}🎬 抖音直播流提取器${NC}"
echo -e "${BLUE}===============================${NC}"

# 切换到项目目录
cd "$SCRIPT_DIR"

# 检查Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 未找到Python环境"
    exit 1
fi

# 检查主程序文件
if [ ! -f "app.py" ]; then
    echo "❌ 未找到app.py文件"
    exit 1
fi

echo -e "${GREEN}🚀 启动程序...${NC}"
echo ""

# 启动主程序
$PYTHON_CMD app.py

echo ""
echo -e "${BLUE}👋 程序已退出${NC}"
