from . import save_uv_layout
from . import render_save_image
from . import add_camera
from . import add_image_node
from . import sequence_arranger
from . import add_empty_object
from . import add_empty_curve
from . import add_empty_mesh
from . import nanobanana_texture_gen

# Module definitions
MODULE_REGISTRY = [
    {
        "prop": "enable_save_uv_layout",
        "name": "Save UV Layout",
        "module": save_uv_layout,
        "category": "UV / Image",
        "description": "Export the UV layout of the selected object to an image file."
    },
    {
        "prop": "enable_render_save_image",
        "name": "Render Save Image",
        "module": render_save_image,
        "category": "UV / Image",
        "description": "Render the current viewport or camera view and save it to a file."
    },
    {
        "prop": "enable_add_camera",
        "name": "Add Camera",
        "module": add_camera,
        "category": "Object",
        "description": "Add a new camera object to the scene."
    },
    {
        "prop": "enable_add_image_node",
        "name": "Add Image Node",
        "module": add_image_node,
        "category": "Shading",
        "description": "Add an image texture node to the current shader editor."
    },
    {
        "prop": "enable_sequence_arranger",
        "name": "Sequence Arranger",
        "module": sequence_arranger,
        "category": "Sequencer",
        "description": "Arrange sequences in the Video Sequence Editor."
    },
    {
        "prop": "enable_add_empty_object",
        "name": "Add Empty Object",
        "module": add_empty_object,
        "category": "Object",
        "description": "Add an empty object to the scene."
    },
    {
        "prop": "enable_add_empty_curve",
        "name": "Add Empty Curve",
        "module": add_empty_curve,
        "category": "Object",
        "description": "Add an empty curve object to the scene."
    },
    {
        "prop": "enable_add_empty_mesh",
        "name": "Add Empty Mesh",
        "module": add_empty_mesh,
        "category": "Object",
        "description": "Add an empty mesh object to the scene."
    },
    {
        "prop": "enable_nanobanana_texture_gen",
        "name": "Nanobanana Texture Gen",
        "module": nanobanana_texture_gen,
        "category": "Texture",
        "description": "Generate textures using Nanobanana features."
    },
]
