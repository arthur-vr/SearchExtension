import bpy
import json
import os
from .._commons.constants import ADDON_NAME, ADDON_VERSION

SERVICE_NAME = "render_save_image"
KEY_FILE_PATH = "file_path"
KEY_NAME_INPUT = "name_input"
KEY_SET_ACTIVE = "set_active"
KEY_AUTO_REPEAT = "auto_repeat"
KEY_AUTO_REPEAT_INTERVAL = "auto_repeat_interval"
KEY_RESOLUTION_LEVEL = "resolution_level"
KEY_SAMPLE_LEVEL = "sample_level"
KEY_USE_JPEG_FORMAT = "use_jpeg_format"
KEY_JPEG_QUALITY_LEVEL = "jpeg_quality_level"
KEY_IMAGE_HASHES = "image_hashes"

DEFAULT_VALUE = {
    KEY_FILE_PATH: "",
    KEY_NAME_INPUT: "",
    KEY_SET_ACTIVE: True,
    KEY_AUTO_REPEAT: False,
    KEY_AUTO_REPEAT_INTERVAL: 2.0,
    KEY_RESOLUTION_LEVEL: 10,
    KEY_SAMPLE_LEVEL: 10,
    KEY_USE_JPEG_FORMAT: False,
    KEY_JPEG_QUALITY_LEVEL: 8,
    KEY_IMAGE_HASHES: {},
}


class RenderSaveImageExternalStorage:
    def __init__(self):
        self.file_path = os.path.join(
            bpy.utils.user_resource('SCRIPTS'),
            "addons",
            f"{ADDON_NAME}_{ADDON_VERSION}_{SERVICE_NAME}.json"
        )
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        merged = DEFAULT_VALUE.copy()
                        merged.update(loaded)
                        hashes = merged.get(KEY_IMAGE_HASHES)
                        if isinstance(hashes, dict):
                            merged[KEY_IMAGE_HASHES] = hashes.copy()
                        else:
                            merged[KEY_IMAGE_HASHES] = {}
                        return merged
            except Exception:
                pass
        default_copy = DEFAULT_VALUE.copy()
        default_copy[KEY_IMAGE_HASHES] = DEFAULT_VALUE[KEY_IMAGE_HASHES].copy()
        return default_copy

    def save_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save_data()

    def update(self, values):
        self.data.update(values)
        self.save_data()

    def get_image_hash(self, name):
        hashes = self.data.get(KEY_IMAGE_HASHES, {})
        return hashes.get(name)

    def set_image_hash(self, name, value):
        hashes = self.data.get(KEY_IMAGE_HASHES)
        if hashes is None:
            hashes = {}
            self.data[KEY_IMAGE_HASHES] = hashes
        hashes[name] = value
        self.save_data()