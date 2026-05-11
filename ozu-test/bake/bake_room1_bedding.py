"""
Bake PBR maps for the room-1 bedding: cotton sheet, white sleeping pillow,
and grey velour throw cushion.

Why this exists: the runtime in ozu-test.html ships a high-resolution
sheen-material approximation, but the wrinkles and plush dimples are
procedural noise. To get photo-grade close-up detail (the photos in
ozu-test/interior-images/room-1/corner-ac-{entrance,window}/ show real
cloth folds + slubs + sleeper-creases), we bake albedo + normal + roughness
+ AO offline from a Blender cloth sim + sculpted plush meshes.

Run on the A6000 (CUDA device 1):

    CUDA_VISIBLE_DEVICES=1 \
        ~/blender/blender-5.1.1-linux-x64/blender \
        --background \
        --python ozu-test/bake/bake_room1_bedding.py

Outputs (1024 x 1024 PNGs):

    ozu-test/room-1-textures/bedding/sheet/{sheet_albedo,sheet_normal,
                                            sheet_roughness,sheet_ao}.png
    ozu-test/room-1-textures/bedding/white_pillow/{white_pillow_*}.png
    ozu-test/room-1-textures/bedding/grey_cushion/{grey_cushion_*}.png

Total bake budget on A6000 with OptiX: ~5-8 min for all three at 1024px.

Dimensions and positions MUST stay in sync with ozu-test.html's bedding
block (around line 4063+). If you change pillow size, change both.
"""

import bpy
import os
import math
import sys
from mathutils import Vector
from random import seed, uniform

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_BASE   = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'room-1-textures', 'bedding')
)

# Bake settings
TEX_RES        = 1024
CYCLES_SAMPLES = 256
NORMAL_SAMPLES = 64
AO_DISTANCE    = 0.10
MARGIN         = 8

# Mattress dimensions (must match ozu-test.html line ~3814)
MAT_X = (0.7, 2.67)
MAT_Y = (0.1, 0.5)
MAT_Z = (1.7, 2.67)
MAT_TOP = MAT_Y[1]


# ---------------------------------------------------------------------------
# Scene setup
# ---------------------------------------------------------------------------

def reset():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for db in (bpy.data.meshes, bpy.data.materials, bpy.data.images,
               bpy.data.textures, bpy.data.node_groups, bpy.data.armatures,
               bpy.data.lights):
        for it in list(db):
            db.remove(it)


def configure_cycles_optix():
    """Cycles + OptiX on whatever CUDA_VISIBLE_DEVICES exposes (A6000 = 1)."""
    bpy.context.scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for d in prefs.devices:
        d.use = (d.type == 'OPTIX')
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = CYCLES_SAMPLES
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.cycles.use_adaptive_sampling = True
    bpy.context.scene.cycles.adaptive_threshold = 0.01
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_depth = '8'


def add_sun():
    """A directional sun aimed at the bedding from the window direction."""
    sun_data = bpy.data.lights.new('sun', 'SUN')
    sun_data.energy = 3.0
    sun_data.angle = math.radians(2.5)
    sun = bpy.data.objects.new('sun', sun_data)
    bpy.context.collection.objects.link(sun)
    sun.location = (5.0, 4.0, 1.5)
    sun.rotation_euler = (math.radians(50), 0, math.radians(20))


def add_world_environment():
    """Neutral white environment so AO bakes are not biased by colour."""
    world = bpy.data.worlds.new('world') if not bpy.data.worlds else bpy.data.worlds[0]
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (1, 1, 1, 1)
    bg.inputs['Strength'].default_value = 0.3
    bpy.context.scene.world = world


# ---------------------------------------------------------------------------
# Material factory
# ---------------------------------------------------------------------------

def make_image(name, color_space='Non-Color'):
    """Make (or replace) an Image datablock targeted by the bake."""
    if name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[name])
    img = bpy.data.images.new(name, width=TEX_RES, height=TEX_RES, alpha=False)
    img.colorspace_settings.name = color_space
    return img


def make_principled_material(name, base_color, roughness, sheen, sheen_tint):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Roughness'].default_value = roughness
    if 'Sheen Weight' in bsdf.inputs:        # Blender 4.x
        bsdf.inputs['Sheen Weight'].default_value = sheen
        bsdf.inputs['Sheen Tint'].default_value = (*sheen_tint, 1.0)
        bsdf.inputs['Sheen Roughness'].default_value = 0.3
    elif 'Sheen' in bsdf.inputs:             # Blender 3.x fallback
        bsdf.inputs['Sheen'].default_value = sheen
        bsdf.inputs['Sheen Tint'].default_value = sheen_tint[0]
    # Add an Image Texture node and select it; the bake target.
    img_node = nt.nodes.new('ShaderNodeTexImage')
    img_node.location = (-300, -300)
    img_node.name = '_bake_target'
    img_node.select = True
    nt.nodes.active = img_node
    return mat, img_node


# ---------------------------------------------------------------------------
# Geometry construction
# ---------------------------------------------------------------------------

