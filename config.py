import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

YOLO_MODEL = "yolov8n.pt"
VEHICLE_CLASS_IDS = {2, 3, 5, 7}

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
