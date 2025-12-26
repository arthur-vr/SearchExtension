import bpy
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_add_image_node(bpy.types.Operator):
    """Add material with image node to selected objects"""
    bl_idname = "search_extension.add_image_node"
    bl_label = "Add Image Node" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the active image from the Image Editor (if any)
        active_image = None
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        active_image = space.image
                        break
                if active_image:
                    break
        
        # Process selected objects
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'ERROR'}, "No mesh objects selected")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            self._add_material_with_image(obj, active_image)
        
        if active_image:
            self.report({'INFO'}, f"Added image material to {len(selected_objects)} object(s)")
        else:
            self.report({'INFO'}, f"Added empty image node to {len(selected_objects)} object(s)")
        return {'FINISHED'}
    
    def _add_material_with_image(self, obj, image):
        """Add or update material with Principled BSDF and Image Texture node"""
        # Check if object already has a material
        if obj.data.materials:
            mat = obj.data.materials[0]
        else:
            # Create new material
            mat = bpy.data.materials.new(name=f"{obj.name}_Material")
            obj.data.materials.append(mat)
        
        # Enable nodes
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear existing nodes
        nodes.clear()
        
        # Create Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (300, 0)
        
        # Create Principled BSDF node
        principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_node.location = (0, 0)
        
        # Create Image Texture node
        image_node = nodes.new(type='ShaderNodeTexImage')
        image_node.location = (-300, 0)
        # Set image only if one is provided
        if image:
            image_node.image = image
        
        # Connect nodes: Image -> Principled BSDF -> Output
        links.new(image_node.outputs['Color'], principled_node.inputs['Base Color'])
        links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
