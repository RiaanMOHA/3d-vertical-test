"""
Bake per-surface ambient occlusion for the stairs-test scene.

Builds the L-shape stair shaft in Blender with the same dimensions as
stairs-test.html (treads, winders, upper flight, walls, ceilings, parapet)
plus simple Cycles AO bake per wall surface. Output PNGs are loaded by
the runtime as MeshStandardMaterial.aoMap on each surface — gives corner
darkening in places the runtime lighting alone can't reach (under treads,
behind the parapet, in the L-bend pocket).

Run on A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \\
        ~/blender/blender-5.1.1-linux-x64/blender \\
        --background \\
        --python stairs-test/bake/bake_room_ao.py

Output: stairs-test/textures/ao/{east_wall,west_wall_1f,north_wall,plank_ceiling,parapet,floor_2f}.png
"""

import bpy
import os
import math

RES = 1024
SAMPLES = 256
MARGIN = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'textures', 'ao'))
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


def make_neutral_material():
    mat = bpy.data.materials.new('neutral')
    mat.use_nodes = True
    return mat


def add_box(name, x0, x1, y0, y1, z0, z1, mat, is_target=False):
    """BoxGeometry-equivalent, axis-aligned. Returns the mesh object."""
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


def add_box_xz(name, x0, x1, y0, y1, z0, z1, mat, is_target=False):
    """Add a box with explicit world-space corners (x, y, z dimensions). y is up."""
    return add_box(name, x0, x1, y0, y1, z0, z1, mat, is_target)


def add_winder_wedge(name, verts2D, y_top, y_bot, mat, is_target=False):
    """Triangular wedge in the X-Z plane, extruded along Y from y_bot to y_top.
    verts2D = [(x, z), (x, z), (x, z)] in CCW order looking down +Y."""
    me = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    verts = []
    for v in verts2D:
        verts.append((v[0], y_bot, v[1]))
    for v in verts2D:
        verts.append((v[0], y_top, v[1]))
    faces = [
        (0, 1, 2),                         # bottom face (CCW from +Y looking down? actually CW)
        (5, 4, 3),                         # top face (reverse of bottom for correct normals)
        (0, 3, 4, 1),                      # side 1
        (1, 4, 5, 2),                      # side 2
        (2, 5, 3, 0),                      # side 3
    ]
    me.from_pydata(verts, [], faces)
    me.update(calc_edges=True)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    obj['is_target'] = is_target
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


def bake_ao_for(obj, slug):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    planar_uv_project(obj, TARGET_AXES[slug])
    img = bpy.data.images.new(
        name=f'{slug}_ao',
        width=RES, height=RES,
        alpha=False, float_buffer=False,
    )
    img.colorspace_settings.name = 'Non-Color'
    add_bake_target_node(obj, img)
    scene = bpy.context.scene
    scene.render.bake.use_pass_direct = False
    scene.render.bake.use_pass_indirect = False
    bpy.ops.object.bake(type='AO', use_clear=True, margin=MARGIN)
    out_path = os.path.join(OUT_DIR, f'{slug}.png')
    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f'  -> {out_path}')


