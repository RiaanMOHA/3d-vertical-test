"""
living-dining-test (LDK) room-shell LIGHTMAP bake (Cycles + OptiX, A6000 GPU 1).

Path-traces the FULL lighting solution into a per-surface texture (Combined =
Direct + Indirect + Diffuse + AO) for every wall, the floor, the ceiling, and
the two stairwell partitions. Mirrors the laundry-test/bake/bake_room_lightmap.py
pattern but adapted for the LDK:

  - dimensions 6.30 (E-W) × 4.50 (N-S) × 2.50 (H) m
  - NW stair carve-out: 0.90 × 1.60 m (floor + ceiling open in that footprint)
  - 3 window apertures (each gets its own Light Portal):
      south slider 1: x=[0.80, 3.00], y=[0.05, 2.10]
      south slider 2: x=[3.30, 5.50], y=[0.05, 2.10]
      east window:    z=[1.50, 3.00], y=[0.80, 2.00]
  - Sun lamp: Kumamoto, sunny spring, 11 AM JST → azimuth 160°, elevation 60°
    (same as the laundry-test rig — single SUN serves the whole house)
  - TV console + TV body added as occluders so floor/ceiling shadows under the
    console + brick-wall light bouncing off the TV all get path-traced.

Output: living-dining-test/textures/lightmap/<surface>.png  (17 files, 1K, color)
  4 floor / ceiling halves (NW carve-out)
  2 garden-wall halves (mullion split)
  1 brick-wall (with east-window cutout)
  6 kitchen-wall fragments (around corridor door + pass-through)
  1 alcove brick splash (back wall visible through pass-through)
  1 stairs-wall
  2 stairwell partition faces

Run:
  CUDA_VISIBLE_DEVICES=1 ~/blender/blender-5.1.1-linux-x64/blender \\
    --background --python living-dining-test/bake/bake_room_lightmap.py
"""

import os
import math
import bpy
import bmesh
import mathutils

# ============================================================================
# Geometry — must mirror living-dining-test.html exactly.
# ============================================================================
ROOM_W = 6.30      # E-W (along +X)
ROOM_D = 4.50      # N-S (along +Z)
ROOM_H = 2.50      # up   (along +Y)

# NW stair carve-out (floor + ceiling open in this footprint)
STAIR_W = 0.90
STAIR_D = 1.60
STAIR_X0 = 0.0
STAIR_X1 = STAIR_W                  # 0.90
STAIR_Z0 = ROOM_D - STAIR_D         # 2.90
STAIR_Z1 = ROOM_D                   # 4.50

# South sliding-door openings (garden-wall, z=0)
SD_SILL  = 0.05
SD_HEAD  = 2.10
SD1_X0, SD1_X1 = 0.80, 3.00
SD2_X0, SD2_X1 = 3.30, 5.50

# East brick-wall window opening (x=ROOM_W)
BW_Z0, BW_Z1 = 1.50, 3.00
BW_Y0, BW_Y1 = 0.80, 2.00

# TV console occluder (against kitchen-wall, north) — repositioned east
# of the corridor entry door so the door isn't visually blocked.
CON_W = 1.65
CON_D = 0.40
CON_H = 0.50
CON_CX = 2.775
CON_CZ = ROOM_D - CON_D / 2     # back flush with kitchen-wall

# Corridor door + kitchen pass-through — openings cut from kitchen-wall
COR_X0, COR_X1 = 1.10, 1.90
COR_HEAD = 2.05
PT_X0, PT_X1 = 3.65, 6.20
PT_SILL = 1.05
PT_HEAD = 2.05

# Kitchen alcove behind the pass-through — a shallow backdrop visible
# through the opening (brick splash + fridge + range hood).
ALCOVE_DEPTH = 0.85
ALCOVE_Z0 = ROOM_D
ALCOVE_Z1 = ROOM_D + ALCOVE_DEPTH

