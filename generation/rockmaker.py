import random
import bpy
import bmesh

from .utilities import get_me_mode, activate_object

def choose_location(island):
    # Choose location.
    activate_object(island)
    get_me_mode('EDIT')
    bm = bmesh.from_edit_mesh(island.data)
    verts_above_ground = [vertex for vertex in bm.verts if vertex.co.z < 0.15]

    if len(verts_above_ground) < 1:
        # If there are no vertices, make a new one.
        vert = bm.verts.new((random.random(), random.random(), 0.0))
        coordinates = vert.co

    else:
        coordinates = random.choice(verts_above_ground).co

        wc = (bpy.context.active_object.matrix_world * coordinates)
        while (int(wc.x * 10) == 0 or int(wc.y * 10) == 0):
            coordinates = random.choice(verts_above_ground).co
            wc = (bpy.context.active_object.matrix_world * coordinates)

    world_coordinates = (bpy.context.active_object.matrix_world * coordinates)
    world_coordinates.x += (random.random() * 0.2) - 0.1
    world_coordinates.y += (random.random() * 0.2) - 0.1

    return world_coordinates

def place_rock(island):
    get_me_mode('OBJECT')
    position = choose_location(island)
    get_me_mode('OBJECT')
    bpy.ops.mesh.primitive_cube_add(location=position, radius=0.2 + (random.random() * 0.2), enter_editmode=True)
    bpy.ops.mesh.subdivide(fractal=2.743 + random.random())
    bpy.ops.mesh.subdivide(fractal=9.743)
    bpy.ops.mesh.subdivide(fractal=6.743)
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].iterations = 4
    bpy.context.object.modifiers["Decimate"].decimate_type = 'UNSUBDIV'
    get_me_mode('OBJECT')
    bpy.ops.object.modifier_apply(modifier="Decimate")
    get_me_mode('EDIT')
    bpy.ops.mesh.vertices_smooth(factor=0.9123)
    bpy.ops.mesh.vertices_smooth(factor=0.9123)

    rock = bpy.context.active_object
    # Apply material.
    rock.data.materials.append(bpy.data.materials.get('Grey'))

    # Maybe it would be a good idea to return the newly created object.
    get_me_mode('OBJECT')
