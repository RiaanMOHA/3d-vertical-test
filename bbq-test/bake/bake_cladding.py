"""
Bake PBR maps for the bbq-test cream ALC cladding (back-wall facade).

Photo references: ozu-test/exterior-images/ozu-1-test-exterior-{125,126,127}.webp
— off-white horizontal-ribbed exterior cladding (ALC panels).

Procedural recipe:
  - Cream off-white base (#d6cfbf)
  - Fine paint-stipple micro-texture (small-scale Noise)
  - Subtle dirt mottle for weathering (large-scale Noise)
  - Slight gradient streaking from a Wave Texture

The horizontal RIBS are NOT in the baked texture (they're modeled as
real geometry in bbq-test.html). This bake only covers the paint surface
between ribs.

Outputs → bbq-test-textures/cladding/cladding_{albedo,normal,roughness,ao}.png
"""

import bpy
import os

RES = 2048
SAMPLES = 512
MARGIN = 8
SLUG = 'cladding'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..', 'bbq-test-textures'))
os.makedirs(OUT_DIR, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for db in (bpy.data.meshes, bpy.data.materials,
               bpy.data.images, bpy.data.textures, bpy.data.node_groups):
        for it in list(db):
            db.remove(it)


def configure_cycles():
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


def make_cladding_material(name='alc_cladding_cream'):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.0, 1.0, 1.0)
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])

    # Tiny paint-stipple noise (high frequency)
    noi_fine = nt.nodes.new('ShaderNodeTexNoise')
    noi_fine.inputs['Scale'].default_value = 60.0
    noi_fine.inputs['Detail'].default_value = 4.0
    noi_fine.inputs['Roughness'].default_value = 0.5
    nt.links.new(tc.outputs['UV'], noi_fine.inputs['Vector'])

    # Larger dirt mottle
    noi_lg = nt.nodes.new('ShaderNodeTexNoise')
    noi_lg.inputs['Scale'].default_value = 1.2
    noi_lg.inputs['Detail'].default_value = 3.0
    noi_lg.inputs['Roughness'].default_value = 0.7
    nt.links.new(tc.outputs['UV'], noi_lg.inputs['Vector'])

    # Albedo ramp on dirt: mostly clean, slightly darker patches
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (0.78, 0.74, 0.65, 1)  # dirty patches
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = (0.86, 0.83, 0.77, 1)  # clean cream
    nt.links.new(noi_lg.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])

    # Roughness: 0.82 base, ±0.04 with fine noise (paint stipple)
    rmix = nt.nodes.new('ShaderNodeMix')
    rmix.data_type = 'FLOAT'
    rmix.inputs[2].default_value = 0.80
    rmix.inputs[3].default_value = 0.88
    nt.links.new(noi_fine.outputs['Fac'], rmix.inputs['Factor'])
    nt.links.new(rmix.outputs[0], bsdf.inputs['Roughness'])

    # Subtle bump from the paint stipple (very low strength)
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.20
    bump.inputs['Distance'].default_value = 0.002
    nt.links.new(noi_fine.outputs['Fac'], bump.inputs['Height'])
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


def bake_pass(obj, slug, kind, bake_type):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    img = bpy.data.images.new(name=f'{slug}_{kind}', width=RES, height=RES,
                               alpha=False, float_buffer=False)
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
    print(f'=== bbq-test {SLUG} PBR bake start ===')
    clear_scene()
    configure_cycles()
    add_neutral_world()
    mat = make_cladding_material()
    plane = add_plane_for_bake(f'{SLUG}_plane', 2.0, 2.0, mat)
    bake_all_for(plane, SLUG)
    print(f'=== bbq-test {SLUG} PBR bake done ===')


if __name__ == '__main__' or '__main__' in __name__:
    main()