# Fridge occluder (alcove east portion)
FR_W, FR_D, FR_H = 0.70, 0.66, 1.85
FR_CX = 5.65
FR_CZ = ALCOVE_Z1 - FR_D / 2 - 0.020
FRIDGE_BOX = (
    FR_CX - FR_W / 2, FR_CX + FR_W / 2,
    0.0, FR_H,
    FR_CZ - FR_D / 2, FR_CZ + FR_D / 2,
)

# Range hood occluder (alcove west portion)
HD_W, HD_H, HD_D = 0.78, 0.50, 0.42
HD_CX = 4.20
HD_CY = 1.85 + HD_H / 2
HD_CZ = ALCOVE_Z1 - HD_D / 2 - 0.020
HOOD_BOX = (
    HD_CX - HD_W / 2, HD_CX + HD_W / 2,
    HD_CY - HD_H / 2, HD_CY + HD_H / 2,
    HD_CZ - HD_D / 2, HD_CZ + HD_D / 2,
)

# Sofa occluder (living zone) — simple bounding box for shadow + leather bounce
SOFA_BOX = (
    2.30 - 0.75, 2.30 + 0.75,
    0.0, 0.78,
    1.55 - 0.40, 1.55 + 0.40,
)

# Coffee table occluder
CT_BOX = (
    2.30 - 0.55, 2.30 + 0.55,
    0.0, 0.40,
    2.70 - 0.275, 2.70 + 0.275,
)

# Dining table occluder
DT_BOX = (
    4.70 - 0.80, 4.70 + 0.80,
    0.0, 0.74,
    2.05 - 0.425, 2.05 + 0.425,
)
CON_BOX = (
    CON_CX - CON_W / 2, CON_CX + CON_W / 2,
    0.0, CON_H,
    CON_CZ - CON_D / 2, CON_CZ + CON_D / 2,
)

# TV body sitting on the console (with-stand variant — small base)
TV_W = 1.462
TV_H = 0.842
TV_D = 0.071
STAND_H = 0.070
TV_CY0 = CON_H + STAND_H
TV_CY1 = TV_CY0 + TV_H
TV_CX  = CON_CX
TV_CZ  = CON_CZ + 0.02
TV_BOX = (
    TV_CX - TV_W / 2, TV_CX + TV_W / 2,
    TV_CY0,           TV_CY1,
    TV_CZ - TV_D / 2, TV_CZ + TV_D / 2,
)

# ============================================================================
# Surface colours (linear sRGB) — match the JS canvas-procedural materials
# so colour-bleed (brick onto floor, oak floor onto ceiling, etc.) renders
# faithfully into the bake.
# ============================================================================
COL_WALL    = (0.640, 0.580, 0.470, 1.0)   # warm grey-beige paint
COL_BRICK   = (0.260, 0.110, 0.070, 1.0)   # warm red-brown terracotta
COL_FLOOR   = (0.620, 0.500, 0.320, 1.0)   # light oak (Poly Haven laminate)
COL_CEIL    = (0.800, 0.720, 0.580, 1.0)   # whitewashed plank base
COL_TV_DARK = (0.020, 0.025, 0.035, 1.0)   # near-black TV screen / bezel
COL_WOOD_DK = (0.050, 0.025, 0.012, 1.0)   # dark walnut console
COL_FRIDGE  = (0.380, 0.395, 0.420, 1.0)   # brushed stainless
COL_HOOD    = (0.025, 0.030, 0.035, 1.0)   # near-black range hood
COL_LEATHER = (0.075, 0.040, 0.022, 1.0)   # dark brown leather sofa
COL_TABLE_W = (0.310, 0.130, 0.045, 1.0)   # warm rustic dining table

