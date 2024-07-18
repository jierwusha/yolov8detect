from ultralytics import YOLO
import cv2
def track_cam(src, name):
    model = YOLO(name)
    cap = cv2.VideoCapture(src)#src的值为0或1，0代表前置摄像头，1代表网络摄像头
    cv2.namedWindow("aminos", cv2.WINDOW_AUTOSIZE)

    if not cap.isOpened():
        print("打不开摄像头")
        exit()
    run = True
    while run:
        # 读取摄像头的一帧
        ret, frame = cap.read()
        image_det = cv2.resize(frame, (640, 640))
        result = model.predict(source=image_det, conf=0.6, save=False)
        # 显示帧
        cv2.imshow("摄像头", result[0].plot())
        # 按下 'q' 键退出
        if cv2.waitKey(1) == ord('q'):
            run = False
    # 释放摄像头并关闭所有窗口
    cap.release()
    cv2.destroyAllWindows()
    return
