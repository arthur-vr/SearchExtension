import bpy
import json
import os
import time
import shutil
from typing import Optional
from .._commons.constants import ADDON_NAME, ADDON_VERSION

SERVICE_NAME = "nanobanana_texture_gen"
KEY_REFERENCE_MODE = "reference_mode"
KEY_IMAGE_FILEPATH = "image_filepath"
KEY_PROMPT = "prompt"
KEY_NEGATIVE_PROMPT = "negative_prompt"
KEY_FULL_PROMPT = "full_prompt"
KEY_FULL_PROMPT_CUSTOMIZED = "full_prompt_customized"
KEY_SEED = "seed"
KEY_MODEL_VERSION = "model_version"
KEY_CUSTOM_MODEL_NAME = "custom_model_name"
KEY_BAKE_MODE = "bake_mode"
KEY_API_KEY = "api_key"
KEY_PROMPT_HISTORY = "prompt_history"
KEY_REFERENCE_INFO = "reference"
KEY_TEXTURE_PREFIX = "texture_prefix"
KEY_APPEND_TIMESTAMP = "append_timestamp"
KEY_IMAGE_DATA_NAME = "image_data_name"
KEY_USE_ACTIVE_OBJ = "use_active_object"
KEY_USE_WORKBENCH = "use_workbench"

DEFAULT_VALUE = {
    KEY_REFERENCE_MODE: "RENDER",
    KEY_IMAGE_FILEPATH: "",
    KEY_PROMPT: "",
    KEY_NEGATIVE_PROMPT: "",
    KEY_FULL_PROMPT: "Generate a high-quality seamless, tileable texture based on the provided reference image. Keep lighting neutral and avoid baked shadows.",
    KEY_FULL_PROMPT_CUSTOMIZED: False,
    KEY_SEED: 0,
    KEY_MODEL_VERSION: "gemini-2.5-flash-image",
    KEY_CUSTOM_MODEL_NAME: "",
    KEY_BAKE_MODE: "COMBINED",
    KEY_API_KEY: "",
    KEY_PROMPT_HISTORY: [],
    KEY_TEXTURE_PREFIX: "nanobanana_texture",
    KEY_APPEND_TIMESTAMP: True,
    KEY_IMAGE_DATA_NAME: "",
    KEY_USE_ACTIVE_OBJ: True,
    KEY_USE_WORKBENCH: True,
}


class NanoBananaTextureGenExternalStorage:
    def __init__(self):
        self.file_path = os.path.join(
            bpy.utils.user_resource('SCRIPTS'),
            "addons",
            f"{ADDON_NAME}_{ADDON_VERSION}_{SERVICE_NAME}.json"
        )
        self.reference_dir = os.path.join(
            os.path.dirname(self.file_path),
            f"{SERVICE_NAME}_references"
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
                        return merged
            except Exception:
                pass
        return DEFAULT_VALUE.copy()

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

    def _sanitize_name(self, name: str) -> str:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name or "")
        safe = safe.strip("_")
        return safe or "uv_bake"

    def _ensure_reference_dir(self) -> str:
        os.makedirs(self.reference_dir, exist_ok=True)
        return self.reference_dir

    def save_baked_reference(self, source_path: str, object_name: Optional[str] = None, name_hint: Optional[str] = None) -> Optional[str]:
        """Persist a copy of the baked UV reference so it can be inspected later."""
        if not source_path or not os.path.exists(source_path):
            return None

        try:
            reference_dir = self._ensure_reference_dir()
            ext = os.path.splitext(source_path)[1] or ".png"
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_name = self._sanitize_name(name_hint or object_name or "uv_bake")
            dest_path = os.path.join(reference_dir, f"{safe_name}_{timestamp}{ext}")
            shutil.copy2(source_path, dest_path)
            return dest_path
        except Exception:
            return None

    def add_prompt_to_history(self, prompt, negative_prompt="", model_version="", seed=0, reference_info=None):
        """Add a prompt to history with timestamp"""
        history = self.data.get(KEY_PROMPT_HISTORY, [])

        # Create history entry
        entry = {
            "timestamp": time.time(),
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "model_version": model_version,
            "seed": seed
        }

        if reference_info:
            entry[KEY_REFERENCE_INFO] = reference_info

        # Add to beginning of list (most recent first)
        history.insert(0, entry)

        self.data[KEY_PROMPT_HISTORY] = history
        self.save_data()

    def get_prompt_history(self, limit=None):
        """Get prompt history, optionally limited to N most recent entries"""
        history = self.data.get(KEY_PROMPT_HISTORY, [])
        # Ensure sorted by timestamp (newest first)
        history.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        if limit:
            return history[:limit]
        return history

    def delete_history_entry(self, index):
        """Delete a specific history entry by index"""
        history = self.data.get(KEY_PROMPT_HISTORY, [])
        if 0 <= index < len(history):
            history.pop(index)
            self.data[KEY_PROMPT_HISTORY] = history
            self.save_data()
            return True
        return False

    def clear_all_history(self):
        """Clear all prompt history"""
        self.data[KEY_PROMPT_HISTORY] = []
        self.save_data()
