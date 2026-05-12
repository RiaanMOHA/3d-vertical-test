"""
Bake PBR maps (albedo + normal + roughness + AO) for the room-1 pendant
fixture components: stained-wood crossbar, woven-linen shades, brass hub
+ shade collars.

Why this exists: the runtime pendant uses flat colors + a Canvas2D linen
'photo' texture on the shades — no normal map, no roughness variation. The
shades read as printed photos on smooth cylinders, the wood crossbar reads
as flat plastic. Per CLAUDE.md cutting-edge rule, every room-1 object pass
must engage the A6000 with a Cycles bake.

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \
        ~/blender/blender-5.1.1-linux-x64/blender \
        --background \
        --python ozu-test/bake/bake_room1_pendant.py

Output: ozu-test/room-1-textures/pendant/<slug>/<slug>_{albedo,normal,roughness,ao}.png
  - wood/   — orange-brown stained pine (Voronoi grain + plank seams)
  - linen/  — woven cotton/linen burlap (warp+weft micro-weave)
  - brass/  — warm yellow-brass with anisotropic finish (small bevels)

12 PNGs total, 1024² each. Runtime wires them into MeshStandardMaterial.
"""

import bpy
import os
import math
from mathutils import Vector

RES         = 1024
SAMPLES     = 256
MARGIN      = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'room-1-textures', 'pendant')
)
os.makedirs(OUT_DIR, exist_ok=True)


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
    """Neutral white environment so the bake captures material response,
    not lighting bias."""
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


# ---------- Material builders (procedural shaders for Cycles bake) ----------