def make_mattress():
    """Mattress AABB used as the cloth-collider for the sheet."""
    cx = (MAT_X[0] + MAT_X[1]) / 2
    cy = (MAT_Y[0] + MAT_Y[1]) / 2
    cz = (MAT_Z[0] + MAT_Z[1]) / 2
    sx = MAT_X[1] - MAT_X[0]
    sy = MAT_Y[1] - MAT_Y[0]
    sz = MAT_Z[1] - MAT_Z[0]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cz, cy))
    obj = bpy.context.object
    obj.name = 'mattress'
    obj.scale = (sx, sz, sy)              # Blender's Y is depth here (treats z↔z)
    bpy.ops.object.transform_apply(scale=True)
    # Add collision so the cloth lands on it.
    obj.modifiers.new('Collision', 'COLLISION')
    obj.hide_render = True
    return obj


def make_sheet_cloth():
    """A high-resolution plane dropped onto the mattress and cloth-simulated."""
    sheetW = (MAT_X[1] - MAT_X[0]) + 0.20    # extra slack so it drapes properly
    sheetD = (MAT_Z[1] - MAT_Z[0]) + 0.20
    cx = (MAT_X[0] + MAT_X[1]) / 2
    cz = (MAT_Z[0] + MAT_Z[1]) / 2
    bpy.ops.mesh.primitive_plane_add(
        size=1.0,
        # Drop from 60 cm above the mattress so cloth has room to develop
        # folds on the way down. 18 cm (prior run) only made it crease at
        # the mattress edges; nothing in the interior.
        location=(cx, cz, MAT_TOP + 0.60),
    )
    obj = bpy.context.object
    obj.name = 'sheet'
    obj.scale = (sheetW, sheetD, 1)
    bpy.ops.object.transform_apply(scale=True)
    # Slight asymmetric tilt + jiggle so the drape isn't perfectly symmetric
    obj.rotation_euler = (math.radians(2.0), math.radians(-3.0), 0)
    bpy.ops.object.transform_apply(rotation=True)
    # Subdivide for sim resolution
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=80)
    bpy.ops.object.mode_set(mode='OBJECT')
    # Apply cloth modifier — softer settings so the sheet folds visibly.
    cloth = obj.modifiers.new('Cloth', 'CLOTH')
    cloth.settings.quality = 10
    cloth.settings.mass = 0.50
    cloth.settings.tension_stiffness = 4          # was 8; softer = more crinkle
    cloth.settings.compression_stiffness = 4
    cloth.settings.shear_stiffness = 4
    cloth.settings.bending_stiffness = 0.20       # was 0.5; lower = sharper folds
    cloth.settings.use_internal_springs = True
    cloth.collision_settings.distance_min = 0.005
    cloth.collision_settings.collision_quality = 5
    cloth.collision_settings.self_distance_min = 0.005
    cloth.collision_settings.use_self_collision = True
    # Simulate — more frames so the drape fully settles after the fall.
    sim_frames = 160
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = sim_frames
    bpy.context.view_layer.update()
    for f in range(1, sim_frames + 1):
        bpy.context.scene.frame_set(f)
    # Apply the cloth modifier to lock in the drape
    bpy.ops.object.modifier_apply(modifier='Cloth')
    # Do NOT smart-project — the runtime sheet uses three.js PlaneGeometry's
    # default planar UVs (0..1 across the surface). primitive_plane_add gave
    # us exactly that layout, and the subdivide + cloth sim preserved it.
    # Smart-projecting would re-pack into a smaller region, leaving most of
    # the bake texture unused and mis-aligning with the runtime UVs.
    return obj


def make_plush_box(name, dims, dimple_axis, dimple_strength, location):
    """Create a rounded-corner cushion box and sculpt subtle dimples.

    dims: (w, h, d) in metres
    dimple_axis: 'y' (top face) or 'x' (front face)
    """
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (dims[0], dims[1], dims[2])
    bpy.ops.object.transform_apply(scale=True)
    # Bevel the corners so it reads as plush
    bvl = obj.modifiers.new('Bevel', 'BEVEL')
    bvl.width = min(dims) * 0.18
    bvl.segments = 6
    bvl.profile = 0.6
    bpy.ops.object.modifier_apply(modifier='Bevel')
    # Subsurf for smooth + a Displace modifier with random noise for dimples
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=3)
    bpy.ops.object.mode_set(mode='OBJECT')
    # Displace modifier driven by Voronoi for plush
    tex = bpy.data.textures.new(f'{name}_noise', type='VORONOI')
    tex.noise_scale = 0.10
    disp = obj.modifiers.new('Disp', 'DISPLACE')
    disp.texture = tex
    disp.strength = dimple_strength
    bpy.ops.object.modifier_apply(modifier='Disp')
    # Smart UV project
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')
    return obj


# ---------------------------------------------------------------------------
# Baking
# ---------------------------------------------------------------------------

