import os
from moviepy.editor import *

os.makedirs("videos", exist_ok=True)

def create_video_for_scene(index):
    image_path = f"composed/scene{index}.jpg"
    audio_path = f"scenes/scene{index}.mp3"
    output_path = f"videos/scene{index}.mp4"

    if not os.path.exists(image_path) or not os.path.exists(audio_path):
        print(f"[❌] Eksik dosya: scene{index}")
        return

    audio = AudioFileClip(audio_path)
    image = ImageClip(image_path).set_duration(audio.duration)
    image = image.set_audio(audio)
    image = image.set_fps(24)

    image.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"[🎞️] Video oluşturuldu: {output_path}")

def create_all_videos(total_scenes=10):
    for i in range(1, total_scenes + 1):
        create_video_for_scene(i)

if __name__ == "__main__":
    create_all_videos()
