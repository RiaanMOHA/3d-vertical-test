"""
Bake per-surface Cycles lightmap (Combined pass) for the stairs-test scene.

Same geometry as bake_room_ao.py, plus the Kumamoto sun + corridor sky
proxy + LDK sky proxy lights matching the runtime rig in stairs-test.html.
Cycles "Combined" pass encodes Direct + Indirect + Diffuse + AO into a
single PNG per surface — replaces both the procedural fill and the AO
maps at runtime (lightmap subsumes AO).

Run on A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python stairs-test/bake/bake_room_lightmap.py

Output: stairs-test/textures/lightmap/{east_wall,west_wall_1f,north_wall,plank_ceiling,parapet,floor_2f}.png
"""

import bpy
import os
import math

RES = 1024
SAMPLES = 512
MARGIN = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'textures', 'lightmap'))
os.makedirs(OUT_DIR, exist_ok=True)

# === Stair geometry constants (must match stairs-test.html) ===
F1H = 2.50
TOTAL_RISERS = 13
RISE = F1H / TOTAL_RISERS
TREAD = 0.225
TREAD_T = 0.040
NOSING = 0.025
STAIR_W = 0.90
WT = 0.10
WB_Z0 = 5 * TREAD
WB_Z1 = WB_Z0 + 0.475
UF_X_EAST = 0.90
UF_X_WEST = UF_X_EAST - 6 * TREAD
SH_X0 = UF_X_WEST
SH_X1 = STAIR_W
SH_Z0 = WB_Z1 - 0.90
SH_Z1 = WB_Z1
CEIL_LOW = F1H
CEIL_HIGH = F1H + 1.95
BULKHEAD_Z = WB_Z0
PARAPET_H = 1.05
PARAPET_T = 0.06

# Each target surface is projected planarly along its inside-face normal axis,
# so the runtime can mirror the exact same projection on its BoxGeometry's
# uv2 attribute. SmartUV would generate auto-packed islands the runtime can't
# reproduce.
TARGET_AXES = {
    'east_wall':     'x',   # inside face faces -X
    'west_wall_1f':  'x',   # inside face faces +X
    'north_wall':    'z',   # inside face faces -Z
    'plank_ceiling': 'y',   # inside face faces -Y
    'parapet':       'z',   # inside face faces +Z
    'floor_2f':      'y',   # inside face faces +Y
}


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


def add_kumamoto_world():
    """Sky background — cool pale-blue tinted to match the Kumamoto 11 AM
    diffuse sky. Lower strength than direct sun (sun is added below as a
    SUN lamp). The shaft itself has no direct exposure to the sun, but the
    bright corridor on the other side of the top exit acts as the dominant
    indirect source — modelled below via a fake-sun positioned outside the
    top exit."""
    scene = bpy.context.scene
    world = scene.world or bpy.data.worlds.new('World')
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    bg = nt.nodes.new('ShaderNodeBackground')
    bg.inputs['Color'].default_value = (0.78, 0.85, 0.93, 1)   # cool sky
    bg.inputs['Strength'].default_value = 1.5
    out = nt.nodes.new('ShaderNodeOutputWorld')
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])


def add_kumamoto_lights():
    """Replicate stairs-test.html Phase 2 lighting rig in Cycles."""
    # Top-exit corridor sun — DirectionalLight equivalent (Cycles SUN lamp).
    # Cool tint, scattered indirect light.
    bpy.ops.object.light_add(type='SUN', location=(SH_X0 - 2.5, 3.5 + F1H, (SH_Z0 + SH_Z1) / 2))
    sun = bpy.context.active_object
    sun.name = 'corridor_sun'
    sun.data.energy = 6.0
    sun.data.color = (0.88, 0.91, 0.95)
    sun.data.angle = math.radians(8.0)        # soft penumbra
    # Aim the sun toward the L-bend area
    target = (0.40, 0.80, (SH_Z0 + SH_Z1) / 2)
    dx = target[0] - sun.location.x
    dy = target[1] - sun.location.y
    dz = target[2] - sun.location.z
    sun.rotation_euler = (
        math.atan2(math.sqrt(dx * dx + dz * dz), -dy),
        0,
        math.atan2(dz, dx),
    )

    # Top-exit area light — fills the corridor opening with diffuse skylight
    bpy.ops.object.light_add(type='AREA', location=(SH_X0 - 0.05, F1H + 0.85, (SH_Z0 + SH_Z1) / 2))
    top_area = bpy.context.active_object
    top_area.name = 'top_exit_area'
    top_area.data.shape = 'RECTANGLE'
    top_area.data.size = SH_Z1 - SH_Z0
    top_area.data.size_y = 1.60
    top_area.data.energy = 80.0
    top_area.data.color = (0.86, 0.90, 0.95)
    # Faces +X (into the shaft)
    top_area.rotation_euler = (math.pi / 2, 0, math.pi / 2)

    # Bottom-exit area light — LDK side
    bpy.ops.object.light_add(type='AREA', location=(STAIR_W / 2, 1.05, -0.05))
    bot_area = bpy.context.active_object
    bot_area.name = 'bottom_exit_area'
    bot_area.data.shape = 'RECTANGLE'
    bot_area.data.size = STAIR_W - 0.10
    bot_area.data.size_y = 1.80
    bot_area.data.energy = 40.0
    bot_area.data.color = (0.90, 0.93, 0.96)
    # Faces +Z (into the shaft)
    bot_area.rotation_euler = (math.pi / 2, 0, 0)


