import numpy as np
import pyautogui
import cv2
import win32api, win32con, win32gui
from PIL import ImageGrab
from numberExtract import number_get

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
    grab_image = ImageGrab.grab((x1 + 20, y1, x2 - 20, y2-20))

    return grab_image


class OutputAnalysis:

    def check_image(self, image_path):
        # 读取目标图片和截屏
        template = cv2.imread('mario_bros.png', cv2.IMREAD_UNCHANGED)
        screenshot = cv2.imread('screenshot.png', cv2.IMREAD_UNCHANGED)
        if template is None or screenshot is None:
            print('Could not open or find the images!')
            exit(0)

        # 获取模板的透明度信息（alpha通道）
        template_alpha = template[:, :, 3]
        # 使用透明度信息创建掩码
        mask = template_alpha > 0
        # 将模板的透明背景保留
        template_rgb = template[:, :, :3]  # 获取RGB通道
        template_with_alpha = np.zeros_like(template_rgb, dtype=np.uint8)
        template_with_alpha[mask] = template_rgb[mask]

        templateGray = cv2.cvtColor(template_with_alpha, cv2.COLOR_BGR2GRAY)
        screenshotGray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Template", templateGray)
        cv2.imshow("Screenshot", screenshotGray)
        # 使用模板匹配方法
        result = cv2.matchTemplate(screenshotGray, templateGray, cv2.TM_CCORR_NORMED)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
        (startX, startY) = maxLoc
        endX = startX + template.shape[1]
        endY = startY + template.shape[0]

        cv2.rectangle(screenshot, (startX, startY), (endX, endY), (255, 0, 0), 3)

        print(np.max(result))
        cv2.imshow("Output", screenshot)
        cv2.waitKey(0)

        # # 设置匹配阈值，根据具体情况调整
        # threshold = 0.8
        #
        # # 如果最大匹配值大于阈值，认为目标存在
        # if np.max(result) > threshold:
        #     return True
        # else:
        #     return False

    # image_path 为截屏路径如 screenshot.png。
    def extract_score_from_image(self, image_path):
        screen = cv2.imread(image_path)
        imgROI = screen[165:219, 140:429]
        # cv2.imshow("ROI_WIN", imgROI)
        # cv2.waitKey(0)
        res = number_get(imgROI)
        if len(res) > 6:
            res = res[0:6]
        print("score:"+res)
        return res

    def extract_gold_from_image(self, image_path):
        screen = cv2.imread(image_path)
        imgROI = screen[165:219, 635:730]
        # cv2.imshow("ROI_WIN", imgROI)
        # cv2.waitKey(0)
        res = number_get(imgROI)
        if len(res) > 2:
            res = res[0:2]
        print("gold:"+res)
        return res


if __name__ == "__main__":
    s = fetch_image()
    s.save("screenshot.png")
    analysis = OutputAnalysis()
    print(analysis.extract_score_from_image("screenshot.png"))
    print(analysis.extract_gold_from_image("screenshot.png"))


