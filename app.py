# app.py

from flask import Flask, request, jsonify
from generate_images import generate_image
from create_video import create_video

app = Flask(__name__)

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.json
    prompt = data.get("prompt")
    audio_file = data.get("audio")  # mp3 dosya yolu

    if not prompt or not audio_file:
        return jsonify({"error": "Eksik veri"}), 400

    try:
        image_path = generate_image(prompt)
        video_path = "output.mp4"
        create_video(image_path, audio_file, output_path=video_path)
        return jsonify({"video": video_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
