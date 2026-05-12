"""
Bake per-surface ambient occlusion for the room-2 standalone scene in
ozu-test.html.

Why this exists: same reason as room-1 — the walls run on MeshBasicMaterial
with a locked paint colour (#afa299) so the four walls keep a uniform tint.
Path-traced AO baked offline into a per-surface map gives us corner darkening
WITHOUT shifting the paint colour. Middle of each wall stays #afa299,
corners darken via a multiply against the AO map.

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \
        ~/blender/blender-5.1.1-linux-x64/blender \
        --background \
        --python ozu-test/bake/bake_room2_ao.py

Output: ozu-test/room-2-textures/wall_ao/<surface>.png  (6 files, 1K each)

Differences from room-1:
- ac-wall hole position differs (room-2 narrow vertical privacy window is at
  y=[0.95, 1.80] vs room-1's y=[0.9, 1.9])
- closet-wall (x=0) has a 4-panel bi-fold occluder mounted on it, included
  here as a thin slab so the AO map captures shadow around the bi-folds
- hutch in the corner-ac-window area also occludes wall AO
The 4 walls + ceiling + floor dimensions match room-2's geometry shell in
ozu-test.html registerScene('room-2') at lines ~4779-5118.
"""

import bpy
import os
from mathutils import Vector

# --- room-2 constants (must match ozu-test.html registerScene('room-2')) ---
RW, RD, RH = 2.70, 2.70, 2.50

# Sliding window on window-wall (x=RW): hole at z=[0.405, 1.595], y=[0.85, 1.75]
W_WB = (0.405, 1.595, 0.85, 1.75)   # (u1, u2, v1, v2) where u=z, v=y

# Narrow vertical frosted window on ac-wall (z=RD): hole at x=[0.30, 0.56], y=[0.95, 1.80]
W_WD = (0.95, 1.80, 0.30, 0.56)     # (u1, u2, v1, v2) where u=y, v=x

# Bi-fold closet panel on closet-wall (x=0): z=[0.55, 1.95], y=[0.05, 2.30]
CLOSET = (0.55, 1.95, 0.05, 2.30, 0.04)   # z1, z2, y1, y2, depth into room

# Hutch in corner-ac-window: x=[2.10, 2.70], z=[2.30, 2.70], y=[0, 1.95]
HUTCH = (2.10, 2.70, 2.30, 2.70, 1.95)    # x1, x2, z1, z2, height

# --- bake settings ---
RES         = 1024
SAMPLES     = 256
AO_DISTANCE = 0.6
MARGIN      = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'room-2-textures', 'wall_ao')
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
    """Build a flat rectangle with optional rectangular hole.
    UV maps a (u_dir) → UV.x and b (v_dir) → UV.y, both in [0, 1]."""
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
            (0, 0), (u_len, 0), (u_len, v_len), (0, v_len),
            (h_u1, h_v1), (h_u2, h_v1),
            (h_u2, h_v2), (h_u1, h_v2),
        ]
        verts = [pt(*c) for c in coords]
        uvs   = [uv(*c) for c in coords]
        faces = [
            (0, 1, 5), (0, 5, 4),
            (1, 2, 6), (1, 6, 5),
            (2, 3, 7), (2, 7, 6),
            (3, 0, 4), (3, 4, 7),
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


def make_occluder_box(name, x1, x2, y1, y2, z1, z2):
    """Add a solid box as an AO occluder (no UV map needed — won't be baked)."""
    verts = [
        (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1),
        (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2),
    ]
    faces = [
        (0, 1, 2, 3), (4, 5, 6, 7),
        (0, 1, 5, 4), (2, 3, 7, 6),
        (1, 2, 6, 5), (3, 0, 4, 7),
    ]
    mesh = bpy.data.meshes.new(name + '_mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def setup_bake_image(obj, image):
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
    print('=== room-2 AO bake start ===')
    clear_scene()

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

    world = scene.world
    if world is None:
        world = bpy.data.worlds.new('World')
        scene.world = world
    world.light_settings.distance = AO_DISTANCE
    world.light_settings.ao_factor = 1.0

    scene.render.bake.margin = MARGIN
    scene.render.bake.use_pass_direct   = False
    scene.render.bake.use_pass_indirect = False
    scene.render.bake.use_pass_color    = False

    # 6 baked surfaces — wall holes match the room-2 ozu-test.html shell.
    surfaces = [
        ('floor',     (0,  0, 0),  (0,0,1),  (1,0,0),  RD, RW, None),
        ('ceiling',   (0, RH, 0),  (1,0,0),  (0,0,1),  RW, RD, None),
        ('wall_x0',   (0,  0, 0),  (0,1,0),  (0,0,1),  RH, RD, None),    # closet-wall (no hole — closet panel is occluder)
        ('wall_xW',   (RW, 0, 0),  (0,0,1),  (0,1,0),  RD, RH, W_WB),    # window-wall
        ('wall_z0',   (0,  0, 0),  (1,0,0),  (0,1,0),  RW, RH, None),    # entrance-wall (door is occluder, not hole)
        ('wall_zD',   (0,  0,RD),  (0,1,0),  (1,0,0),  RH, RW, W_WD),    # ac-wall
    ]

    objs = []
    for name, origin, u, v, ul, vl, hole in surfaces:
        objs.append(make_face(name, origin, u, v, ul, vl, hole))

    # Occluders — not baked, only contribute shadows to the surfaces above.
    cz1, cz2, cy1, cy2, cd = CLOSET
    make_occluder_box('closet_bifold', 0.0, cd, cy1, cy2, cz1, cz2)

    hx1, hx2, hz1, hz2, hh = HUTCH
    make_occluder_box('hutch', hx1, hx2, 0.0, hh, hz1, hz2)

    # Door panel (entrance-wall) — adds a thin shadow band around the doorway
    # opening on the entrance-wall AO.
    make_occluder_box('door_panel', 0.0, 0.8, 0.0, 2.0, 0.0, 0.04)

    print(f'Built {len(objs)} bake surfaces + occluders. Baking...')
    for obj in objs:
        out_path = os.path.join(OUT_DIR, obj.name + '.png')
        bake_one(obj, out_path)

    print('=== room-2 AO bake done ===')
    print(f'Outputs in {OUT_DIR}')


if __name__ == '__main__' or '__main__' in __name__:
    main()
