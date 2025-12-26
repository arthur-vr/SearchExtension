import bpy
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_input_console(bpy.types.Operator):
    """Open a console input dialog"""
    bl_idname = "search_extension.input_console"
    bl_label = "Input Console" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    text_input: bpy.props.StringProperty(
        name="Input",
        description="Text to print to console",
        default=""
    )

    def execute(self, context):
        print(f"Input Console: {self.text_input}")
        self.report({'INFO'}, f"Console Output: {self.text_input}")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
