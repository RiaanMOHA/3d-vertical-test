"""
laundry-test washing-machine front-face AO bake (Cycles + OptiX, A6000 GPU 1).

Bakes a high-resolution AO map for the FRONT face of the Sharp ES-11K1
cabinet, with all the door / drum / agitator / lint-hatch / control-panel
geometry placed as occluders. The bake captures contact shadows around the
chrome bezel, behind the recessed door plate, around the lint hatch, behind
the SHARP logo, and along the cabinet seams.

Output: laundry-test/textures/ao/washer_front.png  (2048², grayscale, ~30 sec)

The bake operates in CABINET-LOCAL coordinates:
    x = 0 is the front face (visible to the room)
    +x extends INTO the cabinet (toward the back wall)
    y from 0 (floor) to h (top)
    z = 0 at the cabinet's centerline; z spans ±w/2

Run:
  CUDA_VISIBLE_DEVICES=1 ~/blender/blender-5.1.1-linux-x64/blender \\
    --background --python laundry-test/bake/bake_washer_ao.py
"""

import os
import math
import bpy

# === Geometry constants — must mirror laundry-test.html makeWashingMachine() ===
W = 0.595
D = 0.732
H = 1.055

DOOR_R_OUTER = 0.230
DOOR_R_INNER = 0.205
DOOR_R_GLASS = 0.180
DOOR_Y       = H * 0.50

# Bake settings
RES         = 2048
SAMPLES     = 512
AO_DISTANCE = 0.10      # 10 cm — tight contact shadows
MARGIN      = 12

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "textures", "ao"
)
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "washer_front.png")


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
    img = bpy.data.images.new(name='washer_front', width=RES, height=RES,
                              alpha=False, float_buffer=False)
    img.colorspace_settings.name = 'Non-Color'
    img.filepath_raw = OUT_PATH
    img.file_format = 'PNG'
    return img


def make_target_material(image):
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


def make_plain_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = (0.5, 0.5, 0.5, 1.0)
    return mat


def add_target_plane(mat):
    """Front face plane at x=0, normal -X (faces the viewer / room).

    UV mapping:
      UV (0, 0) = (y=0, z=-W/2)  → bottom-back-left of front face
      UV (1, 1) = (y=H, z=+W/2)  → top-front-right of front face
    """
    verts = [
        (0, 0, -W / 2),     # vert 0 → UV (0, 0)   [bottom, z=-W/2]
        (0, H, -W / 2),     # vert 1 → UV (0, 1)   [top, z=-W/2]
        (0, H, +W / 2),     # vert 2 → UV (1, 1)   [top, z=+W/2]
        (0, 0, +W / 2),     # vert 3 → UV (1, 0)   [bottom, z=+W/2]
    ]
    uvs = [(0, 0), (0, 1), (1, 1), (1, 0)]
    mesh = bpy.data.meshes.new('front_face_mesh')
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.update()
    layer = mesh.uv_layers.new(name='UVMap')
    for li, vi in enumerate([0, 1, 2, 3]):
        layer.data[li].uv = uvs[vi]
    obj = bpy.data.objects.new('front_face', mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_box(name, x0, x1, y0, y1, z0, z1, mat):
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (x1 - x0, y1 - y0, z1 - z0)
    bpy.ops.object.transform_apply(scale=True)
    obj.data.materials.append(mat)
    return obj


def add_cylinder(name, x, y, z, radius, length, axis='X', mat=None):
    """Cylinder oriented along the given axis (default X)."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=length, vertices=32, location=(x, y, z)
    )
    obj = bpy.context.active_object
    obj.name = name
    if axis == 'X':
        obj.rotation_euler[1] = math.pi / 2
    elif axis == 'Z':
        obj.rotation_euler[0] = math.pi / 2
    bpy.ops.object.transform_apply(rotation=True)
    if mat:
        obj.data.materials.append(mat)
    return obj


def add_torus(name, x, y, z, major_r, minor_r, axis='X', mat=None):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_r, minor_radius=minor_r, location=(x, y, z),
        major_segments=64, minor_segments=18,
    )
    obj = bpy.context.active_object
    obj.name = name
    if axis == 'X':
        obj.rotation_euler[1] = math.pi / 2
    bpy.ops.object.transform_apply(rotation=True)
    if mat:
        obj.data.materials.append(mat)
    return obj


def build_occluders(mat):
    # === Door assembly === (sits at x ~ 0..0.025, slightly proud of front face)
    add_torus('door_bezel', 0.005, DOOR_Y, 0, DOOR_R_OUTER, 0.010, 'X', mat)
    add_cylinder('door_plate', 0.012, DOOR_Y, 0, DOOR_R_OUTER - 0.008, 0.008, 'X', mat)
    add_torus('door_inner_rim', 0.014, DOOR_Y, 0, DOOR_R_INNER, 0.005, 'X', mat)
    add_cylinder('door_glass', 0.030, DOOR_Y, 0, DOOR_R_GLASS, 0.040, 'X', mat)

    # === Drum cavity behind the door ===
    add_cylinder('drum', 0.150, DOOR_Y, 0, DOOR_R_GLASS * 0.95, 0.260, 'X', mat)
    add_cylinder('drum_back', 0.275, DOOR_Y, 0, DOOR_R_GLASS * 0.95, 0.005, 'X', mat)

    # === Agitator (3 arms + hub) ===
    arm_len = DOOR_R_GLASS * 0.88
    for i in range(3):
        ang = (i / 3) * math.pi * 2
        cx = 0.105
        cy = DOOR_Y + math.sin(ang) * (arm_len * 0.20)
        cz = math.cos(ang) * (arm_len * 0.20)
        add_box(
            f'arm_{i}',
            cx - 0.017, cx + 0.017,
            cy - 0.014, cy + 0.014,
            cz - arm_len / 2, cz + arm_len / 2,
            mat
        )
    add_cylinder('agitator_hub', 0.105, DOOR_Y, 0, 0.030, 0.040, 'X', mat)

    # === Bottom-right lint-filter hatch (proud of front face) ===
    add_box(
        'lint_hatch',
        0.001, 0.006,
        0.030, 0.180,
        W / 2 - 0.080 - 0.015, W / 2 - 0.080 + 0.015,
        mat
    )

    # === Hinge nub (left side of door) ===
    add_cylinder('hinge', 0.012, DOOR_Y, -DOOR_R_OUTER - 0.012, 0.014, 0.050, 'Z', mat)

    # === Top control panel (slim sloped block at the top-front) ===
    add_box(
        'control_panel',
        0.010, 0.150,
        H - 0.030, H - 0.005,
        -W / 2 + 0.030, W / 2 - 0.030,
        mat
    )


def bake(target_obj, image):
    bpy.ops.object.select_all(action='DESELECT')
    target_obj.select_set(True)
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.bake(type='AO', use_clear=True, margin=MARGIN)
    image.save()


def main():
    print("=== laundry-test washer-front AO bake start ===")
    print(f"  res={RES}, samples={SAMPLES}, distance={AO_DISTANCE} m")
    print(f"  output: {OUT_PATH}")

    reset_scene()
    configure_cycles()

    img = make_image()
    target_mat = make_target_material(img)
    occluder_mat = make_plain_material('mat_occluder')

    target = add_target_plane(target_mat)
    build_occluders(occluder_mat)

    bake(target, img)

    print(f"  -> wrote {OUT_PATH}")
    print("=== laundry-test washer-front AO bake done ===")


if __name__ == '__main__':
    main()
