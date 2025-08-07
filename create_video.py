# create_video.py

from moviepy.editor import *
import os

def create_video(image_path, audio_path, output_path="output.mp4"):
    audio = AudioFileClip(audio_path)
    duration = audio.duration

    image = ImageClip(image_path).set_duration(duration).set_audio(audio)
    image = image.set_fps(24)

    image.write_videofile(output_path, codec="libx264", audio_codec="aac")
