import bpy
import math
import random
import os

print("=== Generating Enhanced Cinematic 3D Ruins Scene ===")

# Reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Render Settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

output_dir = "/Users/cheng-kuanglee/post-future-zoo/m1-world"
image_path = os.path.join(output_dir, "ruins_400y_scene.png")
blend_path = os.path.join(output_dir, "ruins_400y_scene.blend")
scene.render.filepath = image_path

# --- World & Volumetric Atmosphere ---
world = bpy.data.worlds.new("ApocalypticAtmosphere")
scene.world = world
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links
world_nodes.clear()

w_output = world_nodes.new('ShaderNodeOutputWorld')
w_bg = world_nodes.new('ShaderNodeBackground')
w_bg.inputs["Color"].default_value = (0.45, 0.38, 0.32, 1.0) # Dusty warm amber sky
w_bg.inputs["Strength"].default_value = 1.5
world_links.new(w_bg.outputs['Background'], w_output.inputs['Surface'])

# Volumetric Fog (Sunbeams & Atmospheric Depth)
w_vol = world_nodes.new('ShaderNodeVolumeScatter')
w_vol.inputs['Color'].default_value = (0.85, 0.82, 0.78, 1.0)
w_vol.inputs['Density'].default_value = 0.015
w_vol.inputs['Anisotropy'].default_value = 0.75 # Forward scattering for god rays

# --- Procedural Materials ---
def make_rust_mat():
    mat = bpy.data.materials.new("ProceduralRust")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Texture for Rust Patches
    tex_coord = nodes.new('ShaderNodeTexCoord')
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 12.0
    noise.inputs['Detail'].default_value = 6.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (0.42, 0.16, 0.06, 1.0) # Dark oxide rust
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = (0.75, 0.32, 0.12, 1.0) # Vivid orange iron rust
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    # Bump for rust pits
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.4
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = 0.8
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = 0.7
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def make_ground_mat():
    mat = bpy.data.materials.new("CrackedRubbleGround")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    out = nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 4.0
    noise.inputs['Detail'].default_value = 8.0
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.2
    ramp.color_ramp.elements[0].color = (0.16, 0.15, 0.14, 1.0) # Dark ash earth
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.45, 0.42, 0.38, 1.0) # Weathered concrete
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.6
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = 0.95
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

def make_simple_mat(name, color, roughness=0.5):
    mat = bpy.data.materials.new(name)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    out = nodes.get("Material Output") or nodes.new('ShaderNodeOutputMaterial')
    bsdf = nodes.get("Principled BSDF") or nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = color
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = roughness
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

mat_rust = make_rust_mat()
mat_ground = make_ground_mat()
mat_mineral = make_simple_mat("WhiteLimestone", (0.95, 0.94, 0.90, 1.0), roughness=0.3)
mat_charred = make_simple_mat("CharredFossilTree", (0.02, 0.02, 0.02, 1.0), roughness=0.98)

# --- Lighting ---
# Powerful warm low-angle sun
sun_data = bpy.data.lights.new("LowSun", type='SUN')
sun_data.color = (1.0, 0.78, 0.55) # Golden hour dust ray
sun_data.energy = 15.0
sun_data.angle = math.radians(2.0)
sun_obj = bpy.data.objects.new("LowSun", sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(35), math.radians(15), math.radians(-115))

# Sky rim fill light
rim_data = bpy.data.lights.new("CoolRim", type='SUN')
rim_data.color = (0.4, 0.6, 0.85)
rim_data.energy = 1.8
rim_obj = bpy.data.objects.new("CoolRim", rim_data)
scene.collection.objects.link(rim_obj)
rim_obj.rotation_euler = (math.radians(-45), math.radians(-30), math.radians(65))

# --- Camera ---
cam_data = bpy.data.cameras.new("HeroCamera")
cam_data.lens = 20 # Ultra-wide angle dramatic hero view
cam_obj = bpy.data.objects.new("HeroCamera", cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj
cam_obj.location = (-6.5, -16.0, 2.8)
cam_obj.rotation_euler = (math.radians(80), math.radians(0), math.radians(-22))

# --- Ground Terrain ---
bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
ground.data.materials.append(mat_ground)

# Scattered rubble & concrete slabs
random.seed(99)
for _ in range(40):
    rx = random.uniform(-30, 30)
    ry = random.uniform(-15, 45)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(rx, ry, random.uniform(0.2, 1.2)))
    b = bpy.context.active_object
    b.scale = (random.uniform(0.6, 4.0), random.uniform(0.6, 3.5), random.uniform(0.3, 1.2))
    b.rotation_euler = (random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), random.uniform(0, 3.14))
    b.data.materials.append(mat_ground)

