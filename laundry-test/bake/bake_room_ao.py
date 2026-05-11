"""
laundry-test room-shell AO bake (Cycles + OptiX, A6000 GPU 1).

Mirrors the kitchen-test pattern. Builds 6 parametric room surfaces (floor,
ceiling, bath/door/vanity/window walls — vanity has no cutout, window-wall
has the high sliding-window cutout) at the same dimensions as
laundry-test.html, plus the washing machine as an occluder, then bakes AO
into per-surface PNGs.

Output: laundry-test/textures/ao/<surface>.png  (6 files, 1K each)

Run:
  CUDA_VISIBLE_DEVICES=1 ~/blender/blender-5.1.1-linux-x64/blender \\
    --background --python laundry-test/bake/bake_room_ao.py
"""

import os
import bpy

# === Room constants — must mirror laundry-test.html ===
ROOM_W = 1.80
ROOM_D = 2.70
ROOM_H = 2.50

# Window cutout on north wall (z = ROOM_D)
WIN_X0, WIN_X1 = 0.60, 1.20
WIN_Y0, WIN_Y1 = 1.50, 1.80

# Washing-machine occluder (Sharp ES-11K1)
WASHER_W = 0.595          # cabinet width along Z
WASHER_D = 0.732          # cabinet depth along X (front-to-back)
WASHER_H = 1.055
WASHER_CX = ROOM_W - WASHER_D / 2
WASHER_CZ = ROOM_D - WASHER_W / 2 - 0.05
# Bounds in (x0, x1, y0, y1, z0, z1)
WASHER_BOX = (
    WASHER_CX - WASHER_D / 2, WASHER_CX + WASHER_D / 2,
    0.0, WASHER_H,
    WASHER_CZ - WASHER_W / 2, WASHER_CZ + WASHER_W / 2,
)

RES         = 1024
SAMPLES     = 256
AO_DISTANCE = 0.6        # 60 cm — same as kitchen-test
MARGIN      = 8

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "textures", "ao"
)
os.makedirs(OUT_DIR, exist_ok=True)


def reset_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for db in (bpy.data.meshes, bpy.data.materials, bpy.data.images):
        for it in list(db):
            db.remove(it)


def configure_cycles():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.refresh_devices()
    print("=== Cycles devices ===")
    for d in prefs.devices:
        d.use = (d.type == 'OPTIX')
        print(f"  device: {d.name}  type={d.type}  use={d.use}")
    scene.world.light_settings.distance = AO_DISTANCE
    scene.world.light_settings.ao_factor = 1.0


def make_image(slug):
    img = bpy.data.images.new(name=slug, width=RES, height=RES,
                              alpha=False, float_buffer=False)
    img.colorspace_settings.name = 'Non-Color'
    img.filepath_raw = os.path.join(OUT_DIR, f"{slug}.png")
    img.file_format = 'PNG'
    return img


def make_target_material(name, image):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfDiffuse')
    img_node = nt.nodes.new('ShaderNodeTexImage')
    img_node.image = image
    img_node.select = True
    nt.nodes.active = img_node
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    nt.links.new(img_node.outputs['Color'], bsdf.inputs['Color'])
    return mat


def make_plain_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = (0.5, 0.5, 0.5, 1.0)
    return mat