def make_paint_material(slug, color):
    mat = bpy.data.materials.new(slug)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = 0.85
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def add_box_xz(name, x0, x1, y0, y1, z0, z1, mat, is_target=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (x1 - x0, y1 - y0, z1 - z0)
    obj.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    bpy.ops.object.transform_apply(location=True, scale=True)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    obj['is_target'] = is_target
    return obj


def add_winder_wedge(name, verts2D, y_top, y_bot, mat):
    me = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    verts = []
    for v in verts2D:
        verts.append((v[0], y_bot, v[1]))
    for v in verts2D:
        verts.append((v[0], y_top, v[1]))
    faces = [
        (0, 1, 2),
        (5, 4, 3),
        (0, 3, 4, 1),
        (1, 4, 5, 2),
        (2, 5, 3, 0),
    ]
    me.from_pydata(verts, [], faces)
    me.update(calc_edges=True)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj


def planar_uv_project(obj, axis):
    """Project every face's UVs along `axis` (the inside-face normal). All 6
    faces of the box use the SAME planar projection, so the visible inside
    face maps cleanly to [0..1]^2. Hidden faces' UVs overlap — fine, they're
    not sampled at runtime.

    Runtime mirrors this in stairs-test.html by setting geometry.uv2 with the
    same planar projection on each wall mesh's vertex positions.
    """
    me = obj.data
    if not me.uv_layers:
        me.uv_layers.new(name='UVMap')
    uv = me.uv_layers.active.data
    verts = me.vertices
    if axis == 'x':
        a_lo = min(v.co.z for v in verts); a_hi = max(v.co.z for v in verts)
        b_lo = min(v.co.y for v in verts); b_hi = max(v.co.y for v in verts)
        def proj(co): return ((co.z - a_lo) / (a_hi - a_lo),
                              (co.y - b_lo) / (b_hi - b_lo))
    elif axis == 'y':
        a_lo = min(v.co.x for v in verts); a_hi = max(v.co.x for v in verts)
        b_lo = min(v.co.z for v in verts); b_hi = max(v.co.z for v in verts)
        def proj(co): return ((co.x - a_lo) / (a_hi - a_lo),
                              (co.z - b_lo) / (b_hi - b_lo))
    else:  # 'z'
        a_lo = min(v.co.x for v in verts); a_hi = max(v.co.x for v in verts)
        b_lo = min(v.co.y for v in verts); b_hi = max(v.co.y for v in verts)
        def proj(co): return ((co.x - a_lo) / (a_hi - a_lo),
                              (co.y - b_lo) / (b_hi - b_lo))
    for poly in me.polygons:
        for li in poly.loop_indices:
            v_idx = me.loops[li].vertex_index
            uv[li].uv = proj(verts[v_idx].co)


def add_bake_target_node(obj, image):
    mat = obj.data.materials[0]
    if not mat.use_nodes:
        mat.use_nodes = True
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


def bake_combined_for(obj, slug):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    planar_uv_project(obj, TARGET_AXES[slug])
    img = bpy.data.images.new(
        name=f'{slug}_lightmap',
        width=RES, height=RES,
        alpha=False, float_buffer=False,
    )
    img.colorspace_settings.name = 'sRGB'
    add_bake_target_node(obj, img)
    scene = bpy.context.scene
    scene.render.bake.use_pass_direct = True
    scene.render.bake.use_pass_indirect = True
    scene.render.bake.use_pass_color = True
    bpy.ops.object.bake(type='COMBINED', use_clear=True, margin=MARGIN)
    out_path = os.path.join(OUT_DIR, f'{slug}.png')
    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f'  -> {out_path}')


