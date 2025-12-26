"""Camera rendering utilities for texture generation."""

import bpy
import os
import tempfile
import time


def render_camera_view(scene=None, resolution=1024, samples=16, use_workbench=False):
    """Render current camera view and return temp file path.
    
    Args:
        scene: Blender scene (defaults to current)
        resolution: Output resolution (square)
        samples: Render samples for Cycles
        use_workbench: If True, use Workbench engine instead of Cycles
        
    Returns:
        str: Path to rendered image file
        
    Raises:
        RuntimeError: If no camera or render fails
    """
    if scene is None:
        scene = bpy.context.scene
    
    # Validate camera exists
    if not scene.camera:
        raise RuntimeError("No active camera in scene. Please set a camera.")
    
    # Save original settings
    orig_engine = scene.render.engine
    orig_res_x = scene.render.resolution_x
    orig_res_y = scene.render.resolution_y
    orig_res_percent = scene.render.resolution_percentage
    orig_filepath = scene.render.filepath
    orig_file_format = scene.render.image_settings.file_format
    orig_samples = None
    
    if hasattr(scene, 'cycles'):
        orig_samples = scene.cycles.samples
    
    try:
        # Configure render settings
        if use_workbench:
            scene.render.engine = 'BLENDER_WORKBENCH'
        else:
            scene.render.engine = 'CYCLES'
        scene.render.resolution_x = resolution
        scene.render.resolution_y = resolution
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'PNG'
        
        if not use_workbench and hasattr(scene, 'cycles'):
            scene.cycles.samples = samples
        
        # Set output path
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"nanobanana_camera_{int(time.time())}.png")
        scene.render.filepath = temp_file
        
        # Perform render
        bpy.ops.render.render(write_still=True)
        
        if not os.path.exists(temp_file):
            raise RuntimeError("Camera render failed to create output file")
        
        return temp_file
        
    finally:
        # Restore original settings
        scene.render.engine = orig_engine
        scene.render.resolution_x = orig_res_x
        scene.render.resolution_y = orig_res_y
        scene.render.resolution_percentage = orig_res_percent
        scene.render.filepath = orig_filepath
        scene.render.image_settings.file_format = orig_file_format
        
        if orig_samples is not None and hasattr(scene, 'cycles'):
            scene.cycles.samples = orig_samples


def get_camera_info(scene=None):
    """Get information about the active camera.
    
    Args:
        scene: Blender scene (defaults to current)
        
    Returns:
        dict: Camera information or None if no camera
    """
    if scene is None:
        scene = bpy.context.scene
    
    if not scene.camera:
        return None
    
    cam = scene.camera
    return {
        'name': cam.name,
        'type': cam.data.type if cam.data else 'UNKNOWN',
        'lens': cam.data.lens if cam.data and hasattr(cam.data, 'lens') else None,
    }