# ============================================================================
# Bake settings — same defaults as laundry-test (1024² × 512 samples + OIDN).
# Larger LDK could justify 2048², but 1024 keeps the bake under ~3 hours
# for 10 surfaces on the A6000.
# ============================================================================
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
    # OIDN preferred for static lightmap bakes (per laundry-test recipe).
    try:
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
        scene.cycles.denoising_prefilter = 'ACCURATE'
    except (TypeError, AttributeError):
        pass
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
    """Sky Texture (Nishita) world — physically-grounded sky model.
    Sun at Kumamoto 11 AM spring (azimuth 160° SSE, elevation 60°)."""
    world = bpy.context.scene.world
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')
    sky = nt.nodes.new('ShaderNodeTexSky')
    # Blender 5.x renamed Nishita -> MULTIPLE_SCATTERING (same atmospheric model).
    # Some atmospheric params (dust_density, ozone_density) are Nishita-only.
    try:
        sky.sky_type = 'NISHITA'
    except TypeError:
        sky.sky_type = 'MULTIPLE_SCATTERING'
    def _safe_set(attr, value):
        if hasattr(sky, attr):
            setattr(sky, attr, value)
    _safe_set('sun_elevation', math.radians(60.0))
    _safe_set('sun_rotation',  math.radians(-20.0))   # azimuth 160° from south = -20°
    _safe_set('sun_intensity', 1.0)
    _safe_set('altitude',      0.0)
    _safe_set('air_density',   1.0)
    _safe_set('dust_density',  0.3)
    _safe_set('ozone_density', 1.0)
    nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 0.9       # was 1.2 — user reported "too bright"
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])


def add_window_portal(name, cx, cy, cz, w, h, axis):
    """Light Portal at a window aperture. axis ∈ {'+Z', '-Z', '+X', '-X'}
    is the outward normal direction (i.e. portal samples WORLD light coming
    from that direction). Portals are the single biggest quality lever for
    small-aperture interiors — they MIS-sample the sky through the opening."""
    light_data = bpy.data.lights.new(name=name, type='AREA')
    light_data.shape = 'RECTANGLE'
    if axis in ('+Z', '-Z'):
        light_data.size = w
        light_data.size_y = h
    else:
        light_data.size = h
        light_data.size_y = w
    light_data.cycles.is_portal = True
    light_data.energy = 0.0          # portals don't emit; they sample the world
    obj = bpy.data.objects.new(name + '_obj', light_data)
    bpy.context.collection.objects.link(obj)
    obj.location = (cx, cy, cz)
    # Default area-light normal is -Z. Rotate to face the desired axis.
    if axis == '+Z':
        obj.rotation_euler = (math.pi, 0, 0)
    elif axis == '-Z':
        obj.rotation_euler = (0, 0, 0)
    elif axis == '+X':
        obj.rotation_euler = (0, math.pi / 2, 0)
    elif axis == '-X':
        obj.rotation_euler = (0, -math.pi / 2, 0)


def add_window_portals():
    """3 portals — south slider 1, south slider 2, east brick window. Outward
    normal direction is -Z for south windows (sun comes from south outside)
    and +X for east window (sun comes from east outside)."""
    # South slider 1 — opening centre, normal -Z (outward = south)
    add_window_portal(
        'win_portal_south_1',
        cx=(SD1_X0 + SD1_X1) / 2,
        cy=(SD_SILL + SD_HEAD) / 2,
        cz=-0.02,
        w=SD1_X1 - SD1_X0, h=SD_HEAD - SD_SILL,
        axis='-Z',
    )
    # South slider 2
    add_window_portal(
        'win_portal_south_2',
        cx=(SD2_X0 + SD2_X1) / 2,
        cy=(SD_SILL + SD_HEAD) / 2,
        cz=-0.02,
        w=SD2_X1 - SD2_X0, h=SD_HEAD - SD_SILL,
        axis='-Z',
    )
    # East brick window — opening centre, normal +X (outward = east)
    add_window_portal(
        'win_portal_east',
        cx=ROOM_W + 0.02,
        cy=(BW_Y0 + BW_Y1) / 2,
        cz=(BW_Z0 + BW_Z1) / 2,
        w=BW_Z1 - BW_Z0, h=BW_Y1 - BW_Y0,
        axis='+X',
    )


