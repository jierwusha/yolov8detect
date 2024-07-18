from ultralytics import YOLO
from PIL import Image
import cv2


def plot_bboxes(image, boxes, names, colors, line_thickness=None):
    tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # 线条/字体粗细
    detected_classes = []  # 初始化识别结果的列表

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # 提取边界框坐标并转换为整数
        cls_id = int(box.cls[0])  # 提取类别ID
        conf = box.conf[0]  # 提取置信度分数

        if cls_id >= len(names):
            print(f"无效的类别ID {cls_id}，超出了名称列表的范围")
            continue

        color = colors[cls_id]
        c1, c2 = (x1, y1), (x2, y2)
        cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        tf = max(tl - 1, 1)  # 字体粗细
        label = f'{names[cls_id]} {conf:.2f}'
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3

        # 添加文本背景矩形
        text_bg_color = (0, 0, 0)  # 黑色背景
        cv2.rectangle(image, c1, c2, text_bg_color, -1, cv2.LINE_AA)  # 填充
        cv2.putText(image, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

        # 收集识别结果，附带边界框左上角的x坐标
        detected_classes.append((x1, names[cls_id]))

    # 根据x坐标对识别结果进行排序，输出预测结果
    detected_classes.sort(key=lambda x: x[0])
    detected_classes_str = ''.join([cls[1] for cls in detected_classes])

    return image, detected_classes_str


def video_process(conf, model_path, video_path, save_path):
    # 加载模型
    model = YOLO(model_path)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频的帧宽度、高度和帧率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 设置输出视频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 执行推理
        results = model(frame, conf)

        # 保存结果帧
        r = results[0]
        boxes = r.boxes
        names = r.names
        # 生成颜色列表，长度与类别数量一致
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] * (len(names) // 3 + 1)
        colors = colors[:len(names)]
        im_array = frame.copy()
        im_array, detected_classes_str = plot_bboxes(im_array, boxes, names, colors)

        out.write(im_array)

    cap.release()
    out.release()
    cv2.destroyAllWindows()