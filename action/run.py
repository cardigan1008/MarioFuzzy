import cv2
import numpy as np
import subprocess
import os
import yaml
import time
import pyautogui

from pynput.keyboard import Key, Controller


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

def play_game(operation_list):
    # 打开 YAML 文件
    with open("config.yaml", "r") as file:
        # 使用 PyYAML 加载 YAML 文件的内容
        yaml_data = yaml.safe_load(file)
    game_path = yaml_data["game_path"]

    os.chdir(game_path)

    pygame_process = subprocess.Popen(['python', game_path+'/mario_level_1.py'])

    actions = KeyboardActions()

    time.sleep(1)
    actions.press_enter_key()
    time.sleep(5)
    counter = 0
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
        # 获取屏幕尺寸
        screen_width, screen_height = pyautogui.size()
        # 截取整个屏幕图像
        screenshot = pyautogui.screenshot()
        # 保存截图
        screenshot.save("screenshot.png")

    pygame_process.terminate()

if __name__ == "__main__":
    time.sleep(1)
    play_game("llaassddrr")