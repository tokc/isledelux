import os
import time

from config import *

def render():
    time_handle = str(time.time())

    render = os.system(BLENDER_PATH + " -b auto_frogtree_5.blend -P cycles_island.py -t 1 -f //cycles/" + time_handle + " -f 1")

if __name__ == "__main__":
    print(render())
