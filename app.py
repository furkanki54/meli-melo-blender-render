import os
import sys

os.makedirs("scenes", exist_ok=True)

# Xvfb ile headless Blender
cmd = "xvfb-run -a blender -b --python scene.py"
print("→ Çalıştırılıyor:", cmd)
exit_code = os.system(cmd)

if exit_code != 0:
    print("❌ Blender çalıştırılamadı. Loglara bak.")
    sys.exit(1)
else:
    print("✅ Blender sahne scripti tamamlandı.")
