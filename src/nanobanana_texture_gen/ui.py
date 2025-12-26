
import bpy


# PropertyGroups for multiple reference images
class NanoBananaFileRefItem(bpy.types.PropertyGroup):
    """Single file path reference item."""
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Path to reference image file",
        subtype='FILE_PATH',
        default=""
    )


class NanoBananaImageRefItem(bpy.types.PropertyGroup):
    """Single Blender image reference item."""
    image_name: bpy.props.StringProperty(
        name="Image Name",
        description="Name of Blender image datablock",
        default=""
    )


def register_properties():
    """Register properties to WindowManager."""
    bpy.types.WindowManager.nanobanana_show_history = bpy.props.BoolProperty(
        name="Show History",
        default=False
    )

    # Multiple file references
    bpy.types.WindowManager.nanobanana_file_refs = bpy.props.CollectionProperty(
        type=NanoBananaFileRefItem
    )

    # Multiple image references
    bpy.types.WindowManager.nanobanana_image_refs = bpy.props.CollectionProperty(
        type=NanoBananaImageRefItem
    )


def unregister_properties():
    """Unregister properties from WindowManager."""
    props = [
        'nanobanana_image_refs',
        'nanobanana_file_refs',
        'nanobanana_show_history',
    ]
    for prop in props:
        if hasattr(bpy.types.WindowManager, prop):
            delattr(bpy.types.WindowManager, prop)