import subprocess
import os
import yaml
import time
import pyautogui
from pynput.keyboard import Key, Controller
from ewmh import EWMH


class KeyboardActions:
    def __init__(self):
        self.keyboard = Controller()
        self.time_interval = 0.5

    def press_a_key(self):
        self.keyboard.press('a')
        time.sleep(self.time_interval)
        self.keyboard.release('a')

    def press_s_key(self):
        self.keyboard.press('s')
        time.sleep(self.time_interval)
        self.keyboard.release('s')

    def press_left_key(self):
        self.keyboard.press(Key.left)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.left)

    def press_right_key(self):
        self.keyboard.press(Key.right)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.right)

    def press_down_key(self):
        self.keyboard.press(Key.down)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.down)

    def press_enter_key(self):
        self.keyboard.press(Key.enter)
        time.sleep(self.time_interval)
        self.keyboard.release(Key.enter)


def take_screenshot(window, counter, current_directory):
    # 使用 xdotool 获取活动窗口的几何信息
    geometry_info = subprocess.run(['xdotool', 'getactivewindow', 'getwindowgeometry'], capture_output=True, text=True)

    # 解析获取到的几何信息
    lines = geometry_info.stdout.split('\n')
    for line in lines:
        if line.startswith('Geometry:'):
            _, geometry = line.split(':', 1)
            geometry = geometry.strip().split(' ')
            window_x, window_y = map(int, geometry[0].split('+'))
            window_width, window_height = map(int, geometry[1].split('x'))

            # 截取窗口图像
            screenshot = pyautogui.screenshot(region=(window_x, window_y, window_width, window_height))
            # 保存截图
            screenshot.save(os.path.join(current_directory, f"screenshot{counter}.png"))

            # 可以根据需要返回截图对象或者其他信息
            break


def play_game(operation_list):
    # 打开 YAML 文件
    with open("action/config.yaml", "r") as file:
        # 使用 PyYAML 加载 YAML 文件的内容
        yaml_data = yaml.safe_load(file)
    game_path = yaml_data["game_path"]

    current_directory = os.getcwd()
    print(current_directory)

    os.chdir(game_path)
    pygame_process = subprocess.Popen(['python', game_path + '/mario_level_1.py'])
    actions = KeyboardActions()

    time.sleep(5)
    actions.press_enter_key()
    time.sleep(5)
    counter = 0

    # 获取 Pygame 窗口句柄
    ewmh = EWMH()
    window = ewmh.getActiveWindow()

    for i in operation_list:
        if i == "l":
            actions.press_left_key()
        elif i == "r":
            actions.press_right_key()
        elif i == "a":
            actions.press_a_key()
        elif i == "s":
            actions.press_s_key()
        elif i == "d":
            actions.press_down_key()

        # 每次执行操作都截取游戏窗口的截图
        take_screenshot(window, counter, current_directory)
        counter = counter + 1

        time.sleep(1)  # 可以根据需要调整截图的时间间隔

    time.sleep(3)
    pygame_process.terminate()


if __name__ == "__main__":
    time.sleep(1)
    play_game("llllaaaarrrr")
