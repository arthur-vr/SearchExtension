"""Storage singleton and helper utilities."""

import os
from ..external_storage import NanoBananaTextureGenExternalStorage

_STORAGE_INSTANCE = None


def get_persistent_storage():
    """Get or create the persistent storage instance.

    Returns:
        NanoBananaTextureGenExternalStorage: Storage instance
    """
    global _STORAGE_INSTANCE
    if _STORAGE_INSTANCE is None:
        _STORAGE_INSTANCE = NanoBananaTextureGenExternalStorage()
    return _STORAGE_INSTANCE


def format_reference_info(ref_info):
    """Return a short label and path for the stored reference info.

    Args:
        ref_info: Reference information dictionary

    Returns:
        tuple: (label, path) or (None, None) if invalid
    """
    if not isinstance(ref_info, dict):
        return None, None

    mode = ref_info.get("mode", "")
    mode_label = "UV Bake" if mode == "RENDER" else "File" if mode == "FILE" else "Image" if mode == "IMAGE" else mode

    object_name = ref_info.get("object_name") or ""
    saved_path = ref_info.get("saved_path") or ref_info.get("path") or ""
    filename = os.path.basename(saved_path) if saved_path else ""

    parts = [part for part in [mode_label, object_name, filename] if part]
    label = " | ".join(parts) if parts else None
    return label, saved_path
