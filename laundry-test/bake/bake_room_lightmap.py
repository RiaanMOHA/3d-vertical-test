"""
laundry-test room-shell LIGHTMAP bake (Cycles + OptiX, A6000 GPU 1).

Path-traces the FULL lighting solution into a per-surface texture (Combined =
Direct + Indirect + Diffuse + AO) for every wall, the floor, and the ceiling.

Why this beats the prior AO bake: a lightmap encodes COLOR, not just darkness.
The brick vanity-wall casts warm-tinted bounce light onto the floor; the
window-side daylight tints the bath-wall blue; corners get true contact shadow
plus indirect fill — none of which an aoMap or runtime IBL alone can produce.

Output: laundry-test/textures/lightmap/<surface>.png  (6 files, 1K, color)

Run:
  CUDA_VISIBLE_DEVICES=1 ~/blender/blender-5.1.1-linux-x64/blender \\
    --background --python laundry-test/bake/bake_room_lightmap.py
"""

import os
import math
import bpy

# === Room — must mirror laundry-test.html ===
ROOM_W = 1.80
ROOM_D = 2.70
ROOM_H = 2.50

WIN_X0, WIN_X1 = 0.60, 1.20
WIN_Y0, WIN_Y1 = 1.50, 1.80

# Washing-machine occluder
WASHER_W = 0.595
WASHER_D = 0.732
WASHER_H = 1.055
WASHER_CX = ROOM_W - WASHER_D / 2
WASHER_CZ = ROOM_D - WASHER_W / 2 - 0.05
WASHER_BOX = (
    WASHER_CX - WASHER_D / 2, WASHER_CX + WASHER_D / 2,
    0.0, WASHER_H,
    WASHER_CZ - WASHER_W / 2, WASHER_CZ + WASHER_W / 2,
)

# Surface diffuse colors (linear sRGB) — match the JS runtime materials
COL_FLOOR  = (0.62, 0.50, 0.32, 1.0)   # warm light oak
COL_WALL   = (0.58, 0.55, 0.50, 1.0)   # taupe paint
COL_BRICK  = (0.78, 0.74, 0.68, 1.0)   # cool grey-white brick
COL_CEIL   = (0.91, 0.89, 0.85, 1.0)   # warm off-white
COL_WASHER = (0.92, 0.93, 0.95, 1.0)   # white cabinet

# Bake settings
RES         = 1024
SAMPLES     = 512
MARGIN      = 12

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "textures", "lightmap"
)
os.makedirs(OUT_DIR, exist_ok=True)


def reset_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for db in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.lights):
        for it in list(db):
            db.remove(it)


def configure_cycles():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    # Per May-2026 best practice (Agent 1 research): for STATIC lightmap
    # bakes prefer OIDN over OptiX denoiser — OIDN gives cleaner static
    # output without OptiX's temporal-tuned bias. OIDN 2.4 (GPU) is current.
    try:
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        scene.cycles.denoising_prefilter = 'ACCURATE'
    except (TypeError, AttributeError):
        pass   # older Blender — falls back to default denoiser
    scene.cycles.bake_type = 'COMBINED'
    scene.render.bake.use_pass_direct = True
    scene.render.bake.use_pass_indirect = True
    scene.render.bake.use_pass_diffuse = True
    scene.render.bake.use_pass_glossy = False
    scene.render.bake.use_pass_transmission = False
    scene.render.bake.margin = MARGIN

    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.refresh_devices()
    print("=== Cycles devices ===")
    for d in prefs.devices:
        d.use = (d.type == 'OPTIX')
        print(f"  device: {d.name}  type={d.type}  use={d.use}")


def configure_world():
    """Sky-Texture (Nishita) world background — physically-grounded sky model.
    Per May-2026 Cycles best practice (Cycles 5.1 manual, BlenderArtists
    interior threads): for a small north-facing window, Sky Texture in the
    world + a Light Portal at the window aperture is more accurate than a
    sun lamp + colored background. The portal gives MIS for sky sampling
    through the small opening, killing the speckle that a closed-room bake
    otherwise gets at low sample counts."""
    world = bpy.context.scene.world
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')
    sky = nt.nodes.new('ShaderNodeTexSky')
    sky.sky_type = 'NISHITA'
    # Kumamoto (lat 32.8°N), sunny spring, 11:00 AM JST → solar azimuth ≈ 160°
    # (SSE, 20° east of south), elevation ≈ 60°. Per CLAUDE.md interior-
    # render daylight rule. Sky_texture sun_rotation is measured from south
    # going clockwise viewed from above; +160°-180° = -20° → +20° in Blender
    # convention. Tune if the runtime feels off.
    sky.sun_elevation = math.radians(60.0)
    sky.sun_rotation  = math.radians(-20.0)
    sky.sun_intensity = 1.0
    sky.altitude = 0.0
    sky.air_density = 1.0
    sky.dust_density = 0.3
    sky.ozone_density = 1.0
    nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 1.2
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])


