import bpy
from . import operator


def menu_func(self, context):
    self.layout.operator(operator.SEARCHEXT_OT_render_save_image.bl_idname)


def register():
    operator.register_scene_properties()
    bpy.utils.register_class(operator.SEARCHEXT_OT_render_save_image)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(operator.SEARCHEXT_OT_render_save_image)
    operator.unregister_scene_properties()
