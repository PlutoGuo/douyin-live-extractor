# 抖音直播流 URL 提取器

一个功能强大的抖音直播流URL提取工具，支持多种清晰度提取、主播管理、自动播放等功能。

## ✨ 功能特性

### 🎯 核心功能
- **直播流提取**: 从抖音直播间URL提取多种清晰度的直播流
- **多格式支持**: 支持HLS (m3u8) 和 FLV 格式
- **质量选择**: 原画质、超高清(1080p)、高清(720p)、标清、流畅等多种清晰度
- **备用线路**: 自动提取主线路和备用线路确保稳定性

### 📱 界面功能
- **交互式菜单**: 简洁直观的命令行界面
- **主播管理**: 自动记录和管理提取过的主播信息
- **历史记录**: 提取成功率统计和时间记录
- **快速操作**: 支持重新提取、直接播放等快捷操作

### 🎬 播放功能
- **多播放器支持**: IINA、VLC、QuickTime Player
- **自动打开**: 提取完成后可直接调用播放器
- **文件管理**: 智能的文件命名和存储

### 🔧 高级功能
- **Cookie管理**: 支持自定义Cookie以应对反爬限制
- **文件存储设置**: 可自定义保存目录
- **旧记录清理**: 自动清理过期的主播记录
- **错误诊断**: 详细的错误信息和调试功能

## 🚀 快速开始

### 环境要求
- Python 3.7+
- 网络连接
- macOS 系统 (推荐安装IINA播放器)

### 依赖安装
```bash
pip install requests beautifulsoup4
```

### 启动方式

#### 方式一：快速启动 (推荐)
```bash
chmod +x scripts/quick_start.sh
./scripts/quick_start.sh
```

#### 方式二：完整启动
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

#### 方式三：直接运行
```bash
python src/main.py
```

### 便捷命令
项目提供了多个快捷命令：
```bash
# 使用便捷脚本
./scripts/dy          # 快速启动
./scripts/dyfast      # 极速模式
./scripts/dydev       # 开发者模式
```

## 📖 使用指南

### 1. 基本使用流程

1. **启动程序**
   ```bash
   ./scripts/quick_start.sh
   ```

2. **选择功能**
   - 🎯 提取直播流URL
   - 🎭 查看提取过的主播
   - 💾 文件存储设置
   - 🍪 Cookie管理
   - ❓ 使用帮助

3. **输入直播间信息**
   - 支持完整URL: `https://live.douyin.com/123456789`
   - 支持分享链接: `https://v.douyin.com/xxx/`
   - 支持直播间ID: `123456789`

4. **选择质量和播放**
   - 自动提取所有可用清晰度
   - 生成m3u8播放列表文件
   - 可选择播放器直接播放

### 2. 主播管理

程序会自动记录每次提取的主播信息：
- 主播昵称和直播间ID
- 提取时间和成功率统计
- 快速重新提取和播放功能
- 支持删除和清理旧记录

### 3. 高级设置

#### Cookie 配置
如遇到访问限制，可通过以下方式配置Cookie：
1. 在程序中选择"Cookie管理"
2. 输入从浏览器复制的Cookie值
3. Cookie将自动保存并在后续请求中使用

#### 存储目录设置
默认保存到：`~/Documents/直播源/抖音直播源/`
- 可通过"文件存储设置"修改
- 支持绝对路径和相对路径
- 程序会自动创建目录

## 📁 项目结构

```
douyin_live_extractor/
├── src/                          # 源代码目录
│   ├── main.py                   # 主程序入口
│   ├── config.py                 # 配置管理
│   ├── parser.py                 # 直播流解析器
│   ├── network.py                # 网络请求模块
│   ├── m3u8_generator.py         # M3U8文件生成器
│   ├── streamer_manager.py       # 主播信息管理
│   ├── cookie_manager.py         # Cookie管理
│   ├── iina_player.py            # 播放器集成
│   ├── ui.py                     # 用户界面
│   ├── simple_menu.py            # 简化菜单
│   ├── interactive_menu.py       # 交互式菜单
│   └── file_utils.py             # 文件工具
├── scripts/                      # 启动脚本
│   ├── quick_start.sh            # 快速启动脚本
│   ├── start.sh                  # 完整启动脚本
│   ├── dy                        # 便捷命令
│   ├── dyfast                    # 快速命令
│   └── dydev                     # 开发命令
├── docs/                         # 文档目录
├── logs/                         # 日志目录
├── temp/                         # 临时文件
└── README.md                     # 项目文档
```

## 🔧 技术实现

### 核心技术
- **HTML解析**: 使用BeautifulSoup解析直播页面
- **JSON数据提取**: 正则表达式匹配和JSON解析
- **流媒体处理**: 支持HLS和FLV协议
- **多线程**: 异步处理提高响应速度

### 数据提取流程
1. **页面获取**: 发送HTTP请求获取直播页面
2. **信息解析**: 提取主播信息、直播状态
3. **流数据解析**: 从JavaScript数据中提取流URL
4. **质量分析**: 解析技术参数(分辨率、帧率、编码)
5. **文件生成**: 生成标准m3u8播放列表

### 错误处理
- 网络超时重试机制
- 多种解析模式备份
- 详细的错误日志记录
- 用户友好的错误提示

## 📋 输出格式

### M3U8 播放列表文件
```m3u8
#EXTM3U
#EXT-X-VERSION:3
# 抖音直播流 - 主播名称
# 主播: 主播名称
# 直播间URL: https://live.douyin.com/123456
# 直播间ID: 123456
# 生成时间: 2024-08-08 17:00:01
# 质量等级: 6个

#EXTINF:-1,原画质 1920x1080 60fps H264 8000kbps
https://pull-f5-tt02.fcdn.us.tiktokcdn.com/game/stream-123456_uhd/playlist.m3u8

#EXTINF:-1,超高清 (1080p) 1920x1080 30fps H264 6000kbps
https://pull-f5-tt02.fcdn.us.tiktokcdn.com/game/stream-123456_hd/playlist.m3u8
```

### 主播记录数据
程序自动维护主播信息数据库：
```json
{
  "123456": {
    "nickname": "主播名称",
    "room_id": "123456",
    "live_url": "https://live.douyin.com/123456",
    "first_extract_time": "2024-08-08T17:00:01",
    "last_extract_time": "2024-08-08T17:00:01",
    "extract_history": [
      {
        "timestamp": "2024-08-08T17:00:01",
        "success": true,
        "nickname": "主播名称"
      }
    ]
  }
}
```

## ⚠️ 注意事项

1. **合法使用**: 仅用于个人学习和研究，请遵守抖音平台服务条款
2. **网络环境**: 需要稳定的网络连接和正常的DNS解析
3. **Cookie限制**: 如遇访问限制，可能需要配置有效的Cookie
4. **播放器兼容**: 推荐使用IINA播放器以获得最佳体验
5. **系统兼容**: 主要针对macOS优化，其他系统可能需要调整

## 🔄 版本更新

- **v1.0**: 基础直播流提取功能
- **v1.1**: 添加主播管理和历史记录
- **v1.2**: 优化用户界面和错误处理
- **v1.3**: 增加多播放器支持和便捷脚本
- **v1.4**: 完善Cookie管理和文件存储设置

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目。

## 📄 许可证

本项目仅供学习和研究使用，请勿用于商业用途。
https://vsllm.cc

---

**免责声明**: 本工具仅用于技术研究和个人学习，使用者需自行承担使用风险，并遵守相关法律法规和平台服务条款。
