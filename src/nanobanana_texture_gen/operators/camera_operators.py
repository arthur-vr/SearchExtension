"""Camera-related operators."""

import bpy
import os
import time
from bpy.types import Operator
from ..._commons.constants import ADDON_LABEL_SUFFIX
from ..external_storage import NanoBananaTextureGenExternalStorage, KEY_USE_WORKBENCH


class NanoBananaFocusCameraOperator(Operator):
    """Focus view on active camera."""
    bl_idname = "nanobanana.focus_camera"
    bl_label = "Focus on Camera" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        if not scene.camera:
            self.report({'ERROR'}, "No active camera in scene")
            return {'CANCELLED'}

        # Set view to camera
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.region_3d.view_perspective = 'CAMERA'
                        break
                break

        self.report({'INFO'}, f"Focused on camera: {scene.camera.name}")
        return {'FINISHED'}


class NanoBananaAddCameraOperator(Operator):
    """Add a new camera and set it as active."""
    bl_idname = "nanobanana.add_camera"
    bl_label = "Add Camera" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.camera_add()
        cam_obj = context.active_object
        context.scene.camera = cam_obj
        self.report({'INFO'}, f"Added and set active camera: {cam_obj.name}")
        return {'FINISHED'}


class NanoBananaRenderCameraOperator(Operator):
    """Render camera view and save as Blender image."""
    bl_idname = "nanobanana.render_camera"
    bl_label = "Render Camera View" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        from ..camera_utils import render_camera_view

        scene = context.scene
        if not scene.camera:
            self.report({'ERROR'}, "No active camera in scene")
            return {'CANCELLED'}

        # Get workbench setting
        storage = NanoBananaTextureGenExternalStorage()
        use_workbench = storage.get(KEY_USE_WORKBENCH, True)

        engine_name = "Workbench" if use_workbench else "Cycles"
        self.report({'INFO'}, f"Rendering with {engine_name} from '{scene.camera.name}'...")

        try:
            temp_path = render_camera_view(scene, resolution=1024, samples=16, use_workbench=use_workbench)
        except Exception as e:
            self.report({'ERROR'}, f"Camera render failed: {str(e)}")
            return {'CANCELLED'}

        # Load into Blender and set active
        image_name = f"Camera_{scene.camera.name}_{int(time.time())}"
        img = bpy.data.images.load(temp_path)
        img.name = image_name
        img.pack()

        # Set active in Image Editors
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                area.spaces.active.image = img

        # Auto-add to image refs list
        wm = context.window_manager
        if hasattr(wm, 'nanobanana_image_refs'):
            exists = any(item.image_name == image_name for item in wm.nanobanana_image_refs)
            if not exists and len(wm.nanobanana_image_refs) < 14:
                new_ref = wm.nanobanana_image_refs.add()
                new_ref.image_name = image_name
                self.report({'INFO'}, f"Added '{image_name}' to References")

        # Clean up temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

        self.report({'INFO'}, f"Camera rendered: {image_name}")
        return {'FINISHED'}


class NanoBananaToggleWorkbenchOperator(Operator):
    """Toggle Workbench render mode for camera."""
    bl_idname = "nanobanana.toggle_workbench"
    bl_label = "Toggle Workbench Mode" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER'}

    def execute(self, context):
        storage = NanoBananaTextureGenExternalStorage()
        current = storage.get(KEY_USE_WORKBENCH, True)
        storage.set(KEY_USE_WORKBENCH, not current)
        return {'FINISHED'}
