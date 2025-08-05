import os

print("✅ Blender sistem başlatıldı.")

# Blender kurulu mu test et
status = os.system("blender --version")
if status != 0:
    print("❌ Blender çalışmıyor!")
else:
    print("✅ Blender başarıyla yüklü.")
