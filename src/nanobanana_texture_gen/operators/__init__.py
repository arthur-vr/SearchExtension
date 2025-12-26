"""NanoBanana texture generation operators - split by responsibility."""

from .storage_utils import get_persistent_storage, format_reference_info
from .bake_operators import NanoBananaApplyBakeOperator
from .camera_operators import (
    NanoBananaFocusCameraOperator,
    NanoBananaAddCameraOperator,
    NanoBananaRenderCameraOperator,
    NanoBananaToggleWorkbenchOperator,
)
from .text_operators import (
    NanoBananaShowMessageOperator,
    NanoBananaCreatePromptTextOperator,
    NanoBananaOpenTextEditorOperator,
)
from .settings_operator import NanoBananaSettingsOperator
from .history_operators import (
    NanoBananaCopyPromptOperator,
    NanoBananaLoadPromptOperator,
    NanoBananaDeleteHistoryOperator,
    NanoBananaClearAllHistoryOperator,
    NanoBananaHistoryPanel,
)
from .reference_operators import (
    NanoBananaAddFileRefOperator,
    NanoBananaRemoveFileRefOperator,
    NanoBananaAddImageRefOperator,
    NanoBananaRemoveImageRefOperator,
)
from .texture_gen_operator import NanoBananaTextureGenOperator

__all__ = [
    # Storage utilities
    "get_persistent_storage",
    "format_reference_info",
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
