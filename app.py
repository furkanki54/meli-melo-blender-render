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
import os
from flask import Flask, request, jsonify
from create_video import create_video

app = Flask(__name__)

@app.get("/trigger")
def trigger_get():
    # Güvenlik için anahtar kontrolü
    key = request.args.get("key", "")
    if key != os.getenv("TRIGGER_KEY"):
        return jsonify(status="error", message="unauthorized"), 401
    
    create_video()
    return jsonify(status="success", via="GET")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
