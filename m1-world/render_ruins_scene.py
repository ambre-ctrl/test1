import bpy
import math
import random
import os

print("=== Starting Procedural 3D Scene Generation in Blender ===")

# 1. Clear scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# 2. Render Settings (Cycles for photorealistic lighting & materials)
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
output_dir = "/Users/cheng-kuanglee/post-future-zoo/m1-world"
image_path = os.path.join(output_dir, "ruins_400y_scene.png")
blend_path = os.path.join(output_dir, "ruins_400y_scene.blend")
scene.render.filepath = image_path

# 3. Create Materials
def create_mat(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        if 'Metallic' in bsdf.inputs:
            bsdf.inputs['Metallic'].default_value = metallic
        if 'Roughness' in bsdf.inputs:
            bsdf.inputs['Roughness'].default_value = roughness
    return mat

mat_rust = create_mat("RustedSteel", (0.35, 0.14, 0.06, 1.0), metallic=0.85, roughness=0.65)
mat_concrete = create_mat("CrumblingConcrete", (0.42, 0.40, 0.38, 1.0), metallic=0.0, roughness=0.95)
mat_mineral = create_mat("WhiteLimestoneStalactite", (0.92, 0.92, 0.88, 1.0), metallic=0.0, roughness=0.35)
mat_charred = create_mat("CharredFossilTree", (0.03, 0.03, 0.03, 1.0), metallic=0.0, roughness=0.98)

# 4. Environment / World Lighting (Dusty Hazy Sky)
world = bpy.data.worlds.new("DustySky")
world.use_nodes = True
scene.world = world
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.22, 0.20, 0.18, 1.0)
    bg_node.inputs['Strength'].default_value = 0.8

# 5. Sun Lamp (Low dramatic angle warm sun rays)
sun_data = bpy.data.lights.new("WarmSun", type='SUN')
sun_data.color = (1.0, 0.82, 0.65)
sun_data.energy = 5.0
sun_data.angle = math.radians(1.5)
sun_obj = bpy.data.objects.new("WarmSun", sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(45), math.radians(25), math.radians(-50))