def select_only(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def bake_pass(obj, slug, kind, bake_type, samples=None, save_color='Non-Color'):
    """Bake one map into a fresh image, save it to disk."""
    out_dir = os.path.join(OUT_BASE, slug)
    os.makedirs(out_dir, exist_ok=True)
    img_name = f'{slug}_{kind}'
    img = make_image(img_name, color_space=save_color)
    # Wire the object's material's _bake_target to this image
    mat = obj.data.materials[0]
    target_node = mat.node_tree.nodes.get('_bake_target')
    target_node.image = img
    target_node.select = True
    mat.node_tree.nodes.active = target_node
    # Bake
    select_only(obj)
    bpy.context.scene.cycles.samples = samples or CYCLES_SAMPLES
    bake_kwargs = dict(type=bake_type, margin=MARGIN, use_clear=True,
                       use_selected_to_active=False)
    if bake_type == 'NORMAL':
        bake_kwargs['normal_space'] = 'TANGENT'
    bpy.ops.object.bake(**bake_kwargs)
    out_path = os.path.join(out_dir, f'{img_name}.png')
    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f'  → wrote {out_path}', flush=True)


def bake_all_for(obj, slug, base_color, roughness, sheen, sheen_tint):
    """Bake the four PBR maps for a single object."""
    # Build material with sheen so the diffuse bake captures sheen-modulated
    # albedo at glancing angles (matches what we want the runtime to render).
    mat, _img_node = make_principled_material(
        f'{slug}_mat', base_color, roughness, sheen, sheen_tint
    )
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    print(f'baking {slug} ({obj.name})…', flush=True)
    bake_pass(obj, slug, 'albedo',    'DIFFUSE',
              save_color='sRGB', samples=CYCLES_SAMPLES)
    bake_pass(obj, slug, 'normal',    'NORMAL',
              samples=NORMAL_SAMPLES)
    bake_pass(obj, slug, 'roughness', 'ROUGHNESS', samples=NORMAL_SAMPLES)
    bake_pass(obj, slug, 'ao',        'AO',        samples=CYCLES_SAMPLES)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    seed(2026_05_11)
    reset()
    configure_cycles_optix()
    add_sun()
    add_world_environment()
    print(f'output dir: {OUT_BASE}', flush=True)

    # AO / normal need the mattress present as occluder for the sheet.
    make_mattress()

    # Sheet — cloth-sim drape
    print('cloth-simulating sheet…', flush=True)
    sheet = make_sheet_cloth()

    # White pillow — slightly flattened, top-face dimple
    wp_loc = (2.37, 2.18, MAT_TOP + 0.10)
    print('building white pillow…', flush=True)
    wp = make_plush_box('white_pillow', (0.50, 0.10, 0.35),
                        dimple_axis='y', dimple_strength=-0.012,
                        location=wp_loc)

    # Grey velour cushion — upright, plush front-face dimple
    cu_loc = (2.10, 2.18, MAT_TOP + 0.20)
    print('building grey cushion…', flush=True)
    cu = make_plush_box('grey_cushion', (0.16, 0.36, 0.40),
                        dimple_axis='x', dimple_strength=-0.018,
                        location=cu_loc)

    # AO needs the other bedding pieces present for inter-shadowing.
    # Each bake_all_for call swaps the target's material; other objects keep
    # their materials (or have no material → bake just sees them as occluders).

    bake_all_for(sheet, 'sheet',
                 base_color=(0.96, 0.94, 0.92),
                 roughness=0.95, sheen=1.0, sheen_tint=(1.0, 0.98, 0.94))

    # Export the cloth-simmed sheet as glTF so the runtime can load the
    # EXACT deformed mesh. Without this, the baked textures (which encode
    # AO + normal at the cloth-sim vertex positions) would map onto the
    # runtime's procedurally-displaced plane and the wrinkles would land in
    # the wrong places. With the glTF, runtime mesh + textures are 1:1.
    sheet_glb = os.path.join(OUT_BASE, 'sheet', 'sheet.glb')
    select_only(sheet)
    print('exporting sheet glTF…', flush=True)
    bpy.ops.export_scene.gltf(
        filepath=sheet_glb,
        export_format='GLB',
        use_selection=True,
        export_apply=True,
        export_yup=True,            # three.js convention (+Y up)
        export_normals=True,
        export_tangents=False,
        export_texcoords=True,
        export_materials='NONE',    # runtime applies the sheet PBR material
        export_animations=False,
    )
    print(f'  → wrote {sheet_glb}', flush=True)

    bake_all_for(wp, 'white_pillow',
                 base_color=(0.98, 0.97, 0.95),
                 roughness=0.90, sheen=1.0, sheen_tint=(1.0, 0.98, 0.94))

    bake_all_for(cu, 'grey_cushion',
                 base_color=(0.24, 0.26, 0.25),
                 roughness=0.95, sheen=1.0, sheen_tint=(0.71, 0.74, 0.73))

    print('done.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        sys.stderr.write(f'bake failed: {e}\n')
        import traceback
        traceback.print_exc()
        sys.exit(1)
