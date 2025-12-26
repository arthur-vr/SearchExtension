import bpy
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_add_empty_object(bpy.types.Operator):
    """Add an Empty Object to the scene"""
    bl_idname = "search_extension.add_empty_object"
    bl_label = "Add Empty Object" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    empty_type: bpy.props.EnumProperty(
        name="Empty Type",
        description="Type of empty object to add",
        items=[
            ('PLAIN_AXES', "Plain Axes", ""),
            ('ARROWS', "Arrows", ""),
            ('SINGLE_ARROW', "Single Arrow", ""),
            ('CIRCLE', "Circle", ""),
            ('CUBE', "Cube", ""),
            ('SPHERE', "Sphere", ""),
            ('CONE', "Cone", ""),
            ('IMAGE', "Image", ""),
        ],
        default='PLAIN_AXES'
    )

    def execute(self, context):
        bpy.ops.object.empty_add(type=self.empty_type)
        empty_obj = context.active_object
        self.report({'INFO'}, f"Added Empty Object: {empty_obj.name}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


