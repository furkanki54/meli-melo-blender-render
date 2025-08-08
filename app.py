import os
import sys

# scenes klasörünü oluştur
os.makedirs("scenes", exist_ok=True)

# Headless (GUI’siz) Blender çalıştırma
exit_code = os.system("blender --background --python scene.py")
if exit_code != 0:
    print("❌ Blender çalıştırılamadı. Loglara bak.")
    sys.exit(1)
else:
    print("✅ Blender sahne scripti tamamlandı.")
