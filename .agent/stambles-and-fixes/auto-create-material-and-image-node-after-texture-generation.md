## Stumbling Point

After texture generation, users had to manually create a material, add an Image Texture node, and assign the generated image. This was tedious and provided poor UX.

## Solution

Automatically create/update materials and Image Texture nodes after texture generation:

```python
def create_material_with_texture(obj, image):
    # Create material if none exists
    if not obj.data.materials:
        mat = bpy.data.materials.new(name=f"{obj.name}_NanoBanana")
        mat.use_nodes = True
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]

    nodes = mat.node_tree.nodes

    # Update existing Image Texture node if present
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            node.image = image
            return mat

    # Create new node and connect to Principled BSDF
    principled = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if principled:
        image_node = nodes.new(type='ShaderNodeTexImage')
        image_node.image = image
        mat.node_tree.links.new(
            image_node.outputs['Color'],
            principled.inputs['Base Color']
        )
```

This ensures textures are immediately applied to objects after generation.

Reference implementation: `src/save_uv_layout/operator.py` `_create_preview_plane()` method
