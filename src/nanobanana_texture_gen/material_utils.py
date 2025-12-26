"""Blender material creation and manipulation utilities."""

import bpy


def create_material_with_texture(obj, image):
    """Create material with image texture node and ensure it's connected to Principled BSDF.

    Args:
        obj: Blender object to apply material to
        image: Blender image to use as texture

    Returns:
        bpy.types.Material: Created or updated material
    """
    # Check if object already has a material
    mat = None
    if obj.data.materials and len(obj.data.materials) > 0 and obj.data.materials[0] is not None:
        mat = obj.data.materials[0]
        # If material doesn't use nodes, enable it
        if not mat.use_nodes:
            mat.use_nodes = True

    if mat is None:
        # Create new material
        mat = bpy.data.materials.new(name=f"{obj.name}_NanoBanana")
        mat.use_nodes = True
        if len(obj.data.materials) == 0:
            obj.data.materials.append(mat)
        else:
            obj.data.materials[0] = mat

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Find or create Principled BSDF node
    principled = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled = node
            break

    if not principled:
        # No Principled BSDF, create basic setup
        nodes.clear()
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (300, 0)

        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)

        links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])

    # Find existing Image Texture node or create new one
    image_node = None
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            image_node = node
            break

    if image_node:
        # Update existing image texture node
        image_node.image = image
    else:
        # Create new Image Texture node
        image_node = nodes.new(type='ShaderNodeTexImage')
        image_node.location = (principled.location.x - 300, principled.location.y)
        image_node.image = image

    # Ensure connection to Principled BSDF Base Color
    base_color_input = principled.inputs['Base Color']

    # Check if already connected
    is_connected = False
    for link in base_color_input.links:
        if link.from_node == image_node and link.from_socket == image_node.outputs['Color']:
            is_connected = True
            break

    # If not connected, remove existing connections and create new one
    if not is_connected:
        # Remove any existing connections to Base Color
        for link in list(base_color_input.links):
            links.remove(link)
        # Connect image node to Base Color
        links.new(image_node.outputs['Color'], base_color_input)

    # Set as active node
    nodes.active = image_node

    return mat
