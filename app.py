from flask import Flask, render_template, Response, request, redirect
import os
import cv2

from modules.detector import VehicleDetector
from modules.video_stream import VideoStream
from modules.signal_controller import SignalController

app = Flask(__name__)

detector = VehicleDetector()
stream = VideoStream(0)
controller = SignalController()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate():
    global stream
    while True:
        frame = stream.read()

        if frame is None:
            continue

        frame, count = detector.detect(frame)
        green_time = controller.get_green_time(count)

        cv2.putText(frame, f"Vehicles: {count}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, f"Green Time: {green_time}s", (10,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['POST'])
def upload():
    global stream

    file = request.files['video']
    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    stream = VideoStream(filepath)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
