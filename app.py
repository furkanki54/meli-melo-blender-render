import os, subprocess
from flask import Flask, send_from_directory, request, jsonify
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

app = Flask(__name__)

SCENES_DIR = "scenes"   # hem görseller hem mp3'ler burada
OUTPUT_DIR = "output"
os.makedirs(SCENES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_blender(scene_py="scene.py"):
    # Headless (GUI yok) Blender
    cmd = ["xvfb-run","-a","blender","-b","--python",scene_py]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + "\n" + p.stderr

@app.get("/")
def root():
    return "OK: Meli-Melo render server"

# ---------- RENDER ----------
@app.post("/render")
def render_post():
    code, logs = run_blender()
    return jsonify({"ok": code==0, "logs": logs[-2000:]}), (200 if code==0 else 500)

@app.get("/render")
def render_get():
    code, logs = run_blender()
    return ("OK" if code==0 else "FAIL") + "\n\n" + logs[-2000:], (200 if code==0 else 500)

# ---------- İNDİR ----------
@app.get("/download/<path:fname>")
def download_file(fname):
    base = OUTPUT_DIR
    if fname.startswith("scene"):  # scene1.jpg gibi render çıktıları
        base = SCENES_DIR
    return send_from_directory(base, fname, as_attachment=True)

# ---------- TEK SES + TEK GÖRSEL ----------
def make_one(image, audio, fps):
    img_path = os.path.join(SCENES_DIR, image)
    aud_path = os.path.join(SCENES_DIR, audio)
    out_path = os.path.join(OUTPUT_DIR, "video.mp4")

    if not os.path.exists(img_path):
        return False, f"Image not found: {img_path}"
    if not os.path.exists(aud_path):
        return False, f"Audio not found: {aud_path}"

    a = AudioFileClip(aud_path)
    v = ImageClip(img_path).set_duration(a.duration).set_audio(a)
    v.write_videofile(out_path, fps=fps)
    return True, out_path

@app.post("/make-video")
def make_video_post():
    data = request.get_json(force=True, silent=True) or {}
    image = data.get("image","meli_melo.png.PNG")  # scenes/
    audio = data.get("audio","scene1.mp3")         # scenes/
    fps   = int(data.get("fps",24))
    ok, res = make_one(image, audio, fps)
    return (jsonify({"ok": ok, "video": "video.mp4", "download_url": "/download/video.mp4"})
            if ok else (jsonify({"ok": False, "error": res}), 400))

@app.get("/make-video")
def make_video_get():
    image = request.args.get("image", "meli_melo.png.PNG")
    audio = request.args.get("audio", "scene1.mp3")
    fps   = int(request.args.get("fps", "24"))
    ok, res = make_one(image, audio, fps)
    return (f"OK\n/download/video.mp4" if ok else f"FAIL: {res}"), (200 if ok else 400)

# ---------- ÇOKLU SES (scene1.mp3..sceneN.mp3) -> TEK VİDEO ----------
def make_batch(image, prefix, count, fps):
    img_path = os.path.join(SCENES_DIR, image)
    if not os.path.exists(img_path):
        return False, f"Image not found: {img_path}"

    clips = []
    for i in range(1, count+1):
        p = os.path.join(SCENES_DIR, f"{prefix}{i}.mp3")
        if not os.path.exists(p):
            print(f"[WARN] missing {p}")
            continue
        a = AudioFileClip(p)
        clips.append(ImageClip(img_path).set_duration(a.duration).set_audio(a))

    if not clips:
        return False, "No audio segments found."

    out_path = os.path.join(OUTPUT_DIR, "video.mp4")
    concatenate_videoclips(clips, method="compose").write_videofile(out_path, fps=fps)
    return True, out_path

@app.post("/make-video-batch")
def make_batch_post():
    data   = request.get_json(force=True, silent=True) or {}
    image  = data.get("image","meli_melo.png.PNG")
    prefix = data.get("prefix","scene")  # scene1.mp3, scene2.mp3 ...
    count  = int(data.get("count",1))
    fps    = int(data.get("fps",24))
    ok, res = make_batch(image, prefix, count, fps)
    return (jsonify({"ok": ok, "video": "video.mp4", "download_url": "/download/video.mp4"})
            if ok else (jsonify({"ok": False, "error": res}), 400))

@app.get("/make-video-batch")
def make_batch_get():
    image  = request.args.get("image","meli_melo.png.PNG")
    prefix = request.args.get("prefix","scene")
    count  = int(request.args.get("count","1"))
    fps    = int(request.args.get("fps","24"))
    ok, res = make_batch(image, prefix, count, fps)
    return (f"OK\n/download/video.mp4" if ok else f"FAIL: {res}"), (200 if ok else 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
