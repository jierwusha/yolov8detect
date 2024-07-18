import argparse
import os
import cv2
import numpy as np
from ultralytics import YOLO, solutions
import run_LPRNet
from model.LPRNet import build_lprnet
from data.load_data import CHARS, CHARS_DICT, LPRDataLoader
import torch
from image_correction import image_correction
from PIL import Image, ImageDraw, ImageFont


def mainProcess(YOLOmodelPath, LPRNetModelPath, dataPath, savePath):
    #初始化
    #加载字体
    font = ImageFont.truetype('SourceHanSansCN-Heavy.otf', 20)
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
    cap = cv2.VideoCapture(dataPath)
    isVideo = cap.isOpened()
    if isVideo:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video = cv2.VideoWriter(savePath, fourcc, fps, (width, height))

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
        # 重新将图片合成为视频
        if isVideo:
            video.write(fimg)
        else:
            cv2.imwrite(savePath, fimg)


def crop_boxes_from_image(result):
    image = result.orig_img
    boxes = result.boxes
    cropped_images = []
    for xyxy in boxes.xyxy:
        x1, y1, x2, y2 = xyxy
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cropped_image = image[y1:y2, x1:x2]
        cropped_image = image_correction(cropped_image)
        #cv2.imshow("result", cropped_image)
        #cv2.waitKey(1)
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


def countCar():
    model = YOLO("..\\runs\\detect\\train14\\weights\\car.pt")
    cap = cv2.VideoCapture("E:\\Desktop\\Yolo\\Licence-Recognition\\车牌识别视频素材.flv.mp4")
    assert cap.isOpened(), "Error reading video file"
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Define line points
    line_points = [(20, 400), (1080, 400)]

    # Video writer
    video_writer = cv2.VideoWriter("object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    # Init Object Counter
    counter = solutions.ObjectCounter(
        view_img=True,
        reg_pts=line_points,
        classes_names=model.names,
        draw_tracks=True,
        line_thickness=2,
    )

    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        tracks = model.track(im0, persist=True, show=False)

        im0 = counter.start_counting(im0, tracks)
        video_writer.write(im0)

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    mainProcess('..\\..\\runs\\detect\\train14\\weights\\car.pt', 'lprnet_best.pth',
                'E:\\Desktop\\Yolo\\Licence-Recognition\\车牌识别视频素材.flv.mp4', 'output.mp4')
