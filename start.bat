@echo off
chcp 65001 >nul
echo Bilibili直播聊天机器人启动中...
echo.
echo 请确保：
echo 1. 已安装所需依赖（pip install requests pywin32）
echo 2. 已配置 config.json 文件
echo 3. 游戏窗口已经打开
echo.
python main.py
pause