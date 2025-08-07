import os
import replicate
import requests
from scene_texts import scenes

# Replicate API anahtarın (senin anahtarın sabitlenmişti)
os.environ["REPLICATE_API_TOKEN"] 

def generate_image(prompt, index):
    output = replicate.run(
        "stability-ai/sdxl:latest",
        input={"prompt": prompt}
    )
    if output and isinstance(output, list):
        image_url = output[0]
        print(f"[🎨] Sahne {index} için görsel üretildi: {image_url}")

        # scenes klasörü varsa kaydet
        os.makedirs("scenes", exist_ok=True)
        img_path = f"scenes/scene{index}.jpg"
        response = requests.get(image_url)
        with open(img_path, "wb") as f:
            f.write(response.content)
        print(f"[✅] Kaydedildi: {img_path}")
    else:
        print(f"[❌] Sahne {index} için görsel alınamadı.")

def generate_all_images():
    for i, scene in enumerate(scenes, start=1):
        prompt = scene["text"]
        generate_image(prompt, i)

if __name__ == "__main__":
    generate_all_images()
