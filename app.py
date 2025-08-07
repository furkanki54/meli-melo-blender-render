from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route("/generate-demo", methods=["POST"])
def generate_demo():
    try:
        # 1. AI sahne üretimi
        subprocess.run(["python3", "generate_images.py"], check=True)
        
        # 2. Karakter bindirme
        subprocess.run(["python3", "compose_scene.py"], check=True)
        
        # 3. Video üretimi
        subprocess.run(["python3", "create_video.py"], check=True)

        return jsonify({"status": "success", "message": "Demo video üretimi tamamlandı."})
    
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Bir adım hata verdi: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
