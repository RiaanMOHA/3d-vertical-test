"""
kitchen-test room-shell AO bake (Cycles + OptiX, A6000 GPU 1)

Builds 5 parametric room surfaces (floor, ceiling, back wall, left wall,
right wall with window hole) at the same dimensions as kitchen-test.html,
bakes ambient occlusion via Cycles, saves grayscale PNGs to
kitchen-test/textures/ao/.

Mirrors the room-1 bake pattern at ozu-test/bake/bake_room1_ao.py.

Run:
  CUDA_VISIBLE_DEVICES=1 ~/blender/blender-5.1.1-linux-x64/blender \\
    --background --python kitchen-test/bake/bake_room_ao.py
"""

import os
import bpy

# === Constants — mirror kitchen-test.html ===
ROOM_W = 4.80   # x extent
ROOM_D = 3.50   # z extent
ROOM_H = 2.50   # y extent

# Window cutout on the right wall (x = ROOM_W). z + y range, in (z0, z1, y0, y1)
WIN = (0.70, 1.95, 1.10, 1.95)

# Bake settings
RES         = 1024
SAMPLES     = 256
AO_DISTANCE = 0.6       # 60 cm — closer = more contrast in contact shadows
MARGIN      = 8

# === Appliance / cabinet occluders (mirrored from kitchen-test.html) ===
# Each entry is (x0, x1, y0, y1, z0, z1) in metres.
# These are non-bake meshes added to the scene to BLOCK rays so the
# floor + walls show contact shadows + corner darkening near them.
OCCLUDERS = [
    # Fridge alcove (Panasonic, ~60 cm wide × 185 cm tall × 65 cm deep)
    (0.00, 0.60, 0.00, 1.85, 0.00, 0.65),
    # Base cabinet run + counter (one solid block from CAB1 to CAB4 end,
    # 88 cm tall including counter top, 62 cm deep)
    (0.60, 4.50, 0.00, 0.88, 0.00, 0.62),
    # Microwave on counter at CAB1 (Sharp RE-TS174, ~46 × 35 × 28 cm)
    (0.65, 1.11, 0.88, 1.16, 0.10, 0.45),
    # Wall cabinets + range hood + dish dryer (one continuous block above)
    (0.60, 4.50, 1.50, 2.20, 0.00, 0.38),
    # Range hood duct stub (cooktop, x=[1.20, 1.95]) up to ceiling
    (1.30, 1.85, 2.10, 2.50, 0.00, 0.35),
]

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "textures", "ao"
)
os.makedirs(OUT_DIR, exist_ok=True)


def reset_scene():
    """Wipe everything in the default scene."""
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        bpy.data.meshes.remove(m, do_unlink=True)
    for img in list(bpy.data.images):
        bpy.data.images.remove(img, do_unlink=True)
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat, do_unlink=True)


def configure_cycles():
    """Set Cycles + OptiX, tone mapping, world settings for AO."""
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

    # World AO settings (Blender 5.x — no use_ambient_occlusion flag)
    scene.world.light_settings.distance = AO_DISTANCE
    scene.world.light_settings.ao_factor = 1.0


def make_ao_image(slug):
    """Create a square baking image and return it."""
    img = bpy.data.images.new(name=slug, width=RES, height=RES, alpha=False, float_buffer=False)
    img.colorspace_settings.name = 'Non-Color'
    img.filepath_raw = os.path.join(OUT_DIR, f"{slug}.png")
    img.file_format = 'PNG'
    return img


def make_material_with_image_node(name, image):
    """Material whose ACTIVE image-texture node is the bake target."""
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


