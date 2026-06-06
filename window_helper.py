"""
窗口助手工具 - 帮助用户轻松获取窗口信息
"""

import win32gui
import win32con
import time
import json
from config_manager import config

def list_windows():
    """列出所有可见窗口"""
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # 只显示有标题的窗口
                class_name = win32gui.GetClassName(hwnd)
                windows.append({
                    'hwnd': hwnd,
                    'title': title,
                    'class': class_name
                })
        return True

    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def find_window_by_keywords(keywords):
    """根据关键词查找窗口"""
    windows = list_windows()
    matches = []

    for window in windows:
        for keyword in keywords:
            if keyword.lower() in window['title'].lower():
                matches.append(window)
                break

    return matches

def interactive_window_selection():
    """交互式窗口选择"""
    print("=== 窗口选择助手 ===\n")

    # 获取当前配置的窗口标题
    current_title = config.get("game.window_title", "")

    if current_title and current_title != "YOUR_GAME_WINDOW_TITLE":
        print(f"当前配置的窗口标题: {current_title}")
        print("1. 使用当前配置")
        print("2. 重新选择窗口")
        print("3. 查看所有窗口")

        choice = input("\n请选择 (1/2/3): ")
        if choice == "1":
            return current_title
        elif choice == "2":
            pass  # 继续选择
        elif choice == "3":
            pass  # 继续查看所有窗口
        else:
            print("无效选择，继续查看窗口")

    print("\n正在搜索窗口...")

    # 常见游戏窗口关键词
    game_keywords = [
        "game", "play", "steam", "origin", "epic", "battle.net",
        "window", "client", "launcher", "executable"
    ]

    matches = find_window_by_keywords(game_keywords)

    if not matches:
        print("未找到匹配的游戏窗口")
        print("\n所有可见窗口:")
        matches = list_windows()
    else:
        print(f"找到 {len(matches)} 个可能的窗口:")

    # 显示窗口列表
    for i, window in enumerate(matches[:20], 1):  # 最多显示20个
        print(f"{i}. {window['title']}")
        if i == 10 and len(matches) > 20:
            print(f"... 还有 {len(matches) - 20} 个窗口")
            break

    # 让用户选择
    if matches:
        print("\n请输入窗口编号，或输入关键词搜索: ", end="")
        user_input = input().strip()

        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(matches):
                return matches[index]['title']

        # 如果输入的不是数字，作为关键词搜索
        elif user_input:
            new_matches = find_window_by_keywords([user_input])
            if new_matches:
                print(f"\n找到 {len(new_matches)} 个匹配窗口:")
                for i, window in enumerate(new_matches[:5], 1):
                    print(f"{i}. {window['title']}")

                if len(new_matches) > 0:
                    choice = input(f"\n请选择 (1-{len(new_matches)}): ")
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(new_matches):
                            return new_matches[idx]['title']

    # 手动输入
    print("\n请手动输入窗口标题:")
    manual_title = input().strip()
    return manual_title if manual_title else "YOUR_GAME_WINDOW_TITLE"

def test_window_connection(window_title):
    """测试窗口连接"""
    try:
        hwnd = win32gui.FindWindowEx(None, None, window_title, None)
        if hwnd:
            print(f"✓ 找到窗口: {window_title}")
            print(f"  窗口句柄: {hwnd}")
            print(f"  窗口类名: {win32gui.GetClassName(hwnd)}")
            return True
        else:
            print(f"✗ 未找到窗口: {window_title}")
            print("  请确保窗口已打开且标题正确")
            return False
    except Exception as e:
        print(f"测试窗口时发生错误: {e}")
        return False

def auto_detect_game_window():
    """自动检测游戏窗口"""
    print("=== 自动检测游戏窗口 ===\n")

    # 常见游戏窗口类名
    game_classes = [
        "UnrealWindow", "UnityPlayer", "SDL_app",
        "GameWindow", "MainWindow", "Qt5152QWindowIcon"
    ]

    def enum_windows_callback(hwnd, matches):
        if win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)

            if title and class_name in game_classes:
                matches.append({
                    'hwnd': hwnd,
                    'title': title,
                    'class': class_name
                })
        return True

    matches = []
    win32gui.EnumWindows(enum_windows_callback, matches)

    if matches:
        print(f"自动检测到 {len(matches)} 个可能的游戏窗口:")
        for i, window in enumerate(matches, 1):
            print(f"{i}. {window['title']} (类: {window['class']})")

        if len(matches) == 1:
            title = matches[0]['title']
            print(f"\n自动选择: {title}")
            return title
        else:
            choice = input("\n请选择窗口编号: ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(matches):
                    return matches[idx]['title']

    return None

def main():
    """主函数"""
    print("窗口助手 - 帮助您获取游戏窗口标题")
    print("=" * 50)

    while True:
        print("\n请选择操作:")
        print("1. 交互式选择窗口")
        print("2. 自动检测游戏窗口")
        print("3. 测试窗口连接")
        print("4. 生成配置文件")
        print("5. 退出")

        choice = input("\n请选择 (1-5): ").strip()

        if choice == "1":
            title = interactive_window_selection()
            config._config["game"]["window_title"] = title
            print(f"\n已设置窗口标题: {title}")

        elif choice == "2":
            title = auto_detect_game_window()
            if title:
                config._config["game"]["window_title"] = title
                print(f"\n已设置窗口标题: {title}")
            else:
                print("未检测到游戏窗口，请使用交互式选择")

        elif choice == "3":
            title = config.get("game.window_title", "")
            if title and title != "YOUR_GAME_WINDOW_TITLE":
                test_window_connection(title)
            else:
                print("请先设置窗口标题")

        elif choice == "4":
            config_file = input("输入配置文件名 (默认: config.json): ").strip()
            if not config_file:
                config_file = "config.json"
            config.save()
            print(f"\n配置已保存到: {config_file}")

        elif choice == "5":
            print("退出窗口助手")
            break

        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()