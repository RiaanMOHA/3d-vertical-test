"""
Bake light-colored woodgrain laminate ceiling for room-1.

Source albedo: ../../new-textures/ceiling-woodgrain-clean.jpg (WD-061, pale
grey woodgrain laminate sample with vertical grain). Procedural normal +
roughness + AO are layered on top.

Plank layout: 5 planks per 1 m x 1 m tile (each plank 0.2 m wide).
Grain runs along plank length (V axis). A per-plank hash shifts V so
adjacent planks read with different grain. Dark recessed seam at every
plank boundary.

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python ozu-test/bake/bake_room1_ceiling_woodgrain.py

Output (2048^2 each):
    ozu-test/room-1-textures/ceiling/woodgrain_laminate/
        woodgrain_laminate_{albedo,normal,roughness,ao}.png
"""

import bpy
import os

ROOM_ID = 1
RES     = 2048
SAMPLES = 256
MARGIN  = 8
SLUG    = 'woodgrain_laminate'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_OUT   = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', f'room-{ROOM_ID}-textures'))
IMG_PATH   = os.path.normpath(os.path.join(
    SCRIPT_DIR, '..', '..', 'new-textures', 'ceiling-woodgrain-clean.jpg'))


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


def make_woodgrain_laminate_material(name='woodgrain_laminate'):
    """Pale grey woodgrain laminate ceiling.

    Uses the ceiling-woodgrain-clean.jpg image as the base albedo. Plank grid
    of 5 planks per tile along U; per-plank V hash shifts the sampled
    band so adjacent planks differ. Dark, slightly recessed seam at
    every plank boundary. Subtle bump from image luminance.
    """
    img = bpy.data.images.load(IMG_PATH)
    img.colorspace_settings.name = 'sRGB'

    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)

    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')

    tc = nt.nodes.new('ShaderNodeTexCoord')

    # ===== Plank grid: 5 planks per tile along U axis =====
    N_PLANKS = 5
    plank_map = nt.nodes.new('ShaderNodeMapping')
    plank_map.inputs['Scale'].default_value = (float(N_PLANKS), 1.0, 1.0)
    nt.links.new(tc.outputs['UV'], plank_map.inputs['Vector'])

    sep_uv = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(plank_map.outputs['Vector'], sep_uv.inputs['Vector'])

    fract_u = nt.nodes.new('ShaderNodeMath')
    fract_u.operation = 'FRACT'
    nt.links.new(sep_uv.outputs['X'], fract_u.inputs[0])

    plank_idx = nt.nodes.new('ShaderNodeMath')
    plank_idx.operation = 'FLOOR'
    nt.links.new(sep_uv.outputs['X'], plank_idx.inputs[0])

    inv_u = nt.nodes.new('ShaderNodeMath')
    inv_u.operation = 'SUBTRACT'
    inv_u.inputs[0].default_value = 1.0
    nt.links.new(fract_u.outputs[0], inv_u.inputs[1])

    near_seam = nt.nodes.new('ShaderNodeMath')
    near_seam.operation = 'MINIMUM'
    nt.links.new(fract_u.outputs[0], near_seam.inputs[0])
    nt.links.new(inv_u.outputs[0], near_seam.inputs[1])

    seam_dist = nt.nodes.new('ShaderNodeMath')
    seam_dist.operation = 'MULTIPLY'
    seam_dist.inputs[1].default_value = 2.0
    nt.links.new(near_seam.outputs[0], seam_dist.inputs[0])

    seam_mask = nt.nodes.new('ShaderNodeMapRange')
    seam_mask.interpolation_type = 'SMOOTHSTEP'
    seam_mask.inputs['From Min'].default_value = 0.0
    seam_mask.inputs['From Max'].default_value = 0.020
    seam_mask.inputs['To Min'].default_value = 0.0
    seam_mask.inputs['To Max'].default_value = 1.0
    nt.links.new(seam_dist.outputs[0], seam_mask.inputs['Value'])

    # ===== Per-plank V shift =====
    plank_hash = nt.nodes.new('ShaderNodeTexWhiteNoise')
    plank_hash.noise_dimensions = '1D'
    nt.links.new(plank_idx.outputs[0], plank_hash.inputs['W'])

    v_plus_hash = nt.nodes.new('ShaderNodeMath')
    v_plus_hash.operation = 'ADD'
    nt.links.new(sep_uv.outputs['Y'], v_plus_hash.inputs[0])
    nt.links.new(plank_hash.outputs['Value'], v_plus_hash.inputs[1])

    sample_uv = nt.nodes.new('ShaderNodeCombineXYZ')
    nt.links.new(fract_u.outputs[0], sample_uv.inputs['X'])
    nt.links.new(v_plus_hash.outputs[0], sample_uv.inputs['Y'])

    # ===== Image texture (the laminate sample) =====
    img_tex = nt.nodes.new('ShaderNodeTexImage')
    img_tex.image = img
    img_tex.extension = 'REPEAT'
    nt.links.new(sample_uv.outputs['Vector'], img_tex.inputs['Vector'])

    # ===== Seam: dark recessed line at plank boundaries =====
    seam_color = nt.nodes.new('ShaderNodeMix')
    seam_color.data_type = 'RGBA'
    seam_color.inputs['A'].default_value = (0.20, 0.18, 0.16, 1)
    nt.links.new(seam_mask.outputs[0], seam_color.inputs['Factor'])
    nt.links.new(img_tex.outputs['Color'], seam_color.inputs['B'])

    nt.links.new(seam_color.outputs['Result'], bsdf.inputs['Base Color'])

    # ===== Roughness: laminate ~0.50, slightly rougher at seam =====
    rough_mix = nt.nodes.new('ShaderNodeMix')
    rough_mix.data_type = 'FLOAT'
    rough_mix.inputs[2].default_value = 0.50
    rough_mix.inputs[3].default_value = 0.70
    nt.links.new(seam_mask.outputs[0], rough_mix.inputs['Factor'])
    nt.links.new(rough_mix.outputs[0], bsdf.inputs['Roughness'])

    bsdf.inputs['Metallic'].default_value = 0.0

    # ===== Bump: subtle grain from image luminance, recessed seams =====
    img_lum = nt.nodes.new('ShaderNodeRGBToBW')
    nt.links.new(img_tex.outputs['Color'], img_lum.inputs['Color'])

    seam_bump = nt.nodes.new('ShaderNodeMix')
    seam_bump.data_type = 'FLOAT'
    seam_bump.inputs[2].default_value = 0.0
    nt.links.new(img_lum.outputs['Val'], seam_bump.inputs[3])
    nt.links.new(seam_mask.outputs[0], seam_bump.inputs['Factor'])

    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.15
    nt.links.new(seam_bump.outputs[0], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


# ---------- Bake helpers ----------

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
    print(f'=== room-{ROOM_ID} woodgrain laminate ceiling bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()
    mat = make_woodgrain_laminate_material()
    plane = add_plane_for_bake('ceiling_plane', 1.0, 1.0, mat)
    bake_all_for(plane, f'ceiling/{SLUG}', SLUG)
    print(f'=== room-{ROOM_ID} woodgrain laminate ceiling bake done ===')
    print(f'Outputs in {ROOT_OUT}/ceiling/{SLUG}/')


if __name__ == '__main__' or '__main__' in __name__:
    main()
