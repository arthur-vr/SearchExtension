bl_info = {
    "name": "searchExtension",
    "author": "SmileyCat",
    "version": (1, 0, 1),
    "blender": (5, 0, 0),
    "location": "Search > searchExtension",
    "description": "Collection of utility operators for F3 search",
    "warning": "",
    "wiki_url": "",
    "category": "System",
}

import bpy
from . import registry
from . import preferences
from ._commons import addon_loader

def register():
    # 1. Initialize properties on Preferences class
    addon_loader.init_properties(preferences.SearchExtensionPreferences, registry.MODULE_REGISTRY, __package__)
    
    # 2. Register Preferences class
    bpy.utils.register_class(preferences.SearchExtensionPreferences)

    # 3. Register enabled modules
    addon_loader.register_initial_modules(__package__, registry.MODULE_REGISTRY)


def unregister():
    # 1. Unregister modules
    addon_loader.unregister_all_modules(__package__, registry.MODULE_REGISTRY)

    # 2. Unregister class
    bpy.utils.unregister_class(preferences.SearchExtensionPreferences)


if __name__ == "__main__":
    register()
