## Stumbling Point

Blender addon UI was completely invisible.

**Symptoms:**
- Only some properties (like Reference Mode) appeared in operator dialogs
- API Key, Model Version, Full Prompt input fields were missing
- Blender console showed these errors:
  ```
  ValueError: bpy_struct "NANOBANANA_OT_generate_texture" registration error:
  'image_data' PointerProperty could not register because this type doesn't support data-block properties
  ```
  ```
  rna_uiItemR: property not found: NANOBANANA_OT_generate_texture.texture_prefix
  rna_uiItemR: property not found: NANOBANANA_OT_generate_texture.api_key
  rna_uiItemR: property not found: NANOBANANA_OT_generate_texture.full_prompt
  ```

**Root Cause:**
1. `Operator` classes don't support `PointerProperty` (pointers to data-blocks)
2. Registration of `image_data: PointerProperty(type=bpy.types.Image)` failed
3. Property registration error caused ALL properties to fail registration, making them invisible in UI
4. Additionally, `options={'MULTILINE'}` on `full_prompt` doesn't work correctly in Operators

## Solution

### 1. Remove PointerProperty

`Operator` classes cannot use `PointerProperty`. Instead, use `StringProperty` to store the image name and retrieve it with `bpy.data.images.get()`.

**Before:**
```python
image_data: PointerProperty(
    name="Image",
    description="Blender image to use as reference",
    type=bpy.types.Image,
    update=_on_image_data_update,
)

image_data_name: StringProperty(
    name="Image Name",
    description="Name of Blender image to use as reference",
    default="",
)
```

**After:**
```python
# Remove PointerProperty, use only StringProperty
image_data_name: StringProperty(
    name="Image Name",
    description="Name of Blender image to use as reference",
    default="",
)
```

### 2. Remove Unnecessary Callback Functions

Delete the `_on_image_data_update()` callback function.

### 3. Update UI Usage

**Before:**
```python
elif self.reference_mode == "IMAGE":
    layout.prop(self, "image_data")
    layout.prop_search(self, "image_data_name", bpy.data, "images", text="Image Name")
```

**After:**
```python
elif self.reference_mode == "IMAGE":
    layout.prop_search(self, "image_data_name", bpy.data, "images", text="Image")
```

### 4. Update Image Retrieval in execute()

**Before:**
```python
image = self.image_data or bpy.data.images.get(self.image_data_name)
```

**After:**
```python
image = bpy.data.images.get(self.image_data_name) if self.image_data_name else None
```

### 5. Remove MULTILINE Option

Remove `options={'MULTILINE'}` from `StringProperty`.

**Before:**
```python
full_prompt: StringProperty(
    name="Full Prompt",
    description="Final prompt sent to the API",
    default=DEFAULT_FULL_PROMPT,
    options={'MULTILINE'},
    update=_on_full_prompt_edit,
)
```

**After:**
```python
full_prompt: StringProperty(
    name="Full Prompt",
    description="Final prompt sent to the API",
    default=DEFAULT_FULL_PROMPT,
    update=_on_full_prompt_edit,
)
```

**Note:** Multi-line text input can be achieved by specifying `text=""` in the `draw()` method: `layout.prop(self, "full_prompt", text="")`

### 6. Add Safety to Update Callbacks

Add try-except to property `update` callbacks to prevent registration issues:

```python
def _on_full_prompt_edit(self, context):
    """Mark that the user manually edited full prompt."""
    try:
        if getattr(self, "_suppress_full_prompt_update", False):
            return
        self.full_prompt_customized = True
    except Exception:
        pass
```

## Key Points

1. **Operator vs Panel/PropertyGroup Limitations**
   - `Operator` classes cannot use `PointerProperty`
   - When data-block references are needed, store names in `StringProperty` and retrieve from `bpy.data.*`
   - `Panel` and `PropertyGroup` CAN use `PointerProperty`

2. **Scope of Property Registration Errors**
   - When one property fails to register, ALL properties in that class fail
   - When you see multiple "property not found" messages, check the first error ("see previous error")

3. **Debugging Methods**
   - Check errors in Blender's System Console (Window > Toggle System Console)
   - Add `print()` debugging to `draw()` method to see execution flow
   - Check if properties are registered: `hasattr(operator_instance, "property_name")`

4. **Implementing Multi-line Text Input**
   - Don't use `options={'MULTILINE'}`
   - Specify `text=""` parameter in `draw()` method for automatic multi-line display
   ```python
   layout.prop(self, "full_prompt", text="")  # Multi-line display
   ```
