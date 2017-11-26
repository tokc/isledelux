import bpy


def get_me_mode(new_mode):
    # Blender throws an error if you try to set mode to the current mode.
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
