import bpy
import sys
import random
from time import time

""" Run script and set up Blender environment for command line rendering. """

# Folder where all the scripts live.
# Change this if it's different from where your .blend lives.
directory = bpy.path.abspath("//")
if not directory in sys.path:
    sys.path.append(directory)

from config import *
import cycles_island

# RENDERING PARAMETERS
def set_render_options():
    sky = bpy.data.worlds['World'].node_tree.nodes['Sky Texture']
    # Make the sky point at the sun.
    sky.sun_direction = bpy.data.objects['Sun34587873456'].rotation_euler

    # Random amount of haziness.
    sky.turbidity = (random.random() * 9.0) + 1.0

    # Random reflected ground color.
    sky.ground_albedo = random.random()

    # Cycles options
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.sampling_pattern = 'SOBOL'
    bpy.context.scene.cycles.film_exposure = 1.9
    bpy.context.scene.cycles.samples = RENDER_SAMPLES
    bpy.context.scene.render.threads_mode = 'FIXED'
    bpy.context.scene.render.threads = 1
    bpy.context.scene.render.filepath = '//cycles/' + str(time()) + ".png"
    bpy.context.scene.render.use_overwrite = False

cycles_island.generate_scene()    

set_render_options()
