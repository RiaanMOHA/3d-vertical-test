"""
Bake per-surface ambient occlusion for the room-1 standalone scene in
ozu-test.html.

Why this exists: the room-1 walls are deliberately on MeshBasicMaterial
with a locked paint colour (#afa299). That keeps the colour uniform but
removes all corner shading, so the four walls read as one flat painted
card folded into a box. We want corner darkening WITHOUT shifting the
paint colour. Path-traced AO baked offline into a per-surface map gives
us exactly that: middles stay #afa299, corners darken via a multiply.

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \
        ~/blender/blender-5.1.1-linux-x64/blender \
        --background \
        --python ozu-test/bake/bake_room1_ao.py

Output: ozu-test/room-1-textures/wall_ao/<surface>.png  (6 files, 1K each)

The bake builds a thin parametric replica of the room interior — 4 walls
+ ceiling + floor, normals pointing inward, two of the walls have window
holes. Each surface is then baked individually with the others present as
AO occluders. The room dimensions and window cutouts must stay in sync
with ozu-test.html lines ~3014-3015 and ~3270-3279.
"""

import bpy
import os
import sys
from mathutils import Vector

# --- room-1 constants (must match ozu-test.html registerScene('room-1')) ---
RW, RD, RH = 2.70, 2.70, 2.50

# Window in window-wall (x = RW): hole at z in [0.405, 1.595], y in [0.85, 1.75]
W_WB = (0.405, 1.595, 0.85, 1.75)   # (u1, u2, v1, v2) where u=z, v=y

# Window in ac-wall (z = RD): hole at x in [0.30, 0.56], y in [0.9, 1.9]
W_WD = (0.9, 1.9, 0.30, 0.56)       # (u1, u2, v1, v2) where u=y, v=x

