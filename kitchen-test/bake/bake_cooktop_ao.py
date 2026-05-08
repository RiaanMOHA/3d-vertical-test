"""
kitchen-test cooktop AO bake (Cycles + OptiX, A6000 GPU 1).

Bakes a high-resolution AO map for the gas-hob top plate. All 3 burners,
their cast-iron grates, chrome caps, dark heads, spark electrodes, and the
perforated grease-catcher slats are placed as occluders so the bake captures:

  - 4 shadow stripes per burner from each grate prong
  - circular contact-shadow ring under each burner cap
  - linear shadows under each vent slat
  - faint shadow under the spark electrode pins

Output: kitchen-test/textures/ao/cooktop_top.png  (2048², grayscale, ~25 sec)

Run:
  CUDA_VISIBLE_DEVICES=1 ~/blender/blender-5.1.1-linux-x64/blender \\
    --background --python kitchen-test/bake/bake_cooktop_ao.py
"""

import os
import math
import bpy

# === Geometry constants — must match kitchen-test.html makeCooktop() ===
CT_W      = 0.59
CT_D      = 0.52
TOP_T     = 0.012     # top-plate thickness
TOP_Y     = TOP_T / 2 # top-plate top surface (cooktop-local coords)

# Burner layout: front-left big, back-center small, front-right medium
BURNERS = [
    {'dx': -0.165, 'dz': +0.075, 'gr': 0.085, 'hr': 0.030},
    {'dx':  0.000, 'dz': -0.115, 'gr': 0.067, 'hr': 0.024},
    {'dx': +0.150, 'dz': +0.045, 'gr': 0.075, 'hr': 0.027},
]

# Grate prong dimensions
PRONG_LEN_OFFSET = -0.005   # inner end overlap with cap
PRONG_W = 0.012
PRONG_H = 0.018

# Grease-catcher (perforated vent) at the back of the top plate
VENT_W = CT_W * 0.92
VENT_D = 0.055
VENT_Z = -CT_D / 2 + 0.014 + VENT_D / 2  # cooktop-local Z (back is -Z)

# Bake settings
RES         = 2048
SAMPLES     = 512
AO_DISTANCE = 0.12     # 12 cm — keeps shadows tight & punchy
MARGIN      = 12

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "textures", "ao"
)
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "cooktop_top.png")


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


def make_image():
    img = bpy.data.images.new(name='cooktop_top', width=RES, height=RES,
                              alpha=False, float_buffer=False)
    img.colorspace_settings.name = 'Non-Color'
    img.filepath_raw = OUT_PATH
    img.file_format = 'PNG'
    return img


def make_target_material(image):
    """Diffuse + image-texture node so Cycles knows where to write the bake."""
    mat = bpy.data.materials.new(name='mat_target')
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


def make_plain_material(name, color=(0.5, 0.5, 0.5, 1.0)):
    """Any material works for occluders — bake reads only geometry."""
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color
    return mat


def add_target_plane(mat):
    """Flat plane at TOP_Y representing the visible top surface of the enamel.
    Vertices and UVs aligned so UV (0,0) = (x=-CT_W/2, z=-CT_D/2) corner."""
    verts = [
        (-CT_W / 2, TOP_Y, -CT_D / 2),     # back-left  → UV (0, 0)
        ( CT_W / 2, TOP_Y, -CT_D / 2),     # back-right → UV (1, 0)
        ( CT_W / 2, TOP_Y,  CT_D / 2),     # front-right → UV (1, 1)
        (-CT_W / 2, TOP_Y,  CT_D / 2),     # front-left  → UV (0, 1)
    ]
    uvs = [(0, 0), (1, 0), (1, 1), (0, 1)]
    mesh = bpy.data.meshes.new('top_plate_mesh')
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()
    layer = mesh.uv_layers.new(name='UVMap')
    for li, vi in enumerate([0, 1, 2, 3]):
        layer.data[li].uv = uvs[vi]
    obj = bpy.data.objects.new('top_plate', mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_box(name, x0, x1, y0, y1, z0, z1, mat):
    cx = (x0 + x1) / 2; cy = (y0 + y1) / 2; cz = (z0 + z1) / 2
    sx = x1 - x0; sy = y1 - y0; sz = z1 - z0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    return obj


def add_cylinder(name, x, y, z, radius, height, axis='Y', mat=None):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=height, vertices=24, location=(x, y, z)
    )
    obj = bpy.context.active_object
    obj.name = name
    if axis == 'Y':
        obj.rotation_euler[0] = math.pi / 2
        bpy.ops.object.transform_apply(rotation=True)
    if mat:
        obj.data.materials.append(mat)
    return obj


