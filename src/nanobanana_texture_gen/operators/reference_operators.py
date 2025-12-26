"""Reference list operators."""

from bpy.props import IntProperty
from bpy.types import Operator
from ..._commons.constants import ADDON_LABEL_SUFFIX


class NanoBananaAddFileRefOperator(Operator):
    """Add a file reference to the list."""
    bl_idname = "nanobanana.add_file_ref"
    bl_label = "Add File Reference" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager
        if len(wm.nanobanana_file_refs) >= 14:
            self.report({'WARNING'}, "Maximum 14 reference images allowed")
            return {'CANCELLED'}
        wm.nanobanana_file_refs.add()
        return {'FINISHED'}


class NanoBananaRemoveFileRefOperator(Operator):
    """Remove a file reference from the list."""
    bl_idname = "nanobanana.remove_file_ref"
    bl_label = "Remove File Reference" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    index: IntProperty(default=0)

    def execute(self, context):
        wm = context.window_manager
        if 0 <= self.index < len(wm.nanobanana_file_refs):
            wm.nanobanana_file_refs.remove(self.index)
        return {'FINISHED'}


class NanoBananaAddImageRefOperator(Operator):
    """Add an image reference to the list."""
    bl_idname = "nanobanana.add_image_ref"
    bl_label = "Add Image Reference" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager
        if len(wm.nanobanana_image_refs) >= 14:
            self.report({'WARNING'}, "Maximum 14 reference images allowed")
            return {'CANCELLED'}
        wm.nanobanana_image_refs.add()
        return {'FINISHED'}


class NanoBananaRemoveImageRefOperator(Operator):
    """Remove an image reference from the list."""
    bl_idname = "nanobanana.remove_image_ref"
    bl_label = "Remove Image Reference" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    index: IntProperty(default=0)

    def execute(self, context):
        wm = context.window_manager
        if 0 <= self.index < len(wm.nanobanana_image_refs):
            wm.nanobanana_image_refs.remove(self.index)
        return {'FINISHED'}