def add_quad(name, verts, uvs, mat):
    mesh = bpy.data.meshes.new(name + '_mesh')
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()
    layer = mesh.uv_layers.new(name='UVMap')
    for li, vi in enumerate([0, 1, 2, 3]):
        layer.data[li].uv = uvs[vi]
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_polygon_with_hole(name, outer, hole, uvs_outer, uvs_hole, mat):
    """Quad with rectangular hole — 8 verts, 8 triangles around the hole."""
    verts = list(outer) + list(hole)
    faces = [
        (0, 1, 5), (0, 5, 4),
        (1, 2, 6), (1, 6, 5),
        (2, 3, 7), (2, 7, 6),
        (3, 0, 4), (3, 4, 7),
    ]
    mesh = bpy.data.meshes.new(name + '_mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    uvs_all = list(uvs_outer) + list(uvs_hole)
    layer = mesh.uv_layers.new(name='UVMap')
    li = 0
    for face in faces:
        for vi in face:
            layer.data[li].uv = uvs_all[vi]
            li += 1
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_occluder_box(name, x0, x1, y0, y1, z0, z1, mat):
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = ((x1 - x0), (y1 - y0), (z1 - z0))
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    return obj


def build_surfaces():
    surfaces = []   # list of (slug, obj, image)

    # === Floor: y=0, normal +y, u=+x, v=+z ===
    img = make_image('floor')
    mat = make_target_material('mat_floor', img)
    obj = add_quad(
        'floor',
        verts=[(0, 0, 0), (ROOM_W, 0, 0), (ROOM_W, 0, ROOM_D), (0, 0, ROOM_D)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append(('floor', obj, img))

    # === Ceiling: y=ROOM_H, normal -y (CCW seen from below) ===
    img = make_image('ceiling')
    mat = make_target_material('mat_ceiling', img)
    obj = add_quad(
        'ceiling',
        verts=[(0, ROOM_H, 0), (0, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    surfaces.append(('ceiling', obj, img))

    # === Door-wall (south, z=0, normal +z → faces into room) ===
    img = make_image('door_wall')
    mat = make_target_material('mat_door', img)
    obj = add_quad(
        'door_wall',
        verts=[(0, 0, 0), (0, ROOM_H, 0), (ROOM_W, ROOM_H, 0), (ROOM_W, 0, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    surfaces.append(('door_wall', obj, img))

    # === Bath-wall (west, x=0, normal +x) ===
    img = make_image('bath_wall')
    mat = make_target_material('mat_bath', img)
    obj = add_quad(
        'bath_wall',
        verts=[(0, 0, 0), (0, 0, ROOM_D), (0, ROOM_H, ROOM_D), (0, ROOM_H, 0)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append(('bath_wall', obj, img))

    # === Vanity-wall (east, x=ROOM_W, normal -x → faces into room) ===
    img = make_image('vanity_wall')
    mat = make_target_material('mat_vanity', img)
    # CCW seen from -x:
    # UV.x maps to z=ROOM_D→0 (front-to-back along the wall)
    # UV.y maps to y=0→ROOM_H (floor-to-ceiling)
    obj = add_quad(
        'vanity_wall',
        verts=[(ROOM_W, 0, ROOM_D), (ROOM_W, 0, 0), (ROOM_W, ROOM_H, 0), (ROOM_W, ROOM_H, ROOM_D)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append(('vanity_wall', obj, img))

    # === Window-wall (north, z=ROOM_D, normal -z → faces into room), with window hole ===
    img = make_image('window_wall')
    mat = make_target_material('mat_window', img)
    # CCW seen from -z (looking from inside room toward the north wall):
    # outer rectangle vertices in CCW order
    outer_v = [
        (ROOM_W, 0,      ROOM_D),    # bottom-right (in interior view)
        (0,     0,      ROOM_D),     # bottom-left
        (0,     ROOM_H, ROOM_D),     # top-left
        (ROOM_W, ROOM_H, ROOM_D),    # top-right
    ]
    # UVs: u from x=ROOM_W→0 (since interior view flips X), v from y=0→ROOM_H
    outer_uv = [(0, 0), (1, 0), (1, 1), (0, 1)]
    # Hole — vertices in same CCW order
    hole_v = [
        (WIN_X1, WIN_Y0, ROOM_D),
        (WIN_X0, WIN_Y0, ROOM_D),
        (WIN_X0, WIN_Y1, ROOM_D),
        (WIN_X1, WIN_Y1, ROOM_D),
    ]
    def wuv(x, y):
        return ((ROOM_W - x) / ROOM_W, y / ROOM_H)
    hole_uv = [wuv(WIN_X1, WIN_Y0), wuv(WIN_X0, WIN_Y0), wuv(WIN_X0, WIN_Y1), wuv(WIN_X1, WIN_Y1)]
    obj = add_polygon_with_hole(
        'window_wall',
        outer=outer_v, hole=hole_v,
        uvs_outer=outer_uv, uvs_hole=hole_uv,
        mat=mat,
    )
    surfaces.append(('window_wall', obj, img))

    return surfaces


def bake_one(obj, image):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    print(f"  baking {obj.name} -> {image.filepath_raw}")
    bpy.ops.object.bake(type='AO', use_clear=True, margin=MARGIN)
    image.save()


def main():
    print("=== laundry-test room-shell AO bake start ===")
    print(f"  room dims: {ROOM_W} x {ROOM_D} x {ROOM_H} m")
    print(f"  res={RES}, samples={SAMPLES}, distance={AO_DISTANCE} m")
    print(f"  output: {OUT_DIR}")

    reset_scene()
    configure_cycles()

    occluder_mat = make_plain_material('mat_occluder')

    # Add washing-machine occluder FIRST so it exists during all bakes
    add_occluder_box('washer', *WASHER_BOX, occluder_mat)

    surfaces = build_surfaces()
    print(f"Built {len(surfaces)} surfaces.")

    for slug, obj, img in surfaces:
        bake_one(obj, img)

    print("=== laundry-test room-shell AO bake done ===")


if __name__ == '__main__':
    main()