def add_rotated_box(name, cx, cy, cz, sx, sy, sz, ry, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    obj.rotation_euler[1] = ry
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    obj.data.materials.append(mat)
    return obj


def build_occluders(mat):
    """Add all geometry that should cast AO onto the top plate."""
    # === Burners ===
    for bi, b in enumerate(BURNERS):
        bx, bz = b['dx'], b['dz']
        # Cap (chrome cylinder)
        add_cylinder(f'cap_{bi}', bx, TOP_Y + 0.005, bz,
                     radius=b['hr'], height=0.012, axis='Y', mat=mat)
        # Head (small dark cylinder on top of cap)
        add_cylinder(f'head_{bi}', bx, TOP_Y + 0.014, bz,
                     radius=b['hr'] * 0.85, height=0.008, axis='Y', mat=mat)
        # 4 grate prongs
        prong_len = b['gr']
        prong_y = TOP_Y + 0.014  # raised above top
        for ai, ang in enumerate([0, math.pi / 2, math.pi, 3 * math.pi / 2]):
            offset = b['hr'] + prong_len / 2 + PRONG_LEN_OFFSET
            cx = bx + math.cos(ang) * offset
            cz = bz + math.sin(ang) * offset
            add_rotated_box(
                f'prong_{bi}_{ai}',
                cx, prong_y, cz,
                prong_len, PRONG_H, PRONG_W,
                -ang,    # rotate around Y to point in direction `ang`
                mat
            )
        # 2 spark electrodes
        add_cylinder(f'pin1_{bi}', bx + 0.004, TOP_Y + 0.015, bz,
                     radius=0.0022, height=0.014, axis='Y', mat=mat)
        add_cylinder(f'pin2_{bi}', bx - 0.004, TOP_Y + 0.013, bz,
                     radius=0.0022, height=0.010, axis='Y', mat=mat)

    # === Grease-catcher slats (9 thin slats forming the perforated grille) ===
    slat_gap = VENT_D / 11
    for i in range(9):
        z_center = (VENT_Z - VENT_D / 2) + slat_gap * (i + 1)
        add_box(
            f'slat_{i}',
            -VENT_W / 2 * 0.96, +VENT_W / 2 * 0.96,
            TOP_Y + 0.0015, TOP_Y + 0.005,
            z_center - slat_gap * 0.275, z_center + slat_gap * 0.275,
            mat
        )


def bake(target_obj, image):
    bpy.ops.object.select_all(action='DESELECT')
    target_obj.select_set(True)
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.bake(type='AO', use_clear=True, margin=MARGIN)
    image.save()


def main():
    print("=== kitchen-test cooktop AO bake start ===")
    print(f"  res={RES}, samples={SAMPLES}, distance={AO_DISTANCE} m")
    print(f"  output: {OUT_PATH}")

    reset_scene()
    configure_cycles()

    img = make_image()
    target_mat = make_target_material(img)
    occluder_mat = make_plain_material('mat_occluder', (0.4, 0.4, 0.4, 1.0))

    target = add_target_plane(target_mat)
    build_occluders(occluder_mat)

    bake(target, img)

    print(f"  -> wrote {OUT_PATH}")
    print("=== kitchen-test cooktop AO bake done ===")


if __name__ == '__main__':
    main()
