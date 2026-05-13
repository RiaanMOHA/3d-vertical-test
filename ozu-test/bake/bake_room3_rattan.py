"""
Bake PBR maps (albedo + normal + roughness + AO) for the room-3 rattan
pendant shade.

The runtime shade uses:
  matRattan = { color: 0xc9a980, roughness: 0.85 }

Rattan/wicker is a coarser, more structured weave than linen: thick round
strands in a square interlaced grid, straw-tan color, high roughness from
the fibrous surface. Two materials are baked:
  - rattan/  — the cylindrical wicker shade (coarse over-under grid)
  - brass/   — ceiling cup + cord ferrule hardware (warm satin brass)

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python ozu-test/bake/bake_room3_rattan.py

Output: ozu-test/room-3-textures/rattan_pendant/<slug>/<slug>_{albedo,normal,roughness,ao}.png
"""

import bpy
import os

RES     = 1024
SAMPLES = 256
MARGIN  = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'room-3-textures', 'rattan_pendant')
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


def make_rattan_material(name='rattan_wicker'):
    """Coarse wicker/rattan interlaced grid matching 0xc9a980 (straw-tan).

    Rattan strands are round, ~6-8mm diameter, arranged in a square
    over-under pattern. The albedo shows dark strand recesses vs bright
    strand tops; the normal map shows the round cross-section bump.
    """
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc   = nt.nodes.new('ShaderNodeTexCoord')

    # Tile: 6 strands per direction per UV unit gives ~6 strands around the
    # 320mm-circumference shade and ~6 along its 300mm height = ~53mm spacing
    # (matches visible chunky rattan weave in room-3 photos).
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (6.0, 6.0, 1.0)
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])

    # Horizontal strands (warp)
    warp = nt.nodes.new('ShaderNodeTexWave')
    warp.wave_type        = 'BANDS'
    warp.bands_direction  = 'X'
    warp.wave_profile     = 'SIN'
    warp.inputs['Scale'].default_value       = 1.0
    warp.inputs['Distortion'].default_value  = 0.0
    warp.inputs['Detail'].default_value      = 0.0
    nt.links.new(mp.outputs['Vector'], warp.inputs['Vector'])

    # Vertical strands (weft)
    weft = nt.nodes.new('ShaderNodeTexWave')
    weft.wave_type        = 'BANDS'
    weft.bands_direction  = 'Y'
    weft.wave_profile     = 'SIN'
    weft.inputs['Scale'].default_value       = 1.0
    weft.inputs['Distortion'].default_value  = 0.0
    weft.inputs['Detail'].default_value      = 0.0
    nt.links.new(mp.outputs['Vector'], weft.inputs['Vector'])

    # MAX of warp + weft: gives a grid pattern where strand tops are bright
    # and the spaces where strands cross the back side dip dark.
    grid_max = nt.nodes.new('ShaderNodeMath')
    grid_max.operation = 'MAXIMUM'
    nt.links.new(warp.outputs['Color'], grid_max.inputs[0])
    nt.links.new(weft.outputs['Color'], grid_max.inputs[1])

    # MULTIPLY gives the recessed gaps (both low = gap between strands)
    grid_gap = nt.nodes.new('ShaderNodeMath')
    grid_gap.operation = 'MULTIPLY'
    nt.links.new(warp.outputs['Color'], grid_gap.inputs[0])
    nt.links.new(weft.outputs['Color'], grid_gap.inputs[1])

    # Over-under weave: DIFFERENCE between warp and weft determines which
    # strand is on top at each crossing point.
    diff = nt.nodes.new('ShaderNodeMath')
    diff.operation = 'SUBTRACT'
    nt.links.new(warp.outputs['Color'], diff.inputs[0])
    nt.links.new(weft.outputs['Color'], diff.inputs[1])

    diff_remap = nt.nodes.new('ShaderNodeMapRange')
    diff_remap.interpolation_type = 'LINEAR'
    diff_remap.inputs['From Min'].default_value = -1.0
    diff_remap.inputs['From Max'].default_value =  1.0
    diff_remap.inputs['To Min'].default_value   =  0.0
    diff_remap.inputs['To Max'].default_value   =  1.0
    nt.links.new(diff.outputs[0], diff_remap.inputs['Value'])

    # Fibrous noise — gives natural strand surface variation (rattan is
    # slightly fibrous/textured along the strand length).
    fiber_noi = nt.nodes.new('ShaderNodeTexNoise')
    fiber_noi.inputs['Scale'].default_value     = 40.0
    fiber_noi.inputs['Detail'].default_value    = 5.0
    fiber_noi.inputs['Roughness'].default_value = 0.55
    nt.links.new(mp.outputs['Vector'], fiber_noi.inputs['Vector'])

    # Bright-strand color — warm straw-tan, matches 0xc9a980
    col_top = nt.nodes.new('ShaderNodeMix')
    col_top.data_type = 'RGBA'
    col_top.inputs['A'].default_value = (0.79, 0.66, 0.50, 1)   # bright strand top
    col_top.inputs['B'].default_value = (0.70, 0.57, 0.40, 1)   # fiber shade variation
    nt.links.new(fiber_noi.outputs['Fac'], col_top.inputs['Factor'])

    # Dark-gap color — deep shadowed recess between strands
    col_gap = nt.nodes.new('ShaderNodeMix')
    col_gap.data_type = 'RGBA'
    col_gap.inputs['A'].default_value = (0.22, 0.16, 0.09, 1)   # shadowed gap
    col_gap.inputs['B'].default_value = (0.32, 0.23, 0.13, 1)   # slightly lighter gap
    nt.links.new(fiber_noi.outputs['Fac'], col_gap.inputs['Factor'])

    # Mix top vs gap based on the grid max (bright = strand top, dark = gap)
    col_grid = nt.nodes.new('ShaderNodeMix')
    col_grid.data_type = 'RGBA'
    nt.links.new(grid_max.outputs[0], col_grid.inputs['Factor'])
    nt.links.new(col_gap.outputs['Result'], col_grid.inputs['A'])
    nt.links.new(col_top.outputs['Result'], col_grid.inputs['B'])

    nt.links.new(col_grid.outputs['Result'], bsdf.inputs['Base Color'])

    # Roughness — fibrous rattan surface is very matte, slight variation
    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.80
    rmix.inputs[3].default_value = 0.95
    nt.links.new(fiber_noi.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])

    # Bump — round strand cross-section profile from the grid height, plus
    # fine fibrous texture from noise.
    bump_mix = nt.nodes.new('ShaderNodeMath')
    bump_mix.operation = 'ADD'
    nt.links.new(grid_max.outputs[0], bump_mix.inputs[0])

    fiber_bump = nt.nodes.new('ShaderNodeMath')
    fiber_bump.operation = 'MULTIPLY'
    fiber_bump.inputs[1].default_value = 0.20
    nt.links.new(fiber_noi.outputs['Fac'], fiber_bump.inputs[0])
    nt.links.new(fiber_bump.outputs[0], bump_mix.inputs[1])

    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.60
    nt.links.new(bump_mix.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_brass_material(name='pendant_brass'):
    """Warm satin brass for ceiling cup + hardware, 0xb88c4a."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.72, 0.55, 0.29, 1)   # 0xb88c4a
    bsdf.inputs['Metallic'].default_value   = 1.0
    tc   = nt.nodes.new('ShaderNodeTexCoord')
    mp   = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (8.0, 8.0, 8.0)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
    noi  = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value  = 80.0
    noi.inputs['Detail'].default_value = 2.0
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])
    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.30
    rmix.inputs[3].default_value = 0.45
    nt.links.new(noi.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_plane_for_bake(name, w, h, mat, y_offset=0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y_offset, 0))
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
    nt  = mat.node_tree
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
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    img = bpy.data.images.new(
        name=f'{slug}_{kind}',
        width=RES, height=RES,
        alpha=False, float_buffer=False,
    )
    img.colorspace_settings.name = 'sRGB' if kind == 'albedo' else 'Non-Color'

    add_bake_target_node(obj, img)

    scene = bpy.context.scene
    if bake_type == 'DIFFUSE':
        scene.render.bake.use_pass_direct   = False
        scene.render.bake.use_pass_indirect = False
        scene.render.bake.use_pass_color    = True
    elif bake_type == 'NORMAL':
        scene.render.bake.normal_space = 'TANGENT'

    bpy.ops.object.bake(type=bake_type, use_clear=True, margin=MARGIN)

    out_path = os.path.join(OUT_DIR, slug, f'{slug}_{kind}.png')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.filepath_raw = out_path
    img.file_format  = 'PNG'
    img.save()
    print(f'  -> {out_path}')


def bake_all_for(obj, slug):
    bake_pass(obj, slug, 'albedo',    'DIFFUSE')
    bake_pass(obj, slug, 'normal',    'NORMAL')
    bake_pass(obj, slug, 'roughness', 'ROUGHNESS')
    bake_pass(obj, slug, 'ao',        'AO')


def main():
    print('=== room-3 rattan pendant PBR bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()

    rattan_mat = make_rattan_material()
    brass_mat  = make_brass_material()

    rattan_plane = add_plane_for_bake('rattan_plane', 2.0, 2.0, rattan_mat, y_offset=0)
    brass_plane  = add_plane_for_bake('brass_plane',  2.0, 2.0, brass_mat,  y_offset=5)

    print('Built 2 bake planes. Baking maps...')
    bake_all_for(rattan_plane, 'rattan')
    bake_all_for(brass_plane,  'brass')

    print('=== room-3 rattan pendant PBR bake done ===')
    print(f'Outputs in {OUT_DIR}')


if __name__ == '__main__' or '__main__' in __name__:
    main()
