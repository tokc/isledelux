import bpy
import bmesh
import random

from time import time

import sys
import os

from config import *
import planemaker


# Parameter stuff.
reset_old_stuff = True

UNIQUE_ID = "34587873456"
ISLAND_NAME = "Island" + UNIQUE_ID
tree_name = "Tree" + UNIQUE_ID
top_name = "Top" + UNIQUE_ID
SUN_NAME = "Sun" + UNIQUE_ID
SEA_NAME = "Sea" + UNIQUE_ID


# Utility stuff.

def select_only(thing):
    # Deselect everything and select only the named object.
    get_me_mode('OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    try:
        bpy.data.objects[thing].select = True
    except:
        pass

def activate_object(object):
    # Deselect everything and select only the named object.
    get_me_mode('OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    try:
        bpy.context.scene.objects.active = object
    except:
        pass

def get_me_mode(new_mode):
    try:
        bpy.ops.object.mode_set(mode=new_mode)

    except:
        pass


# Linear stuff.

def generate_scene():
    create_sun(SUN_NAME)
    create_sea()
    
    set_up_camera()
    
    island_plane = create_island(ISLAND_NAME)
    lots_of_trees(island_plane)

def lots_of_trees(island):
    more = True

    while more:
        generate_tree(island)

        if random.random() > 0.5:
            more = False

def set_up_camera():
    # CAMERA STUFF
    get_me_mode('OBJECT')
    bpy.ops.object.empty_add()
    target = bpy.context.active_object
    #                       Y between -3.0 and 3.0         Z between 1.0 and 2.0
    target.location = (0.0, (random.random() - 0.5) * 6.0, 0.5 + random.random() * 2.0)

    create_camera(target)

def generate_tree(island):
    # Make a tree.
    activate_object(island)
    get_me_mode('EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    treetop_position, treetop_size = place_tree(bm)
    make_tree_top(treetop_position, treetop_size)

def delete_old_stuff():
    get_me_mode('OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
def t():
    # Grab the "front" of the plane and pull it down with connected falloff.
    bpy.ops.transform.translate(value=(0.0, 0.0, -1.5) , proportional='CONNECTED', proportional_edit_falloff='SMOOTH', proportional_size=2.0)

def r():
    get_me_mode('OBJECT')
    bpy.ops.transform.rotate(
        value=(random.random() * 6.2),
        axis=(0, 0, 1),
        constraint_axis=(False, False, True),
        constraint_orientation='GLOBAL'
        )

def select_outer_loop(bm):
    for vertex in bm.verts:
        if (len(vertex.link_edges) < 4) and vertex.co.z > 0.0:
            vertex.select = True
            vertex.co.z = 0.0

def delete_faces_under(bm, under=0.0):
    get_me_mode('EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    for face in bm.faces:
        is_under = True
        for vertex in face.verts:
            if vertex.co.z > under:
                is_under = False
        if is_under:
            face.select = True

    bpy.ops.mesh.delete(type='FACE')


# Generate stuff.

def create_camera(target):
    get_me_mode('OBJECT')
    bpy.ops.object.camera_add(location=(13.0, 0.0, (random.random() * 0.2) + 0.2))
    camera = bpy.context.active_object
    # Set the new camera as the active rendering camera.
    bpy.context.scene.camera = camera
    
    track = camera.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

def random_spike(island_plane, num_spikes):
    for i in range(num_spikes):
        get_me_mode('EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        get_me_mode('OBJECT')
        random.choice(island_plane.data.vertices).select = True
        
        get_me_mode('EDIT')
        spike_height = (random.random() * 1)
        bpy.ops.transform.translate(value=(0.0, 0.0, spike_height) , proportional='CONNECTED', proportional_edit_falloff='SMOOTH', proportional_size=(random.random() * 1) + spike_height)

def create_sea():
    get_me_mode('OBJECT')
    bpy.ops.mesh.primitive_plane_add(radius=200.0, location=(0.0, 0.0, 0.15), enter_editmode=False)
    #bpy.ops.transform.resize(value=(2.0, 2.0, 2.0))
    
    # Apply island material.
    sea = bpy.context.active_object
    sea.data.materials.append(bpy.data.materials.get('Blue'))

def create_island(name):
    get_me_mode('OBJECT')
    
    plane = planemaker.generate_plane(name, True)
    select_only(name)
    plane.location.z
    
    get_me_mode('EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(0.2, 0.2, 0.2))
    
    select_only(name)
    
    random_spike(plane, 8)
    
    # Select edge loop.
    get_me_mode('EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    select_outer_loop(bm)
    
    # Pull down edge of island plane.
    t()
    
    # Rotate island object.
    r()
    
    # Smooth
    get_me_mode('EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.vertices_smooth(factor=0.9)
    bpy.ops.mesh.vertices_smooth(factor=0.9)
    
    # Clean up unneded vertices.
    get_me_mode('EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    delete_faces_under(bm)

    # Move the island to a spot.
    plane.location = ((random.random() * 5.0) - 1.0, 0.0, 0.0)

    # Apply island material.
    plane.data.materials.append(bpy.data.materials.get('Sand'))

    return plane

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
        
        # I have no idea why some of these trunks are ending up at 0, 0.
        # Aaaaah~
        # But...
        # It works now?
        # So, I'm just going to leave it like this.
        wc = (bpy.context.active_object.matrix_world * coordinates)
        print(wc)
        while (int(wc.x * 10) == 0 or int(wc.y * 10) == 0):
            print("ABOVE HERE")
            coordinates = random.choice(verts_above_ground).co
            wc = (bpy.context.active_object.matrix_world * coordinates)

    world_coordinates = (bpy.context.active_object.matrix_world * coordinates)
    world_coordinates.x += (random.random() * 0.2) - 0.1
    world_coordinates.y += (random.random() * 0.2) - 0.1
    
    get_me_mode('OBJECT')
    trunk_thickness = (random.random() * 0.04) + 0.03
    bpy.ops.mesh.primitive_plane_add(
        radius=trunk_thickness,
        location=world_coordinates,
        enter_editmode=True)

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

    return top_of_tree, trunk_thickness

def make_tree_top(position=(0.0, 0.0, 0.0), top_size=0.0):
    position[1] += 0.05
    get_me_mode('OBJECT')
    bpy.ops.mesh.primitive_ico_sphere_add(size=0.3 * (1 + (top_size * 9)), subdivisions=1, enter_editmode=True, location=(position))
    bpy.ops.transform.rotate(value=(random.random() * 6.4))
    bpy.context.active_object.name = top_name
    bpy.ops.mesh.subdivide(fractal=9.56, fractal_along_normal=0.15)
    bpy.ops.mesh.vertices_smooth(factor=0.9)
    bpy.ops.obj
    bpy.context.active_object.data.materials.append(bpy.data.materials.get('Green'))

def create_sun(sun_name):
    get_me_mode('OBJECT')
    bpy.ops.object.lamp_add(type='SUN', location=(3.0, 7.0, 2.0))
    sun = bpy.context.active_object
    sun.name = sun_name
    sun.rotation_euler = (random.random() * 1.4, 0.0, random.random() * 6.3)


# Do stuff.
if reset_old_stuff:
    delete_old_stuff()

generate_scene()

get_me_mode('OBJECT')

# This is the stupidest thing I have ever seen. But apparently it's the easiest way to change the view to the camera.
next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D').spaces[0].region_3d.view_perspective = 'CAMERA'
bpy.ops.object.select_all(action='DESELECT')
