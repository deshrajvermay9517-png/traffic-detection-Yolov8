import cv2

class VideoStream:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            print("❌ Cannot open video")

    def read(self):
        if self.cap is None:
            return None

        ret, frame = self.cap.read()

        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return None

        return frame
