"""Bake-related operators."""

import bpy
import os
import time
from bpy.props import EnumProperty
from bpy.types import Operator
from ..baking import bake_uv_reference
from ..material_utils import create_material_with_texture


class NanoBananaApplyBakeOperator(Operator):
    """Bake vertex colors and apply strictly to material (preview)."""
    bl_idname = "nanobanana.apply_bake_preview"
    bl_label = "Bake & Apply Preview"
    bl_options = {'REGISTER', 'UNDO'}

    bake_mode: EnumProperty(
        name="Bake Mode",
        items=[
            ("VERTEX_COLOR", "Vertex Color", ""),
            ("COMBINED", "Combined", ""),
            ("DIFFUSE", "Diffuse", ""),
            ("NORMAL", "Normal", ""),
        ],
        default="VERTEX_COLOR"
    )

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a Mesh")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Baking {self.bake_mode} for {obj.name}...")
        try:
            image_path = bake_uv_reference(obj, resolution=1024, bake_mode=self.bake_mode)
            if not image_path or not os.path.exists(image_path):
                 self.report({'ERROR'}, "Bake failed to produce image")
                 return {'CANCELLED'}

            # Load image into Blender
            image_name = f"Bake_{obj.name}_{int(time.time())}"
            img = bpy.data.images.load(image_path)
            img.name = image_name
            img.pack()

            # Apply to material
            create_material_with_texture(obj, img)

            # Update visible Image Editors
            for area in context.screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    area.spaces.active.image = img

            # Auto-add to image refs list
            wm = context.window_manager
            if hasattr(wm, 'nanobanana_image_refs'):
                # Check if not already in list
                exists = any(item.image_name == image_name for item in wm.nanobanana_image_refs)
                if not exists and len(wm.nanobanana_image_refs) < 14:
                    new_ref = wm.nanobanana_image_refs.add()
                    new_ref.image_name = image_name
                    self.report({'INFO'}, f"Added '{image_name}' to References")

            self.report({'INFO'}, f"Baked texture applied to {obj.name}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to apply bake: {str(e)}")
            return {'CANCELLED'}
