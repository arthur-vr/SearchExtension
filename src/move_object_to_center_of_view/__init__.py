import bpy
from . import operator

def menu_func(self, context):
    self.layout.operator(operator.SEARCHEXT_OT_move_object_to_center_of_view.bl_idname)

def register():
    bpy.utils.register_class(operator.SEARCHEXT_OT_move_object_to_center_of_view)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(operator.SEARCHEXT_OT_move_object_to_center_of_view)
    bpy.types.VIEW3D_MT_object.remove(menu_func)