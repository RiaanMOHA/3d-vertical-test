"""
laundry-test washing-machine drum hex-hole NORMAL map bake (Cycles + OptiX, A6000 GPU 1).

Sculpt-then-bake workflow per the May 2026 research-brief technique 2: model
a high-poly cylinder with REAL hex-pattern indentations as actual geometry,
then bake its tangent-space normals onto a low-poly target cylinder's UVs.

Beats the runtime procedural canvas-derived normal because the holes have
true rim curvature — better light response at glancing angles and proper
dark-edge highlight on each hole's circumference.

Output: laundry-test/textures/normal/drum_hex.png  (1024 × 256, ~30 sec)

Run:
  CUDA_VISIBLE_DEVICES=1 ~/blender/blender-5.1.1-linux-x64/blender \\
    --background --python laundry-test/bake/bake_drum_normal.py
"""

import os
import math
import bpy
import bmesh

# === Drum dimensions (mirror laundry-test.html makeWashingMachine) ===
DRUM_R = 0.171      # 0.180 * 0.95 — runtime drum radius
DRUM_L = 0.260      # runtime drum length
LOW_SEGS = 96       # ↑ from runtime 48 — softer silhouette in the low-poly bake target
LOW_LEN_SEGS = 4
HIGH_SEGS = 384     # high-poly circumference — needs to resolve each hole at ≥4 verts wide
HIGH_LEN_SEGS = 96

# === Hex hole pattern ===
HOLE_R = 0.0040     # 4 mm hole radius
HOLE_DEPTH = 0.0009 # 0.9 mm indent depth
PITCH = 0.0110      # 11 mm centre-to-centre spacing

# === Bake settings ===
TEX_W = 1024
TEX_H = 256
SAMPLES = 64        # tangent normal bakes are noise-free at low samples
MARGIN = 12

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "textures", "normal"
)
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, "drum_hex.png")


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
    scene.cycles.use_denoising = False
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.refresh_devices()
    print("=== Cycles devices ===")
    for d in prefs.devices:
        d.use = (d.type == 'OPTIX')
        print(f"  device: {d.name}  type={d.type}  use={d.use}")


def cylinder_uv_layout(obj):
    """Manual UV unwrap matching three.js CylinderGeometry: U around the
    circumference (0..1), V along length (0..1, V=0 at -L/2 end)."""
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    uv_layer = bm.loops.layers.uv.verify()
    for face in bm.faces:
        for loop in face.loops:
            v = loop.vert
            theta = math.atan2(v.co.y, v.co.x)
            u = (theta + math.pi) / (2 * math.pi)   # 0..1 around
            v_uv = (v.co.z + DRUM_L / 2) / DRUM_L  # 0..1 along
            loop[uv_layer].uv = (u, v_uv)
    bm.to_mesh(me)
    bm.free()


def make_low_poly():
    """Low-poly target cylinder (matches runtime topology, simpler UVs)."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=LOW_SEGS, radius=DRUM_R, depth=DRUM_L,
        end_fill_type='NOTHING',
    )
    obj = bpy.context.active_object
    obj.name = 'drum_low'

    # Subdivide along length for cleaner cage
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    for _ in range(int(math.log2(LOW_LEN_SEGS))):
        bpy.ops.mesh.subdivide()
    bpy.ops.object.mode_set(mode='OBJECT')

    cylinder_uv_layout(obj)
    bpy.ops.object.shade_smooth()
    return obj


def make_high_poly():
    """High-poly cylinder with real hex-pattern indentations."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=HIGH_SEGS, radius=DRUM_R, depth=DRUM_L,
        end_fill_type='NOTHING',
    )
    obj = bpy.context.active_object
    obj.name = 'drum_high'

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    for _ in range(int(math.log2(HIGH_LEN_SEGS))):
        bpy.ops.mesh.subdivide()
    bpy.ops.object.mode_set(mode='OBJECT')

    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)

    row_pitch = PITCH * math.sqrt(3) / 2
    z_min = -DRUM_L / 2
    n_rows = max(1, int(DRUM_L / row_pitch))
    circ = 2 * math.pi * DRUM_R
    n_per_row = max(1, round(circ / PITCH))
    angle_pitch = 2 * math.pi / n_per_row

    print(f"  hex grid: {n_rows} rows × {n_per_row} cols/row = {n_rows * n_per_row} holes")

    bm.verts.ensure_lookup_table()
    indented = 0
    for v in bm.verts:
        # Skip cap-edge verts (no hex pattern there — stays smooth at the lip)
        if abs(v.co.z - DRUM_L / 2) < 1e-5 or abs(v.co.z + DRUM_L / 2) < 1e-5:
            continue

        theta_v = math.atan2(v.co.y, v.co.x) % (2 * math.pi)
        z_v = v.co.z
        row_idx = int((z_v - z_min) / row_pitch)
        if row_idx < 0 or row_idx >= n_rows:
            continue

        best_d = float('inf')
        # Check current hex cell + 8 neighbours (handles boundary cases)
        for dr in (-1, 0, 1):
            ri = row_idx + dr
            if ri < 0 or ri >= n_rows:
                continue
            z_c = z_min + row_pitch * (ri + 0.5)
            offset = (angle_pitch / 2) if (ri % 2 == 1) else 0.0
            col_v = (theta_v - offset) / angle_pitch
            col_idx = int(round(col_v))
            for dc in (-1, 0, 1):
                ci = (col_idx + dc) % n_per_row
                theta_c = (angle_pitch * ci + offset) % (2 * math.pi)
                dtheta = (theta_v - theta_c + math.pi) % (2 * math.pi) - math.pi
                arc_d = abs(dtheta) * DRUM_R
                axial_d = z_v - z_c
                d = math.sqrt(arc_d * arc_d + axial_d * axial_d)
                if d < best_d:
                    best_d = d

        if best_d < HOLE_R:
            # Smoothstep falloff — full depth at centre, tangent to surface at edge
            t = best_d / HOLE_R
            falloff = (1.0 - t * t) ** 2
            r_in = math.sqrt(v.co.x * v.co.x + v.co.y * v.co.y)
            new_r = r_in - HOLE_DEPTH * falloff
            scale = new_r / r_in if r_in > 0 else 1.0
            v.co.x *= scale
            v.co.y *= scale
            indented += 1

    bm.to_mesh(me)
    bm.free()
    print(f"  indented {indented} verts")

    bpy.ops.object.shade_smooth()
    return obj


def make_target_image():
    img = bpy.data.images.new(
        name='drum_normal', width=TEX_W, height=TEX_H,
        alpha=False, float_buffer=False,
    )
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


def bake(low, high, image):
    bpy.ops.object.select_all(action='DESELECT')
    high.select_set(True)
    low.select_set(True)
    bpy.context.view_layer.objects.active = low  # active = bake target

    print(f"  baking selected→active ({high.name} → {low.name})")
    bpy.ops.object.bake(
        type='NORMAL',
        normal_space='TANGENT',
        use_selected_to_active=True,
        cage_extrusion=0.005,
        margin=MARGIN,
        use_clear=True,
    )
    image.save()


def main():
    print("=== drum hex normal bake start ===")
    print(f"  output: {OUT_PATH}")
    reset_scene()
    configure_cycles()

    low = make_low_poly()
    high = make_high_poly()

    img = make_target_image()
    mat = make_target_material(img)
    low.data.materials.append(mat)

    bake(low, high, img)
    print(f"  -> wrote {OUT_PATH}")
    print("=== drum hex normal bake done ===")


if __name__ == '__main__':
    main()
