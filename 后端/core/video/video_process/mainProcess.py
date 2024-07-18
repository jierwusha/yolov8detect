import argparse
import os
import time
from collections import Counter

import cv2
import numpy as np
from ultralytics import YOLO, solutions

from core.video.video_process import run_LPRNet
from core.video.video_process.data import CHARS
from core.video.video_process.image_correction import image_correction
from core.video.video_process.model import build_lprnet


import torch

from PIL import Image, ImageDraw, ImageFont
import Levenshtein


def mainProcess(YOLOmodelPath, LPRNetModelPath, dataPath, savePath):
    #初始化
    #加载字体
    font = ImageFont.truetype('./core/video/video_process/SourceHanSansCN-Heavy.otf', 20)
    # 导入模型
    model = YOLO(YOLOmodelPath)
    print("导入模型成功:" + YOLOmodelPath)

    # LPRNet网络构建
    args = get_parser()
    lprnet = build_lprnet(lpr_max_len=args.lpr_max_len, phase=args.phase_train, class_num=len(CHARS),
                          dropout_rate=args.dropout_rate)
    device = torch.device("cuda:0" if args.cuda else "cpu")
    lprnet.to(device)
    print("成功构建网络")

    # 文件保存初始化
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
    file_extension = os.path.splitext(savePath)[1].lower()
    isVideo = file_extension in video_extensions
    cap = cv2.VideoCapture(dataPath)
    base_name = os.path.splitext(os.path.basename(dataPath))[0]
    if isVideo:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video = cv2.VideoWriter(savePath, fourcc, fps, (width, height))
        savePath = os.path.join(savePath, base_name + '_检测结果.mp4')
    else:
        savePath = os.path.join(savePath, base_name + '_检测结果.png')

    # LPRNet模型加载
    if args.pretrained_model:
        lprnet.load_state_dict(torch.load(LPRNetModelPath))
        print("加载模型成功:" + args.pretrained_model)
    else:
        print("[Error] 无法找到模型：" + args.pretrained_model)
        return False

    # 推理
    results = model.predict(dataPath, stream=True, conf=0.1)
    for result in results:
        start_time = time.time()
        # 将图像分割
        cimages = crop_boxes_from_image(result)
        # 使用lprnet处理
        labels = run_LPRNet.Predict(lprnet, cimages, args)
        # 进行标记
        lbs = []
        for label in labels:
            lb = ""
            for i in label:
                lb += CHARS[i]
            print(lb)
            lbs.append(lb)
        fimg = draw_boxes(result, lbs, font)
        end_time = time.time()
        print(str(end_time - start_time))
        # 重新将图片合成为视频
        if isVideo:
            video.write(fimg)
            print("文件已保存" + savePath)
            return True
        else:
            # cv2.imwrite(savePath, fimg)
            print("文件已保存" + savePath)
            return lbs[0]
    if isVideo:
        video.release()
        cap.release()


def crop_boxes_from_image(result):
    image = result.orig_img
    boxes = result.boxes
    cropped_images = []
    for xyxy in boxes.xyxy:
        x1, y1, x2, y2 = xyxy
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cropped_image = image[y1:y2, x1:x2]
        cropped_image = image_correction(cropped_image)
        cropped_images.append(cropped_image)
    return cropped_images

def get_parser():
    parser = argparse.ArgumentParser(description='parameters to train net')
    parser.add_argument('--img_size', default=[94, 24], help='the image size')
    parser.add_argument('--test_img_dirs', default="./data/test", help='the test images path')
    parser.add_argument('--dropout_rate', default=0, help='dropout rate.')
    parser.add_argument('--lpr_max_len', default=8, help='license plate number max length.')
    parser.add_argument('--test_batch_size', default=100, help='testing batch size.')
    parser.add_argument('--phase_train', default=False, type=bool, help='train or test phase flag.')
    parser.add_argument('--num_workers', default=8, type=int, help='Number of workers used in dataloading')
    parser.add_argument('--cuda', default=True, type=bool, help='Use cuda to train model')
    parser.add_argument('--show', default=False, type=bool, help='show test image and its predict result or not.')
    parser.add_argument('--pretrained_model', default='./weights/Final_LPRNet_model.pth', help='pretrained base model')

    args = parser.parse_args()

    return args

def draw_boxes(result, labels, font):
    image = result.orig_img
    boxes = result.boxes
    for xyxy, label in zip(boxes.xyxy, labels):
        x1, y1, x2, y2 = xyxy
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # 绘制边界框
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绿色边框，线宽为2
        # 添加类别名称和置信度
        label = f"{label}"
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)
        draw.text((x1, y1 - 30), label, font=font, fill=(0, 255, 0, 0))
        image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        # cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image