def add_sun():
    """Single SUN lamp, Kumamoto 11 AM spring. Direction-TO-sun:
       (sin 160° · cos 60°, sin 60°, cos 160° · cos 60°)
       ≈ (0.171, 0.866, -0.470).  Sun is SSE high outside the building.
    Lights both the south sliders (direct sun streams in) AND the east
    brick window (oblique morning sun)."""
    sun_data = bpy.data.lights.new(name='sun', type='SUN')
    sun_data.energy = 2.4                    # was 3.5 — user reported "too bright"
    sun_data.color = (1.0, 0.985, 0.96)     # ~5500 K neutral-cool daylight
    sun_data.angle = math.radians(0.5)      # crisp disc — clear sky
    sun = bpy.data.objects.new('sun_obj', sun_data)
    bpy.context.collection.objects.link(sun)
    sun_dir = mathutils.Vector((0.171, 0.866, -0.470))
    sun.location = sun_dir * 12.0
    sun.rotation_euler = (-sun_dir).to_track_quat('-Z', 'Y').to_euler()


# ============================================================================
# Mesh + material helpers
# ============================================================================

def make_image(slug):
    img = bpy.data.images.new(name=slug, width=RES, height=RES,
                              alpha=False, float_buffer=False)
    img.colorspace_settings.name = 'sRGB'
    img.filepath_raw = os.path.join(OUT_DIR, f"{slug}.png")
    img.file_format = 'PNG'
    return img


def make_target_material(name, image, base_color):
    """Diffuse material with base colour + image-texture node where the bake writes."""
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
    """Plain diffuse material for occluders — bounces colour but is not baked."""
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


def add_polygon_with_holes(name, outer_v, hole_vs, outer_uv, hole_uvs, mat):
    """Quad with one or more rectangular holes. outer_v: 4 verts (CCW from
    interior view). hole_vs: list of 4-vert hole rectangles (CCW). UVs supplied
    in matching order. Builds a triangle strip between outer + each hole edge.

    For multiple holes this is naive: assumes holes are disjoint and the
    triangulation around each hole follows the simple 8-tri pattern used in
    laundry-test. For the LDK we have at most 2 holes (south wall) so we
    decompose by splitting the outer rect into vertical strips per hole.
    """
    # Simpler: caller is responsible for splitting into single-hole polygons.
    raise NotImplementedError("Use add_polygon_with_hole for single-hole walls.")


def add_polygon_with_hole(name, outer, hole, uvs_outer, uvs_hole, mat):
    """Quad with one rectangular hole — 8 verts, 8 triangles around the hole."""
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


