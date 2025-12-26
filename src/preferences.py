import bpy
from . import registry
from ._commons import addon_loader

class SearchExtensionPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__
    
    # Properties are injected dynamically via addon_loader.init_properties

    def draw(self, context):
        layout = self.layout
        layout.label(text="Enable/Disable Operators:")
        addon_loader.draw_registry_ui(layout, self, registry.MODULE_REGISTRY)
