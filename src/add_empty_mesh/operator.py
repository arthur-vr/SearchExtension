import bpy
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_add_empty_mesh(bpy.types.Operator):
    """Add an Empty Mesh (no vertices) to the scene"""
    bl_idname = "search_extension.add_empty_mesh"
    bl_label = "Add Empty Mesh" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Create a new mesh data with no vertices
        mesh_data = bpy.data.meshes.new(name="Mesh")
        
        # Create a new object with the mesh data
        mesh_obj = bpy.data.objects.new("Mesh", mesh_data)
        
        # Link the object to the current collection
        context.collection.objects.link(mesh_obj)
        
        # Set as active and select
        context.view_layer.objects.active = mesh_obj
        mesh_obj.select_set(True)
        
        self.report({'INFO'}, f"Added Empty Mesh: {mesh_obj.name}")
        return {'FINISHED'}


