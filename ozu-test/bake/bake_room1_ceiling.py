"""
Bake PBR maps for the whitewashed reclaimed-pine plank ceiling shared
across rooms 1-4.

In all 4 photo sets (ozu-test/interior-images/room-{1,2,3,4}/), the
ceiling reads as the SAME material: heavily distressed lime-washed
pine boards where:
  - the warm pine grain shows through ~30-40% of the surface
  - the rest is patchy off-white lime-wash with long brush streaks
  - planks have hard dark seams between them
  - per-plank colour variance is large (some planks ~all wood,
    some ~all paint)

Procedural Cycles material:
  - 8 planks per tile, stacked along V (so planks run along U)
  - Per-plank random hash for paint coverage + wood tint
  - Pine grain via stretched Wave along plank length
  - Whitewash mask = Voronoi (large patches) + stretched Noise (streaks)
    + fine Noise (wear pattern), thresholded via ColorRamp
  - Seam pattern: smooth_step on distance to nearest plank boundary
  - Roughness: pine ~0.72, paint ~0.92
  - Bump combines grain + paint texture; seams are recessed

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python ozu-test/bake/bake_room1_ceiling.py

Output:
  ozu-test/room-1-textures/ceiling/whitewashed_pine/
      whitewashed_pine_{albedo,normal,roughness,ao}.png  (2048^2 each)

4 PNGs total. ~4 min on A6000.
"""

import bpy
import os

RES     = 2048
SAMPLES = 256
MARGIN  = 8

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


