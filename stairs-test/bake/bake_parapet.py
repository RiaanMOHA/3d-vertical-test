"""
Bake PBR maps for the stairs-test parapet — white-painted wall body +
white-painted bullnose wood cap. Two materials in one script (two passes
per material).

Photos (stairs-1, 2, 3, 21) show:
  - Body: white-painted plaster, slight texture, eggshell finish
  - Cap: white-painted wood, slight grain visible through paint, satin finish

Run on A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python stairs-test/bake/bake_parapet.py

Output:
  stairs-test/textures/parapet/white_paint/white_paint_{albedo,normal,roughness,ao}.png
  stairs-test/textures/parapet/white_cap_wood/white_cap_wood_{albedo,normal,roughness,ao}.png
"""

import bpy
import os

RES = 1024
SAMPLES = 256
MARGIN = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'textures', 'parapet')
)


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
    scene.cycles.device = 'GPU'
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True


def add_neutral_world():
    scene = bpy.context.scene
    world = scene.world or bpy.data.worlds.new('World')
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


def make_white_paint_material(name='white_paint'):
    """Plaster wall paint — slight stipple texture."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (8.0, 8.0, 8.0)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])

    # Fine stipple noise
    stip_noi = nt.nodes.new('ShaderNodeTexNoise')
    stip_noi.inputs['Scale'].default_value = 25.0
    stip_noi.inputs['Detail'].default_value = 4.0
    nt.links.new(mp.outputs['Vector'], stip_noi.inputs['Vector'])

    # Color: white with tiny variation
    color_ramp = nt.nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.30
    color_ramp.color_ramp.elements[0].color = (0.93, 0.93, 0.91, 1)
    color_ramp.color_ramp.elements[1].position = 0.85
    color_ramp.color_ramp.elements[1].color = (0.97, 0.97, 0.95, 1)
    nt.links.new(stip_noi.outputs['Fac'], color_ramp.inputs['Fac'])
    nt.links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    bsdf.inputs['Roughness'].default_value = 0.85

    # Bump
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.06
    nt.links.new(stip_noi.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_white_cap_wood_material(name='white_cap_wood'):
    """White-painted wood cap — paint mostly hides grain but a faint long
    grain pattern shows through in highlights."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')

    # Stretched mapping for faint grain
    grain_mp = nt.nodes.new('ShaderNodeMapping')
    grain_mp.inputs['Scale'].default_value = (3.0, 16.0, 3.0)
    nt.links.new(tc.outputs['Generated'], grain_mp.inputs['Vector'])

    grain_wave = nt.nodes.new('ShaderNodeTexWave')
    grain_wave.wave_type = 'BANDS'
    grain_wave.bands_direction = 'X'
    grain_wave.wave_profile = 'SAW'
    grain_wave.inputs['Scale'].default_value = 4.0
    grain_wave.inputs['Distortion'].default_value = 0.5
    nt.links.new(grain_mp.outputs['Vector'], grain_wave.inputs['Vector'])

    # Color: bright white with faint grain
    color_ramp = nt.nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.40
    color_ramp.color_ramp.elements[0].color = (0.95, 0.94, 0.91, 1)
    color_ramp.color_ramp.elements[1].position = 0.75
    color_ramp.color_ramp.elements[1].color = (0.98, 0.97, 0.94, 1)
    nt.links.new(grain_wave.outputs['Color'], color_ramp.inputs['Fac'])
    nt.links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    bsdf.inputs['Roughness'].default_value = 0.55

    # Faint bump from grain
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.04
    nt.links.new(grain_wave.outputs['Color'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


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
    bake_pass(obj, slug, 'albedo',    'DIFFUSE')
    bake_pass(obj, slug, 'normal',    'NORMAL')
    bake_pass(obj, slug, 'roughness', 'ROUGHNESS')
    bake_pass(obj, slug, 'ao',        'AO')


def main():
    print('=== stairs-test parapet PBR bake start ===')
    configure_cycles_optix()
    add_neutral_world()

    # Pass 1: white paint (parapet body)
    clear_scene()
    add_neutral_world()
    paint_mat = make_white_paint_material()
    paint_plane = add_plane_for_bake('white_paint_plane', 2.0, 2.0, paint_mat)
    print('Baking parapet white paint...')
    bake_all_for(paint_plane, 'white_paint')

    # Pass 2: white cap wood
    clear_scene()
    add_neutral_world()
    cap_mat = make_white_cap_wood_material()
    cap_plane = add_plane_for_bake('white_cap_wood_plane', 2.0, 2.0, cap_mat)
    print('Baking parapet white cap wood...')
    bake_all_for(cap_plane, 'white_cap_wood')

    print('=== stairs-test parapet bake done ===')


if __name__ == '__main__' or '__main__' in __name__:
    main()
