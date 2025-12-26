import bpy
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_move_object_to_center_of_view(bpy.types.Operator):
    """Move selected object(s) to the center of the current 3D viewport"""
    bl_idname = "search_extension.move_object_to_center_of_view"
    bl_label = "Move Object to Center of View (mocv)" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # Check if we're in a 3D viewport and have selected objects
        return (context.area and context.area.type == 'VIEW_3D' and 
                context.selected_objects and 
                context.space_data and 
                hasattr(context.space_data, 'region_3d'))

    def execute(self, context):
        # Get the 3D viewport's view center location
        space_data = context.space_data
        region_3d = space_data.region_3d
        
        if not region_3d:
            self.report({'ERROR'}, "No 3D view found")
            return {'CANCELLED'}
        
        # Get the view center location
        view_center = region_3d.view_location.copy()
        
        # Move all selected objects to the view center
        moved_count = 0
        for obj in context.selected_objects:
            obj.location = view_center
            moved_count += 1
        
        self.report({'INFO'}, f"Moved {moved_count} object(s) to view center")
        return {'FINISHED'}