def flip_normals(obj):
    """Reverse face winding so the surface normal points the other way.
    Cycles COMBINED bake reads incident light hitting the FRONT face only
    (the side the normal points away from is back-facing → ignored). When
    a bake target's normal points OUT of the room, the bake samples the
    world sky directly → uniform white. Flipping fixes that."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


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


# ============================================================================
# 10 bake-target surfaces — see file header for the list.
# ============================================================================
def build_surfaces():
    surfaces = []   # list of (obj, image)

    # --- FLOOR — split around NW carve-out -----------------------------------
    # 1) floor_east: x=[STAIR_X1, ROOM_W], z=[0, ROOM_D] — main floor
    img = make_image('floor_east')
    mat = make_target_material('mat_floor_east', img, COL_FLOOR)
    obj = add_quad(
        'floor_east',
        verts=[(STAIR_X1, 0, 0), (ROOM_W, 0, 0), (ROOM_W, 0, ROOM_D), (STAIR_X1, 0, ROOM_D)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    flip_normals(obj)   # CW winding above gives -Y; flip to +Y (up into room)
    surfaces.append((obj, img))

    # 2) floor_south: x=[0, STAIR_X1], z=[0, STAIR_Z0]
    img = make_image('floor_south')
    mat = make_target_material('mat_floor_south', img, COL_FLOOR)
    obj = add_quad(
        'floor_south',
        verts=[(0, 0, 0), (STAIR_X1, 0, 0), (STAIR_X1, 0, STAIR_Z0), (0, 0, STAIR_Z0)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    flip_normals(obj)
    surfaces.append((obj, img))

    # --- CEILING — same split, normal -Y (down into room) --------------------
    # 3) ceiling_east
    img = make_image('ceiling_east')
    mat = make_target_material('mat_ceiling_east', img, COL_CEIL)
    obj = add_quad(
        'ceiling_east',
        verts=[(STAIR_X1, ROOM_H, 0), (STAIR_X1, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, ROOM_D), (ROOM_W, ROOM_H, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    flip_normals(obj)   # current winding gives +Y; flip to -Y (down into room)
    surfaces.append((obj, img))

    # 4) ceiling_south
    img = make_image('ceiling_south')
    mat = make_target_material('mat_ceiling_south', img, COL_CEIL)
    obj = add_quad(
        'ceiling_south',
        verts=[(0, ROOM_H, 0), (0, ROOM_H, STAIR_Z0), (STAIR_X1, ROOM_H, STAIR_Z0), (STAIR_X1, ROOM_H, 0)],
        uvs=[(0, 0), (0, 1), (1, 1), (1, 0)],
        mat=mat,
    )
    flip_normals(obj)
    surfaces.append((obj, img))

    # --- GARDEN-WALL (south, z=0, normal +Z) — TWO door cutouts ---------------
    # We split into LEFT + RIGHT halves at the mullion to keep single-hole
    # poly per surface. Each half bakes to its own image.

    # 5) garden_wall_left  — x=[0, SD1_X1] with door 1 cutout
    img = make_image('garden_wall_left')
    mat = make_target_material('mat_garden_left', img, COL_WALL)
    outer_v = [
        (SD1_X1, 0,      0),
        (0,     0,      0),
        (0,     ROOM_H, 0),
        (SD1_X1, ROOM_H, 0),
    ]
    outer_uv = [(0, 0), (1, 0), (1, 1), (0, 1)]
    hole_v = [
        (SD1_X1, SD_SILL, 0),
        (SD1_X0, SD_SILL, 0),
        (SD1_X0, SD_HEAD, 0),
        (SD1_X1, SD_HEAD, 0),
    ]
    def gl_uv(x, y):
        return ((SD1_X1 - x) / SD1_X1, y / ROOM_H)
    hole_uv = [gl_uv(SD1_X1, SD_SILL), gl_uv(SD1_X0, SD_SILL),
               gl_uv(SD1_X0, SD_HEAD), gl_uv(SD1_X1, SD_HEAD)]
    obj = add_polygon_with_hole(
        'garden_wall_left',
        outer=outer_v, hole=hole_v,
        uvs_outer=outer_uv, uvs_hole=hole_uv,
        mat=mat,
    )
    flip_normals(obj)   # outer winding gives -Z; flip to +Z (north into LDK)
    surfaces.append((obj, img))

    # 6) garden_wall_right — x=[SD1_X1, ROOM_W] with door 2 cutout
    img = make_image('garden_wall_right')
    mat = make_target_material('mat_garden_right', img, COL_WALL)
    outer_v = [
        (ROOM_W, 0,      0),
        (SD1_X1, 0,      0),
        (SD1_X1, ROOM_H, 0),
        (ROOM_W, ROOM_H, 0),
    ]
    outer_uv = [(0, 0), (1, 0), (1, 1), (0, 1)]
    hole_v = [
        (SD2_X1, SD_SILL, 0),
        (SD2_X0, SD_SILL, 0),
        (SD2_X0, SD_HEAD, 0),
        (SD2_X1, SD_HEAD, 0),
    ]
    span = ROOM_W - SD1_X1
    def gr_uv(x, y):
        return ((ROOM_W - x) / span, y / ROOM_H)
    hole_uv = [gr_uv(SD2_X1, SD_SILL), gr_uv(SD2_X0, SD_SILL),
               gr_uv(SD2_X0, SD_HEAD), gr_uv(SD2_X1, SD_HEAD)]
    obj = add_polygon_with_hole(
        'garden_wall_right',
        outer=outer_v, hole=hole_v,
        uvs_outer=outer_uv, uvs_hole=hole_uv,
        mat=mat,
    )
    flip_normals(obj)
    surfaces.append((obj, img))

    # --- BRICK-WALL (east, x=ROOM_W, normal -X) — single window cutout --------
    # 7) brick_wall
    img = make_image('brick_wall')
    mat = make_target_material('mat_brick', img, COL_BRICK)
    # CCW seen from -X (looking from inside room toward east wall):
    outer_v = [
        (ROOM_W, 0,      0),
        (ROOM_W, 0,      ROOM_D),
        (ROOM_W, ROOM_H, ROOM_D),
        (ROOM_W, ROOM_H, 0),
    ]
    # UV: u maps to z=0..ROOM_D, v maps to y=0..ROOM_H
    outer_uv = [(0, 0), (1, 0), (1, 1), (0, 1)]
    hole_v = [
        (ROOM_W, BW_Y0, BW_Z0),
        (ROOM_W, BW_Y0, BW_Z1),
        (ROOM_W, BW_Y1, BW_Z1),
        (ROOM_W, BW_Y1, BW_Z0),
    ]
    def bw_uv(z, y):
        return (z / ROOM_D, y / ROOM_H)
    hole_uv = [bw_uv(BW_Z0, BW_Y0), bw_uv(BW_Z1, BW_Y0),
               bw_uv(BW_Z1, BW_Y1), bw_uv(BW_Z0, BW_Y1)]
    obj = add_polygon_with_hole(
        'brick_wall',
        outer=outer_v, hole=hole_v,
        uvs_outer=outer_uv, uvs_hole=hole_uv,
        mat=mat,
    )
    surfaces.append((obj, img))

    # --- KITCHEN-WALL (north, z=ROOM_D, normal -Z) — fragmented around
    #     corridor door (x=[COR_X0, COR_X1], y=[0, COR_HEAD]) and the
    #     kitchen pass-through (x=[PT_X0, PT_X1], y=[PT_SILL, PT_HEAD]).
    #     Six fragments, each its own bake target — keeps the polygons
    #     simple (no multi-hole triangulation) and lets light correctly
    #     stream through both openings during the bake.
    def kw_quad(slug, x0, x1, y0, y1):
        img = make_image(slug)
        mat = make_target_material(f'mat_{slug}', img, COL_WALL)
        obj = add_quad(
            slug,
            verts=[(x0, y0, ROOM_D), (x1, y0, ROOM_D), (x1, y1, ROOM_D), (x0, y1, ROOM_D)],
            uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
            mat=mat,
        )
        flip_normals(obj)   # current winding gives +Z; flip to -Z (south into LDK)
        surfaces.append((obj, img))

    # 8a) west solid (between stair partition and corridor)
    kw_quad('kitchen_wall_west', STAIR_X1, COR_X0, 0, ROOM_H)
    # 8b) above corridor door
    kw_quad('kitchen_wall_above_door', COR_X0, COR_X1, COR_HEAD, ROOM_H)
    # 8c) mid solid (between corridor and pass-through — clock mounts here)
    kw_quad('kitchen_wall_mid', COR_X1, PT_X0, 0, ROOM_H)
    # 8d) below pass-through (the half-height counter wall stub)
    kw_quad('kitchen_wall_below_pt', PT_X0, PT_X1, 0, PT_SILL)
    # 8e) above pass-through (the bulkhead)
    kw_quad('kitchen_wall_above_pt', PT_X0, PT_X1, PT_HEAD, ROOM_H)
    # 8f) east solid (between pass-through and brick-wall corner)
    kw_quad('kitchen_wall_east', PT_X1, ROOM_W, 0, ROOM_H)

    # --- ALCOVE BACK-WALL — brick splash visible through the pass-through.
    #     Position: z=ALCOVE_Z1, faces -Z (LDK side seen through opening),
    #     spans counter sill to ceiling. Uses brick colour so the indirect
    #     bounce warming the LDK through the pass-through reads correctly.
    img = make_image('alcove_brick')
    mat = make_target_material('mat_alcove_brick', img, COL_BRICK)
    obj = add_quad(
        'alcove_brick',
        verts=[
            (PT_X0, PT_SILL, ALCOVE_Z1),
            (PT_X1, PT_SILL, ALCOVE_Z1),
            (PT_X1, ROOM_H, ALCOVE_Z1),
            (PT_X0, ROOM_H, ALCOVE_Z1),
        ],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    flip_normals(obj)   # current +Z; flip to -Z (faces LDK through pass-through)
    surfaces.append((obj, img))

    # --- STAIRS-WALL (west, x=0, normal +X) — full ROOM_D ---------------------
    # 9) stairs_wall
    img = make_image('stairs_wall')
    mat = make_target_material('mat_stairs', img, COL_WALL)
    # CCW seen from +X:
    obj = add_quad(
        'stairs_wall',
        verts=[(0, 0, ROOM_D), (0, 0, 0), (0, ROOM_H, 0), (0, ROOM_H, ROOM_D)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append((obj, img))

    # --- STAIRWELL PARTITIONS — interior LDK-facing sides --------------------
    # 10) stairwell_partition (south + east, combined into one image with
    #     each face in its own UV quadrant since they're small and similar)
    img = make_image('stairwell_partition')
    mat = make_target_material('mat_stairwell_part', img, COL_WALL)

    # South face of stairwell (z=STAIR_Z0, x=[0, STAIR_X1]) — normal -Z (faces LDK)
    # Use UV [0, 0.5] x [0, 1]
    obj_s = add_quad(
        'stairwell_part_south',
        verts=[(0, 0, STAIR_Z0), (STAIR_X1, 0, STAIR_Z0), (STAIR_X1, ROOM_H, STAIR_Z0), (0, ROOM_H, STAIR_Z0)],
        uvs=[(0, 0), (0.49, 0), (0.49, 1), (0, 1)],
        mat=mat,
    )
    surfaces.append((obj_s, img))

    # East face of stairwell (x=STAIR_X1, z=[STAIR_Z0, STAIR_Z1]) — normal +X (faces LDK)
    # Use UV [0.51, 1] x [0, 1] — note the partition shares the same image,
    # but each surface bakes to its UV quadrant in separate bake passes.
    # For the bake pass we treat the east face as its own surface (re-bake
    # into the same image won't preserve south's pixels). Simpler: give each
    # partition face its own image.
    # Refactor: split into 2 images.

    # Re-do: drop the combined image. Each partition gets its own.
    surfaces.pop()
    bpy.data.objects.remove(obj_s, do_unlink=True)
    bpy.data.images.remove(img, do_unlink=True)

    img_s = make_image('stairwell_part_south')
    mat_s = make_target_material('mat_stairwell_s', img_s, COL_WALL)
    obj_s = add_quad(
        'stairwell_part_south',
        verts=[(0, 0, STAIR_Z0), (STAIR_X1, 0, STAIR_Z0), (STAIR_X1, ROOM_H, STAIR_Z0), (0, ROOM_H, STAIR_Z0)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat_s,
    )
    flip_normals(obj_s)   # current +Z; flip to -Z (faces LDK from stairwell side)
    surfaces.append((obj_s, img_s))

    img_e = make_image('stairwell_part_east')
    mat_e = make_target_material('mat_stairwell_e', img_e, COL_WALL)
    obj_e = add_quad(
        'stairwell_part_east',
        verts=[(STAIR_X1, 0, STAIR_Z1), (STAIR_X1, 0, STAIR_Z0), (STAIR_X1, ROOM_H, STAIR_Z0), (STAIR_X1, ROOM_H, STAIR_Z1)],
        uvs=[(0, 0), (1, 0), (1, 1), (0, 1)],
        mat=mat_e,
    )
    surfaces.append((obj_e, img_e))

    return surfaces


# ============================================================================
# Bake driver
# ============================================================================

def bake_one(obj, image):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    print(f"  baking {obj.name} -> {image.filepath_raw}")
    bpy.ops.object.bake(type='COMBINED', use_clear=True, margin=MARGIN)
    image.save()


def main():
    print("=== living-dining-test (LDK) LIGHTMAP bake start ===")
    print(f"  res={RES}, samples={SAMPLES}")
    print(f"  output: {OUT_DIR}")

    reset_scene()
    configure_cycles()
    configure_world()
    add_window_portals()
    add_sun()

    # === Occluders — bounce + shadow contributors (NOT bake targets) ===

    # TV console + body
    console_mat = make_diffuse_material('mat_console_dk', COL_WOOD_DK)
    add_box('tv_console', *CON_BOX, console_mat)
    tv_mat = make_diffuse_material('mat_tv_dk', COL_TV_DARK)
    add_box('tv_body', *TV_BOX, tv_mat)

    # Sofa + coffee table + dining table — major furniture occluders so
    # contact shadows on the floor + dark-leather/walnut bounce land in
    # the lightmaps.
    sofa_mat  = make_diffuse_material('mat_sofa', COL_LEATHER)
    add_box('sofa',         *SOFA_BOX, sofa_mat)
    add_box('coffee_table', *CT_BOX,   console_mat)
    table_mat = make_diffuse_material('mat_dining_table', COL_TABLE_W)
    add_box('dining_table', *DT_BOX,   table_mat)

    # Kitchen alcove — back wall (already a bake target as alcove_brick),
    # plus side returns + ceiling + floor as plain occluders so light
    # entering the alcove via the pass-through bounces realistically.
    wall_mat   = make_diffuse_material('mat_alc_wall',   COL_WALL)
    floor_mat  = make_diffuse_material('mat_alc_floor',  COL_FLOOR)
    ceil_mat   = make_diffuse_material('mat_alc_ceil',   COL_CEIL)
    # West return  (x=PT_X0..PT_X0+0.05, z=ALCOVE_Z0..ALCOVE_Z1)
    add_box('alcove_west_return',
            PT_X0 - 0.05, PT_X0, 0, ROOM_H, ALCOVE_Z0, ALCOVE_Z1, wall_mat)
    # East return  (x=PT_X1..PT_X1+0.05)
    add_box('alcove_east_return',
            PT_X1, PT_X1 + 0.05, 0, ROOM_H, ALCOVE_Z0, ALCOVE_Z1, wall_mat)
    # Floor (thin slab at y=-0.005..0)
    add_box('alcove_floor',
            PT_X0, PT_X1, -0.005, 0.0, ALCOVE_Z0, ALCOVE_Z1, floor_mat)
    # Ceiling (thin slab at y=ROOM_H..ROOM_H+0.005)
    add_box('alcove_ceiling',
            PT_X0, PT_X1, ROOM_H, ROOM_H + 0.005, ALCOVE_Z0, ALCOVE_Z1, ceil_mat)

    # Fridge + range hood — appliance occluders inside the alcove
    fridge_mat = make_diffuse_material('mat_fridge', COL_FRIDGE)
    add_box('fridge', *FRIDGE_BOX, fridge_mat)
    hood_mat = make_diffuse_material('mat_hood', COL_HOOD)
    add_box('range_hood', *HOOD_BOX, hood_mat)

    surfaces = build_surfaces()
    print(f"Built {len(surfaces)} bake-target surfaces.")

    for obj, img in surfaces:
        bake_one(obj, img)

    print("=== living-dining-test (LDK) LIGHTMAP bake done ===")


if __name__ == '__main__':
    main()