def add_window_portal():
    """Light Portal (mesh-area-light with portal flag) flush with the window
    aperture. Gates MIS sampling so the sky reaches the bake efficiently —
    biggest single quality lever for a small-opening interior in Cycles."""
    win_cx = (WIN_X0 + WIN_X1) / 2
    win_cy = (WIN_Y0 + WIN_Y1) / 2
    win_w  = WIN_X1 - WIN_X0
    win_h  = WIN_Y1 - WIN_Y0
    light_data = bpy.data.lights.new(name='win_portal', type='AREA')
    light_data.shape = 'RECTANGLE'
    light_data.size = win_w
    light_data.size_y = win_h
    light_data.cycles.is_portal = True       # the magic flag
    light_data.energy = 0.0                  # portals don't emit; they sample the world
    obj = bpy.data.objects.new('win_portal_obj', light_data)
    bpy.context.collection.objects.link(obj)
    # Place at the window's OUTER face, normal pointing -Z into the room.
    # Three.js Y-up; Blender area-light default normal is -Z (same axis), so
    # no rotation needed beyond yaw to face into the room.
    obj.location = (win_cx, win_cy, ROOM_D + 0.10)
    obj.rotation_euler = (0.0, 0.0, 0.0)


def add_lights():
    """Kumamoto 11 AM spring SUN lamp — neutral-cool direct disc at
    azimuth ≈ 160° (SSE), elevation ≈ 60°. Does NOT enter through the
    north window; it lights the south/east outside of the building. The
    portal lets the diffuse sky reach the room; the SUN gives any south-
    facing object cast-shadows that bounce indirect into the room."""
    sun_data = bpy.data.lights.new(name='sun', type='SUN')
    sun_data.energy = 3.5
    sun_data.color = (1.0, 0.985, 0.96)     # ≈ 5500 K neutral-cool daylight
    sun_data.angle = math.radians(0.5)      # crisp disc — clear sky
    sun = bpy.data.objects.new('sun_obj', sun_data)
    bpy.context.collection.objects.link(sun)
    # Aim from azimuth 160° (SSE), elevation 60°. In three.js coords
    # (+Z = north, -Z = south, +X = east, +Y = up): sun position direction =
    #   x = sin(160°)·cos(60°) ≈ +0.171  (slightly east)
    #   y = sin(60°)            ≈ +0.866 (high overhead)
    #   z = cos(160°)·cos(60°) ≈ -0.470  (mostly south)
    # Sun light direction is -position, so the lamp points from +pos toward 0.
    import mathutils
    sun_dir = mathutils.Vector((0.171, 0.866, -0.470))
    sun.location = sun_dir * 6.0            # 6 m offset away from origin
    # SUN lamp default points -Z in its local frame; rotate so -Z lines up
    # with -sun_dir (lamp shines from sun toward origin).
    sun.rotation_euler = (-sun_dir).to_track_quat('-Z', 'Y').to_euler()

    # 3 ceiling area lights (mimic the warm spot fills) — dimmed to match
    # runtime; daylight from the window is the dominant contributor now.
    for x, z in [(0.45, 0.70), (0.90, 1.55), (1.35, 0.70)]:
        d = bpy.data.lights.new(name=f'spot_{x}_{z}', type='AREA')
        d.energy = 2.0
        d.color = (1.0, 0.88, 0.69)
        d.size = 0.25
        o = bpy.data.objects.new(f'spot_obj_{x}_{z}', d)
        bpy.context.collection.objects.link(o)
        o.location = (x, ROOM_H - 0.02, z)
        o.rotation_euler = (0, 0, 0)        # area light points -Y by default → wrong axis
        # We want it pointing DOWN (-Y in Blender = down? actually +Z in three.js / Blender Y-up...
        # we're using three.js Y-up convention, so -Y is down. But Blender uses Z-up by default.
        # Since our coords are in three.js terms passed through unchanged, the area light
        # default direction (-Z in Blender) will point in some direction relative to our coords.
        # For a Y-up world, the area light is created facing -Z by default in Blender;
        # in our three.js coords that maps to -Z which is BACK in our convention.
        # We want it pointing DOWN (-Y in three.js coords). Rotate -90° around X.
        o.rotation_euler = (math.pi / 2, 0, 0)