def make_whitewashed_pine_material(name='whitewashed_pine'):
    """Heavily distressed reclaimed pine planks with worn-off lime-wash.

    Photo-matched against ozu-test/interior-images/room-1/corner-ac-entrance/
    frames 02-05 (clearest ceiling shots). Key features:
      - ~50% of surface shows warm sienna pine wood through worn paint
      - Long horizontal grain streaks ALONG plank length (very directional)
      - Pronounced dark seams between planks (1-2px effective gap)
      - Subtle per-plank variation (each plank reads similar, not stark)
      - Paint where present is warm off-white with grey-brown streak overlay
    """
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)

    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')

    tc = nt.nodes.new('ShaderNodeTexCoord')

    # ===== Plank grid =====
    N_PLANKS = 8
    plank_map = nt.nodes.new('ShaderNodeMapping')
    plank_map.inputs['Scale'].default_value = (1.0, float(N_PLANKS), 1.0)
    nt.links.new(tc.outputs['UV'], plank_map.inputs['Vector'])

    sep_uv = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(plank_map.outputs['Vector'], sep_uv.inputs['Vector'])

    fract_v = nt.nodes.new('ShaderNodeMath')
    fract_v.operation = 'FRACT'
    nt.links.new(sep_uv.outputs['Y'], fract_v.inputs[0])

    plank_idx = nt.nodes.new('ShaderNodeMath')
    plank_idx.operation = 'FLOOR'
    nt.links.new(sep_uv.outputs['Y'], plank_idx.inputs[0])

    inv_v = nt.nodes.new('ShaderNodeMath')
    inv_v.operation = 'SUBTRACT'
    inv_v.inputs[0].default_value = 1.0
    nt.links.new(fract_v.outputs[0], inv_v.inputs[1])

    near_seam = nt.nodes.new('ShaderNodeMath')
    near_seam.operation = 'MINIMUM'
    nt.links.new(fract_v.outputs[0], near_seam.inputs[0])
    nt.links.new(inv_v.outputs[0], near_seam.inputs[1])

    seam_dist = nt.nodes.new('ShaderNodeMath')
    seam_dist.operation = 'MULTIPLY'
    seam_dist.inputs[1].default_value = 2.0
    nt.links.new(near_seam.outputs[0], seam_dist.inputs[0])

    # Pronounced seam: smooth band 0..0.018 (~1.8% of plank height) for
    # a thicker visible gap matching the photos.
    seam_mask = nt.nodes.new('ShaderNodeMapRange')
    seam_mask.interpolation_type = 'SMOOTHSTEP'
    seam_mask.inputs['From Min'].default_value = 0.0
    seam_mask.inputs['From Max'].default_value = 0.018
    seam_mask.inputs['To Min'].default_value = 0.0
    seam_mask.inputs['To Max'].default_value = 1.0
    nt.links.new(seam_dist.outputs[0], seam_mask.inputs['Value'])

    # ===== Pine wood grain — fine horizontal streaks along plank =====
    # Stretched noise produces long horizontal streaks (along U / plank length).
    grain_map = nt.nodes.new('ShaderNodeMapping')
    grain_map.inputs['Scale'].default_value = (4.0, 60.0, 1.0)
    nt.links.new(tc.outputs['UV'], grain_map.inputs['Vector'])

    grain_noise = nt.nodes.new('ShaderNodeTexNoise')
    grain_noise.inputs['Scale'].default_value = 2.5
    grain_noise.inputs['Detail'].default_value = 5.0
    grain_noise.inputs['Roughness'].default_value = 0.6
    nt.links.new(grain_map.outputs['Vector'], grain_noise.inputs['Vector'])

    # Pine colour: warm sienna mixed with darker walnut via grain. KEEP
    # this saturated — the photos show deep brown wood, not pale pine.
    pine_mix = nt.nodes.new('ShaderNodeMix')
    pine_mix.data_type = 'RGBA'
    pine_mix.inputs['A'].default_value = (0.46, 0.30, 0.17, 1)   # warm sienna
    pine_mix.inputs['B'].default_value = (0.26, 0.15, 0.07, 1)   # dark walnut
    nt.links.new(grain_noise.outputs['Fac'], pine_mix.inputs['Factor'])

    # Per-plank tint variation — kept VERY subtle (each plank looks similar)
    plank_hash = nt.nodes.new('ShaderNodeTexWhiteNoise')
    plank_hash.noise_dimensions = '1D'
    nt.links.new(plank_idx.outputs[0], plank_hash.inputs['W'])

    plank_tint = nt.nodes.new('ShaderNodeMix')
    plank_tint.data_type = 'RGBA'
    plank_tint.inputs['A'].default_value = (0.92, 0.90, 0.88, 1)
    plank_tint.inputs['B'].default_value = (1.00, 0.97, 0.93, 1)
    nt.links.new(plank_hash.outputs['Value'], plank_tint.inputs['Factor'])

    pine_per_plank = nt.nodes.new('ShaderNodeMix')
    pine_per_plank.data_type = 'RGBA'
    pine_per_plank.blend_type = 'MULTIPLY'
    pine_per_plank.inputs['Factor'].default_value = 1.0
    nt.links.new(pine_mix.outputs['Result'], pine_per_plank.inputs['A'])
    nt.links.new(plank_tint.outputs['Result'], pine_per_plank.inputs['B'])

    # ===== Whitewash mask — BOLD patches with chaotic edges =====
    # Use medium-scale Voronoi (organic patches) as primary mask, modulated by
    # streaks for directional flow. Hard threshold for high contrast — paint
    # is either THERE or NOT, with chaotic transitions.

    # Voronoi with HEAVILY ANISOTROPIC coords — cells stretch along U so paint
    # patches look like long brush-stroke regions, not round dalmatian spots.
    voro_map = nt.nodes.new('ShaderNodeMapping')
    voro_map.inputs['Scale'].default_value = (0.4, 3.5, 1.0)
    nt.links.new(tc.outputs['UV'], voro_map.inputs['Vector'])

    voro = nt.nodes.new('ShaderNodeTexVoronoi')
    voro.voronoi_dimensions = '2D'
    voro.feature = 'F1'
    voro.inputs['Scale'].default_value = 3.5
    nt.links.new(voro_map.outputs['Vector'], voro.inputs['Vector'])

    # Long horizontal streaks — dominant brush-stroke pattern along plank.
    streak_map = nt.nodes.new('ShaderNodeMapping')
    streak_map.inputs['Scale'].default_value = (0.6, 25.0, 1.0)
    nt.links.new(tc.outputs['UV'], streak_map.inputs['Vector'])

    long_streak = nt.nodes.new('ShaderNodeTexNoise')
    long_streak.inputs['Scale'].default_value = 2.5
    long_streak.inputs['Detail'].default_value = 5.0
    long_streak.inputs['Roughness'].default_value = 0.65
    nt.links.new(streak_map.outputs['Vector'], long_streak.inputs['Vector'])

    # Mix: streaks dominate (0.7), voronoi just modulates boundary shape (0.3).
    paint_mix = nt.nodes.new('ShaderNodeMix')
    paint_mix.data_type = 'FLOAT'
    paint_mix.inputs['Factor'].default_value = 0.30
    nt.links.new(long_streak.outputs['Fac'], paint_mix.inputs[2])
    nt.links.new(voro.outputs['Distance'], paint_mix.inputs[3])

    # Threshold ~50% paint coverage with soft transitions for natural fade
    paint_ramp = nt.nodes.new('ShaderNodeValToRGB')
    nt.links.new(paint_mix.outputs[0], paint_ramp.inputs['Fac'])
    el = paint_ramp.color_ramp.elements
    el[0].position = 0.35
    el[0].color = (0, 0, 0, 1)
    el[1].position = 0.62
    el[1].color = (1, 1, 1, 1)

    # Fine wear noise — only used for bump + paint colour variation
    fine_map = nt.nodes.new('ShaderNodeMapping')
    fine_map.inputs['Scale'].default_value = (8.0, 25.0, 1.0)
    nt.links.new(tc.outputs['UV'], fine_map.inputs['Vector'])

    fine_noise = nt.nodes.new('ShaderNodeTexNoise')
    fine_noise.inputs['Scale'].default_value = 5.0
    fine_noise.inputs['Detail'].default_value = 5.0
    nt.links.new(fine_map.outputs['Vector'], fine_noise.inputs['Vector'])

    # ===== Paint colour — warm cream mottled toward grey-brown =====
    paint_color_mix = nt.nodes.new('ShaderNodeMix')
    paint_color_mix.data_type = 'RGBA'
    paint_color_mix.inputs['A'].default_value = (0.95, 0.91, 0.83, 1)  # cream
    paint_color_mix.inputs['B'].default_value = (0.75, 0.68, 0.58, 1)  # weathered grey-brown
    nt.links.new(long_streak.outputs['Fac'], paint_color_mix.inputs['Factor'])

    # ===== Mix wood ↔ paint via paint mask =====
    wood_or_paint = nt.nodes.new('ShaderNodeMix')
    wood_or_paint.data_type = 'RGBA'
    nt.links.new(paint_ramp.outputs['Color'], wood_or_paint.inputs['Factor'])
    nt.links.new(pine_per_plank.outputs['Result'], wood_or_paint.inputs['A'])
    nt.links.new(paint_color_mix.outputs['Result'], wood_or_paint.inputs['B'])

    # ===== Seam: very dark gap between planks =====
    seam_color = nt.nodes.new('ShaderNodeMix')
    seam_color.data_type = 'RGBA'
    seam_color.inputs['A'].default_value = (0.06, 0.04, 0.02, 1)
    nt.links.new(seam_mask.outputs[0], seam_color.inputs['Factor'])
    nt.links.new(wood_or_paint.outputs['Result'], seam_color.inputs['B'])

    nt.links.new(seam_color.outputs['Result'], bsdf.inputs['Base Color'])

    # ===== Roughness: pine 0.78, paint 0.92 =====
    rough_mix = nt.nodes.new('ShaderNodeMix')
    rough_mix.data_type = 'FLOAT'
    rough_mix.inputs[2].default_value = 0.78
    rough_mix.inputs[3].default_value = 0.92
    nt.links.new(paint_ramp.outputs['Color'], rough_mix.inputs['Factor'])
    nt.links.new(rough_mix.outputs[0], bsdf.inputs['Roughness'])

    bsdf.inputs['Metallic'].default_value = 0.0

    # ===== Bump: grain + paint texture, recessed seams =====
    bump_combo = nt.nodes.new('ShaderNodeMix')
    bump_combo.data_type = 'FLOAT'
    bump_combo.inputs['Factor'].default_value = 0.4
    nt.links.new(grain_noise.outputs['Fac'], bump_combo.inputs[2])
    nt.links.new(fine_noise.outputs['Fac'], bump_combo.inputs[3])

    seam_bump = nt.nodes.new('ShaderNodeMix')
    seam_bump.data_type = 'FLOAT'
    seam_bump.inputs[2].default_value = 0.0
    nt.links.new(bump_combo.outputs[0], seam_bump.inputs[3])
    nt.links.new(seam_mask.outputs[0], seam_bump.inputs['Factor'])

    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.55
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
    print('=== whitewashed pine ceiling bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()
    mat = make_whitewashed_pine_material()
    plane = add_plane_for_bake('ceiling_plane', 2.0, 2.0, mat)
    bake_all_for(plane, 'ceiling/whitewashed_pine', 'whitewashed_pine')
    print('=== whitewashed pine ceiling bake done ===')
    print(f'Outputs in {ROOT_OUT}/ceiling/whitewashed_pine/')


if __name__ == '__main__' or '__main__' in __name__:
    main()
