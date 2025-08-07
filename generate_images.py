# generate_images.py

import requests
import os

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

def generate_image(prompt, output_path="scene.png"):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "db21e45c...",  # model versiyonu (kullanacağımız sabit prompt modeline göre ayarlanacak)
        "input": {
            "prompt": prompt,
            "width": 768,
            "height": 512
        }
    }

    response = requests.post(url, headers=headers, json=data)
    prediction = response.json()
    image_url = prediction['urls']['get']
    
    # Bekleyip sonucu al
    import time
    for _ in range(10):
        r = requests.get(image_url, headers=headers)
        prediction = r.json()
        if prediction['status'] == 'succeeded':
            image = prediction['output'][0]
            img_data = requests.get(image).content
            with open(output_path, 'wb') as f:
                f.write(img_data)
            return output_path
        time.sleep(1)

    raise Exception("Görsel üretimi başarısız.")
