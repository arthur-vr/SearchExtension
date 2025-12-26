## Stumbling Point

Initially tried to render objects to create reference images, but encountered these problems:
1. Camera is required - cannot use without a camera in the scene
2. Render results don't match UV layout (camera angle dependent)
3. Generated textures don't map correctly to object UVs

## Solution

Use `bpy.ops.uv.export_layout()` instead of `bpy.ops.render.render()` to perform UV bake:

```python
def bake_uv_reference(obj, resolution=1024):
    # Switch to Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Export UV layout
    bpy.ops.uv.export_layout(
        filepath=temp_file,
        size=(resolution, resolution),
        opacity=1.0
    )
```

Benefits:
- No camera required
- Produces images that perfectly match the object's UV layout
- Generated textures map accurately to UVs

Reference implementation: `src/save_uv_layout/operator.py`
