import os
import cv2
from ultralytics import YOLO


def seconds_to_minutes_seconds(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f'{minutes:02}:{remaining_seconds:02}'


def plot_bboxes(image, boxes, names, line_thickness=None):
    tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
    detected_classes = []

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        conf = box.conf[0]

        color = (255, 0, 0)
        c1, c2 = (x1, y1), (x2, y2)
        cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        tf = max(tl - 1, 1)
        label = f'{names[cls_id]} {conf:.2f}'
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

        text_bg_color = (0, 0, 0)
        cv2.rectangle(image, c1, c2, text_bg_color, -1, cv2.LINE_AA)
        cv2.putText(image, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

        detected_classes.append((x1, names[cls_id]))

    detected_classes.sort(key=lambda x: x[0])
    detected_classes_str = ''.join([cls[1] for cls in detected_classes])

    return image, detected_classes_str


def video_process(conf, model_path, video_path, save_path, max_attempts=3):
    model = YOLO(model_path)
    last_detected_classes_str = ''
    detected_classes_str_list = []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'VP90')
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_number += 1
        time_in_seconds = frame_number / fps

        attempts = 0
        detected_classes_str = ''

        # 尝试多次检测直到结果符合条件
        while attempts < max_attempts and len(detected_classes_str) != 5:
            results = model(frame, conf=conf)

            for r in results:
                boxes = r.boxes
                names = r.names
                im_array = frame.copy()

                im_array, detected_classes_str = plot_bboxes(im_array, boxes, names)

            attempts += 1

        if len(detected_classes_str) == 5 and detected_classes_str != last_detected_classes_str:
            detected_classes_str_list.append(
                (len(detected_classes_str_list) + 1, detected_classes_str, seconds_to_minutes_seconds(time_in_seconds)))
            last_detected_classes_str = detected_classes_str

        out.write(im_array)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return detected_classes_str_list

