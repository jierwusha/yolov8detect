import torch
import numpy as np
from random import randint
from ultralytics import YOLO
from PIL import Image
import cv2


class Detector(object):

    def __init__(self, weights):
        self.img_size = 640
        self.threshold = 0.4
        self.weights = weights
        self.init_model()

    def init_model(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = YOLO(self.weights).to(self.device)
        self.names = self.model.names
        self.colors = [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in self.names]

    def plot_bboxes(self, image, boxes, line_thickness=None):
        tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # 线条/字体粗细
        detected_classes = []  # 初始化识别结果的列表

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 提取边界框坐标并转换为整数
            cls_id = int(box.cls[0])  # 提取类别ID
            conf = box.conf[0]  # 提取置信度分数

            if cls_id >= len(self.names):
                print(f"无效的类别ID {cls_id}，超出了名称列表的范围")
                continue

            color = self.colors[cls_id]
            c1, c2 = (x1, y1), (x2, y2)
            cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
            tf = max(tl - 1, 1)  # 字体粗细
            label = f'{self.names[cls_id]} {conf:.2f}'
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

            # 添加文本背景矩形
            text_bg_color = (0, 0, 0)  # 黑色背景
            cv2.rectangle(image, c1, c2, text_bg_color, -1, cv2.LINE_AA)  # 填充
            cv2.putText(image, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf,
                        lineType=cv2.LINE_AA)

            # 收集识别结果，附带边界框左上角的x坐标
            detected_classes.append((x1, self.names[cls_id]))

        # 根据x坐标对识别结果进行排序
        detected_classes.sort(key=lambda x: x[0])
        detected_classes_str = ''.join([cls[1] for cls in detected_classes])

        return image, detected_classes_str

    def detect(self, image_path, output_image_path='results.jpg'):
        # 加载图像
        orig_img = cv2.imread(image_path)

        # 计算新的尺寸，同时保持纵横比
        height, width = orig_img.shape[:2]
        new_width = self.img_size
        scale_ratio = new_width / width
        new_height = int(height * scale_ratio)

        # 在保持纵横比的同时调整图像大小
        resized_img = cv2.resize(orig_img, (new_width, new_height))

        # 执行推理
        results = self.model(resized_img)

        # 处理结果并绘制边界框
        r = results[0]
        boxes = r.boxes
        im_array = r.orig_img.copy()
        im_array, detected_classes_str = self.plot_bboxes(im_array, boxes)

        im = Image.fromarray(cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB))  # 确保颜色空间转换正确
        im.save(output_image_path)  # 保存图像

        return detected_classes_str





# def plot_bboxes(self, image, bboxes, line_thickness=None):
#     tl = line_thickness or round(
#         0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
#     for (x1, y1, x2, y2, cls_id, conf) in bboxes:
#         color = self.colors[self.names.index(cls_id)]
#         c1, c2 = (x1, y1), (x2, y2)
#         cv2.rectangle(image, c1, c2, color,
#                       thickness=tl, lineType=cv2.LINE_AA)
#         tf = max(tl - 1, 1)  # font thickness
#         t_size = cv2.getTextSize(
#             cls_id, 0, fontScale=tl / 3, thickness=tf)[0]
#         c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
#         cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)  # filled
#         cv2.putText(image, '{} ID-{:.2f}'.format(cls_id, conf), (c1[0], c1[1] - 2), 0, tl / 3,
#                     [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
#     return image
#
# def detect(self, im):
#     im0, img = self.preprocess(im)
#
#     pred = self.model(img)[0]
#
#     pred_boxes = []
#     image_info = {}
#     count = 0
#     for det in pred:
#         if det is not None and len(det):
#             det[:, :4] = scale_coords(
#                 img.shape[2:], det[:, :4], im0.shape).round()
#
#             for *x, conf, cls_id in det:
#                 lbl = self.names[int(cls_id)]
#                 x1, y1 = int(x[0]), int(x[1])
#                 x2, y2 = int(x[2]), int(x[3])
#                 pred_boxes.append(
#                     (x1, y1, x2, y2, lbl, conf))
#                 count += 1
#                 key = f'{lbl}-{count:02}'
#                 image_info[key] = [f'{x2 - x1}×{y2 - y1}', np.round(float(conf), 3)]
#
#     im = self.plot_bboxes(im, pred_boxes)
#     return im, image_info


#
#
# def detect(image, boxes, names, colors, line_thickness=None):
#     tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # 线条/字体粗细
#     detected_classes = []  # 初始化识别结果的列表
#
#     for box in boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])  # 提取边界框坐标并转换为整数
#         cls_id = int(box.cls[0])  # 提取类别ID
#         conf = box.conf[0]  # 提取置信度分数
#
#         if cls_id >= len(names):
#             print(f"无效的类别ID {cls_id}，超出了名称列表的范围")
#             continue
#
#         color = colors[cls_id]
#         c1, c2 = (x1, y1), (x2, y2)
#         cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
#         tf = max(tl - 1, 1)  # 字体粗细
#         label = f'{names[cls_id]} {conf:.2f}'
#         t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
#         c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
#
#         # 添加文本背景矩形
#         text_bg_color = (0, 0, 0)  # 黑色背景
#         cv2.rectangle(image, c1, c2, text_bg_color, -1, cv2.LINE_AA)  # 填充
#         cv2.putText(image, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
#
#         # 收集识别结果，附带边界框左上角的x坐标
#         detected_classes.append((x1, names[cls_id]))
#
#     # 根据x坐标对识别结果进行排序
#     detected_classes.sort(key=lambda x: x[0])
#     detected_classes_str = ''.join([cls[1] for cls in detected_classes])
#
#     return image, detected_classes_str
#
#
# model = YOLO("E:\\ultralytics-main\\runs\\detect\\train10\\weights\\best.pt")
# image_path = "E:/ultralytics-main/img/test/1.jpg"
#
# # 加载图像
# orig_img = cv2.imread(image_path)
#
# # 计算新的尺寸，同时保持纵横比
# height, width = orig_img.shape[:2]
# new_width = 640
# scale_ratio = new_width / width
# new_height = int(height * scale_ratio)
#
# # 在保持纵横比的同时调整图像大小
# resized_img = cv2.resize(orig_img, (new_width, new_height))
#
# # 执行推理
# results = model(resized_img)
#
# # 保存裁剪后的图像到指定目录
# for r in results:
#     boxes = r.boxes
#     names = r.names
#     # 生成颜色列表，长度与类别数量一致
#     colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] * (len(names) // 3 + 1)
#     colors = colors[:len(names)]
#     im_array = r.orig_img.copy()
#     im_array, detected_classes_str = plot_bboxes(im_array, boxes, names, colors)
#
#     im = Image.fromarray(cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB))  # 确保颜色空间转换正确
#     im.save('results.jpg')  # 保存图像
#
#     print(detected_classes_str)  # 输出识别结果字符串
