import bpy
from . import operator

def menu_func(self, context):
    self.layout.operator(operator.SEARCHEXT_OT_input_console.bl_idname)

def register():
    bpy.utils.register_class(operator.SEARCHEXT_OT_input_console)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(operator.SEARCHEXT_OT_input_console)
    bpy.types.VIEW3D_MT_object.remove(menu_func)