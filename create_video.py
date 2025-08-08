import os, re, random
from moviepy.editor import ImageClip, AudioFileClip, ColorClip, concatenate_videoclips

SCENES_FOLDER = "scenes"          # Hem sesler hem görseller burada
OUTPUT_FILE   = "output_video.mp4"
FPS = 24

def natural_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def find_matching_image(base_name):
    # Aynı isimli görsel var mı?
    for ext in (".jpg", ".jpeg", ".png"):
        p = os.path.join(SCENES_FOLDER, base_name + ext)
        if os.path.exists(p):
            return p
    # scene_1 yerine scene1, scene-1 gibi varyasyonları da dene
    alt = base_name.replace("_","").replace("-","")
    for f in os.listdir(SCENES_FOLDER):
        name, ext = os.path.splitext(f)
        if ext.lower() in (".jpg",".jpeg",".png"):
            n2 = name.replace("_","").replace("-","")
            if n2 == alt:
                return os.path.join(SCENES_FOLDER, f)
    return None

def create_video():
    # scenes içindeki mp3’leri sırala
    mp3s = [f for f in os.listdir(SCENES_FOLDER) if f.lower().endswith(".mp3")]
    if not mp3s:
        raise FileNotFoundError("scenes/ klasöründe mp3 bulunamadı.")
    mp3s.sort(key=natural_key)

    clips = []
    for mp3 in mp3s:
        base = os.path.splitext(mp3)[0]
        audio_path = os.path.join(SCENES_FOLDER, mp3)

        # Ses klibini yükle
        audio = AudioFileClip(audio_path)
        dur = max(0.1, audio.duration)

        # Görsel var mı?
        img_path = find_matching_image(base)
        if img_path and os.path.exists(img_path):
            clip = ImageClip(img_path).set_duration(dur)
        else:
            # Otomatik düz renk arka plan (1280x720)
            color = random.choice([(20,20,20), (30,10,60), (10,40,90), (50,20,20)])
            clip = ColorClip(size=(1280,720), color=color).set_duration(dur)

        clip = clip.set_audio(audio).set_fps(FPS)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(OUTPUT_FILE, fps=FPS, codec="libx264", audio_codec="aac")
    print(f"✅ Video hazır: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_video()
