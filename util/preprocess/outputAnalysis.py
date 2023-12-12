import glob
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
        template_image_path = './mario/small_normal/right_small_normal_0.png'

        # 遍历文件
        PATH_TO_TEST_IMAGES_DIR = './mario'
        for pidImage in glob.glob(PATH_TO_TEST_IMAGES_DIR + "/*/*.png"):
            template_image_path = pidImage
            template_image_path = template_image_path.replace('\\', '/')
            print(template_image_path)

            # 读取mario和背景
            template = cv2.imread(template_image_path, 0)
            screenshot = cv2.imread(image_path, 0)
            if template is None or screenshot is None:
                print('Could not open or find the images!')
                exit(0)
            template = cv2.resize(template, None, fx=2, fy=2)
            # 创建SIFT对象
            sift = cv2.xfeatures2d.SIFT_create()
            # 提取特征点
            kp1, des1 = sift.detectAndCompute(template, None)
            kp2, des2 = sift.detectAndCompute(screenshot, None)
            # 创建BFMatcher对象
            bf = cv2.BFMatcher()
            # 匹配特征点
            matches = bf.knnMatch(des1, des2, k=2)
            # 应用ratio test
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            # 若匹配超过5点则认为存在
            if len(good) > 5:
                # # 画出匹配结果
                # img3 = cv2.drawMatchesKnn(template, kp1, screenshot, kp2, good, None, flags=2)
                # # 显示图片
                # cv2.imshow('result', img3)
                # cv2.waitKey(0)
                return True
        return False


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
    print(analysis.check_image("screenshot.png"))
    print(analysis.extract_score_from_image("screenshot.png"))
    print(analysis.extract_gold_from_image("screenshot.png"))


