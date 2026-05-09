import cv2
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        results = self.model(frame)[0]
        count = 0

        if results.boxes is not None:
            for box in results.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
                count += 1

        return frame, count
