import bpy
import os

# --- Temiz başlangıç ---
bpy.ops.wm.read_factory_settings(use_empty=True)

# Render motoru
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Kamera
bpy.ops.object.camera_add(location=(0, -8, 3), rotation=(1.1, 0.0, 0.0))
bpy.context.scene.camera = bpy.context.object

# Işık
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))

# --- World güvenli kurulum ---
if bpy.data.worlds:
    world = bpy.data.worlds[0]
else:
    world = bpy.data.worlds.new("World")

bpy.context.scene.world = world

if not world.use_nodes:
    world.use_nodes = True

bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[1].default_value = 1.0  # parlaklık

# Zemin
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))

# --- Malzemeler ---
def make_mat(name, rgba):
    m = bpy.data.materials.new(name=name)
    m.diffuse_color = rgba
    return m

MAT_HAIR   = make_mat("Hair",   (1.0, 0.9, 0.6, 1))      # sarışın
MAT_PINK   = make_mat("ShirtPink", (1.0, 0.4, 0.7, 1))   # Meli tişört
MAT_BLUE   = make_mat("ShirtBlue", (0.3, 0.5, 1.0, 1))   # Melo tişört
MAT_YELLOW = make_mat("PantsYellow", (1.0, 1.0, 0.2, 1)) # pantolon
MAT_SKIN   = make_mat("Skin",   (1.0, 0.8, 0.65, 1))     # ten
MAT_EYE_G  = make_mat("EyeGreen", (0.25, 0.85, 0.35, 1))
MAT_EYE_B  = make_mat("EyeBlue",  (0.3, 0.55, 1.0, 1))

def add_sphere(r, loc, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc)
    ob = bpy.context.object
    ob.data.materials.append(mat)
    return ob

def add_cyl(rad, depth, loc, rot, mat):
    bpy.ops.mesh.primitive_cylinder_add(radius=rad, depth=depth, location=loc, rotation=rot)
    ob = bpy.context.object
    ob.data.materials.append(mat)
    return ob

# --- Karakter kurucu ---
def build_kid(x=0, eye_mat=MAT_EYE_G, shirt_mat=MAT_PINK, name="Kid"):
    head = add_sphere(0.7, (x, 0, 2.5), MAT_SKIN); head.name=f"{name}_Head"
    hair = add_sphere(0.72, (x, 0, 2.65), MAT_HAIR); hair.name=f"{name}_Hair"
    eye_L = add_sphere(0.1, (x-0.2, 0.6, 2.6), eye_mat); eye_L.name=f"{name}_EyeL"
    eye_R = add_sphere(0.1, (x+0.2, 0.6, 2.6), eye_mat); eye_R.name=f"{name}_EyeR"
    body  = add_cyl(0.5, 1.2, (x, 0, 1.3), (0,0,0), shirt_mat); body.name=f"{name}_Body"
    arm_L = add_cyl(0.1, 0.8, (x-0.7, 0, 1.6), (0,0,1.57), shirt_mat); arm_L.name=f"{name}_ArmL"
    arm_R = add_cyl(0.1, 0.8, (x+0.7, 0, 1.6), (0,0,1.57), shirt_mat); arm_R.name=f"{name}_ArmR"
    leg_L = add_cyl(0.15, 0.8, (x-0.2, 0, 0.4), (0,0,0), MAT_YELLOW); leg_L.name=f"{name}_LegL"
    leg_R = add_cyl(0.15, 0.8, (x+0.2, 0, 0.4), (0,0,0), MAT_YELLOW); leg_R.name=f"{name}_LegR"

# Meli & Melo
build_kid(x=-1.6, eye_mat=MAT_EYE_G, shirt_mat=MAT_PINK, name="Meli")
build_kid(x= 1.6, eye_mat=MAT_EYE_B, shirt_mat=MAT_BLUE, name="Melo")

# Render ayarları
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.filepath = os.path.abspath("//scenes/scene1.jpg")
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.resolution_percentage = 100

# Render
bpy.ops.render.render(write_still=True)
print("✅ Render alındı -> scenes/scene1.jpg")
