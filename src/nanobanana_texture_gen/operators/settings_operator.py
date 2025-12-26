"""Settings operator."""

from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from .storage_utils import get_persistent_storage
from ..external_storage import KEY_API_KEY, KEY_MODEL_VERSION, KEY_CUSTOM_MODEL_NAME


class NanoBananaSettingsOperator(Operator):
    """NanoBanana Global Settings (API Key, Model)."""
    bl_idname = "nanobanana.settings"
    bl_label = "NanoBanana Settings"
    bl_options = {'REGISTER', 'INTERNAL'}

    api_key: StringProperty(
        name="API Key",
        description="Google Gemini API Key",
        subtype='PASSWORD'
    )

    model_version: EnumProperty(
        name="Model",
        items=[
            ("gemini-3-pro-image-preview", "NanoBanana 3 Pro Image", "Professional-grade image generation with advanced reasoning"),
            ("gemini-2.5-flash-image", "NanoBanana 2.5 Flash Image", "Fast general-purpose image generation"),
            ("gemini-2.0-flash-exp", "Gemini 2.0 Flash Experimental", "Experimental image generation features"),
            ("CUSTOM", "Custom Model", "Use custom model name below"),
        ],
        default="gemini-2.5-flash-image"
    )

    custom_model_name: StringProperty(
        name="Custom Model Name",
        description="Custom model name to use (only when 'Custom Model' is selected)",
        default=""
    )

    def invoke(self, context, event):
        storage = get_persistent_storage()
        self.api_key = storage.get(KEY_API_KEY, "")
        self.model_version = storage.get(KEY_MODEL_VERSION, "gemini-2.5-flash-image")
        self.custom_model_name = storage.get(KEY_CUSTOM_MODEL_NAME, "")
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        storage = get_persistent_storage()
        storage.update({
            KEY_API_KEY: self.api_key,
            KEY_MODEL_VERSION: self.model_version,
            KEY_CUSTOM_MODEL_NAME: self.custom_model_name
        })
        self.report({'INFO'}, "Settings saved.")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")
        layout.prop(self, "model_version")
        if self.model_version == "CUSTOM":
            layout.prop(self, "custom_model_name")
