import bpy
from . import operator

def menu_func(self, context):
    self.layout.operator(operator.SEARCHEXT_OT_add_empty_curve.bl_idname)

def register():
    bpy.utils.register_class(operator.SEARCHEXT_OT_add_empty_curve)
    bpy.types.VIEW3D_MT_curve_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(operator.SEARCHEXT_OT_add_empty_curve)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_func)


