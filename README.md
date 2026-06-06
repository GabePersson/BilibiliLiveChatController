# Bilibili Live Chat Bot

一个基于Bilibili直播聊天室的游戏控制机器人，可以通过聊天命令控制游戏窗口进行按键操作。

## 功能特点

- 🎮 **实时监控**：实时获取Bilibili直播聊天室消息
- ⌨️ **游戏控制**：通过聊天命令（W/A/S/D）控制游戏窗口
- 🔧 **配置灵活**：支持自定义直播间ID、游戏窗口标题和按键映射
- 🛡️ **安全验证**：自动验证目标窗口，防止误操作
- 📊 **日志记录**：可选的详细日志输出

## 系统要求

- Windows 10/11
- Python 3.7+
- Bilibili直播间ID

## 安装依赖

```bash
pip install requests pywin32
```

## 快速开始

### 1. 获取直播间ID

访问Bilibili直播间，URL中的数字即为直播间ID。例如：
- `https://live.bilibili.com/25614030` → 直播间ID为 `25614030`

### 2. 获取游戏窗口标题

运行窗口助手工具：
```bash
python window_helper.py
```

按提示选择或自动检测游戏窗口，工具会自动设置窗口标题到配置文件。

### 3. 配置设置

复制示例配置文件并编辑：
```bash
cp config.example.json config.json
```

然后编辑 `config.json` 文件：
```json
{
  "room": {
    "id": 25614030,
    "api_url": "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
  },
  "game": {
    "window_title": "你的游戏窗口标题",
    "key_mapping": {
      "w": 87,
      "a": 65,
      "s": 83,
      "d": 68
    }
  },
  "bot": {
    "message_delay": 0.2,
    "key_press_duration": 0.1,
    "max_command_length": 1,
    "enable_logging": true
  }
}
```

### 4. 运行机器人

```bash
python main.py
```

## 配置说明

### room 部分
- `id`: Bilibili直播间ID
- `api_url`: 聊天历史API地址
- `user_agent`: HTTP请求头

### game 部分
- `window_title`: 目标游戏窗口的完整标题（必须完全匹配）
- `key_mapping`: 按键映射表（字符到Windows虚拟键码）

### bot 部分
- `message_delay`: 检查新消息的间隔时间（秒）
- `key_press_duration`: 按键持续时间（秒）
- `max_command_length`: 命令最大长度（1表示只处理单字符命令）
- `enable_logging`: 是否启用详细日志

## 使用方法

1. **启动游戏**：先打开要控制的游戏窗口
2. **运行机器人**：执行 `python main.py`
3. **发送命令**：在Bilibili直播间聊天室发送 W/A/S/D 字符
4. **窗口验证**：机器人会确保当前活动窗口是目标游戏窗口

## 注意事项

### 重要提醒
- **安全第一**：机器人只会发送按键到标题完全匹配的窗口，但请谨慎使用
- **不要关闭聊天窗口**：确保聊天窗口不被遮挡
- **网络连接**：需要稳定的网络连接来获取聊天消息
- **权限问题**：如果遇到权限问题，请以管理员身份运行
- **直播间ID**：直播间ID是公开信息，可以通过直播间URL获取，分享项目时无需隐藏

### 常见问题

1. **按键无效**
   - 检查游戏窗口标题是否正确
   - 确保游戏窗口处于活动状态
   - 检查按键映射是否正确

2. **收不到消息**
   - 检查直播间ID是否正确
   - 确认直播间允许发送弹幕
   - 检查网络连接

3. **窗口找不到**
   - 使用 `window_helper.py` 重新获取窗口标题
   - 确保游戏窗口已经打开
   - 检查窗口标题是否有特殊字符

## 高级功能

### 自定义按键映射

修改 `config.json` 中的 `key_mapping` 部分：
```json
"key_mapping": {
  "w": 87,
  "a": 65,
  "s": 83,
  "d": 68,
  "q": 81,
  "e": 69
}
```

### 批量处理命令

设置 `max_command_length` 为更大的值来处理多字符命令。

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 免责声明

本项目仅供学习和娱乐使用。使用者需要自行承担使用风险，开发者不对任何直接或间接的损失负责。

## 支持我们

如果你觉得这个项目对你有帮助，欢迎支持我们在B站的账号：**KingSm1le** (UID: 1801975372)

你们的关注是我们持续更新的动力！🎮

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的聊天命令控制
- 实现配置管理系统
- 添加窗口助手工具