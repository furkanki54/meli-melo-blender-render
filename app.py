import os, subprocess, traceback
from flask import Flask, send_from_directory, request, jsonify
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

app = Flask(__name__)

SCENES_DIR = "scenes"   # hem görsel hem mp3 burada
OUTPUT_DIR = "output"
os.makedirs(SCENES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_blender(scene_py="scene.py"):
    # Headless Blender render (gerekirse tek kare üretmek için)
    cmd = ["xvfb-run", "-a", "blender", "-b", "--python", scene_py]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + "\n" + p.stderr

@app.get("/")
def health():
    return "OK: Meli-Melo render server"

@app.get("/render")
def render_get():
    code, logs = run_blender()
    return ("OK\n\n" + logs[-2000:] if code == 0 else "FAIL\n\n" + logs[-2000:]), (200 if code == 0 else 500)

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
    """
    scenes/
      - meli_melo.png.PNG (fallback)
      - scene1.mp3 ... sceneN.mp3
      - (opsiyonel) scene1.jpg ... sceneN.jpg
    """
    # fallback görseli doğrula
    fallback_path = os.path.join(SCENES_DIR, fallback_image)
    if not os.path.exists(fallback_path):
        return False, f"Fallback image not found: {fallback_path}"

    clips = []
    for i in range(1, count + 1):
        aud = os.path.join(SCENES_DIR, f"{prefix}{i}.mp3")
        if not os.path.exists(aud):
            # yoksa atla (log ver)
            print(f"[WARN] missing audio: {aud}")
            continue

        # sahneye özel görsel varsa onu kullan, yoksa fallback
        img = os.path.join(SCENES_DIR, f"scene{i}.jpg")
        if not os.path.exists(img):
            img = fallback_path

        aclip = AudioFileClip(aud)
        iclip = ImageClip(img).set_duration(aclip.duration).set_audio(aclip)
        # 1280x720 garanti
        iclip = iclip.resize(height=720).set_position("center")
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
        # count verilmemişse otomatik bul
        count    = request.args.get("count", None)
        count    = int(count) if count else auto_count(prefix)
        fps      = int(request.args.get("fps", "24"))

        ok, res = make_timeline(fallback, prefix, count, fps)
        return (f"OK\n/download/video.mp4" if ok else
