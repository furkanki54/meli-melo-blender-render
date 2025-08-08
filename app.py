import bpy

# Sahneyi temizle
bpy.ops.wm.read_factory_settings(use_empty=True)

# Kamera ekle
bpy.ops.object.camera_add(location=(0, -8, 3))
bpy.context.scene.camera = bpy.context.object

# Işık ekle
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))

# Zemin ekle
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))

# 🎀 MELI (yeşil gözlü, pembe tişört, sarı pantolon, sarışın)

# Kafa
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=(-1.5, 0, 2.5))
meli_head = bpy.context.object

# Saç (sarışın)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.72, location=(-1.5, 0, 2.65))
meli_hair = bpy.context.object
hair_mat = bpy.data.materials.new(name="HairMaterial")
hair_mat.diffuse_color = (1.0, 0.9, 0.6, 1)
meli_hair.data.materials.append(hair_mat)

# Gözler
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-1.7, 0.6, 2.6))
meli_eye_left = bpy.context.object
eye_green = bpy.data.materials.new(name="GreenEyes")
eye_green.diffuse_color = (0.3, 1.0, 0.3, 1)
meli_eye_left.data.materials.append(eye_green)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(-1.3, 0.6, 2.6))
meli_eye_right = bpy.context.object
meli_eye_right.data.materials.append(eye_green)

# Gövde (pembe tişört)
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1.2, location=(-1.5, 0, 1.3))
meli_body = bpy.context.object
shirt_pink = bpy.data.materials.new(name="PinkShirt")
shirt_pink.diffuse_color = (1.0, 0.4, 0.7, 1)
meli_body.data.materials.append(shirt_pink)

# Bacaklar (sarı pantolon)
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(-1.65, 0, 0.4))
meli_leg_left = bpy.context.object
pants_yellow = bpy.data.materials.new(name="YellowPants")
pants_yellow.diffuse_color = (1.0, 1.0, 0.2, 1)
meli_leg_left.data.materials.append(pants_yellow)

bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(-1.35, 0, 0.4))
meli_leg_right = bpy.context.object
meli_leg_right.data.materials.append(pants_yellow)

# 🧢 MELO (mavi gözlü, mavi tişört, sarı pantolon, sarışın)

# Kafa
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(1.5, 0, 2.7))
melo_head = bpy.context.object

# Saç (sarışın)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.82, location=(1.5, 0, 2.85))
melo_hair = bpy.context.object
melo_hair.data.materials.append(hair_mat)

# Gözler
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(1.3, 0.7, 2.8))
eye_blue = bpy.data.materials.new(name="BlueEyes")
eye_blue.diffuse_color = (0.3, 0.5, 1.0, 1)
melo_eye_left = bpy.context.object
melo_eye_left.data.materials.append(eye_blue)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(1.7, 0.7, 2.8))
melo_eye_right = bpy.context.object
melo_eye_right.data.materials.append(eye_blue)

# Gövde (mavi tişört)
bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=1.3, location=(1.5, 0, 1.4))
melo_body = bpy.context.object
shirt_blue = bpy.data.materials.new(name="BlueShirt")
shirt_blue.diffuse_color = (0.3, 0.5, 1.0, 1)
melo_body.data.materials.append(shirt_blue)

# Bacaklar (sarı pantolon)
bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.9, location=(1.35, 0, 0.45))
melo_leg_left = bpy.context.object
melo_leg_left.data.materials.append(pants_yellow)

bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.9, location=(1.65, 0, 0.45))
melo_leg_right = bpy.context.object
melo_leg_right.data.materials.append(pants_yellow)

# Render ayarları
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.filepath = "/app/scenes/scene1.jpg"

# Render
bpy.ops.render.render(write_still=True)
print("✅ Meli & Melo karakterleri oluşturuldu ve render tamam.")