def build_geometry():
    """Build the stairs-test scene with proper Principled-BSDF materials so
    Cycles can compute the correct color bleed between surfaces."""
    matTaupe   = make_paint_material('matTaupe',   (0.71, 0.66, 0.58))
    matWhite   = make_paint_material('matWhite',   (0.95, 0.94, 0.90))
    matWood    = make_paint_material('matWood',    (0.90, 0.80, 0.64))
    matPlank   = make_paint_material('matPlank',   (0.86, 0.82, 0.74))
    matFloor1F = make_paint_material('matFloor1F', (0.79, 0.72, 0.60))
    targets = {}

    # Walls
    targets['east_wall']     = add_box_xz('east_wall',
                                          STAIR_W, STAIR_W + WT, 0, F1H + 2.5,
                                          0, WB_Z1, matTaupe, True)
    targets['west_wall_1f']  = add_box_xz('west_wall_1f',
                                          -WT, 0, 0, F1H, 0, WB_Z1, matTaupe, True)
    add_box_xz('west_wall_2f', SH_X0 - WT, SH_X0,
               F1H, F1H + 2.5, SH_Z0, SH_Z1, matTaupe)
    add_box_xz('north_wall_1f', 0, STAIR_W, 0, F1H, WB_Z1, WB_Z1 + WT, matTaupe)
    targets['north_wall']    = add_box_xz('north_wall_2f',
                                          SH_X0, STAIR_W, F1H, F1H + 2.5,
                                          WB_Z1, WB_Z1 + WT, matTaupe, True)
    add_box_xz('under_uf_south', SH_X0, 0, 0, F1H, SH_Z0 - WT, SH_Z0, matTaupe)
    add_box_xz('under_uf_west',  SH_X0 - WT, SH_X0, 0, F1H, SH_Z0, WB_Z1, matTaupe)

    # Ceilings
    CT = 0.04
    add_box_xz('low_ceiling', 0, STAIR_W, CEIL_LOW, CEIL_LOW + CT,
               0, BULKHEAD_Z, matTaupe)
    targets['plank_ceiling'] = add_box_xz('plank_ceiling',
                                          SH_X0, STAIR_W,
                                          CEIL_HIGH, CEIL_HIGH + CT,
                                          SH_Z0, SH_Z1, matPlank, True)
    add_box_xz('bulkhead_step', 0, STAIR_W, CEIL_LOW, CEIL_HIGH,
               BULKHEAD_Z, BULKHEAD_Z + CT, matTaupe)
    add_box_xz('low_ceiling_west', SH_X0, 0, F1H, F1H + CT,
               SH_Z0, SH_Z1, matTaupe)

    # Floors
    FLOOR_T = 0.02
    add_box_xz('floor_1f', 0, STAIR_W, -FLOOR_T, 0, 0, WB_Z1, matFloor1F)
    targets['floor_2f']      = add_box_xz('floor_2f',
                                          SH_X0 - 1.0, SH_X0,
                                          F1H - FLOOR_T, F1H,
                                          SH_Z0, SH_Z1, matFloor1F, True)

    # Parapet
    targets['parapet']       = add_box_xz('parapet_body',
                                          SH_X0, STAIR_W,
                                          F1H, F1H + PARAPET_H,
                                          SH_Z0 - PARAPET_T, SH_Z0, matWhite, True)
    add_box_xz('parapet_cap', SH_X0, STAIR_W,
               F1H + PARAPET_H, F1H + PARAPET_H + 0.030,
               SH_Z0 - PARAPET_T - 0.010, SH_Z0 + 0.010, matWhite)

    # Lower flight + winders + upper flight (occluders only)
    for i in range(1, 6):
        z0 = (i - 1) * TREAD
        y_top = i * RISE
        add_box_xz(f'tread_lower_{i}', 0, STAIR_W,
                   y_top - TREAD_T, y_top, z0 - NOSING, z0 + TREAD, matWood)
        add_box_xz(f'riser_lower_{i}', 0, STAIR_W,
                   y_top - RISE, y_top, z0, z0 + 0.020, matWood)
    add_winder_wedge('winder_6', [(0, WB_Z0), (STAIR_W, WB_Z0), (0, WB_Z1)],
                     6 * RISE, 6 * RISE - TREAD_T, matWood)
    add_winder_wedge('winder_7', [(STAIR_W, WB_Z0), (STAIR_W, WB_Z1), (0, WB_Z1)],
                     7 * RISE, 7 * RISE - TREAD_T, matWood)
    for i in range(8, 13):
        step_idx = i - 8
        x_right = UF_X_EAST - step_idx * TREAD
        x_left = x_right - TREAD
        y_top = i * RISE
        add_box_xz(f'tread_upper_{i}', x_left, x_right + NOSING,
                   y_top - TREAD_T, y_top, SH_Z0, SH_Z1, matWood)
        add_box_xz(f'riser_upper_{i}', x_right - 0.020, x_right,
                   y_top - RISE, y_top, SH_Z0, SH_Z1, matWood)
    add_box_xz('riser_upper_13',
               UF_X_EAST - 5 * TREAD - 0.020, UF_X_EAST - 5 * TREAD,
               12 * RISE, F1H, SH_Z0, SH_Z1, matWood)

    return targets


def main():
    print('=== stairs-test room lightmap bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_kumamoto_world()
    add_kumamoto_lights()
    targets = build_geometry()
    print(f'Geometry + lights built. {len(targets)} bake targets.')
    for slug, obj in targets.items():
        print(f'Baking lightmap for {slug}...')
        bake_combined_for(obj, slug)
    print('=== stairs-test room lightmap bake done ===')


if __name__ == '__main__' or '__main__' in __name__:
    main()
