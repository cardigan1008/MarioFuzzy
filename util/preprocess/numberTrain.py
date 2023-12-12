import sys
import numpy as np
import cv2
import os

MIN_CONTOUR_AREA = 10

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

def main():
    # 读取训练数字图像
    imgTrainingNumbers = cv2.imread("resources/graphics/numberImage.png")
    if imgTrainingNumbers is None:
        print("错误: 无法从文件中读取图像 \n\n")
        os.system("pause")
        return

    # 调整图像大小
    imgTrainingNumbers = cv2.resize(imgTrainingNumbers, None, fx=2, fy=2)

    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)
    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)

    # 自适应阈值化
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 2)

    imgThreshCopy = imgThresh.copy()

    npaContours, npaHierarchy = cv2.findContours(imgThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 初始化numpy数组，用于存储压平后的图像
    npaFlattenedImages = np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    # 初始化分类列表
    intClassifications = []

    # 允许的有效字符列表
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'),
                     ord('7'), ord('8'), ord('9')]

    # 遍历所有轮廓
    for npaContour in npaContours:
        # 如果轮廓面积大于阈值
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)

            # 在原始图像上绘制红色矩形
            cv2.rectangle(imgTrainingNumbers, (intX, intY), (intX + intW, intY + intH), (0, 0, 255), 2)

            imgROI = imgThresh[intY:intY + intH, intX:intX + intW]
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

            # 显示原始字符区域和调整大小后的字符区域
            cv2.imshow("imgROI", imgROI)
            cv2.imshow("imgROIResized", imgROIResized)
            cv2.imshow("training_numbers.png", imgTrainingNumbers)

            # 获取键盘输入
            intChar = cv2.waitKey(0)

            # 如果按下ESC键，退出程序
            if intChar == 27:
                sys.exit()
            # 如果按下有效字符，添加到分类列表
            elif intChar in intValidChars:
                intClassifications.append(intChar)

                # 压平字符区域并添加到数组
                npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

    # 将分类列表转换为float32数组
    fltClassifications = np.array(intClassifications, np.float32)

    # 将数组重新形状为1D数组
    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))

    print("\n训练完成！！\n")

    # 将分类结果和压平后的图像保存到文件
    np.savetxt("classifications.txt", npaClassifications)
    np.savetxt("flattened_images.txt", npaFlattenedImages)

    # 关闭所有窗口
    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()
