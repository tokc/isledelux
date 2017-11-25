import bpy

def get_me_mode(new_mode):
    try:
        bpy.ops.object.mode_set(mode=new_mode)

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

def select_only(thing):
    # Deselect everything and select only the named object.
    get_me_mode('OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    try:
        bpy.data.objects[thing].select = True
    except:
        pass