def make_wood_material(name='wood_stained_pine'):
    """Warm orange-brown stained pine: Voronoi-driven grain on a noise base.
    Higher roughness than polished wood (matte clear coat / oiled finish)."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    # Texture coords + mapping for grain control.
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (3.0, 30.0, 3.0)   # stretch grain along Y
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    # Voronoi for plank grain — F1 stretched gives long fibers.
    vor = nt.nodes.new('ShaderNodeTexVoronoi')
    vor.inputs['Scale'].default_value = 12.0
    vor.feature = 'F1'
    nt.links.new(mp.outputs['Vector'], vor.inputs['Vector'])
    # Noise for color variation.
    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 8.0
    noi.inputs['Detail'].default_value = 4.0
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])
    # Color ramp to mix dark+light wood tones.
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.20
    ramp.color_ramp.elements[0].color = (0.18, 0.07, 0.03, 1)   # dark grain line
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = (0.55, 0.25, 0.10, 1)   # warm orange-brown body
    nt.links.new(vor.outputs['Distance'], ramp.inputs['Fac'])
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (0.62, 0.28, 0.11, 1)       # base orange-brown
    nt.links.new(ramp.outputs['Color'], mix.inputs['B'])
    nt.links.new(noi.outputs['Fac'], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])
    # Roughness — slightly noisy oiled finish.
    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.60
    rmix.inputs[3].default_value = 0.85
    nt.links.new(noi.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])
    # Bump from Voronoi (gives visible grain).
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.35
    nt.links.new(vor.outputs['Distance'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_linen_material(name='linen_burlap'):
    """Coarse warm-cream linen weave with HIGHLY VISIBLE warp/weft pattern.

    Photo-matched against room-1/corner-ac-entrance/03-05: the pendant
    shades show a distinct chunky cross-hatch weave clearly visible in
    color (not just bump). Threads are ~3mm thick, alternating warm
    cream warp threads with slightly darker weft threads.
    """
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')

    # BIG coarse-linen weave — runtime uses repU=1, so this 8×10 tile gives
    # ~8 threads around the shade circumference and ~10 along its height,
    # matching the chunky burlap-style weave clearly visible in the photos.
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (8.0, 10.0, 1.0)
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])

    # Warp = horizontal bands (vertical threads); Weft = vertical bands.
    warp = nt.nodes.new('ShaderNodeTexWave')
    warp.wave_type = 'BANDS'
    warp.bands_direction = 'X'
    warp.wave_profile = 'SIN'
    warp.inputs['Scale'].default_value = 1.0
    warp.inputs['Distortion'].default_value = 0.15
    warp.inputs['Detail'].default_value = 0.0
    nt.links.new(mp.outputs['Vector'], warp.inputs['Vector'])

    weft = nt.nodes.new('ShaderNodeTexWave')
    weft.wave_type = 'BANDS'
    weft.bands_direction = 'Y'
    weft.wave_profile = 'SIN'
    weft.inputs['Scale'].default_value = 1.0
    weft.inputs['Distortion'].default_value = 0.15
    nt.links.new(mp.outputs['Vector'], weft.inputs['Vector'])

    # Combined cross-hatch: ADD warp + weft and clamp so high-contrast
    # cross-hatch pattern emerges (where threads cross = brightest).
    combo = nt.nodes.new('ShaderNodeMath')
    combo.operation = 'ADD'
    nt.links.new(warp.outputs['Color'], combo.inputs[0])
    nt.links.new(weft.outputs['Color'], combo.inputs[1])

    # Difference of warp - weft gives a TARTAN-style colour separation: where
    # warp threads are visible (top of bump) we see one colour; where weft
    # threads are visible (perpendicular) we see another. This is what makes
    # the weave appear in the ALBEDO not just the normal map.
    warp_weft_diff = nt.nodes.new('ShaderNodeMath')
    warp_weft_diff.operation = 'SUBTRACT'
    nt.links.new(warp.outputs['Color'], warp_weft_diff.inputs[0])
    nt.links.new(weft.outputs['Color'], warp_weft_diff.inputs[1])

    # Map diff (-1..1) to 0..1 for use as mix factor
    diff_remap = nt.nodes.new('ShaderNodeMapRange')
    diff_remap.interpolation_type = 'LINEAR'
    diff_remap.inputs['From Min'].default_value = -1.0
    diff_remap.inputs['From Max'].default_value = 1.0
    diff_remap.inputs['To Min'].default_value = 0.0
    diff_remap.inputs['To Max'].default_value = 1.0
    nt.links.new(warp_weft_diff.outputs[0], diff_remap.inputs['Value'])

    # Slight per-thread color noise for natural variation
    thread_noi = nt.nodes.new('ShaderNodeTexNoise')
    thread_noi.inputs['Scale'].default_value = 80.0
    thread_noi.inputs['Detail'].default_value = 3.0
    nt.links.new(mp.outputs['Vector'], thread_noi.inputs['Vector'])

    # WARP threads colour (raised threads — bright cream)
    warp_col = nt.nodes.new('ShaderNodeMix')
    warp_col.data_type = 'RGBA'
    warp_col.inputs['A'].default_value = (0.95, 0.88, 0.72, 1)
    warp_col.inputs['B'].default_value = (0.88, 0.80, 0.62, 1)
    nt.links.new(thread_noi.outputs['Fac'], warp_col.inputs['Factor'])

    # WEFT threads colour (recessed threads — deeper tan, ~30% darker)
    weft_col = nt.nodes.new('ShaderNodeMix')
    weft_col.data_type = 'RGBA'
    weft_col.inputs['A'].default_value = (0.62, 0.50, 0.34, 1)
    weft_col.inputs['B'].default_value = (0.55, 0.42, 0.28, 1)
    nt.links.new(thread_noi.outputs['Fac'], weft_col.inputs['Factor'])

    # Mix warp vs weft colour by which thread is on top at this pixel
    weave_color = nt.nodes.new('ShaderNodeMix')
    weave_color.data_type = 'RGBA'
    nt.links.new(diff_remap.outputs[0], weave_color.inputs['Factor'])
    nt.links.new(weft_col.outputs['Result'], weave_color.inputs['A'])
    nt.links.new(warp_col.outputs['Result'], weave_color.inputs['B'])

    nt.links.new(weave_color.outputs['Result'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = 0.95

    # Moderate bump — too strong (1.0) produced radial spike artefacts when
    # the shade is viewed nearly edge-on (top-down). 0.5 reads as visible
    # weave from side angles without exaggerating at oblique views.
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.5
    nt.links.new(combo.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_brass_material(name='brass_satin'):
    """Warm yellow-brass with low-roughness satin finish + slight noise."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.78, 0.61, 0.28, 1)   # 0xc7a347
    bsdf.inputs['Metallic'].default_value = 1.0
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (8.0, 8.0, 8.0)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 80.0
    noi.inputs['Detail'].default_value = 2.0
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])
    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.28
    rmix.inputs[3].default_value = 0.42
    nt.links.new(noi.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


# ---------- Geometry builders for the bake stage ----------

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


# ---------- Bake helper ----------

def add_bake_target_node(obj, image):
    """Attach an Image Texture node so Cycles writes into the supplied image."""
    mat = obj.data.materials[0]
    nt = mat.node_tree
    # Remove any existing bake target.
    for n in list(nt.nodes):
        if n.label == '_bake_target':
            nt.nodes.remove(n)
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.label = '_bake_target'
    tex.image = image
    tex.select = True
    nt.nodes.active = tex
    return tex


def bake_pass(obj, slug, kind, bake_type):
    """Bake one channel (kind in {albedo, normal, roughness, ao}) for obj."""
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

    out_path = os.path.join(OUT_DIR, slug, f'{slug}_{kind}.png')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f'  -> {out_path}')


def bake_all_for(obj, slug):
    """Bake albedo, normal, roughness, AO for obj."""
    bake_pass(obj, slug, 'albedo',    'DIFFUSE')
    bake_pass(obj, slug, 'normal',    'NORMAL')
    bake_pass(obj, slug, 'roughness', 'ROUGHNESS')
    bake_pass(obj, slug, 'ao',        'AO')


def main():
    print('=== room-1 pendant PBR bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()

    # Three flat planes, one per material, each at its own Y so they don't
    # share AO (each baked independently anyway via select-set).
    wood_mat  = make_wood_material()
    linen_mat = make_linen_material()
    brass_mat = make_brass_material()

    wood_plane  = add_plane_for_bake('wood_plane',  2.0, 2.0, wood_mat)
    wood_plane.location.y = 0
    linen_plane = add_plane_for_bake('linen_plane', 2.0, 2.0, linen_mat)
    linen_plane.location.y = 5
    brass_plane = add_plane_for_bake('brass_plane', 2.0, 2.0, brass_mat)
    brass_plane.location.y = 10

    print('Built 3 bake planes. Baking maps...')
    bake_all_for(wood_plane,  'wood')
    bake_all_for(linen_plane, 'linen')
    bake_all_for(brass_plane, 'brass')

    print('=== room-1 pendant PBR bake done ===')
    print(f'Outputs in {OUT_DIR}')


if __name__ == '__main__' or '__main__' in __name__:
    main()
