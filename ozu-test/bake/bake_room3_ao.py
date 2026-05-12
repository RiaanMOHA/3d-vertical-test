"""
Bake per-surface ambient occlusion for the room-3 standalone scene in
ozu-test.html.

Room-3 is the 6帖 SE 2F room. Walls run on MeshBasicMaterial with locked
paint colour (#afa299); AO maps add corner darkening WITHOUT shifting the
paint colour.

Run on the idle A6000 (GPU 1):

    CUDA_VISIBLE_DEVICES=1 \
        ~/blender/blender-5.1.1-linux-x64/blender \
        --background \
        --python ozu-test/bake/bake_room3_ao.py

Output: ozu-test/room-3-textures/wall_ao/<surface>.png  (6 files, 1K each)

Differences from room-1/room-2:
- Larger room (2.7 × 3.6 vs 2.7 × 2.7)
- AC + large sliding window share the window-wall (z=RD)
- Shelving on closet-wall acts as occluder (visible darkening on wall behind)
- Door + coat rack on entrance-wall
- The bed (head against window-wall) is included as an occluder so corners
  near the bed-head pick up the right shadow density
"""

import bpy
import os
from mathutils import Vector

# --- room-3 constants (must match ozu-test.html registerScene('room-3')) ---
RW, RD, RH = 2.70, 3.60, 2.50

# Sliding window on window-wall (z=RD): hole at x=[0.60, 2.10], y=[0.85, 1.75]
W_WD = (0.60, 2.10, 0.85, 1.75)     # (u1, u2, v1, v2) where u=x, v=y

# Narrow frosted window on frosted-wall (x=RW): hole at z=[0.40, 0.66], y=[0.95, 1.80]
W_WB = (0.40, 0.66, 0.95, 1.80)     # (u1, u2, v1, v2) where u=z, v=y

# Shelving on closet-wall (x=0): x=[0.05, 0.45], z=[0.30, 1.85], y=[0, 1.55]
SHELF = (0.05, 0.45, 0.0, 1.55, 0.30, 1.85)

# Bed in middle: x=[0.85, 1.85], y=[0, 0.50], z=[1.60, 3.55]
BED = (0.85, 1.85, 0.0, 0.50, 1.60, 3.55)

# AC on window-wall: x=[0.20, 0.90], y=[1.85, 2.10], z=[RD-0.10, RD]
AC = (0.20, 0.90, 1.85, 2.10, RD - 0.10, RD)

RES         = 1024
SAMPLES     = 256
AO_DISTANCE = 0.6
MARGIN      = 8

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.normpath(
    os.path.join(SCRIPT_DIR, '..', 'room-3-textures', 'wall_ao')
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
    print('=== room-3 AO bake start ===')
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

    surfaces = [
        ('floor',     (0,  0, 0),  (0,0,1),  (1,0,0),  RD, RW, None),
        ('ceiling',   (0, RH, 0),  (1,0,0),  (0,0,1),  RW, RD, None),
        ('wall_x0',   (0,  0, 0),  (0,1,0),  (0,0,1),  RH, RD, None),       # closet-wall
        ('wall_xW',   (RW, 0, 0),  (0,0,1),  (0,1,0),  RD, RH, W_WB),       # frosted-wall
        ('wall_z0',   (0,  0, 0),  (1,0,0),  (0,1,0),  RW, RH, None),       # entrance-wall
        ('wall_zD',   (0,  0,RD),  (0,1,0),  (1,0,0),  RH, RW, W_WD),       # window-wall
    ]

    objs = []
    for name, origin, u, v, ul, vl, hole in surfaces:
        objs.append(make_face(name, origin, u, v, ul, vl, hole))

    # Occluders.
    sx1, sx2, sy1, sy2, sz1, sz2 = SHELF
    make_occluder_box('shelf', sx1, sx2, sy1, sy2, sz1, sz2)

    bx1, bx2, by1, by2, bz1, bz2 = BED
    make_occluder_box('bed', bx1, bx2, by1, by2, bz1, bz2)

    ax1, ax2, ay1, ay2, az1, az2 = AC
    make_occluder_box('ac', ax1, ax2, ay1, ay2, az1, az2)

    # Door panel.
    make_occluder_box('door_panel', 0.95, 1.75, 0.0, 2.0, 0.0, 0.04)

    print(f'Built {len(objs)} bake surfaces + occluders. Baking...')
    for obj in objs:
        out_path = os.path.join(OUT_DIR, obj.name + '.png')
        bake_one(obj, out_path)

    print('=== room-3 AO bake done ===')


if __name__ == '__main__' or '__main__' in __name__:
    main()
