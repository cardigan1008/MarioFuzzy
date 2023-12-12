import cv2
import numpy as np
import operator
import os

MIN_CONTOUR_AREA = 10

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


class ContourWithData():
    npaContour = None
    boundingRect = None
    intRectX = 0
    intRectY = 0
    intRectWidth = 0
    intRectHeight = 0
    fltArea = 0.0

    # 计算轮廓的左上点、宽度和高度
    def calculateRectTopLeftPointAndWidthAndHeight(self):
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    # 检查轮廓是否有效
    def checkIfContourIsValid(self):
        if self.fltArea < MIN_CONTOUR_AREA:
            return False
        return True


def number_get(test_image):
    allContoursWithData = []
    validContoursWithData = []

    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)
    except:
        print("错误：无法打开 classifications.txt 文件，退出程序\n")
        os.system("pause")
        return

    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
    except:
        print("错误：无法打开 flattened_images.txt 文件，退出程序\n")
        os.system("pause")
        return

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))

    # 创建KNN对象
    kNearest = cv2.ml.KNearest_create()

    # 训练KNN模型
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    # 读取测试数字图像
    imgTestingNumbers = cv2.resize(test_image, None, fx=2, fy=2)
    if imgTestingNumbers is None:
        print("错误：无法从文件中读取图像 \n\n")
        os.system("pause")
        return

    # 图像预处理：灰度化、模糊、二值化
    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)
    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 2)

    imgThreshCopy = imgThresh.copy()

    # 查找轮廓
    npaContours, npaHierarchy = cv2.findContours(imgThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历所有轮廓
    for npaContour in npaContours:
        contourWithData = ContourWithData()
        contourWithData.npaContour = npaContour
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)
        allContoursWithData.append(contourWithData)

    # 遍历有效轮廓
    for contourWithData in allContoursWithData:
        if contourWithData.checkIfContourIsValid():
            validContoursWithData.append(contourWithData)

    # 根据X坐标对轮廓进行排序
    validContoursWithData.sort(key=operator.attrgetter("intRectX"))

    # 最终识别结果字符串
    strFinalString = ""

    # 遍历有效轮廓
    for contourWithData in validContoursWithData:
        # 在原始图像上绘制绿色矩形
        cv2.rectangle(imgTestingNumbers,
                      (contourWithData.intRectX, contourWithData.intRectY),
                      (contourWithData.intRectX + contourWithData.intRectWidth,
                       contourWithData.intRectY + contourWithData.intRectHeight),
                      (0, 255, 0), 2)

        # 获取数字区域
        imgROI = imgThresh[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                 contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

        # 调整数字区域大小
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

        # 将数字区域展平为一维numpy数组
        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

        # 将数据类型转换为float32
        npaROIResized = np.float32(npaROIResized)

        # 使用KNN进行识别
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k=1)

        # 获取识别结果字符
        strCurrentChar = str(chr(int(npaResults[0][0])))
        strFinalString = strFinalString + strCurrentChar

    # # 打印最终结果字符串
    # print("\n" + strFinalString + "\n")
    #
    # # 显示带有绿色方框的输入图像
    # cv2.imshow("imgTestingNumbers", imgTestingNumbers)
    # cv2.waitKey(0)

    cv2.destroyAllWindows()
    return strFinalString


if __name__ == "__main__":
    number_get("resources/graphics/numberImage.png")
