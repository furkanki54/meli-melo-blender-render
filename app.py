import os
import sys

# scenes çıktıları dursun
os.makedirs("scenes", exist_ok=True)

# Blender'ı headless çalıştır: scene.py içindeki bpy kodu burada koşar
exit_code = os.system("blender --background --python scene.py")
if exit_code != 0:
    print("❌ Blender çalıştırılamadı. Loglara bak.")
    sys.exit(1)
else:
    print("✅ Blender sahne scripti tamamlandı.")
