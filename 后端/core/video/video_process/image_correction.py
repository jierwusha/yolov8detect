import cv2
import math
import numpy as np

def image_correction(img):
    h, w = img.shape[:2]
    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 边缘检测
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    # 霍夫直线变换
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 50)
    # 如果未检测到直线，则退出
    if lines is None:
        print("No lines detected")
        return img
    # 初始化变量
    dst = None
    count = 0
    totalDst = 0
    # 绘制检测到的直线并计算斜率
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        if x1 == x2 or y1 == y2:
            continue
        t = float(y2 - y1) / (x2 - x1)
        if 0 < t < 1:
            dst = t
            count += 1
            totalDst = totalDst + dst
            break
    # 如果未找到合适的斜率，则退出
    if dst is None:
        print("No suitable lines found for rotation")
        return img

    # 计算旋转角度并旋转图像
    dst = totalDst / count
    rotate_angle = math.degrees(math.atan(dst))
    # 若倾斜角过小，则不处理
    if rotate_angle < 15:
        return img
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), borderValue=(255, 255, 255))
    cv2.imshow('img', img)
    cv2.waitKey(1)
    cv2.imshow('edges', rotated)
    cv2.waitKey(1)
    return rotated

if __name__ == '__main__':
    img = cv2.imread("test.jpg")
    image_correction(img)
