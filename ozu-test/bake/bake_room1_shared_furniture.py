"""
Bake PBR maps (albedo + normal + roughness + AO) for the three shared
furniture-surface materials used across rooms 1–4:

  1. white_iron   — painted white iron (room-1 bed, room-2 bed). Subtle
                    brushed-metal grain + paint chip noise. Lower metalness
                    than raw brass because painted, but still some sheen.
  2. cream_cotton — soft cream cotton sheet weave (mattress / sheet surface,
                    all 4 rooms). Tight thread weave + slight noise mottling,
                    high roughness.
  3. abs_plastic  — Toshiba split AC body plastic (all 4 rooms). Smooth white
                    ABS with very subtle injection-mold noise + low-strength
                    surface microfacet variation.

Why this exists: every PBR object pass per CLAUDE.md cutting-edge rule must
engage the A6000. The shared materials in this script originate in room-1
but are reused by rooms 2/3/4 (room-3/4 iron beds reuse the existing
room-3-textures/shelf/black_iron bake; mattress + AC plastic load from
this script's output for all rooms).

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \
        ~/blender/blender-5.1.1-linux-x64/blender \
        --background \
        --python ozu-test/bake/bake_room1_shared_furniture.py

Output:
  ozu-test/room-1-textures/bed/white_iron/white_iron_{albedo,normal,roughness,ao}.png
  ozu-test/room-1-textures/mattress/cream_cotton/cream_cotton_{albedo,normal,roughness,ao}.png
  ozu-test/room-1-textures/ac/abs/abs_{albedo,normal,roughness,ao}.png

12 PNGs total, 1024² each.
"""

import bpy
import os
from mathutils import Vector

RES         = 1024
SAMPLES     = 256
MARGIN      = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_OUT   = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'room-1-textures'))


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for db in (bpy.data.meshes, bpy.data.materials,
               bpy.data.images, bpy.data.textures, bpy.data.node_groups):
        for it in list(db):
            db.remove(it)


def configure_cycles_optix():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.refresh_devices()
    for d in prefs.devices:
        d.use = (d.type == 'OPTIX')
        print(f'  device: {d.name}  type={d.type}  use={d.use}')
    scene.cycles.device = 'GPU'
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.cycles.use_adaptive_sampling = True


def add_neutral_world():
    scene = bpy.context.scene
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new('World')
        scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    bg = nt.nodes.new('ShaderNodeBackground')
    bg.inputs['Color'].default_value = (1, 1, 1, 1)
    bg.inputs['Strength'].default_value = 1.0
    out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])


# ---------- Material builders ----------

