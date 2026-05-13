"""
Bake PBR maps (albedo + normal + roughness + AO) for the room-4 ceiling
spotlight fixture: stained-wood crossbar arms + dark painted-metal cone
shades.

Room-4 has an identical fixture to room-2 (same crossbar shape, same
cone shades, same colors). This script uses the same material recipes
as bake_room2_spotlight_wood.py but writes outputs to room-4-textures/.

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python ozu-test/bake/bake_room4_spotlight_wood.py

Output: ozu-test/room-4-textures/spotlight/<slug>/<slug>_{albedo,normal,roughness,ao}.png
  - wood/   — warm orange-brown stained wood (Voronoi grain + plank variation)
  - shade/  — dark matte painted metal (micro-scratch surface)
"""

import bpy
import os

RES     = 1024
SAMPLES = 256
MARGIN  = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'room-4-textures', 'spotlight')
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


def make_wood_material(name='spotlight_wood_r4'):
    """Warm orange-brown stained wood matching crossbar color 0x8b5a2b."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc   = nt.nodes.new('ShaderNodeTexCoord')
    mp   = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (3.0, 28.0, 3.0)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])

    vor = nt.nodes.new('ShaderNodeTexVoronoi')
    vor.inputs['Scale'].default_value = 10.0
    vor.feature = 'F1'
    nt.links.new(mp.outputs['Vector'], vor.inputs['Vector'])

    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 7.0
    noi.inputs['Detail'].default_value = 4.0
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])

    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.22
    ramp.color_ramp.elements[0].color = (0.14, 0.05, 0.02, 1)
    ramp.color_ramp.elements[1].position = 0.62
    ramp.color_ramp.elements[1].color = (0.54, 0.25, 0.09, 1)
    nt.links.new(vor.outputs['Distance'], ramp.inputs['Fac'])

    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (0.60, 0.27, 0.10, 1)
    nt.links.new(ramp.outputs['Color'], mix.inputs['B'])
    nt.links.new(noi.outputs['Fac'], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])

    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.50
    rmix.inputs[3].default_value = 0.65
    nt.links.new(noi.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])

    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.30
    nt.links.new(vor.outputs['Distance'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_shade_material(name='spotlight_shade_r4'):
    """Dark matte painted metal matching shade color 0x2a2520."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc   = nt.nodes.new('ShaderNodeTexCoord')
    mp   = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (20.0, 20.0, 20.0)
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])

    noi = nt.nodes.new('ShaderNodeTexNoise')
    noi.inputs['Scale'].default_value = 60.0
    noi.inputs['Detail'].default_value = 6.0
    noi.inputs['Roughness'].default_value = 0.65
    nt.links.new(mp.outputs['Vector'], noi.inputs['Vector'])

    cmix = nt.nodes.new('ShaderNodeMix')
    cmix.data_type = 'RGBA'
    cmix.inputs['A'].default_value = (0.165, 0.145, 0.125, 1)
    cmix.inputs['B'].default_value = (0.22,  0.195, 0.170, 1)
    nt.links.new(noi.outputs['Fac'], cmix.inputs['Factor'])
    nt.links.new(cmix.outputs['Result'], bsdf.inputs['Base Color'])

    bsdf.inputs['Metallic'].default_value = 0.10

    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.55
    rmix.inputs[3].default_value = 0.72
    nt.links.new(noi.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])

    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.15
    nt.links.new(noi.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
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
    print('=== room-4 spotlight PBR bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()

    wood_mat  = make_wood_material()
    shade_mat = make_shade_material()

    wood_plane  = add_plane_for_bake('wood_plane',  2.0, 2.0, wood_mat,  y_offset=0)
    shade_plane = add_plane_for_bake('shade_plane', 2.0, 2.0, shade_mat, y_offset=5)

    print('Built 2 bake planes. Baking maps...')
    bake_all_for(wood_plane,  'wood')
    bake_all_for(shade_plane, 'shade')

    print('=== room-4 spotlight PBR bake done ===')
    print(f'Outputs in {OUT_DIR}')


if __name__ == '__main__' or '__main__' in __name__:
    main()
