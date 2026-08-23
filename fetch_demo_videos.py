import os
import urllib.request

# Sample copyright-free traffic demo video for CI/testing
VIDEO_URL = "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/car-detection.mp4"
SAVE_DIR = "demo_videos"
SAVE_PATH = os.path.join(SAVE_DIR, "sample_traffic.mp4")

def fetch_demo_video():
    """Downloads a small sample video for testing and CI pipeline execution."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        print(f"Created directory: {SAVE_DIR}")

    print("Downloading sample traffic video for testing...")
    try:
        urllib.request.urlretrieve(VIDEO_URL, SAVE_PATH)
        print(f"Success! Sample video saved to: {SAVE_PATH}")
    except Exception as e:
        print(f"Error downloading sample video: {e}")

if __name__ == "__main__":
    fetch_demo_video()