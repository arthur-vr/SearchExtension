## Stumbling Point

Operator properties (API Key, Prompt, etc.) were reset every time, requiring users to re-enter them. Blender properties are volatile and are lost after operator execution.

## Solution

Implement external storage using JSON files to persist settings:

```python
# external_storage.py
class NanoBananaTextureGenExternalStorage:
    def __init__(self):
        self.file_path = os.path.join(
            bpy.utils.user_resource('SCRIPTS'),
            "addons",
            f"{ADDON_NAME}_{ADDON_VERSION}_{SERVICE_NAME}.json"
        )
        self.data = self.load_data()

    def save_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

# operator.py
def invoke(self, context, event):
    self._load_persistent_settings()  # Load settings from JSON
    return context.window_manager.invoke_props_dialog(self)

def execute(self, context):
    self._persist_current_settings()  # Save settings to JSON
    # ... execution logic
```

Storage location: `%APPDATA%\Blender Foundation\Blender\X.X\scripts\addons\{addon_name}.json`

Reference implementation: `src/render_save_image/external_storage.py`
