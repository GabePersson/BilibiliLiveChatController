import json
import os
from typing import Dict, Any

class ConfigManager:
    """配置管理器，负责加载和管理应用程序配置"""

    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径，默认为config.json
        """
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            # 如果配置文件不存在，使用默认配置
            return self._get_default_config()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"加载配置文件失败: {e}")
            print("使用默认配置")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "room": {
                "id": "YOUR_ROOM_ID",
                "api_url": "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
            },
            "game": {
                "window_title": "YOUR_GAME_WINDOW_TITLE",
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
                "enable_logging": True
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项，支持点号分隔的嵌套键

        Args:
            key: 配置键，如"room.id"
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def reload(self):
        """重新加载配置文件"""
        self._config = self._load_config()
        print("配置已重新加载")

    def save(self):
        """保存当前配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            print("配置已保存")
        except IOError as e:
            print(f"保存配置文件失败: {e}")

# 全局配置实例
config = ConfigManager()

# 使用示例：
# config.get("room.id")  # 获取直播间ID
# config.get("game.window_title")  # 获取游戏窗口标题
# config.get("bot.message_delay")  # 获取消息延迟时间