# --- bake settings ---
RES         = 1024     # texture resolution per surface
SAMPLES     = 256      # Cycles AO samples
AO_DISTANCE = 0.6      # metres of contact-darkening reach
MARGIN      = 8        # bake margin pixels (for filtering bleed)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'room-1-textures', 'wall_ao')
)
os.makedirs(OUT_DIR, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for db in (bpy.data.meshes, bpy.data.materials,
               bpy.data.images, bpy.data.textures, bpy.data.node_groups):
        for it in list(db):
            db.remove(it)


def make_face(name, origin, u_dir, v_dir, u_len, v_len, hole=None):
    """Build a flat rectangle. Triangulation gives normal = u_dir x v_dir.

    UV: a along u_dir maps to UV.x; b along v_dir maps to UV.y, both in
    [0, 1]. So UV (0,0) is at origin, UV (1,1) is at origin + u + v.

    hole = (u1, u2, v1, v2) cuts a rectangular hole in u-v space.
    """
    o = Vector(origin)
    u = Vector(u_dir).normalized()
    v = Vector(v_dir).normalized()

    def pt(a, b):
        return tuple(o + u * a + v * b)

    def uv(a, b):
        return (a / u_len, b / v_len)

    if hole is None:
        coords = [(0, 0), (u_len, 0), (u_len, v_len), (0, v_len)]
        verts  = [pt(*c) for c in coords]
        uvs    = [uv(*c) for c in coords]
        faces  = [(0, 1, 2), (0, 2, 3)]
    else:
        h_u1, h_u2, h_v1, h_v2 = hole
        coords = [
            (0, 0), (u_len, 0), (u_len, v_len), (0, v_len),       # 0..3 outer
            (h_u1, h_v1), (h_u2, h_v1),                           # 4, 5 hole bottom
            (h_u2, h_v2), (h_u1, h_v2),                           # 6, 7 hole top
        ]
        verts = [pt(*c) for c in coords]
        uvs   = [uv(*c) for c in coords]
        faces = [
            (0, 1, 5), (0, 5, 4),    # bottom strip
            (1, 2, 6), (1, 6, 5),    # right strip
            (2, 3, 7), (2, 7, 6),    # top strip
            (3, 0, 4), (3, 4, 7),    # left strip
        ]

    mesh = bpy.data.meshes.new(name + '_mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.uv_layers.new(name='UVMap')
    uvl = mesh.uv_layers.active.data
    for poly in mesh.polygons:
        for li, vi in zip(poly.loop_indices, poly.vertices):
            uvl[li].uv = uvs[vi]
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def setup_bake_image(obj, image):
    """Attach a fresh material with an Image Texture node so Cycles can
    write the bake into the supplied image."""
    mat = bpy.data.materials.new(obj.name + '_mat')
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    bsdf = nt.nodes.new('ShaderNodeBsdfDiffuse')
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = image
    tex.select = True
    nt.nodes.active = tex
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat


def bake_one(obj, out_path):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    img = bpy.data.images.new(
        name=obj.name + '_ao',
        width=RES, height=RES,
        alpha=False, float_buffer=False,
    )
    img.colorspace_settings.name = 'Non-Color'
    setup_bake_image(obj, img)

    bpy.ops.object.bake(type='AO', use_clear=True, margin=MARGIN)

    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f'  -> {out_path}')


def main():
    print('=== room-1 AO bake start ===')
    clear_scene()

    scene = bpy.context.scene

    # Cycles + GPU (OptiX) — CUDA_VISIBLE_DEVICES=1 outside should already
    # restrict us to the idle A6000.
    scene.render.engine = 'CYCLES'
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.refresh_devices()
    for d in prefs.devices:
        d.use = (d.type == 'OPTIX')
        print(f'  device: {d.name}  type={d.type}  use={d.use}')
    scene.cycles.device = 'GPU'
    scene.cycles.samples = SAMPLES

    # World AO — Cycles bake type 'AO' uses these fall-off settings.
    # In Blender 5.x the legacy `use_ambient_occlusion` toggle was removed;
    # AO is always available for the bake operator. We only set distance
    # (rays past this hit nothing → no contribution → wall-middles stay
    # bright; shorter distance = tighter contact darkening at corners).
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new('World')
        scene.world = world
    world.light_settings.distance = AO_DISTANCE
    world.light_settings.ao_factor = 1.0

    # Bake settings — only AO contribution, no light, no colour.
    scene.render.bake.margin = MARGIN
    scene.render.bake.use_pass_direct   = False
    scene.render.bake.use_pass_indirect = False
    scene.render.bake.use_pass_color    = False

    # 6 surfaces. All inward-facing. (origin, u_dir, v_dir, u_len, v_len, hole)
    # u_dir x v_dir == inward normal — verified per surface.
    surfaces = [
        ('floor',     (0,  0, 0),  (0,0,1),  (1,0,0),  RD, RW, None),
        ('ceiling',   (0, RH, 0),  (1,0,0),  (0,0,1),  RW, RD, None),
        ('wall_x0',   (0,  0, 0),  (0,1,0),  (0,0,1),  RH, RD, None),
        ('wall_xW',   (RW, 0, 0),  (0,0,1),  (0,1,0),  RD, RH, W_WB),
        ('wall_z0',   (0,  0, 0),  (1,0,0),  (0,1,0),  RW, RH, None),
        ('wall_zD',   (0,  0,RD),  (0,1,0),  (1,0,0),  RH, RW, W_WD),
    ]

    objs = []
    for name, origin, u, v, ul, vl, hole in surfaces:
        objs.append(make_face(name, origin, u, v, ul, vl, hole))

    print(f'Built {len(objs)} surfaces. Baking...')
    for obj in objs:
        out_path = os.path.join(OUT_DIR, obj.name + '.png')
        bake_one(obj, out_path)

    print('=== room-1 AO bake done ===')
    print(f'Outputs in {OUT_DIR}')


if __name__ == '__main__' or '__main__' in __name__:
    main()
