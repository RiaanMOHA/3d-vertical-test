"""
Bake PBR maps for the stairs-test light-maple wood tread material.

Photos (stairs-10, 17, 18, 25, 26, 27) show warm honey-yellow maple/birch
with fine straight grain and a matte-satin finish. Procedural shader uses
noise + wave textures for grain direction + roughness variation. Bakes 4
maps so the runtime can swap from flat 0xe6cca3 to true PBR.

Run on A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python stairs-test/bake/bake_treads.py

Output: stairs-test/textures/treads/light_maple/light_maple_{albedo,normal,roughness,ao}.png
"""

import bpy
import os

RES = 1024
SAMPLES = 256
MARGIN = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'textures', 'treads')
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


def make_maple_material(name='light_maple'):
    """Light maple/birch with directional grain. Wave gives the long grain;
    noise adds knots and tonal variation. Roughness slightly varies with grain
    so highlights track the wood fiber direction."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)

    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    # Stretched mapping in one direction so grain reads as long stripes
    mp.inputs['Scale'].default_value = (3.0, 14.0, 3.0)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])

    # Wave texture for the dominant grain stripes
    wave = nt.nodes.new('ShaderNodeTexWave')
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'X'
    wave.wave_profile = 'SAW'
    wave.inputs['Scale'].default_value = 5.0
    wave.inputs['Distortion'].default_value = 1.5
    wave.inputs['Detail'].default_value = 4.0
    wave.inputs['Detail Scale'].default_value = 1.5
    nt.links.new(mp.outputs['Vector'], wave.inputs['Vector'])

    # Noise for tonal variation across the plank
    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 4.0
    noi.inputs['Detail'].default_value = 5.0
    noi.inputs['Roughness'].default_value = 0.6
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])

    # Color ramp on wave: grain pattern from honey-yellow to slightly darker amber
    grain_ramp = nt.nodes.new('ShaderNodeValToRGB')
    grain_ramp.color_ramp.elements[0].position = 0.20
    grain_ramp.color_ramp.elements[0].color = (0.78, 0.62, 0.42, 1)   # darker amber
    grain_ramp.color_ramp.elements[1].position = 0.80
    grain_ramp.color_ramp.elements[1].color = (0.92, 0.78, 0.55, 1)   # honey
    nt.links.new(wave.outputs['Color'], grain_ramp.inputs['Fac'])

    # Mix grain color with a noise-based tonal layer for plank-to-plank variation
    tone_ramp = nt.nodes.new('ShaderNodeValToRGB')
    tone_ramp.color_ramp.elements[0].position = 0.30
    tone_ramp.color_ramp.elements[0].color = (0.85, 0.70, 0.50, 1)
    tone_ramp.color_ramp.elements[1].position = 0.80
    tone_ramp.color_ramp.elements[1].color = (0.93, 0.81, 0.58, 1)
    nt.links.new(noi.outputs['Fac'], tone_ramp.inputs['Fac'])

    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 0.45
    nt.links.new(grain_ramp.outputs['Color'], mix.inputs['A'])
    nt.links.new(tone_ramp.outputs['Color'], mix.inputs['B'])
    nt.links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])

    # Roughness varies with the wave (grain ridges = slightly rougher)
    rough_ramp = nt.nodes.new('ShaderNodeValToRGB')
    rough_ramp.color_ramp.elements[0].position = 0.0
    rough_ramp.color_ramp.elements[0].color = (0.42, 0.42, 0.42, 1)
    rough_ramp.color_ramp.elements[1].position = 1.0
    rough_ramp.color_ramp.elements[1].color = (0.62, 0.62, 0.62, 1)
    nt.links.new(wave.outputs['Color'], rough_ramp.inputs['Fac'])
    nt.links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # Bump from wave for subtle grain micro-relief
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.18
    nt.links.new(wave.outputs['Color'], bump.inputs['Height'])
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
    print('=== stairs-test light-maple wood PBR bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()
    mat = make_maple_material()
    plane = add_plane_for_bake('maple_plane', 2.0, 2.0, mat)
    print('Baking light maple...')
    bake_all_for(plane, 'light_maple')
    print('=== stairs-test light-maple bake done ===')


if __name__ == '__main__' or '__main__' in __name__:
    main()
