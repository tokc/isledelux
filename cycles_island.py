import bpy
import bmesh
import random

from time import time

def delete_old_stuff():
    get_me_mode('OBJECT')
    select_only(ISLAND_NAME)
    bpy.ops.object.delete()
    select_only(tree_name)
    bpy.ops.object.delete()
    select_only(top_name)
    bpy.ops.object.delete()
    select_only(SUN_NAME)
    bpy.ops.object.delete()
    select_only(SEA_NAME)
    bpy.ops.object.delete()

def t():
    # Grab the "front" of the plane and pull it down with connected falloff.
    bpy.ops.transform.translate(value=(0.0, 0.0, -1.0) , proportional='CONNECTED', proportional_edit_falloff='SMOOTH', proportional_size=2.0)

def random_spike(island_plane, num_spikes):
    for i in range(num_spikes):
        get_me_mode('EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        get_me_mode('OBJECT')
        random.choice(island_plane.data.vertices).select = True
        
        get_me_mode('EDIT')
        bpy.ops.transform.translate(value=(0.0, 0.0, (random.random() * 1.5)) , proportional='CONNECTED', proportional_edit_falloff='SMOOTH', proportional_size=random.random()*1.1)

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

def place_tree(bm):
    bm.verts.ensure_lookup_table()
    
    verts_above_ground = [vertex for vertex in bm.verts if vertex.co.z > 0.1]
    if len(verts_above_ground) < 1:
        verts_above_ground = bm.verts
        
    coordinates = random.choice(verts_above_ground).co
    get_me_mode('OBJECT')
    world_coordinates = (bpy.context.active_object.matrix_world * coordinates)
    
    bpy.ops.mesh.primitive_plane_add(radius=0.03, location=world_coordinates, enter_editmode=True)
    bpy.context.active_object.name = tree_name
    bpy.ops.transform.translate(value=(0.0, 0.0, -0.2))
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, (random.random() * 1.5) + 0.19)})
    
    ob = bpy.context.active_object
    ob.update_from_editmode()
    
    bpy.context.active_object.data.materials.append(bpy.data.materials.get('Brown'))
    
    top_of_tree = ob.matrix_world * [v.co for v in ob.data.vertices if v.select][0]
    
    get_me_mode('EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(fractal=0.67)
    
    get_me_mode('OBJECT')
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].decimate_type = 'UNSUBDIV'
    bpy.context.object.modifiers["Decimate"].iterations = 1
    bpy.ops.object.modifier_apply(modifier="Decimate")
    
    return top_of_tree

def r():
    get_me_mode('OBJECT')
    bpy.ops.transform.rotate(
        value=(random.random() * 6.2),
        axis=(0, 0, 1),
        constraint_axis=(False, False, True),
        constraint_orientation='GLOBAL'
        )

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

def make_tree_top(position=(0.0, 0.0, 0.0)):
    get_me_mode('OBJECT')
    bpy.ops.mesh.primitive_ico_sphere_add(size=0.2, subdivisions=1, enter_editmode=True, location=(position))
    bpy.context.active_object.name = top_name
    bpy.ops.mesh.subdivide(fractal=9.56, fractal_along_normal=0.243)
    bpy.ops.mesh.vertices_smooth(factor=0.9)
    bpy.context.active_object.data.materials.append(bpy.data.materials.get('Green'))

def create_sun(sun_name):
    get_me_mode('OBJECT')
    bpy.ops.object.lamp_add(type='SUN', location=(3.0, 7.0, 2.0))
    sun = bpy.context.active_object
    sun.name = sun_name
    #sun = bpy.data.objects['Sun']
    sun.rotation_euler = (random.random() * 1.4, 0.0, random.random() * 6.3)    

print("Henlo.")

reset_old_stuff = True

UNIQUE_ID = "34587873456"
ISLAND_NAME = "Island" + UNIQUE_ID
tree_name = "Tree" + UNIQUE_ID
top_name = "Top" + UNIQUE_ID
SUN_NAME = "Sun" + UNIQUE_ID
SEA_NAME = "Sea" + UNIQUE_ID

if reset_old_stuff:
    delete_old_stuff()

# Create a sun.
create_sun(SUN_NAME)

def create_sea(name, position):
    get_me_mode('OBJECT')
    bpy.ops.mesh.primitive_plane_add(radius=2.0, location=position, enter_editmode=True)
    bpy.context.active_object.name = name
    bpy.ops.transform.resize(value=(2.0, 2.0, 2.0))
    
    select_only(name)
    sea = bpy.context.active_object
    # Apply island material.
    sea.data.materials.append(bpy.data.materials.get('Blue'))

def create_island(name):
    get_me_mode('OBJECT')
    bpy.ops.mesh.primitive_plane_add(location=(0.0, 0.0, 0.0), enter_editmode=True)
    bpy.context.active_object.name = name
    bpy.ops.transform.resize(value=(2.0, 2.0, 2.0))
    bpy.ops.mesh.subdivide(number_cuts=10)
    bpy.ops.mesh.subdivide(number_cuts=2)
    
    select_only(name)
    
    plane = bpy.context.active_object
    
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
    
    # Squash the island down a little bit.
    get_me_mode('OBJECT')
    bpy.ops.transform.resize(value=(1.0, 1.0, 0.75))
    
    # Clean up unneded vertices.
    get_me_mode('EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    delete_faces_under(bm)
    
    # Move the island to a spot.
    plane.location = (random.random() * 5.0, 0.0, 0.0)
    
    # Apply island material.
    plane.data.materials.append(bpy.data.materials.get('Sand'))
    
    sea_location = [plane.location.x, plane.location.y, 0.1]
    #create_sea(SEA_NAME, sea_location)

    return plane
    
# Create an island.
island_plane = create_island(ISLAND_NAME)

# CAMERA STUFF
target = bpy.data.objects['Empty2']
#                       Y between -3.0 and 3.0         Z between 1.0 and 2.0
target.location = (0.0, (random.random() - 0.5) * 6.0, 0.5 + random.random() * 2.0)

print(island_plane.name)
activate_object(island_plane)
print(bpy.context.active_object)
get_me_mode('EDIT')
treetop_position = place_tree(bmesh.from_edit_mesh(bpy.context.active_object.data))
make_tree_top(treetop_position)

get_me_mode('OBJECT')
bpy.ops.object.select_all(action='DESELECT')


# RENDERING PARAMETERS
def set_render_options():
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.sampling_pattern = 'SOBOL'
    bpy.context.scene.cycles.film_exposure = 1.9
    bpy.context.scene.cycles.samples = 2
    bpy.context.scene.render.threads = 1
    bpy.context.scene.render.filepath = '//../automation/cycles/' + str(time()) + ".png"
    bpy.context.scene.render.use_overwrite = False
    
    print(bpy.context.scene.render.filepath)

# RENDER
set_render_options()
#bpy.ops.render.render()
