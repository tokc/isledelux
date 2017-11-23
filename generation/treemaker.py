import random
import bpy
import bmesh

from .utilities import get_me_mode, activate_object

def generate_tree(island):
    # Make a tree.
    activate_object(island)
    get_me_mode('EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    return place_tree(bm)

def place_tree(bm):
    # Choose location.
    bm.verts.ensure_lookup_table()
    verts_above_ground = [vertex for vertex in bm.verts if vertex.co.z > 0.149]

    if len(verts_above_ground) < 1:
        # If there are no vertices above ground height, make a new one.
        vert = bm.verts.new((random.random(), random.random(), 0.0))
        coordinates = vert.co

    else:
        coordinates = random.choice(verts_above_ground).co
        
        # I have no idea why some of these trunks were ending up at 0, 0.
        # Whatever I did, it's working now.
        wc = (bpy.context.active_object.matrix_world * coordinates)
        while (int(wc.x * 10) == 0 or int(wc.y * 10) == 0):
            coordinates = random.choice(verts_above_ground).co
            wc = (bpy.context.active_object.matrix_world * coordinates)

    world_coordinates = (bpy.context.active_object.matrix_world * coordinates)
    world_coordinates.x += (random.random() * 0.2) - 0.1
    world_coordinates.y += (random.random() * 0.2) - 0.1
    
    # Create the trunk mesh.
    get_me_mode('OBJECT')
    trunk_thickness = (random.random() * 0.04) + 0.03
    bpy.ops.mesh.primitive_plane_add(
        radius=trunk_thickness,
        location=world_coordinates,
        enter_editmode=True
    )

    # Extrude the trunk.
    underground_distance = 0.7
    bpy.ops.transform.translate(value=(0.0, 0.0, -underground_distance))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, (random.random() * 0.7) + 0.5 + underground_distance)})

    ob = bpy.context.active_object
    ob.update_from_editmode()
    
    # Rotate the trunk.
    get_me_mode('OBJECT')
    bpy.ops.transform.rotate(value=(random.random() * 0.4) -0.2, axis=(random.random(), random.random(), random.random()))

    # Save location of top of trunk.
    top_of_tree = ob.matrix_world * [v.co for v in ob.data.vertices if v.select][0]

    # Crease the trunk.
    get_me_mode('EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(fractal=0.67)
    bpy.ops.mesh.subdivide(fractal=0.67)

    get_me_mode('OBJECT')
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'UNSUBDIV'
    bpy.context.object.modifiers["Decimate"].iterations = 2
    bpy.ops.object.modifier_apply(modifier="Decimate")

    # Add material.
    bpy.context.active_object.data.materials.append(bpy.data.materials.get('Brown'))
    
    return make_tree_top(top_of_tree, trunk_thickness)

def make_tree_top(position=(0.0, 0.0, 0.0), top_size=0.0):
    position[1] += 0.05
    get_me_mode('OBJECT')
    
    bpy.ops.mesh.primitive_ico_sphere_add(
        size=0.3 * (1 + (top_size * 9)),
        subdivisions=1,
        location=(position),
        enter_editmode=True
    )
    
    bpy.ops.transform.rotate(value=(random.random() * 6.4))
    bpy.ops.mesh.subdivide(fractal=9.56, fractal_along_normal=0.15)
    bpy.ops.mesh.vertices_smooth(factor=0.9)
    bpy.ops.obj
    bpy.context.active_object.data.materials.append(bpy.data.materials.get('Green'))