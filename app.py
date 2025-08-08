import os
from flask import Flask, jsonify
from create_video import create_video

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(ok=True)

@app.route("/create-video", methods=["POST"])
def create_video_endpoint():
    create_video()
    return jsonify(status="success", video="output_video.mp4")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
