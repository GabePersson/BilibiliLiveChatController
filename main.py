import requests
import time
import win32api
import win32con
import win32gui
from datetime import datetime as dt
from config_manager import config

class BilibiliChatController:
    """B站聊天机器人控制器"""

    def __init__(self):
        """初始化控制器"""
        # 从配置加载参数
        self.room_id = config.get("room.id")
        self.api_url = config.get("room.api_url")
        self.user_agent = config.get("room.user_agent")
        self.window_title = config.get("game.window_title")
        self.key_mapping = config.get("game.key_mapping")
        self.message_delay = config.get("bot.message_delay")
        self.key_press_duration = config.get("bot.key_press_duration")
        self.max_command_length = config.get("bot.max_command_length")
        self.enable_logging = config.get("bot.enable_logging")

        # 请求头
        self.headers = {
            'user-agent': self.user_agent
        }

        # 时间戳记录
        self.latest_time = dt(1999, 1, 1, 1, 1, 1)

        # API地址
        self.api_address = f"{self.api_url}?roomid={self.room_id}"

        if self.enable_logging:
            print(f"初始化完成，直播间ID: {self.room_id}")
            print(f"目标窗口: {self.window_title}")

    def get_last_info(self) -> list:
        """
        获取最新的聊天消息

        Returns:
            新消息列表
        """
        info_list = list()
        try:
            # 发送API请求
            response = requests.request('GET', self.api_address, headers=self.headers)
            response.raise_for_status()

            # 解析响应
            data = response.json()
            room_data = data['data']['room']

            for info_dict in room_data:
                info_timestamp = info_dict['timeline']
                info_timestamp = dt.strptime(info_timestamp, '%Y-%m-%d %H:%M:%S')

                # 只处理新消息
                if info_timestamp <= self.latest_time:
                    continue

                self.latest_time = info_timestamp
                info_list.append(info_dict['text'])

            if self.enable_logging and info_list:
                print(f"收到 {len(info_list)} 条新消息")

        except requests.RequestException as e:
            print(f"API请求失败: {e}")
        except KeyError as e:
            print(f"响应数据格式错误: {e}")
        except Exception as e:
            print(f"获取消息时发生错误: {e}")

        return info_list

    def control_game(self, key: str) -> bool:
        """
        控制游戏发送按键

        Args:
            key: 要发送的键

        Returns:
            是否成功发送
        """
        try:
            # 检查当前窗口是否为目标窗口
            hwnd = win32gui.GetForegroundWindow()
            if win32gui.GetWindowText(hwnd) != self.window_title:
                if self.enable_logging:
                    print(f"活动窗口不正确，当前窗口: {win32gui.GetWindowText(hwnd)}")
                return False

            # 发送按键
            vk_key = self.key_mapping.get(key.lower())
            if vk_key is None:
                if self.enable_logging:
                    print(f"未知按键: {key}")
                return False

            if self.enable_logging:
                print(f"发送按键: {key} -> {vk_key}")

            win32api.keybd_event(vk_key, 0, 0, 0)
            time.sleep(self.key_press_duration)
            win32api.keybd_event(vk_key, 0, win32con.KEYEVENTF_KEYUP, 0)

            return True

        except Exception as e:
            print(f"发送按键时发生错误: {e}")
            return False

    def process_commands(self, messages: list):
        """
        处理消息中的命令

        Args:
            messages: 消息列表
        """
        for text in messages:
            # 只处理指定长度的消息
            if len(text) != self.max_command_length:
                continue

            key = text.lower()
            if key not in self.key_mapping:
                continue

            # 发送控制命令
            self.control_game(key)

    def run(self):
        """运行主循环"""
        if self.enable_logging:
            print("机器人启动...")
            print(f"API地址: {self.api_address}")
            print(f"按键映射: {self.key_mapping}")
            print("按Ctrl+C停止")

        try:
            while True:
                # 获取新消息
                info_list = self.get_last_info()

                # 处理命令
                self.process_commands(info_list)

                # 等待下一次检查
                time.sleep(self.message_delay)

        except KeyboardInterrupt:
            print("\n机器人已停止")
        except Exception as e:
            print(f"运行时发生错误: {e}")


def main():
    """主函数"""
    controller = BilibiliChatController()
    controller.run()


if __name__ == '__main__':
    main()