# 6. Camera (Low wide-angle looking up at towering steel skeletons)
cam_data = bpy.data.cameras.new("CinematicCam")
cam_data.lens = 22 # Wide angle
cam_obj = bpy.data.objects.new("CinematicCam", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (-12, -26, 3.5)
cam_obj.rotation_euler = (math.radians(82), math.radians(0), math.radians(-25))

# 7. Ground (Cracked Rubble Terrain)
bpy.ops.mesh.primitive_plane_add(size=120, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "RubbleGround"
ground.data.materials.append(mat_concrete)

# Add some scattered concrete rubble blocks
random.seed(42)
for i in range(25):
    rx = random.uniform(-25, 25)
    ry = random.uniform(-15, 30)
    rz = random.uniform(0.3, 1.8)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(rx, ry, rz/2))
    block = bpy.context.active_object
    block.scale = (random.uniform(0.8, 3.5), random.uniform(0.8, 3.0), rz)
    block.rotation_euler = (random.uniform(0, 0.4), random.uniform(0, 0.4), random.uniform(0, 3.14))
    block.data.materials.append(mat_concrete)

# 8. Function to Build a Skyscraper Steel Skeleton Tower
def build_steel_tower(base_x, base_y, width, depth, floors, floor_h=3.0, tilt_angle=0.0):
    col_radius = 0.22
    beam_radius = 0.14
    
    # 4 Main Vertical Steel Columns
    corners = [
        (-width/2, -depth/2),
        (width/2, -depth/2),
        (width/2, depth/2),
        (-width/2, depth/2)
    ]
    
    tower_objs = []
    
    # Columns
    for cx, cy in corners:
        h = floors * floor_h
        bpy.ops.mesh.primitive_cylinder_add(radius=col_radius, depth=h, location=(base_x + cx, base_y + cy, h/2))
        col = bpy.context.active_object
        col.data.materials.append(mat_rust)
        tower_objs.append(col)
    
    # Horizontal Perimeter Girders & Diagonal X-braces
    for f in range(1, floors + 1):
        z = f * floor_h
        # Horizontal perimeter beams
        for i in range(4):
            x1, y1 = corners[i]
            x2, y2 = corners[(i+1)%4]
            mx = (x1 + x2)/2 + base_x
            my = (y1 + y2)/2 + base_y
            length = math.hypot(x2 - x1, y2 - y1)
            angle = math.atan2(y2 - y1, x2 - x1)
            bpy.ops.mesh.primitive_cylinder_add(radius=beam_radius, depth=length, location=(mx, my, z))
            beam = bpy.context.active_object
            beam.rotation_euler = (0, math.radians(90), angle)
            beam.data.materials.append(mat_rust)
            tower_objs.append(beam)
            
            # Hanging white stalactites on some lower broken beams
            if f <= 4 and random.random() < 0.4:
                bpy.ops.mesh.primitive_cone_add(radius1=0.25, radius2=0.02, depth=random.uniform(1.2, 3.5), location=(mx, my, z - 1.0))
                stal = bpy.context.active_object
                stal.rotation_euler = (math.radians(180), 0, 0)
                stal.data.materials.append(mat_mineral)
                tower_objs.append(stal)
        
        # Diagonal X-Bracing on outer faces (every other floor)
        if f % 2 == 1 and f < floors:
            for i in [0, 2]: # front and back faces
                x1, y1 = corners[i]
                x2, y2 = corners[(i+1)%4]
                mx = (x1 + x2)/2 + base_x
                my = (y1 + y2)/2 + base_y
                dz = floor_h
                d_len = math.hypot(math.hypot(x2 - x1, y2 - y1), dz)
                # Brace 1
                bpy.ops.mesh.primitive_cylinder_add(radius=beam_radius*0.7, depth=d_len, location=(mx, my, z + dz/2))
                b1 = bpy.context.active_object
                pitch = math.atan2(dz, math.hypot(x2 - x1, y2 - y1))
                b1.rotation_euler = (pitch, math.radians(90), math.atan2(y2 - y1, x2 - x1))
                b1.data.materials.append(mat_rust)
                tower_objs.append(b1)

# Build Tower 1 (Main looming foreground tower, 12 floors)
build_steel_tower(base_x=-4, base_y=-2, width=8, depth=8, floors=12, floor_h=3.2)

# Build Tower 2 (Mid-ground tilted/damaged tower, 8 floors)
build_steel_tower(base_x=10, base_y=12, width=6, depth=7, floors=9, floor_h=3.0)

# Build Tower 3 (Distant high-rise frame, 15 floors)
build_steel_tower(base_x=-15, base_y=35, width=9, depth=9, floors=15, floor_h=3.4)

# 9. Build Distant Petrified Carbonized Dead Trees
def build_dead_tree(x, y, scale=1.0):
    # Main crooked trunk
    trunk_h = 7.0 * scale
    bpy.ops.mesh.primitive_cone_add(radius1=0.45*scale, radius2=0.15*scale, depth=trunk_h, location=(x, y, trunk_h/2))
    trunk = bpy.context.active_object
    trunk.rotation_euler = (random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15), random.uniform(0, 3.14))
    trunk.data.materials.append(mat_charred)
    
    # 2-3 Twisted Jagged Branches
    for b in range(3):
        bh = trunk_h * 0.7 + b * 0.8
        blen = random.uniform(2.5, 4.2) * scale
        b_angle = random.uniform(0, math.pi * 2)
        bx = x + math.cos(b_angle) * blen * 0.4
        by = y + math.sin(b_angle) * blen * 0.4
        bz = bh + blen * 0.3
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12*scale, depth=blen, location=(bx, by, bz))
        branch = bpy.context.active_object
        branch.rotation_euler = (math.radians(random.uniform(40, 70)), math.radians(random.uniform(-20, 20)), b_angle)
        branch.data.materials.append(mat_charred)

# Plant a line of distant petrified trees along the horizon
random.seed(101)
for i in range(16):
    tx = random.uniform(-35, 40)
    ty = random.uniform(30, 55) # In the distance
    build_dead_tree(tx, ty, scale=random.uniform(0.9, 1.6))

# 10. Save .blend file for user editing in Blender
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"✓ Blender project file saved: {blend_path}")

# 11. Render Scene to PNG
print("Rendering 1920x1080 3D scene with Cycles...")
bpy.ops.render.render(write_still=True)
print(f"✓ Render output finished: {image_path}")