def make_white_iron_material(name='white_iron'):
    """Painted white iron — bed frames. Off-white base with faint brushed
    horizontal grain + slight noise for paint imperfections. Metallic=0.20
    (painted so most of the metal sheen is masked by paint), roughness ~0.45
    with noise variation."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc   = nt.nodes.new('ShaderNodeTexCoord')
    mp   = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (40.0, 2.0, 40.0)   # stretched X for brushed lines
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    # Brushed-grain noise — stretched horizontally for subtle bed-rail brushing.
    grain = nt.nodes.new('ShaderNodeTexNoise')
    grain.inputs['Scale'].default_value = 1.5
    grain.inputs['Detail'].default_value = 2.0
    nt.links.new(mp.outputs['Vector'], grain.inputs['Vector'])
    # Wider color noise for paint mottling.
    paint_noi = nt.nodes.new('ShaderNodeTexNoise')
    paint_noi.inputs['Scale'].default_value = 5.0
    paint_noi.inputs['Detail'].default_value = 4.0
    tc2 = nt.nodes.new('ShaderNodeTexCoord')
    nt.links.new(tc2.outputs['Generated'], paint_noi.inputs['Vector'])
    # Color: warm off-white with subtle paint variation.
    cmix = nt.nodes.new('ShaderNodeMix')
    cmix.data_type = 'RGBA'
    cmix.inputs['A'].default_value = (0.96, 0.96, 0.94, 1)   # warm white
    cmix.inputs['B'].default_value = (0.92, 0.91, 0.87, 1)   # slightly aged cream
    cmix.inputs['Factor'].default_value = 0.5
    nt.links.new(paint_noi.outputs['Fac'], cmix.inputs['Factor'])
    nt.links.new(cmix.outputs['Result'], bsdf.inputs['Base Color'])
    bsdf.inputs['Metallic'].default_value = 0.20
    # Roughness — noise-modulated.
    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.42
    rmix.inputs[3].default_value = 0.58
    nt.links.new(grain.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])
    # Bump — fine brushed grain.
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.18
    nt.links.new(grain.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_cream_cotton_material(name='cream_cotton'):
    """Cream cotton sheet — tighter weave than the pendant's linen. Higher
    thread count, less mottling, very matte."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc   = nt.nodes.new('ShaderNodeTexCoord')
    mp   = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (80.0, 80.0, 1.0)   # tight square weave
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])
    # Warp + weft as bands.
    warp = nt.nodes.new('ShaderNodeTexWave')
    warp.wave_type = 'BANDS'
    warp.bands_direction = 'X'
    warp.inputs['Scale'].default_value = 1.0
    warp.inputs['Distortion'].default_value = 0.0
    nt.links.new(mp.outputs['Vector'], warp.inputs['Vector'])
    weft = nt.nodes.new('ShaderNodeTexWave')
    weft.wave_type = 'BANDS'
    weft.bands_direction = 'Y'
    weft.inputs['Scale'].default_value = 1.0
    nt.links.new(mp.outputs['Vector'], weft.inputs['Vector'])
    combo = nt.nodes.new('ShaderNodeMath')
    combo.operation = 'MULTIPLY'
    nt.links.new(warp.outputs['Color'], combo.inputs[0])
    nt.links.new(weft.outputs['Color'], combo.inputs[1])
    # Faint color noise for fabric thread-color variance.
    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 300.0
    noi.inputs['Detail'].default_value = 2.0
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])
    # Cream base — slightly off-white toward yellow.
    cmix = nt.nodes.new('ShaderNodeMix')
    cmix.data_type = 'RGBA'
    cmix.inputs['A'].default_value = (0.96, 0.92, 0.85, 1)
    cmix.inputs['B'].default_value = (0.92, 0.86, 0.74, 1)
    nt.links.new(noi.outputs['Fac'], cmix.inputs['Factor'])
    nt.links.new(cmix.outputs['Result'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.96
    # Bump — finer than burlap (higher freq weave).
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.30
    nt.links.new(combo.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_abs_plastic_material(name='abs_plastic'):
    """Smooth ABS plastic — Toshiba AC body. Off-white base, low roughness
    variation, very subtle injection-mold surface texture."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc   = nt.nodes.new('ShaderNodeTexCoord')
    mp   = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (12.0, 12.0, 12.0)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    # Fine noise for plastic micro-grain.
    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 50.0
    noi.inputs['Detail'].default_value = 2.0
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])
    # Color: warm off-white with very subtle variation.
    cmix = nt.nodes.new('ShaderNodeMix')
    cmix.data_type = 'RGBA'
    cmix.inputs['A'].default_value = (0.96, 0.95, 0.93, 1)
    cmix.inputs['B'].default_value = (0.94, 0.93, 0.90, 1)
    cmix.inputs['Factor'].default_value = 0.5
    nt.links.new(noi.outputs['Fac'], cmix.inputs['Factor'])
    nt.links.new(cmix.outputs['Result'], bsdf.inputs['Base Color'])
    bsdf.inputs['Metallic'].default_value = 0.0
    # Roughness — fairly low (plastic has slight sheen) with subtle noise.
    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.32
    rmix.inputs[3].default_value = 0.45
    nt.links.new(noi.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])
    # Very faint bump — just enough to break up specular reflections.
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.08
    nt.links.new(noi.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


# ---------- Geometry + bake helpers ----------

def add_plane_for_bake(name, w, h, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w, h, 1)
    bpy.ops.object.transform_apply(scale=True)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj


def add_bake_target_node(obj, image):
    mat = obj.data.materials[0]
    nt = mat.node_tree
    for n in list(nt.nodes):
        if n.label == '_bake_target':
            nt.nodes.remove(n)
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.label = '_bake_target'
    tex.image = image
    tex.select = True
    nt.nodes.active = tex
    return tex


def bake_pass(obj, sub_dir, slug, kind, bake_type):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    img = bpy.data.images.new(
        name=f'{slug}_{kind}',
        width=RES, height=RES,
        alpha=False, float_buffer=False,
    )
    if kind == 'albedo':
        img.colorspace_settings.name = 'sRGB'
    else:
        img.colorspace_settings.name = 'Non-Color'

    add_bake_target_node(obj, img)

    scene = bpy.context.scene
    if bake_type == 'DIFFUSE':
        scene.render.bake.use_pass_direct = False
        scene.render.bake.use_pass_indirect = False
        scene.render.bake.use_pass_color = True
    elif bake_type == 'NORMAL':
        scene.render.bake.normal_space = 'TANGENT'
    elif bake_type == 'AO':
        scene.render.bake.use_pass_direct = False
        scene.render.bake.use_pass_indirect = False

    bpy.ops.object.bake(type=bake_type, use_clear=True, margin=MARGIN)

    # Layout: ROOT/<object>/<material>/<material>_<kind>.png
    # sub_dir is already "<object>/<material>", slug is the material name and
    # appears only in the filename prefix (NOT another nested folder).
    out_path = os.path.join(ROOT_OUT, sub_dir, f'{slug}_{kind}.png')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f'  -> {out_path}')


def bake_all_for(obj, sub_dir, slug):
    bake_pass(obj, sub_dir, slug, 'albedo',    'DIFFUSE')
    bake_pass(obj, sub_dir, slug, 'normal',    'NORMAL')
    bake_pass(obj, sub_dir, slug, 'roughness', 'ROUGHNESS')
    bake_pass(obj, sub_dir, slug, 'ao',        'AO')


def main():
    print('=== shared furniture PBR bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()

    iron_mat    = make_white_iron_material()
    cotton_mat  = make_cream_cotton_material()
    plastic_mat = make_abs_plastic_material()

    iron_plane    = add_plane_for_bake('iron_plane',    2.0, 2.0, iron_mat)
    iron_plane.location.y = 0
    cotton_plane  = add_plane_for_bake('cotton_plane',  2.0, 2.0, cotton_mat)
    cotton_plane.location.y = 5
    plastic_plane = add_plane_for_bake('plastic_plane', 2.0, 2.0, plastic_mat)
    plastic_plane.location.y = 10

    print('Built 3 bake planes. Baking maps...')
    bake_all_for(iron_plane,    'bed/white_iron',         'white_iron')
    bake_all_for(cotton_plane,  'mattress/cream_cotton',  'cream_cotton')
    bake_all_for(plastic_plane, 'ac/abs',                 'abs')

    print('=== shared furniture PBR bake done ===')
    print(f'Outputs in {ROOT_OUT}')


if __name__ == '__main__' or '__main__' in __name__:
    main()
