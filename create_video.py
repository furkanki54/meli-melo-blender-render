import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

SCENES_FOLDER = "scenes"       # Görsellerin olduğu klasör
VOICES_FOLDER = "scenes"       # Seslerin olduğu klasör
OUTPUT_FILE = "output_video.mp4"

def natural_sort_key(s):
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def create_video():
    try:
        image_files = sorted(
            [f for f in os.listdir(SCENES_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))],
            key=natural_sort_key
        )
        audio_files = sorted(
            [f for f in os.listdir(VOICES_FOLDER) if f.lower().endswith(".mp3")],
            key=natural_sort_key
        )

        if not image_files or not audio_files:
            raise FileNotFoundError("Görsel veya ses dosyaları bulunamadı!")

        if len(image_files) != len(audio_files):
            print(f"⚠️ Uyarı: Görsel ({len(image_files)}) ve ses ({len(audio_files)}) sayıları eşit değil. İlk ortak sayı kadar eşleştirilecek.")

        clips = []
        for img, aud in zip(image_files, audio_files):
            scene_name_img = os.path.splitext(img)[0]
            scene_name_aud = os.path.splitext(aud)[0]

            if scene_name_img != scene_name_aud:
                print(f"⚠️ UYARI: {img} ve {aud} isimleri uyuşmuyor, yine de eşleştiriliyor.")

            img_path = os.path.join(SCENES_FOLDER, img)
            aud_path = os.path.join(VOICES_FOLDER, aud)

            audio_clip = AudioFileClip(aud_path)
            img_clip = ImageClip(img_path).set_duration(audio_clip.duration)
            img_clip = img_clip.set_audio(audio_clip)

            clips.append(img_clip)

        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(OUTPUT_FILE, fps=24)

        print(f"✅ Video oluşturuldu: {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    create_video()