def make_image(slug):
    img = bpy.data.images.new(name=slug, width=RES, height=RES,
                              alpha=False, float_buffer=False)
    img.colorspace_settings.name = 'sRGB'
    img.filepath_raw = os.path.join(OUT_DIR, f"{slug}.png")
    img.file_format = 'PNG'
    return img


def make_target_material(name, image, base_color):
    """Diffuse material with a base color + image-texture node where the bake writes."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfDiffuse')
    bsdf.inputs['Color'].default_value = base_color
    img_node = nt.nodes.new('ShaderNodeTexImage')
    img_node.image = image
    img_node.select = True
    nt.nodes.active = img_node
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat


def make_diffuse_material(name, color):
    """Plain diffuse material for occluders (washer, etc.) — bounces colored light."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfDiffuse')
    bsdf.inputs['Color'].default_value = color
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
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


def build_surfaces():
    """Six bake-target surfaces, each with its own image + material; all 6 in
    the scene simultaneously so they bounce colored light at each other."""
    surfaces = []

    # Floor: y=0, normal +y
    img = make_image('floor')
    mat = make_target_material('mat_floor', img, COL_FLOOR)
    obj = add_quad(
        'floor',
        verts=[(0, 0, 0), (ROOM_W, 0, 0), (ROOM_W, 0, ROOM_D), (0, 0, ROOM_D)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append((obj, img))

    # Ceiling: y=ROOM_H, normal -y
    img = make_image('ceiling')
    mat = make_target_material('mat_ceiling', img, COL_CEIL)
    obj = add_quad(
        'ceiling',
        verts=[(0, ROOM_H, 0), (0, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    surfaces.append((obj, img))

    # Door-wall (south, z=0, normal +z)
    img = make_image('door_wall')
    mat = make_target_material('mat_door', img, COL_WALL)
    obj = add_quad(
        'door_wall',
        verts=[(0, 0, 0), (0, ROOM_H, 0), (ROOM_W, ROOM_H, 0), (ROOM_W, 0, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    surfaces.append((obj, img))

    # Bath-wall (west, x=0, normal +x)
    img = make_image('bath_wall')
    mat = make_target_material('mat_bath', img, COL_WALL)
    obj = add_quad(
        'bath_wall',
        verts=[(0, 0, 0), (0, 0, ROOM_D), (0, ROOM_H, ROOM_D), (0, ROOM_H, 0)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append((obj, img))

    # Vanity-wall (east, x=ROOM_W, normal -x) — BRICK colour for proper bounce
    img = make_image('vanity_wall')
    mat = make_target_material('mat_vanity', img, COL_BRICK)
    obj = add_quad(
        'vanity_wall',
        verts=[(ROOM_W, 0, ROOM_D), (ROOM_W, 0, 0), (ROOM_W, ROOM_H, 0), (ROOM_W, ROOM_H, ROOM_D)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append((obj, img))

    # Window-wall (north, z=ROOM_D, normal -z) — with window cutout
    img = make_image('window_wall')
    mat = make_target_material('mat_window', img, COL_WALL)
    outer_v = [
        (ROOM_W, 0,      ROOM_D),
        (0,     0,      ROOM_D),
        (0,     ROOM_H, ROOM_D),
        (ROOM_W, ROOM_H, ROOM_D),
    ]
    outer_uv = [(0, 0), (1, 0), (1, 1), (0, 1)]
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
    surfaces.append((obj, img))

    return surfaces


def bake_one(obj, image):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    print(f"  baking {obj.name} -> {image.filepath_raw}")
    bpy.ops.object.bake(type='COMBINED', use_clear=True, margin=MARGIN)
    image.save()


def main():
    print("=== laundry-test room LIGHTMAP bake start ===")
    print(f"  res={RES}, samples={SAMPLES}")
    print(f"  output: {OUT_DIR}")

    reset_scene()
    configure_cycles()
    configure_world()
    add_window_portal()
    add_lights()

    # Washer occluder — diffuse white, will catch + reflect the brick wall
    washer_mat = make_diffuse_material('mat_washer', COL_WASHER)
    add_box('washer', *WASHER_BOX, washer_mat)

    surfaces = build_surfaces()
    print(f"Built {len(surfaces)} bake-target surfaces.")

    for obj, img in surfaces:
        bake_one(obj, img)

    print("=== laundry-test room LIGHTMAP bake done ===")


if __name__ == '__main__':
    main()