def countCar(YOLOmodelPath, LPRNetModelPath, dataPath, savePath):
    model = YOLO(YOLOmodelPath)
    cap = cv2.VideoCapture(dataPath)
    assert cap.isOpened(), "Error reading video file"
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = 1 / fps


    # Define line points
    line_points = [(0, 400), (1080, 400)]
    region_points = [(0, 500), (10800, 500), (10800, 600), (0, 600)]

    # Video writer
    video_writer = cv2.VideoWriter(savePath, cv2.VideoWriter_fourcc(*"VP90"), fps, (w, h))

    # Init Object Counter
    counter = solutions.ObjectCounter(
        view_img=True,
        reg_pts=region_points,
        classes_names=model.names,
        draw_tracks=True,
        line_thickness=2,
        region_thickness=5,
        view_out_counts=False

    )

    #LPRNet初始化
    font = ImageFont.truetype('./core/video/video_process/SourceHanSansCN-Heavy.otf', 20)
    # LPRNet网络构建
    args = get_parser()
    lprnet = build_lprnet(lpr_max_len=args.lpr_max_len, phase=args.phase_train, class_num=len(CHARS),
                          dropout_rate=args.dropout_rate)
    device = torch.device("cuda:0" if args.cuda else "cpu")
    lprnet.to(device)
    print("成功构建网络")
    # LPRNet模型加载
    if args.pretrained_model:
        lprnet.load_state_dict(torch.load(LPRNetModelPath))
        print("加载模型成功:" + args.pretrained_model)
    else:
        print("[Error] 无法找到模型：" + args.pretrained_model)
        return False

    # 车牌识别结果存储
    results_list = []

    frame_number = 0
    while cap.isOpened():
        current_time = frame_number * frame_interval
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        tracks = model.track(im0, persist=True, show=False)
        result = tracks[0]
        # 将图像分割
        cimages = crop_boxes_from_image(result)
        # 使用lprnet处理
        labels = run_LPRNet.Predict(lprnet, cimages, args)
        # 进行标记
        lbs = []
        for label in labels:
            lb = ""
            for i in label:
                lb += CHARS[i]
            print(lb)
            lbs.append(lb)
        #将结果存入结果数组
        if result.boxes.id is not None:
            for lb, id in zip(lbs, result.boxes.id):
                isSaved = False
                point = None
                # 检查是否已有id
                for num, ls, time in results_list:
                    if num == id:
                        isSaved = True
                        point = (num, ls)
                # 若存在，则加入其中
                if isSaved:
                    point[1].add(lb)
                # 若不存在，则新建项
                else:
                    results_list.append([id, {lb}, seconds_to_minutes_seconds(current_time)])
        fimg = draw_boxes(result, lbs, font)
        im0 = counter.start_counting(fimg, tracks)
        if tracks[0].boxes.id is not None:
            print(tracks[0].boxes.id.int().cpu())
        video_writer.write(fimg)
        frame_number += 1

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    result_list = []
    id = 0
    for num, lbs, time in results_list:
        result_list.append([id, get_most_frequent_string(lbs), time])
        id += 1
    print(result_list)
    print(results_list)
    return result_list, counter.in_counts

def seconds_to_minutes_seconds(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f'{minutes:02}:{remaining_seconds:02}'

def get_most_frequent_string(string_list):
    if not string_list:
        return None

    count = Counter(string_list)
    most_common_strings = count.most_common()
    max_count = most_common_strings[0][1]

    candidates = [s for s, cnt in most_common_strings if cnt == max_count]

    if len(candidates) == 1:
        return candidates[0]

    def similarity_score(s, others):
        return sum(Levenshtein.ratio(s, other) for other in others if other != s)

    return max(candidates, key=lambda s: similarity_score(s, string_list))

def Ptest(YOLOmodelPath, LPRNetModelPath, dataPath, savePath):
    test_datas = os.listdir(dataPath)
    total = len(test_datas)
    correct = 0
    for item in test_datas:
        lb = os.path.splitext(os.path.basename(item))[0]
        plb = mainProcess(YOLOmodelPath, LPRNetModelPath,dataPath + '\\' + item, savePath)
        if lb == plb:
            correct += 1
    print(total)
    print(correct)
    print(correct/total)

if __name__ == "__main__":
    # 用于图片、视频识别，若是图片则返回识别结果，若是视频则返回“True”
    # mainProcess('..\\runs\\detect\\train14\\weights\\best.pt', 'lprnet_best.pth', '', 'outputs')
    # 仅用于视频，返回车牌列表和计数结果
    countCar('..\\runs\\detect\\train14\\weights\\best.pt', 'lprnet_best.pth', '..\\3.mp4', '.\\')
    # 数据集测试
    # Ptest('E:\\Desktop\\Yolo\\runs\\detect\\train14\\weights\\best.pt', 'lprnet_best.pth', 'E:\Desktop\Yolo\ccpdDataSets\jiance', 'outputs')