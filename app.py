# app.py

from flask import Flask, jsonify
from create_video import create_video

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})

@app.route("/create-video", methods=["POST"])
def create_video_endpoint():
    try:
        create_video()
        return jsonify({"status": "success", "video": "output_video.mp4"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
