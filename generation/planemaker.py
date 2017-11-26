import bpy
import bmesh

import random
import math

from .utilities import get_me_mode

NUM_VERTS = 30

print("Hemlo.")

def generate_plane(name=None, iterate=False):
    get_me_mode('OBJECT')
    
    # Build 2D array of vertices.
    two_dimensions = [[(a, b, 0) for a in range(NUM_VERTS)] for b in range(NUM_VERTS)]
    
    # Make Z adjustments.
    # Highest point is sin(90)
    # Needs to end around sin(180)
    
    multiplier = 0.105
    
    print(len(two_dimensions))
    
    y = 0
    for row in two_dimensions:
        x = 0
        for vert in row:
            #print(math.sin(multiplier * vert[0]))
            two_dimensions[y][x] = (
                vert[0],
                vert[1],
                (random.random() - 0.5) + (math.sin(multiplier * vert[1]) * 3)
                )
            
            x += 1
        y += 1
    
    # Build a flat list of quads.
    faces = []

    for y in range(len(two_dimensions)):
        for x in range(len(two_dimensions[y])):
            if x < NUM_VERTS - 1 and y < NUM_VERTS - 1:
                faces.append(
                    (
                        x + (NUM_VERTS * y),
                        x + (NUM_VERTS * y) + 1,
                        x + (NUM_VERTS * (y + 1)) + 1,
                        x + (NUM_VERTS * (y + 1))
                    )
                )

    # Build a flat list of vertices.
    verts = [a for b in two_dimensions for a in b]

    # Put the vertices and faces into an object.
    bpy.ops.mesh.primitive_plane_add(radius=1, location=(0.0, 0.0, 0.0), enter_editmode=True)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete()
    
    object = bpy.context.active_object

    bm = bmesh.new()
    bm.from_mesh(object.data)

    for vert in verts:
        bm.verts.new(vert)
        
    bm.verts.ensure_lookup_table()

    for face in faces:
        bm.faces.new([bm.verts[x] for x in face])
    
    get_me_mode('OBJECT')
    
    bm.to_mesh(object.data)
    bm.free()
    
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    
    return object

if __name__ == "__main__":
    plane = generate_plane("name", True)

    plane.location.z = 1.0