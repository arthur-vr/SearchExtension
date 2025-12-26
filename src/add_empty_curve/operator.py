import bpy
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_add_empty_curve(bpy.types.Operator):
    """Add an Empty Curve to the scene"""
    bl_idname = "search_extension.add_empty_curve"
    bl_label = "Add Empty Curve" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    curve_type: bpy.props.EnumProperty(
        name="Curve Type",
        description="Type of curve to add",
        items=[
            ('BEZIER', "Bezier", ""),
            ('NURBS', "NURBS", ""),
            ('POLY', "Poly", ""),
        ],
        default='BEZIER'
    )

    def execute(self, context):
        # Create a new curve data
        curve_data = bpy.data.curves.new(name="Curve", type='CURVE')
        curve_data.dimensions = '3D'
        
        # Create a new object with the curve data
        curve_obj = bpy.data.objects.new("Curve", curve_data)
        
        # Link the object to the current collection
        context.collection.objects.link(curve_obj)
        
        # Set as active and select
        context.view_layer.objects.active = curve_obj
        curve_obj.select_set(True)
        
        self.report({'INFO'}, f"Added Empty Curve: {curve_obj.name}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