def build_geometry():
    """Build the full stairs-test scene as Blender objects. Returns a dict
    of {target_slug: target_object} for the surfaces we want to bake AO on."""
    mat = make_neutral_material()
    targets = {}

    # === Shaft walls (occluders + bake targets) ===
    targets['east_wall']     = add_box_xz('east_wall',
                                          STAIR_W, STAIR_W + WT,
                                          0, F1H + 2.5,
                                          0, WB_Z1, mat, True)
    targets['west_wall_1f']  = add_box_xz('west_wall_1f',
                                          -WT, 0,
                                          0, F1H,
                                          0, WB_Z1, mat, True)
    add_box_xz('west_wall_2f', SH_X0 - WT, SH_X0,
               F1H, F1H + 2.5,
               SH_Z0, SH_Z1, mat)
    add_box_xz('north_wall_1f', 0, STAIR_W,
               0, F1H,
               WB_Z1, WB_Z1 + WT, mat)
    targets['north_wall']    = add_box_xz('north_wall_2f',
                                          SH_X0, STAIR_W,
                                          F1H, F1H + 2.5,
                                          WB_Z1, WB_Z1 + WT, mat, True)
    add_box_xz('under_uf_south', SH_X0, 0, 0, F1H, SH_Z0 - WT, SH_Z0, mat)
    add_box_xz('under_uf_west',  SH_X0 - WT, SH_X0, 0, F1H, SH_Z0, WB_Z1, mat)

    # === Ceilings ===
    CT = 0.04
    add_box_xz('low_ceiling', 0, STAIR_W,
               CEIL_LOW, CEIL_LOW + CT,
               0, BULKHEAD_Z, mat)
    targets['plank_ceiling'] = add_box_xz('plank_ceiling',
                                          SH_X0, STAIR_W,
                                          CEIL_HIGH, CEIL_HIGH + CT,
                                          SH_Z0, SH_Z1, mat, True)
    add_box_xz('bulkhead_step', 0, STAIR_W,
               CEIL_LOW, CEIL_HIGH,
               BULKHEAD_Z, BULKHEAD_Z + CT, mat)
    add_box_xz('low_ceiling_west', SH_X0, 0,
               F1H, F1H + CT,
               SH_Z0, SH_Z1, mat)

    # === Floors ===
    FLOOR_T = 0.02
    add_box_xz('floor_1f', 0, STAIR_W,
               -FLOOR_T, 0,
               0, WB_Z1, mat)
    targets['floor_2f']      = add_box_xz('floor_2f',
                                          SH_X0 - 1.0, SH_X0,
                                          F1H - FLOOR_T, F1H,
                                          SH_Z0, SH_Z1, mat, True)

    # === Parapet ===
    targets['parapet']       = add_box_xz('parapet_body',
                                          SH_X0, STAIR_W,
                                          F1H, F1H + PARAPET_H,
                                          SH_Z0 - PARAPET_T, SH_Z0, mat, True)
    add_box_xz('parapet_cap',
               SH_X0, STAIR_W,
               F1H + PARAPET_H, F1H + PARAPET_H + 0.030,
               SH_Z0 - PARAPET_T - 0.010, SH_Z0 + 0.010, mat)

    # === Lower flight treads + risers (occluders) ===
    for i in range(1, 6):
        z0 = (i - 1) * TREAD
        y_top = i * RISE
        add_box_xz(f'tread_lower_{i}',
                   0, STAIR_W,
                   y_top - TREAD_T, y_top,
                   z0 - NOSING, z0 + TREAD, mat)
        add_box_xz(f'riser_lower_{i}',
                   0, STAIR_W,
                   y_top - RISE, y_top,
                   z0, z0 + 0.020, mat)

    # === Winders (occluders) ===
    add_winder_wedge('winder_6',
                     [(0, WB_Z0), (STAIR_W, WB_Z0), (0, WB_Z1)],
                     6 * RISE, 6 * RISE - TREAD_T, mat)
    add_winder_wedge('winder_7',
                     [(STAIR_W, WB_Z0), (STAIR_W, WB_Z1), (0, WB_Z1)],
                     7 * RISE, 7 * RISE - TREAD_T, mat)

    # === Upper flight treads + risers (occluders) ===
    for i in range(8, 13):
        step_idx = i - 8
        x_right = UF_X_EAST - step_idx * TREAD
        x_left = x_right - TREAD
        y_top = i * RISE
        add_box_xz(f'tread_upper_{i}',
                   x_left, x_right + NOSING,
                   y_top - TREAD_T, y_top,
                   SH_Z0, SH_Z1, mat)
        add_box_xz(f'riser_upper_{i}',
                   x_right - 0.020, x_right,
                   y_top - RISE, y_top,
                   SH_Z0, SH_Z1, mat)
    # Riser 13 (final, leading to 2F floor)
    add_box_xz('riser_upper_13',
               UF_X_EAST - 5 * TREAD - 0.020, UF_X_EAST - 5 * TREAD,
               12 * RISE, F1H,
               SH_Z0, SH_Z1, mat)

    return targets


def main():
    print('=== stairs-test room AO bake start ===')
    clear_scene()
    configure_cycles_optix()
    add_neutral_world()
    targets = build_geometry()
    print(f'Geometry built. {len(targets)} bake targets.')
    for slug, obj in targets.items():
        print(f'Baking AO for {slug}...')
        bake_ao_for(obj, slug)
    print('=== stairs-test room AO bake done ===')


if __name__ == '__main__' or '__main__' in __name__:
    main()
