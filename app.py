# app.py — trigger + health + download
import os
from flask import Flask, request, jsonify, send_file
from create_video import create_video  # scene_*.jpg/png + scene_*.mp3 -> output_video.mp4

app = Flask(__name__)

# Healthcheck
@app.get("/health")
def health():
    return jsonify(ok=True)

# POST ile tetikleme (opsiyonel)
@app.post("/create-video")
def create_video_post():
    try:
        create_video()
        return jsonify(status="success", via="POST", video="output_video.mp4")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

# GET ile tetikleme (secret key)
@app.get("/trigger")
def trigger_get():
    key = request.args.get("key", "")
    secret = os.getenv("TRIGGER_KEY")
    if not secret:
        return jsonify(status="error", message="TRIGGER_KEY is not set"), 500
    if key != secret:
        return jsonify(status="error", message="unauthorized"), 401

    try:
        create_video()
        return jsonify(status="success", via="GET", video="output_video.mp4")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

# Üretilen videoyu indir
@app.get("/download")
def download_video():
    path = "output_video.mp4"
    if not os.path.exists(path):
        return jsonify(status="error", message="Video not found"), 404
    # dosyayı indirme olarak gönder
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
