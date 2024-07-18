from ultralytics import YOLO
import numpy as np
import cv2
import torch
import mss
def capture_and_detect(m_name):
    model = YOLO(m_name)
    device = torch.device("cuda:0")
    model.to(device)
    cv2.namedWindow("aminos", cv2.WINDOW_AUTOSIZE)
    # 初始化 Tkinter 主窗口
    monitor = {"top": 0, "left": 0, "width": 900, "height": 1000}
    isRun=True
    with mss.mss() as sct:
        while isRun:
            screenshot = sct.grab(monitor)
            image_src = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
            result = model.predict(source=image_src, conf=0.7, save=False)
            cv2.imshow("aminos", result[0].plot(line_width=1))
            if cv2.waitKey(1) == ord('q'):  # 按 q 退出
                isRun=False
    cv2.destroyWindow("aminos",)
if __name__ == "__main__":
    name = "7171551.pt"
    capture_and_detect(name)