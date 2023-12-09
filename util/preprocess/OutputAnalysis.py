import time
import numpy as np
import pyautogui
from PIL import ImageGrab
import cv2
import win32api, win32con, win32gui
from PIL import Image, ImageGrab


def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
        # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle


def fetch_image():
    (x1, y1, x2, y2), handle = get_window_pos('Super Mario Bros 1-1')
    # 发送还原最小化窗口的信息
    win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    # 设为高亮
    win32gui.SetForegroundWindow(handle)
    # 截图
    grab_image = ImageGrab.grab((x1 + 20, y1, x2 - 20, y2 - 20))

    return grab_image


class OutputAnalysis:

    def check_image(self, image_path):
        # 定义要查找的图像
        target_image = "mario.png"

        template = cv2.imread(target_image, cv2.IMREAD_UNCHANGED)
        image = cv2.imread(image_path)

        # 使用模板匹配方法
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        # 设置匹配阈值，根据具体情况调整
        threshold = 0.8

        # 如果最大匹配值大于阈值，认为目标存在
        if np.max(result) > threshold:
            return True
        else:
            return False

    # TODO:
    def extract_text_from_image(self, image_path):
        # 读取图像
        image = cv2.imread(image_path)
    #
    #     # 转换为灰度图像
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #
    #     # 使用Tesseract进行OCR
    #     text = pytesseract.image_to_string(gray)
    #
    #     print("Extracted Text:")
    #     print(text)

    # if __name__ == "__main__":
        # # 获取屏幕截图
        # s = fetch_image()
        #
        # # 将截图保存为文件,
        # s.save("screenshot.png")
        # extract_text_from_image('screenshot.png')

        # 运行轮询
        # while True:
        #     if check_image('screenshot.png'):
        #         print("找到目标图像！")
        #
        #     # 间隔一段时间再次轮询
        #     time.sleep(1)

        # extract_text_from_image('mario.png')
