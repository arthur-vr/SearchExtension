"""Image handling utilities for texture generation."""

import bpy
import os
import time
import base64
import tempfile


def ensure_image_file(image, name_hint="image_ref"):
    """Ensure a Blender image has a file path; export to temp if needed.

    Args:
        image: Blender image object
        name_hint: Base name for temporary file

    Returns:
        tuple: (path, created_temp) where created_temp is True if a temp file was created

    Raises:
        RuntimeError: If no image provided or export fails
    """
    if not image:
        raise RuntimeError("No image provided")

    abs_path = bpy.path.abspath(image.filepath or image.filepath_raw or "")
    if abs_path and os.path.exists(abs_path):
        return abs_path, False

    # Fall back to exporting a temp copy (packed or unsaved image)
    temp_dir = tempfile.gettempdir()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    ext = ".png"
    try:
        fmt = (image.file_format or "").lower()
        if fmt == "jpeg":
            ext = ".jpg"
        elif fmt:
            ext = f".{fmt}"
    except Exception:
        pass

    temp_path = os.path.join(temp_dir, f"{name_hint}_{timestamp}{ext}")

    try:
        try:
            image.save_render(filepath=temp_path)
        except TypeError:
            image.save_render(temp_path)
        except Exception:
            raise
    except Exception:
        # Fallback: temporarily set filepath_raw and save
        orig_path = image.filepath_raw
        try:
            image.filepath_raw = temp_path
            image.save()
        finally:
            image.filepath_raw = orig_path

    if not os.path.exists(temp_path):
        raise RuntimeError("Could not export the selected image")

    return temp_path, True


def save_image_to_blender(image_data_base64, image_name):
    """Save base64 image data to Blender and return the image object.

    Args:
        image_data_base64: Base64 encoded image data
        image_name: Name for the Blender image

    Returns:
        bpy.types.Image: Loaded Blender image object
    """
    # Decode base64 image
    image_bytes = base64.b64decode(image_data_base64)

    # Save to temp file first
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"{image_name}.png")

    with open(temp_file, 'wb') as f:
        f.write(image_bytes)

    # Load into Blender
    if image_name in bpy.data.images:
        img = bpy.data.images[image_name]
        img.filepath = temp_file
        img.reload()
    else:
        img = bpy.data.images.load(temp_file, check_existing=False)
        img.name = image_name

    # Pack the image so it's embedded in the blend file
    img.pack()

    # Clean up temp file
    try:
        os.remove(temp_file)
    except OSError:
        pass

    return img


def set_image_active_in_editor(image):
    """Set the image as active in all Image Editor windows.

    Args:
        image: Blender image object to set as active
    """
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        space.image = image


def build_texture_name(prefix, append_timestamp=True):
    """Build a texture name with optional timestamp.

    Args:
        prefix: Base name prefix
        append_timestamp: Whether to append timestamp

    Returns:
        str: Generated texture name
    """
    safe_prefix = prefix.strip() or "nanobanana_texture"
    if append_timestamp:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return f"{safe_prefix}_{timestamp}"
    return safe_prefix
