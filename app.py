from flask import Flask, render_template, Response, request, redirect, jsonify
from werkzeug.utils import secure_filename
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
    return render_template('index.html', uploaded_files=os.listdir(UPLOAD_FOLDER))

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


@app.route('/uploads')
def uploads():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route('/select_upload', methods=['POST'])
def select_upload():
    global stream
    fname = secure_filename(request.form.get('filename', ''))
    filepath = os.path.join(UPLOAD_FOLDER, fname)
    if not os.path.isfile(filepath):
        return jsonify({'error': 'not found'}), 404
    stream = VideoStream(filepath)
    return jsonify({'status': 'ok'}), 200

@app.route('/delete_upload', methods=['POST'])
def delete_upload():
    fname = secure_filename(request.form.get('filename', ''))
    filepath = os.path.join(UPLOAD_FOLDER, fname)
    if not os.path.isfile(filepath):
        return jsonify({'error': 'not found'}), 404
    os.remove(filepath)
    return jsonify({'status': 'deleted'}), 200

if __name__ == "__main__":
    app.run(debug=True)
