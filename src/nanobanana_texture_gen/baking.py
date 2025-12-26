"""UV and vertex color baking functionality."""

import bpy
import os
import time
import tempfile


def _bake_with_cycles(obj, resolution, bake_mode):
    """Bake object using Cycles render engine.
    
    Args:
        obj: Blender mesh object to bake
        resolution: Output image resolution
        bake_mode: Bake mode (VERTEX_COLOR, COMBINED, DIFFUSE, NORMAL)
    """
    # Save original settings
    orig_engine = bpy.context.scene.render.engine
    orig_samples = bpy.context.scene.cycles.samples
    orig_selected = [o for o in bpy.context.scene.objects if o.select_get()]
    orig_material = None
    created_temp_material = False
    created_vertex_color = False
    
    try:
        # Set up render engine
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = 16

        # Create temporary bake image
        bake_image = bpy.data.images.new(
            name=f"temp_bake_{int(time.time())}",
            width=resolution,
            height=resolution,
            alpha=True
        )

        if bake_mode == 'VERTEX_COLOR':
             # Ensure object has vertex colors - create white if none exist
            if not obj.data.vertex_colors or len(obj.data.vertex_colors) == 0:
                vcol_layer = obj.data.vertex_colors.new(name="NanoBanana_temp_vcol")
                created_vertex_color = True
                for poly in obj.data.polygons:
                    for loop_idx in poly.loop_indices:
                        vcol_layer.data[loop_idx].color = (1.0, 1.0, 1.0, 1.0)

            active_vcol_name = obj.data.vertex_colors.active.name if obj.data.vertex_colors.active else obj.data.vertex_colors[0].name
            
            if len(obj.data.materials) > 0:
                orig_material = obj.data.materials[0]

            mat = bpy.data.materials.new(name="TempVertexColorBakeMaterial")
            mat.use_nodes = True
            created_temp_material = True
            
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            vcol_node = nodes.new('ShaderNodeVertexColor')
            vcol_node.layer_name = active_vcol_name
            emission_node = nodes.new('ShaderNodeEmission')
            output_node = nodes.new('ShaderNodeOutputMaterial')
            
            mat.node_tree.links.new(vcol_node.outputs['Color'], emission_node.inputs['Color'])
            mat.node_tree.links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])
            
            img_node = nodes.new('ShaderNodeTexImage')
            img_node.image = bake_image
            nodes.active = img_node
            
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat
                
            active_bake_type = 'EMIT'
            
        else:
            # Standard Modes (COMBINED, DIFFUSE, NORMAL, etc.)
            # If object has no materials, create a temp one
            if not obj.data.materials:
                 mat = bpy.data.materials.new(name="TempBakeMaterial")
                 obj.data.materials.append(mat)
                 created_temp_material = True
            
            # Add bake target node to ALL materials
            # Blender requires the active image node to be set on all materials assigned to faces
            temp_nodes_to_remove = [] # List of (material, node) tuples
            
            for mat in obj.data.materials:
                if not mat: continue
                if not mat.use_nodes:
                    mat.use_nodes = True
                
                nodes = mat.node_tree.nodes
                img_node = nodes.new('ShaderNodeTexImage')
                img_node.name = "NanoBanana_Temp_Bake_Node"
                img_node.image = bake_image
                nodes.active = img_node
                temp_nodes_to_remove.append((mat, img_node))
            
            active_bake_type = bake_mode

        # Select only this object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Perform bake
        bpy.ops.object.bake(
            type=active_bake_type,
            use_clear=True,
            margin=4
        )
        
        # Save
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"nanobanana_ref_{int(time.time())}.png")
        bake_image.filepath_raw = temp_file
        bake_image.file_format = 'PNG'
        bake_image.save()
        
        bpy.data.images.remove(bake_image)
        
        if not os.path.exists(temp_file):
            raise RuntimeError(f"{bake_mode} bake failed")
            
        return temp_file

    finally:
        # Cleanup
        if created_vertex_color:
             vcol = obj.data.vertex_colors.get("NanoBanana_temp_vcol")
             if vcol: obj.data.vertex_colors.remove(vcol)
             
        if created_temp_material:
            if orig_material:
                if len(obj.data.materials) > 0:
                     obj.data.materials[0] = orig_material
                else:
                     obj.data.materials.append(orig_material)
            else:
                # Pure temp material, remove it
                if len(obj.data.materials) > 0 and obj.data.materials[0].name.startswith("Temp"):
                     obj.data.materials.pop(0)

            # Clean up datablocks
            temp_mats = [m for m in bpy.data.materials if m.name.startswith("TempVertexColorBakeMaterial") or m.name.startswith("TempBakeMaterial")]
            for m in temp_mats:
                bpy.data.materials.remove(m)
        
        # Remove temp nodes from standard materials
        if 'temp_nodes_to_remove' in locals():
            for mat, node in temp_nodes_to_remove:
                if mat and node:
                    try:
                        mat.node_tree.nodes.remove(node)
                    except:
                        pass # Node might be gone if material was temp and removed

        # Restore settings
        bpy.context.scene.render.engine = orig_engine
        if orig_engine == 'CYCLES':
            bpy.context.scene.cycles.samples = orig_samples
            
        bpy.ops.object.select_all(action='DESELECT')
        for o in orig_selected:
            if o: o.select_set(True)


def bake_uv_reference(obj, resolution=1024, bake_mode='VERTEX_COLOR'):
    """Create reference image using specified bake mode."""
    if not obj or obj.type != 'MESH':
        raise RuntimeError("Active object must be a Mesh")
    if not obj.data.uv_layers:
        raise RuntimeError("Object has no UV layers")
        
    return _bake_with_cycles(obj, resolution, bake_mode)
