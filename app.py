# app.py — FINAL
import os
from flask import Flask, request, jsonify
from create_video import create_video  # scene_*.jpg/png + scene_*.mp3 -> output_video.mp4

app = Flask(__name__)

# Sağlık kontrolü (Railway Health Checks için)
@app.get("/health")
def health():
    return jsonify(ok=True)

# POST ile tetikleme (istenirse)
@app.post("/create-video")
def create_video_post():
    try:
        create_video()
        return jsonify(status="success", via="POST", video="output_video.mp4")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

# GET ile tek-tık tetikleme (gizli anahtar gerekli)
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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