# --- Skyscraper Steel Framework Generator ---
def create_complex_tower(bx, by, w, d, floors, floor_h=3.5, tilt_x=0.0, tilt_y=0.0):
    col_w = 0.28
    beam_w = 0.18
    corners = [(-w/2, -d/2), (w/2, -d/2), (w/2, d/2), (-w/2, d/2)]
    
    # Vertical Steel I-Beams (Columns)
    for cx, cy in corners:
        h = floors * floor_h
        bpy.ops.mesh.primitive_cube_add(size=1, location=(bx + cx, by + cy, h/2))
        col = bpy.context.active_object
        col.scale = (col_w, col_w, h)
        col.rotation_euler = (tilt_x, tilt_y, 0)
        col.data.materials.append(mat_rust)
    
    # Floors & Cross Trusses
    for f in range(1, floors + 1):
        z = f * floor_h
        for i in range(4):
            x1, y1 = corners[i]
            x2, y2 = corners[(i+1)%4]
            mx = (x1 + x2)/2 + bx
            my = (y1 + y2)/2 + by
            length = math.hypot(x2 - x1, y2 - y1)
            angle = math.atan2(y2 - y1, x2 - x1)
            
            # Horizontal girder
            bpy.ops.mesh.primitive_cube_add(size=1, location=(mx, my, z))
            beam = bpy.context.active_object
            beam.scale = (length, beam_w, beam_w*1.5)
            beam.rotation_euler = (tilt_x, tilt_y, angle)
            beam.data.materials.append(mat_rust)
            
            # White mineral leaching stalactites hanging from broken beams
            if f <= 5 and random.random() < 0.45:
                bpy.ops.mesh.primitive_cone_add(radius1=random.uniform(0.18, 0.35), radius2=0.01, depth=random.uniform(1.2, 4.0), location=(mx, my, z - 1.2))
                stal = bpy.context.active_object
                stal.rotation_euler = (math.radians(180), 0, 0)
                stal.data.materials.append(mat_mineral)
            
            # Diagonal X-bracing truss
            if f % 2 == 1 and f < floors:
                dz = floor_h
                d_len = math.hypot(length, dz)
                pitch = math.atan2(dz, length)
                bpy.ops.mesh.primitive_cube_add(size=1, location=(mx, my, z + dz/2))
                brace = bpy.context.active_object
                brace.scale = (d_len, beam_w*0.6, beam_w*0.6)
                brace.rotation_euler = (pitch + tilt_x, tilt_y, angle)
                brace.data.materials.append(mat_rust)

# 1. Main Foreground Looming Skyscraper (Massive, 14 floors, towering over camera)
create_complex_tower(bx=-1.0, by=1.0, w=10.0, d=10.0, floors=15, floor_h=3.6)

# 2. Midground Leaning Skyscraper (Tilted damaged skeleton, 10 floors)
create_complex_tower(bx=14.0, by=12.0, w=8.0, d=8.0, floors=11, floor_h=3.2, tilt_x=math.radians(-6), tilt_y=math.radians(8))

# 3. Distant Skyline Tower 1 (Left background, 18 floors)
create_complex_tower(bx=-22.0, by=38.0, w=12.0, d=12.0, floors=18, floor_h=3.4)

# 4. Distant Skyline Tower 2 (Right background narrow needle, 22 floors)
create_complex_tower(bx=25.0, by=48.0, w=6.0, d=6.0, floors=22, floor_h=3.0)

# --- Distant Petrified Carbonized Dead Forest ---
def plant_petrified_tree(x, y, h_scale=1.0):
    th = 8.0 * h_scale
    bpy.ops.mesh.primitive_cone_add(radius1=0.55*h_scale, radius2=0.12*h_scale, depth=th, location=(x, y, th/2))
    trunk = bpy.context.active_object
    trunk.rotation_euler = (random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15), random.uniform(0, 3.14))
    trunk.data.materials.append(mat_charred)
    
    # 3-4 Twisted jagged fossil branches
    for i in range(4):
        blen = random.uniform(2.5, 4.8) * h_scale
        bz = th * (0.55 + i*0.12)
        b_ang = random.uniform(0, math.pi*2)
        bx = x + math.cos(b_ang)*blen*0.4
        by = y + math.sin(b_ang)*blen*0.4
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12*h_scale, depth=blen, location=(bx, by, bz))
        b = bpy.context.active_object
        b.rotation_euler = (math.radians(random.uniform(40, 75)), math.radians(random.uniform(-25, 25)), b_ang)
        b.data.materials.append(mat_charred)

# Cluster of dead trees in the middle/far horizon
random.seed(555)
for _ in range(25):
    tx = random.uniform(-40, 45)
    ty = random.uniform(25, 65)
    plant_petrified_tree(tx, ty, h_scale=random.uniform(0.8, 1.8))

# Save project file
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"✓ Saved updated project: {blend_path}")

# Render
print("Rendering enhanced 1920x1080 scene with Cycles & Volumetrics...")
bpy.ops.render.render(write_still=True)
print(f"✓ Render complete: {image_path}")
