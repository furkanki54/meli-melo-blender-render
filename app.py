import os, subprocess
from flask import Flask, send_from_directory, request, jsonify
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, vfx

app = Flask(__name__)
SCENES_DIR = "scenes"
OUTPUT_DIR = "output"
os.makedirs(SCENES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_blender(scene_py="scene.py"):
    cmd = ["xvfb-run","-a","blender","-b","--python",scene_py]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + "\n" + p.stderr

@app.get("/")
def root():
    return "OK: Meli-Melo render server"

@app.get("/render")
def render_get():
    code, logs = run_blender()
    return ("OK" if code==0 else "FAIL") + "\n\n" + logs[-2000:], (200 if code==0 else 500)

@app.get("/download/<path:fname>")
def download_file(fname):
    base = OUTPUT_DIR if not fname.startswith("scene") else SCENES_DIR
    return send_from_directory(base, fname, as_attachment=True)

# ---------- ZAMAN ÇİZELGESİ: N adet mp3 + görseller -> tek video ----------
def make_timeline(image_fallback: str, audio_prefix: str, count: int, fps: int, crossfade: float, kenburns: bool):
    clips = []
    for i in range(1, count + 1):
        aud = os.path.join(SCENES_DIR, f"{audio_prefix}{i}.mp3")
        if not os.path.exists(aud):
            print(f"[WARN] missing audio: {aud}")
            continue
        # sahne görseli varsa onu kullan, yoksa fallback
        img_name = f"scene{i}.jpg"
        img_path = os.path.join(SCENES_DIR, img_name)
        if not os.path.exists(img_path):
            img_path = os.path.join(SCENES_DIR, image_fallback)

        a = AudioFileClip(aud)
        img = ImageClip(img_path).set_duration(a.duration)

        if kenburns:
            # hafif zoom/pan: kısa kliplerde sabit kalıyor
            img = img.fx(vfx.resize, width=1280).fx(vfx.crop, x_center=640, y_center=360, width=1280, height=720)
            img = img.fx(vfx.fadein, min(0.3, a.duration/4)).fx(vfx.fadeout, min(0.3, a.duration/4))
            # minik ölçek animasyonu
            img = img.resize(lambda t: 1.02 - 0.04 * (t / max(a.duration, 0.01)))

        clip = img.set_audio(a)
        clips.append(clip)

    if not clips:
        return False, "No audio segments found."

    # crossfade ile birleştir
    if crossfade > 0:
        # ilkini al, sonra sırayla crossfade ekle
        out = clips[0]
        for nxt in clips[1:]:
            cf = min(crossfade, out.duration/3, nxt.duration/3)
            out = concatenate_videoclips([out, nxt.set_start(out.duration - cf)], method="compose", padding=-cf)
        final = out
    else:
        final = concatenate_videoclips(clips, method="compose")

    out_path = os.path.join(OUTPUT_DIR, "video.mp4")
    final.write_videofile(out_path, fps=fps, codec="libx264", audio_codec="aac", bitrate="2000k", threads=2)
    return True, out_path

@app.get("/make-timeline")
def make_timeline_get():
    # Örnek: /make-timeline?fallback=meli_melo.png.PNG&prefix=scene&count=10&fps=24&cf=0.25&kb=1
    fallback = request.args.get("fallback", "meli_melo.png.PNG")
    prefix   = request.args.get("prefix",   "scene")
    count    = int(request.args.get("count","1"))
    fps      = int(request.args.get("fps",  "24"))
    cf       = float(request.args.get("cf", "0.25"))  # crossfade sn
    kb       = request.args.get("kb", "1") != "0"     # kenburns on/off

    ok, res = make_timeline(fallback, prefix, count, fps, cf, kb)
    return (f"OK\n/download/video.mp4" if ok else f"FAIL: {res}"), (200 if ok else 400)

@app.post("/make-timeline")
def make_timeline_post():
    data = request.get_json(force=True, silent=True) or {}
    fallback = data.get("fallback", "meli_melo.png.PNG")
    prefix   = data.get("prefix",   "scene")
    count    = int(data.get("count", 1))
    fps      = int(data.get("fps", 24))
    cf       = float(data.get("cf", 0.25))
    kb       = bool(data.get("kb", True))

    ok, res = make_timeline(fallback, prefix, count, fps, cf, kb)
    return (jsonify({"ok": ok, "video": "video.mp4", "download_url": "/download/video.mp4"})
            if ok else (jsonify({"ok": False, "error": res}), 400))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
