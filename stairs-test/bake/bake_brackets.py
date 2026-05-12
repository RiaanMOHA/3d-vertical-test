"""
Bake PBR maps for the stairs-test brushed-chrome handrail wall brackets +
joint ferrules.

Photos (stairs-7, 25, 19) show slim brushed-metal brackets with a soft
satin finish — not mirror chrome, not matte. Anisotropic brushed pattern
in ONE direction (perpendicular to the rail axis). Slight tarnish noise.

Run on A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python stairs-test/bake/bake_brackets.py

Output: stairs-test/textures/brackets/brushed_chrome/brushed_chrome_{albedo,normal,roughness,ao}.png
"""

import bpy
import os

RES = 1024
SAMPLES = 256
MARGIN = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'textures', 'brackets')
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


def make_brushed_chrome_material(name='brushed_chrome'):
    """Brushed chrome — anisotropic linear scratch pattern + slight tarnish."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)

    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Base Color'].default_value = (0.78, 0.80, 0.84, 1)

    tc = nt.nodes.new('ShaderNodeTexCoord')

    # Anisotropic brush pattern — wave in one direction, very fine
    brush_mp = nt.nodes.new('ShaderNodeMapping')
    brush_mp.inputs['Scale'].default_value = (60.0, 4.0, 4.0)
    nt.links.new(tc.outputs['Generated'], brush_mp.inputs['Vector'])

    brush_noi = nt.nodes.new('ShaderNodeTexNoise')
    brush_noi.inputs['Scale'].default_value = 14.0
    brush_noi.inputs['Detail'].default_value = 5.0
    brush_noi.inputs['Roughness'].default_value = 0.4
    nt.links.new(brush_mp.outputs['Vector'], brush_noi.inputs['Vector'])

    # Slight tarnish for color variation
    tone_noi = nt.nodes.new('ShaderNodeTexNoise')
    tone_noi.inputs['Scale'].default_value = 3.0
    tone_noi.inputs['Detail'].default_value = 3.0
    nt.links.new(tc.outputs['Generated'], tone_noi.inputs['Vector'])

    # Color modulation: very slight warm tint variation in tarnish areas
    color_ramp = nt.nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.30
    color_ramp.color_ramp.elements[0].color = (0.74, 0.76, 0.80, 1)
    color_ramp.color_ramp.elements[1].position = 0.85
    color_ramp.color_ramp.elements[1].color = (0.82, 0.84, 0.88, 1)
    nt.links.new(tone_noi.outputs['Fac'], color_ramp.inputs['Fac'])
    nt.links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

    # Roughness varies with brush pattern (more rough in scratched areas)
    rough_ramp = nt.nodes.new('ShaderNodeValToRGB')
    rough_ramp.color_ramp.elements[0].position = 0.20
    rough_ramp.color_ramp.elements[0].color = (0.22, 0.22, 0.22, 1)
    rough_ramp.color_ramp.elements[1].position = 0.85
    rough_ramp.color_ramp.elements[1].color = (0.40, 0.40, 0.40, 1)
    nt.links.new(brush_noi.outputs['Fac'], rough_ramp.inputs['Fac'])
    nt.links.new(rough_ramp.outputs['Color'], bsdf.inputs['Roughness'])

    # Anisotropic micro-bump from brush pattern
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.05
    nt.links.new(brush_noi.outputs['Fac'], bump.inputs['Height'])
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
    print('=== stairs-test brackets brushed-chrome PBR bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()
    mat = make_brushed_chrome_material()
    plane = add_plane_for_bake('chrome_plane', 2.0, 2.0, mat)
    print('Baking brushed chrome...')
    bake_all_for(plane, 'brushed_chrome')
    print('=== stairs-test brackets bake done ===')


if __name__ == '__main__' or '__main__' in __name__:
    main()
