import bpy
import os

# Sahneyi temizle
bpy.ops.wm.read_factory_settings(use_empty=True)

# Kamera
bpy.ops.object.camera_add(location=(0, -4, 1.5))
bpy.context.scene.camera = bpy.context.object

# Işık
bpy.ops.object.light_add(type='SUN', location=(0, -2, 3))

# Zemin (gerekirse)
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))

# Görselin yolu
image_path = "/app/scenes/meli_melo.png"
if os.path.exists(image_path):
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 1.5))
    plane = bpy.context.object

    # Materyal oluştur
    mat = bpy.data.materials.new(name="CharacterMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Gerekli nodelar
    bsdf = nodes.get("Principled BSDF")
    tex_image = nodes.new("ShaderNodeTexImage")
    tex_image.image = bpy.data.images.load(image_path)

    # Bağlantılar
    links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])

    # Materyali objeye ata
    plane.data.materials.append(mat)
    print("✅ Karakter görseli sahneye yerleştirildi.")
else:
    print("❌ Görsel bulunamadı: meli_melo.png")

# Render ayarları
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.filepath = "/app/scenes/scene1.jpg"
bpy.context.scene.render.film_transparent = False

# Render et
bpy.ops.render.render(write_still=True)
print("✅ Render tamamlandı: scene1.jpg")