def add_quad(name, verts, uvs, mat):
    """Create a single-quad mesh from 4 vertices + 4 UVs (one face)."""
    mesh = bpy.data.meshes.new(name=name + "_mesh")
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()

    uv_layer = mesh.uv_layers.new(name='UVMap')
    for li, vi in enumerate([0, 1, 2, 3]):
        uv_layer.data[li].uv = uvs[vi]

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_polygon_with_hole(name, outer, hole, uvs_outer, uvs_hole, mat):
    """Create a flat surface as a triangulated rectangle with a rectangular hole.

    `outer` and `hole` are lists of 4 (x, y, z) tuples — both axis-aligned to
    the same plane. We build 8 triangles (4 strips around the hole).

    Vertex layout:
        outer[0..3]  = corners of outer rectangle (CCW from world view)
        hole[0..3]   = corners of hole          (same CCW order)
    UVs are passed in matching order.

    Triangles: for each side of the hole, two triangles linking outer corners
    to the corresponding hole corners.
    """
    verts = list(outer) + list(hole)            # 8 verts: outer 0..3, hole 4..7
    faces = [
        (0, 1, 5), (0, 5, 4),    # bottom strip
        (1, 2, 6), (1, 6, 5),    # right strip
        (2, 3, 7), (2, 7, 6),    # top strip
        (3, 0, 4), (3, 4, 7),    # left strip
    ]
    mesh = bpy.data.meshes.new(name=name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    uvs_all = list(uvs_outer) + list(uvs_hole)
    uv_layer = mesh.uv_layers.new(name='UVMap')
    li = 0
    for face in faces:
        for vi in face:
            uv_layer.data[li].uv = uvs_all[vi]
            li += 1

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_occluder_box(name, x0, x1, y0, y1, z0, z1):
    """Add a non-bake-target box that exists only to block AO rays."""
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = ((x1 - x0), (y1 - y0), (z1 - z0))
    bpy.ops.object.transform_apply(scale=True)
    # Plain unlit material (any material works for occluders — bake reads only geometry)
    mat = bpy.data.materials.new(name=f"mat_{name}")
    mat.use_nodes = False
    mat.diffuse_color = (0.5, 0.5, 0.5, 1.0)
    obj.data.materials.append(mat)
    return obj


def build_room():
    """Build 5 surfaces (bake targets) + N occluder boxes (kitchen appliances/
    cabinets). Each bake target gets its own image + material. Other meshes in
    the scene act as AO occluders."""
    surfaces = []   # list of (slug, obj, image)

    # === Occluders FIRST (so they appear in the scene before any bake) ===
    for i, (x0, x1, y0, y1, z0, z1) in enumerate(OCCLUDERS):
        add_occluder_box(f"occ_{i}", x0, x1, y0, y1, z0, z1)
    print(f"Added {len(OCCLUDERS)} occluder boxes.")

    # === Floor: y=0, normal +y, u=+x (room width), v=+z (room depth) ===
    img = make_ao_image('floor')
    mat = make_material_with_image_node('mat_floor', img)
    obj = add_quad(
        'floor',
        verts=[(0, 0, 0), (ROOM_W, 0, 0), (ROOM_W, 0, ROOM_D), (0, 0, ROOM_D)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append(('floor', obj, img))

    # === Ceiling: y=ROOM_H, normal -y. CCW seen from BELOW (i.e. CW from above) ===
    img = make_ao_image('ceiling')
    mat = make_material_with_image_node('mat_ceiling', img)
    obj = add_quad(
        'ceiling',
        verts=[(0, ROOM_H, 0), (0, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    surfaces.append(('ceiling', obj, img))

    # === Back wall: z=0, normal +z (faces into room, where +z is toward user) ===
    # Wait — three.js +z toward user, so z=0 is at the BACK of the room,
    # back wall faces +z (forward into room).
    # CCW seen from +z direction (room interior looking at back wall).
    img = make_ao_image('back_wall')
    mat = make_material_with_image_node('mat_back', img)
    obj = add_quad(
        'back_wall',
        verts=[(0, 0, 0), (0, ROOM_H, 0), (ROOM_W, ROOM_H, 0), (ROOM_W, 0, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    surfaces.append(('back_wall', obj, img))

    # === Left wall: x=0, normal +x (faces into room) ===
    # CCW seen from +x.
    img = make_ao_image('left_wall')
    mat = make_material_with_image_node('mat_left', img)
    obj = add_quad(
        'left_wall',
        verts=[(0, 0, 0), (0, 0, ROOM_D), (0, ROOM_H, ROOM_D), (0, ROOM_H, 0)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append(('left_wall', obj, img))

    # === Right wall: x=ROOM_W, normal -x (faces into room), with window hole ===
    z0, z1, y0, y1 = WIN
    # CCW seen from -x (room interior looking at right wall).
    # Outer rectangle vertices, in same CCW order:
    outer_v = [
        (ROOM_W, 0,      ROOM_D),     # bottom-right (in room view)
        (ROOM_W, 0,      0),           # bottom-left
        (ROOM_W, ROOM_H, 0),           # top-left
        (ROOM_W, ROOM_H, ROOM_D),     # top-right
    ]
    outer_uv = [(0, 0), (1, 0), (1, 1), (0, 1)]   # u from z=ROOM_D->0, v from y=0->ROOM_H
    # Hole rectangle vertices, in CCW order matching outer ordering:
    hole_v = [
        (ROOM_W, y0, z1),   # near bottom-z=z1 corner -> matches outer[0] direction
        (ROOM_W, y0, z0),
        (ROOM_W, y1, z0),
        (ROOM_W, y1, z1),
    ]
    # Hole UVs: same u/v formula as outer
    def ruv(z, y):
        return ((ROOM_D - z) / ROOM_D, y / ROOM_H)
    hole_uv = [ruv(z1, y0), ruv(z0, y0), ruv(z0, y1), ruv(z1, y1)]
    img = make_ao_image('right_wall')
    mat = make_material_with_image_node('mat_right', img)
    obj = add_polygon_with_hole(
        'right_wall',
        outer=outer_v, hole=hole_v,
        uvs_outer=outer_uv, uvs_hole=hole_uv,
        mat=mat,
    )
    surfaces.append(('right_wall', obj, img))

    return surfaces


def bake_one(obj, image):
    """Set this object as active+selected, then bake AO into its image."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    print(f"  baking {obj.name} -> {image.filepath_raw}")
    bpy.ops.object.bake(type='AO', use_clear=True, margin=MARGIN)
    image.save()


def main():
    print("=== kitchen-test room-shell AO bake start ===")
    print(f"  room dims: {ROOM_W} x {ROOM_D} x {ROOM_H} m")
    print(f"  res={RES}, samples={SAMPLES}, distance={AO_DISTANCE} m, margin={MARGIN}")
    print(f"  output: {OUT_DIR}")

    reset_scene()
    configure_cycles()

    surfaces = build_room()
    print(f"Built {len(surfaces)} surfaces.")

    for slug, obj, img in surfaces:
        bake_one(obj, img)

    print("=== kitchen-test room-shell AO bake done ===")


if __name__ == '__main__':
    main()
