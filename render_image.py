import os
import time

def render():
    print("Rendering new image...")
    
    time_handle = str(time.time())
    
    render = os.system("./blender/blender -b auto_frogtree_5.blend -P bootstrapper.py -o //cycles/" + time_handle + " -f 1 > /dev/null")

if __name__ == "__main__":
    print(render())
