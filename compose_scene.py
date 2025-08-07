from PIL import Image

from scene_texts import scenes
import os

# Sabit karakter görselleri
CHARACTER_IMAGES = {
    "meli": "assets/meli.png",
    "melo": "assets/melo.png",
    "narrator": None  # Anlatıcı sahnelerinde karakter bindirme yok
}

# Nerede saklayacağız?
os.makedirs("composed", exist_ok=True)

def compose_scene(scene_index, character):
    base_img_path = f"scenes/scene{scene_index}.jpg"
    output_img_path = f"composed/scene{scene_index}.jpg"

    if not os.path.exists(base_img_path):
        print(f"[❌] Base sahne bulunamadı: {base_img_path}")
        return

    # Anlatıcı ise sadece sahne görselini kopyala
    if CHARACTER_IMAGES.get(character) is None:
        Image.open(base_img_path).save(output_img_path)
        print(f"[ℹ️] Narrator sahnesi: Karakter bindirilmedi (scene{scene_index})")
        return

    # Görselleri yükle
    base = Image.open(base_img_path).convert("RGBA")
    char = Image.open(CHARACTER_IMAGES[character]).convert("RGBA")

    # Karakteri yeniden boyutlandır (isteğe göre ayarlanabilir)
    char = char.resize((300, 300))

    # Pozisyon (alt köşeye yerleştir)
    position = (base.width - char.width - 30, base.height - char.height - 30)

    # Karakteri sahneye yapıştır
    base.paste(char, position, char)

    # Kaydet
    base.convert("RGB").save(output_img_path)
    print(f"[✅] Karakter sahneye bindirildi: {output_img_path}")

def compose_all():
    for i, scene in enumerate(scenes, start=1):
        character = scene["character"]
        compose_scene(i, character)

if __name__ == "__main__":
    compose_all()
