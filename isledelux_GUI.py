import bpy
import sys
import random
from time import time

""" Run script and set up Blender environment for manual operation. """

# Folder where all the scripts live.
# Change this if it's different from where your .blend lives.
directory = bpy.path.abspath("//")
if not directory in sys.path:
    sys.path.append(directory)

from config import *
import cycles_island

cycles_island.generate_scene()

# This is the stupidest thing I have ever seen. But apparently it's the easiest way to change the view to the camera.
next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D').spaces[0].region_3d.view_perspective = 'CAMERA'
bpy.ops.object.select_all(action='DESELECT')