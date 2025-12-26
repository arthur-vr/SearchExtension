"""NanoBanana texture generation operators.

This module re-exports all operators from the operators/ subpackage.
Each operator is organized by single responsibility in separate files.
"""

# Re-export all operators from the operators package
from .operators import (
    # Storage utilities
    get_persistent_storage,
    format_reference_info,
    # Bake
    NanoBananaApplyBakeOperator,
    # Camera
    NanoBananaFocusCameraOperator,
    NanoBananaAddCameraOperator,
    NanoBananaRenderCameraOperator,
    NanoBananaToggleWorkbenchOperator,
    # Text
    NanoBananaShowMessageOperator,
    NanoBananaCreatePromptTextOperator,
    NanoBananaOpenTextEditorOperator,
    # Settings
    NanoBananaSettingsOperator,
    # History
    NanoBananaCopyPromptOperator,
    NanoBananaLoadPromptOperator,
    NanoBananaDeleteHistoryOperator,
    NanoBananaClearAllHistoryOperator,
    NanoBananaHistoryPanel,
    # Reference
    NanoBananaAddFileRefOperator,
    NanoBananaRemoveFileRefOperator,
    NanoBananaAddImageRefOperator,
    NanoBananaRemoveImageRefOperator,
    # Main
    NanoBananaTextureGenOperator,
)

# For backwards compatibility, expose storage singleton function
_get_persistent_storage = get_persistent_storage
_format_reference_info = format_reference_info

__all__ = [
    # Storage utilities
    "get_persistent_storage",
    "format_reference_info",
    "_get_persistent_storage",
    "_format_reference_info",
    # Bake
    "NanoBananaApplyBakeOperator",
    # Camera
    "NanoBananaFocusCameraOperator",
    "NanoBananaAddCameraOperator",
    "NanoBananaRenderCameraOperator",
    "NanoBananaToggleWorkbenchOperator",
    # Text
    "NanoBananaShowMessageOperator",
    "NanoBananaCreatePromptTextOperator",
    "NanoBananaOpenTextEditorOperator",
    # Settings
    "NanoBananaSettingsOperator",
    # History
    "NanoBananaCopyPromptOperator",
    "NanoBananaLoadPromptOperator",
    "NanoBananaDeleteHistoryOperator",
    "NanoBananaClearAllHistoryOperator",
    "NanoBananaHistoryPanel",
    # Reference
    "NanoBananaAddFileRefOperator",
    "NanoBananaRemoveFileRefOperator",
    "NanoBananaAddImageRefOperator",
    "NanoBananaRemoveImageRefOperator",
    # Main
    "NanoBananaTextureGenOperator",
]
