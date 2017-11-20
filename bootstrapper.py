import bpy
import sys
""" """
# Folder where all the scripts live.
# Change this if it's different from where you .blend lives.
directory = bpy.path.abspath("//")
if not directory in sys.path:
    sys.path.append(directory)

import cycles_island
