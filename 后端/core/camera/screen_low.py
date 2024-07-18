from ultralytics import YOLO
import numpy as np
import cv2
import torch
import threading

def capture(name):
    model = YOLO(name)
    device = torch.device("cuda:0")
    model.to(device)
    cap = cv2.VideoCapture(1)
    # 设置期望的捕获分辨率（例如 1920x1080）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cv2.namedWindow("aminos", cv2.WINDOW_AUTOSIZE)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取帧")
            break
        y1, y2, x1, x2 = 100, 900, 100, 900
        cropped_frame = frame[y1:y2, x1:x2]
        image_src = cv2.cvtColor(np.array(cropped_frame), cv2.COLOR_BGRA2BGR)
        size_x, size_y = image_src.shape[1], image_src.shape[0]
        image_det = cv2.resize(image_src, (640, 640))
        result = model.predict(source=image_det, conf=0.6, save=False)
        boxes = result[0].boxes.xywhn  # 获取边界框
        classes = result[0].boxes.cls  # 获取类名
        box_class_pairs = list(zip(boxes, classes))  # 边界框与类名自然连接
        draw_boxes(image_src, box_class_pairs, size_x, size_y)
        display_frame = cv2.resize(image_src, (630, 630))
        cv2.imshow("aminos",  display_frame)
        # 按下 'q' 键退出
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
def draw_boxes(image_src, box_class_pairs, size_x, size_y):
    clsdict = {
        0: {"color": (255, 255, 255), "text": ""},
        1: {"color": (255, 0, 0), "text": "ct_body"},
        2: {"color": (255, 0, 0), "text": "ct_head"},
        3: {"color": (0, 0, 255), "text": "t_body"},
        4: {"color": (0, 0, 255), "text": "t_head"}
    }
    for box, cls in box_class_pairs:
        cid = int(cls.item())
        cv2.rectangle(image_src,
                      (int((box[0] - box[2] / 2) * size_x), int((box[1] - box[3] / 2) * size_y)),
                      (int((box[0] + box[2] / 2) * size_x), int((box[1] + box[3] / 2) * size_y)),
                      color=clsdict[cid]["color"],
                      thickness=1)  # 画出边框
        cv2.putText(image_src,
                    text=clsdict[cid]["text"],
                    org=(int((box[0] - box[2] / 2) * size_x), int((box[1] - box[3] / 2) * size_y)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=clsdict[cid]["color"])  # 标注人物