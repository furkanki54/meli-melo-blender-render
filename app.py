import os, subprocess, traceback
from flask import Flask, send_from_directory, request, jsonify

# --- Pillow 10 uyumluluk yamasi: Image.ANTIALIAS kaldırıldı, LANCZOS'a eşitle ---
try:
    from PIL import Image as _PILImage
    if not hasattr(_PILImage, "ANTIALIAS"):
        # Pillow 10+: Resampling.LANCZOS mevcut
        try:
            _PILImage.ANTIALIAS = _PILImage.Resampling.LANCZOS  # type: ignore
        except Exception:
            # Bazı build'lerde LANCZOS üst düzeyde de olabilir
            _PILImage.ANTIALIAS = getattr(_PILImage, "LANCZOS", 1)  # 1 = default
except Exception:
    pass
# -------------------------------------------------------------------------------

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

app = Flask(__name__)

SCENES_DIR = "scenes"   # hem görsel hem mp3 burada
OUTPUT_DIR = "output"
os.makedirs(SCENES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_blender(scene_py="scene.py"):
    cmd = ["xvfb-run", "-a", "blender", "-b", "--python", scene_py]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + "\n" + p.stderr

@app.get("/")
def health():
    return "OK: Meli-Melo render server"

@app.get("/render")
def render_get():
    code, logs = run_blender()
    text = ("OK\n\n" if code == 0 else "FAIL\n\n") + logs[-2000:]
    status = 200 if code == 0 else 500
    return text, status

@app.get("/download/<path:fname>")
def download_file(fname):
    base = OUTPUT_DIR if not fname.startswith("scene") else SCENES_DIR
    return send_from_directory(base, fname, as_attachment=True)

def auto_count(prefix: str) -> int:
    i = 1
    while os.path.exists(os.path.join(SCENES_DIR, f"{prefix}{i}.mp3")):
        i += 1
    return i - 1

def make_timeline(fallback_image: str, prefix: str, count: int, fps: int):
    fallback_path = os.path.join(SCENES_DIR, fallback_image)
    if not os.path.exists(fallback_path):
        return False, f"Fallback image not found: {fallback_path}"

    clips = []
    for i in range(1, count + 1):
        aud = os.path.join(SCENES_DIR, f"{prefix}{i}.mp3")
        if not os.path.exists(aud):
            print(f"[WARN] missing audio: {aud}")
            continue

        img = os.path.join(SCENES_DIR, f"scene{i}.jpg")
        if not os.path.exists(img):
            img = fallback_path

        aclip = AudioFileClip(aud)
        iclip = ImageClip(img).set_duration(aclip.duration).set_audio(aclip)
        iclip = iclip.resize(height=720).set_position("center")  # 1280x720 garanti
        clips.append(iclip)

    if not clips:
        return False, "No audio segments found."

    final = concatenate_videoclips(clips, method="compose")
    out_path = os.path.join(OUTPUT_DIR, "video.mp4")
    final.write_videofile(out_path, fps=fps, codec="libx264", audio_codec="aac", bitrate="2000k", threads=2)
    return True, out_path

@app.get("/make-timeline")
def make_timeline_get():
    try:
        fallback = request.args.get("fallback", "meli_melo.png.PNG")
        prefix   = request.args.get("prefix",   "scene")
        count_q  = request.args.get("count", None)
        count    = int(count_q) if count_q else auto_count(prefix)
        fps      = int(request.args.get("fps",  "24"))

        ok, res = make_timeline(fallback, prefix, count, fps)
        if ok:
            return "OK\n/download/video.mp4", 200
        else:
            return f"FAIL: {res}", 400
    except Exception as e:
        return f"FAIL: {e}\n\n{traceback.format_exc()}", 500

@app.post("/make-timeline")
def make_timeline_post():
    try:
        data = request.get_json(force=True, silent=True) or {}
        fallback = data.get("fallback", "meli_melo.png.PNG")
        prefix   = data.get("prefix",   "scene")
        count    = int(data.get("count", 0)) or auto_count(prefix)
        fps      = int(data.get("fps", 24))

        ok, res = make_timeline(fallback, prefix, count, fps)
        if ok:
            return jsonify({"ok": True, "video": "video.mp4", "download_url": "/download/video.mp4"})
        else:
            return jsonify({"ok": False, "error": res}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
