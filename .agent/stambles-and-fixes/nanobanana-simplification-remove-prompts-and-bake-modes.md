## Stumbling Point

NanoBanana implementation was overly complex with these issues:

1. **Unnecessary Prompt System**
   - Multiple prompt fields: `prompt`, `negative_prompt`, `full_prompt`
   - Template selection feature existed
   - Complex prompt synchronization logic
   - Actually only wanted to generate textures from reference images

2. **Too Many Bake Modes**
   - ALBEDO (NumPy rasterization)
   - COMBINED (full shading)
   - DIFFUSE (Diffuse lighting)
   - VERTEX_COLOR (vertex colors)
   - Actually only wanted to use VERTEX_COLOR

3. **Errors After Deletion**
   - Deleted prompt-related methods, but `invoke()` was still calling `_ensure_full_prompt_initialized()`
   - `AttributeError: 'NanoBananaTextureGenOperator' object has no attribute '_ensure_full_prompt_initialized'`

## Solution

### 1. Complete Removal of Prompt System

**Deleted Properties:**
```python
# Before
prompt: StringProperty(...)
negative_prompt: StringProperty(...)
full_prompt: StringProperty(...)
full_prompt_customized: BoolProperty(...)
reset_full_prompt_trigger: BoolProperty(...)
prompt_template: EnumProperty(...)

# After
# All these properties removed
```

**Deleted Callback Functions:**
```python
# Deleted
def _on_prompt_part_update(self, context): ...
def _on_full_prompt_edit(self, context): ...
def _on_reset_full_prompt_trigger(self, context): ...
def _on_prompt_template_selected(self, context): ...
```

**Deleted Helper Methods:**
```python
# Deleted
def _build_full_prompt(self): ...
def _sync_full_prompt_from_parts(self, force=False): ...
def _ensure_full_prompt_initialized(self): ...
def _apply_prompt_template(self, text): ...
```

**Deleted Constants:**
```python
# Deleted
DEFAULT_FULL_PROMPT = "..."
PRESET_PROMPTS = [...]
```

**execute() Method Changes:**
```python
# Before:
self._ensure_full_prompt_initialized()
full_prompt = self.full_prompt
...
args=(self.api_key, actual_model, full_prompt, image_path)

# After:
prompt = ""  # Empty prompt - generate from image only
...
args=(self.api_key, actual_model, prompt, image_path)
```

**UI Removal:**
```python
# Before:
full_prompt_col = layout.column(align=True)
header = full_prompt_col.row(align=True)
header.label(text="Full Prompt")
header.prop(self, "reset_full_prompt_trigger", text="Default", toggle=True, icon='FILE_REFRESH')
header.prop(self, "prompt_template", text="")
full_prompt_col.prop(self, "full_prompt", text="")

# After:
# Completely removed
```

### 2. Bake Mode Simplification

**Removed bake_mode Property:**
```python
# Before:
bake_mode: EnumProperty(
    name="Bake Mode",
    items=[
        ("ALBEDO", ...),
        ("COMBINED", ...),
        ("DIFFUSE", ...),
        ("VERTEX_COLOR", ...),
    ],
    default="COMBINED"
)

# After:
# Property itself removed
```

**Simplified bake_uv_reference() Function:**
```python
# Before:
def bake_uv_reference(obj, resolution=1024, bake_mode="ALBEDO"):
    if bake_mode in ("COMBINED", "DIFFUSE", "VERTEX_COLOR"):
        return _bake_with_cycles(obj, resolution, bake_mode)
    # NumPy rasterization processing...

# After:
def bake_uv_reference(obj, resolution=1024):
    # Always use VERTEX_COLOR bake
    return _bake_with_cycles(obj, resolution, "VERTEX_COLOR")
```

**Deleted Functions:**
```python
# Removed NumPy-based UV rasterization implementation
def _triangulate_polygon(uv_coords): ...
def _fill_triangle(img_array, triangle, resolution): ...
```

**Simplified execute() Method:**
```python
# Before:
bake_mode_names = {...}
bake_mode_name = bake_mode_names.get(self.bake_mode, self.bake_mode)
self.report({'INFO'}, f"Baking {bake_mode_name} of selected object...")
image_path = bake_uv_reference(source_obj, resolution=1024, bake_mode=self.bake_mode)

# After:
self.report({'INFO'}, f"Baking vertex colors of selected object...")
image_path = bake_uv_reference(source_obj, resolution=1024)
```

