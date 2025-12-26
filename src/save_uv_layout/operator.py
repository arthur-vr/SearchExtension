import bpy
import os
import tempfile
import numpy as np
from mathutils.geometry import intersect_point_tri_2d
from mathutils import Vector
from .._commons.constants import ADDON_LABEL_SUFFIX

class SEARCHEXT_OT_save_uv_layout(bpy.types.Operator):
    """Save UV Layout to a new Blender Image"""
    bl_idname = "search_extension.save_uv_layout"
    bl_label = "Save UV Layout to Image" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    resolution: bpy.props.IntProperty(
        name="Resolution",
        default=1024,
        min=512,
        max=8192,
        description="Resolution of the UV layout image"
    )
    
    create_preview_plane: bpy.props.BoolProperty(
        name="Create Preview Plane",
        default=False,
        description="Create a plane with the UV layout image displayed using emission shader"
    )
    
    bake_alpha: bpy.props.BoolProperty(
        name="Bake Alpha",
        default=True,
        description="Export UV layout with alpha channel (transparency)"
    )
    
    show_edge_lines: bpy.props.BoolProperty(
        name="Show Edge Lines",
        default=False,
        description="Show UV edge lines. When OFF, only the fill (baked alpha) is displayed"
    )

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a Mesh")
            return {'CANCELLED'}
        
        if not obj.data.uv_layers:
            self.report({'ERROR'}, "Object has no UV layers")
            return {'CANCELLED'}

        # Remember original mode
        original_mode = obj.mode
        
        try:
            if self.show_edge_lines:
                # Use standard export with edge lines
                img = self._export_with_edge_lines(context, obj)
            else:
                # Generate fill-only image without edge lines
                img = self._create_uv_fill_image(obj)
            
            if img is None:
                return {'CANCELLED'}
                
            self.report({'INFO'}, f"Created Image: {img.name}")
            
            # Create preview plane if checkbox is enabled
            if self.create_preview_plane:
                self._create_preview_plane(context, img)
            
            # Set the created image as active in all Image Editor spaces
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    for space in area.spaces:
                        if space.type == 'IMAGE_EDITOR':
                            space.image = img
                
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create UV layout: {e}")
            if obj.mode != original_mode:
                bpy.ops.object.mode_set(mode=original_mode)
            return {'CANCELLED'}
        
        # Restore mode
        if obj.mode != original_mode:
            bpy.ops.object.mode_set(mode=original_mode)

        return {'FINISHED'}
    
    def _export_with_edge_lines(self, context, obj):
        """Export UV layout using standard Blender export (with edge lines)"""
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"{obj.name}_UV_Layout.png")
        
        original_mode = obj.mode
        
        # Switch to Edit Mode and select all faces
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Export layout with optional alpha baking
        export_params = {
            'filepath': temp_path,
            'size': (self.resolution, self.resolution),
            'opacity': 0.25
        }
        
        # If bake_alpha is enabled, modify export settings for alpha channel
        if self.bake_alpha:
            export_params['opacity'] = 1.0
        
        bpy.ops.uv.export_layout(**export_params)
        
        # Restore mode
        bpy.ops.object.mode_set(mode=original_mode)
        
        # Load the image into Blender
        img = bpy.data.images.load(temp_path)
        img.name = f"{obj.name}_UV_Layout"
        img.pack()
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except:
            pass
        
        return img
    
    def _create_uv_fill_image(self, obj):
        """Create UV fill image without edge lines using NumPy rasterization"""
        resolution = self.resolution
        
        # Create empty image array (RGBA) - use white fill with alpha
        # Initialize with transparent pixels
        img_array = np.zeros((resolution, resolution, 4), dtype=np.float32)
        
        # Get mesh data
        mesh = obj.data
        uv_layer = mesh.uv_layers.active
        
        if not uv_layer:
            self.report({'ERROR'}, "No active UV layer found")
            return None
        
        # Process each polygon
        for poly in mesh.polygons:
            # Get UV coordinates for this polygon
            uv_coords = []
            for loop_idx in poly.loop_indices:
                uv = uv_layer.data[loop_idx].uv
                uv_coords.append(Vector((uv.x, uv.y)))
            
            # Triangulate polygon if it has more than 3 vertices
            triangles = self._triangulate_polygon(uv_coords)
            
            # Fill each triangle
            for tri in triangles:
                self._fill_triangle(img_array, tri, resolution)
        
        # Create Blender image
        img = bpy.data.images.new(
            name=f"{obj.name}_UV_Fill",
            width=resolution,
            height=resolution,
            alpha=True
        )
        
        # Blender expects pixels in row-major order from bottom-left
        # Flatten and set pixels (RGBA format)
        img.pixels = img_array.flatten().tolist()
        img.pack()
        
        return img
    
    def _triangulate_polygon(self, uv_coords):
        """Convert polygon to triangles using fan triangulation"""
        triangles = []
        if len(uv_coords) < 3:
            return triangles
        
        # Fan triangulation from first vertex
        for i in range(1, len(uv_coords) - 1):
            triangles.append([uv_coords[0], uv_coords[i], uv_coords[i + 1]])
        
        return triangles
    
    def _fill_triangle(self, img_array, triangle, resolution):
        """Fill a triangle in the image array using scanline rasterization"""
        # Convert UV coordinates to pixel coordinates
        v0 = (triangle[0].x * resolution, triangle[0].y * resolution)
        v1 = (triangle[1].x * resolution, triangle[1].y * resolution)
        v2 = (triangle[2].x * resolution, triangle[2].y * resolution)
        
        # Get bounding box
        min_x = max(0, int(min(v0[0], v1[0], v2[0])))
        max_x = min(resolution - 1, int(max(v0[0], v1[0], v2[0])) + 1)
        min_y = max(0, int(min(v0[1], v1[1], v2[1])))
        max_y = min(resolution - 1, int(max(v0[1], v1[1], v2[1])) + 1)
        
        # Convert to Vector for intersection test
        t0 = Vector((v0[0], v0[1], 0))
        t1 = Vector((v1[0], v1[1], 0))
        t2 = Vector((v2[0], v2[1], 0))
        
        # Fill color (white with full alpha)
        fill_color = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        
        # Rasterize: check each pixel in bounding box
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                # Check if pixel center is inside triangle
                pt = Vector((x + 0.5, y + 0.5, 0))
                if intersect_point_tri_2d(pt, t0, t1, t2):
                    img_array[y, x] = fill_color
    
    def _create_preview_plane(self, context, image):
        """Create a plane with the UV layout image displayed using emission shader"""
        # Add a plane at the 3D cursor location
        bpy.ops.mesh.primitive_plane_add(
            size=2,
            location=context.scene.cursor.location,
            rotation=(0, 0, 0)
        )
        
        plane = context.active_object
        plane.name = f"{image.name}_Plane"
        
        # Create a new material
        mat = bpy.data.materials.new(name=f"{image.name}_Material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Create nodes
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (300, 0)
        
        emission_node = nodes.new(type='ShaderNodeEmission')
        emission_node.location = (0, 0)
        
        image_node = nodes.new(type='ShaderNodeTexImage')
        image_node.location = (-300, 0)
        image_node.image = image
        
        # Connect nodes: Image -> Emission -> Output
        links.new(image_node.outputs['Color'], emission_node.inputs['Color'])
        links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])
        
        # Assign material to plane
        if plane.data.materials:
            plane.data.materials[0] = mat
        else:
            plane.data.materials.append(mat)
        
        # Set viewport shading to Material Preview for immediate visibility
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
                        break

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