**UI Removal:**
```python
# Before:
box = layout.box()
box.label(text="Will render selected object", icon='INFO')
box.prop(self, "bake_mode")

# After:
# RENDER mode - no additional UI needed
```

### 3. invoke() Method Error Fix

**Problem Location:**
```python
# Before (error):
def invoke(self, context, event):
    self._load_persistent_settings()
    self._ensure_full_prompt_initialized()  # This line causes AttributeError
    return context.window_manager.invoke_props_dialog(self, width=400)

# After (fixed):
def invoke(self, context, event):
    self._load_persistent_settings()
    return context.window_manager.invoke_props_dialog(self, width=400)
```

### 4. Persistence Updates

**Simplified _load_persistent_settings():**
```python
# Before:
self._suppress_full_prompt_update = True
self.prompt = storage.get(KEY_PROMPT, "")
self.negative_prompt = storage.get(KEY_NEGATIVE_PROMPT, "")
self.full_prompt = storage.get(KEY_FULL_PROMPT, "")
self.full_prompt_customized = storage.get(KEY_FULL_PROMPT_CUSTOMIZED, False)
self._suppress_full_prompt_update = False
if not self.full_prompt:
    self.full_prompt_customized = False
    self._sync_full_prompt_from_parts(force=True)
self.bake_mode = storage.get(KEY_BAKE_MODE, "COMBINED")

# After:
# All removed
```

**Simplified _persist_current_settings():**
```python
# Before:
KEY_PROMPT: self.prompt,
KEY_NEGATIVE_PROMPT: self.negative_prompt,
KEY_FULL_PROMPT: self.full_prompt,
KEY_FULL_PROMPT_CUSTOMIZED: self.full_prompt_customized,
KEY_BAKE_MODE: self.bake_mode,

# After:
# All removed
```

**Updated History Saving:**
```python
# Before:
_generation_state['history_info'] = {
    'prompt': self.prompt,
    'negative_prompt': self.negative_prompt,
    'model_version': actual_model,
    'seed': self.seed,
    'reference_info': reference_info
}

# After:
_generation_state['history_info'] = {
    'model_version': actual_model,
    'seed': self.seed,
    'reference_info': reference_info
}

# When adding to history:
storage.add_prompt_to_history(
    prompt="",  # Empty prompt
    negative_prompt="",
    model_version=hist_info['model_version'],
    seed=hist_info['seed'],
    reference_info=hist_info['reference_info']
)
```

### 5. Removed Unnecessary Imports

```python
# Before:
import numpy as np
from mathutils.geometry import intersect_point_tri_2d
from mathutils import Vector
from bpy.props import StringProperty, IntProperty, EnumProperty, BoolProperty, PointerProperty

# After:
# Removed numpy, mathutils-related imports
# Also removed PointerProperty (not used)
from bpy.props import StringProperty, IntProperty, EnumProperty, BoolProperty
```

## Key Points

1. **Simplification Strategy**
   - Prompts completely unnecessary -> Send empty string and generate from reference image only
   - Only use VERTEX_COLOR bake mode -> Remove the property entirely

2. **Cautions When Deleting**
   - When removing properties, update ALL locations referencing those properties
   - `invoke()`, `execute()`, `draw()`, `_load_persistent_settings()`, `_persist_current_settings()`, etc.
   - Remove all callback functions and helper methods

3. **Error Cause**
   - Deleting a method without removing its call sites causes `AttributeError`
   - Always search (Grep) the entire codebase to verify deleted method names aren't still referenced

4. **Current Behavior**
   - Uses only reference images (vertex color bake) for texture generation
   - Prompt is empty string
   - Minimal UI (Reference Mode, API Key, Model, Seed only)

## Debugging Methods

1. **When AttributeError Occurs:**
   - Identify the deleted method name from error message
   - Grep all files
   - Remove or fix all call sites

2. **Property-Related Errors:**
   - Check all `self.xxx` format references
   - Check UI `layout.prop(self, "xxx")` calls
   - Check Persistence `storage.get(KEY_XXX)` calls

3. **Verification Commands:**
   ```bash
   # Search for deleted method names
   grep -r "_ensure_full_prompt_initialized" .
   grep -r "self.prompt" .
   grep -r "self.bake_mode" .
   ```
