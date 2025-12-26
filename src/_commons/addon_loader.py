import bpy

# Track which modules are currently registered
_registered_modules = set()

def get_module_by_prop_name(registry, prop_name):
    """Get module by property name."""
    for item in registry:
        if item["prop"] == prop_name:
            return item["module"]
    return None

def register_module(addon_name, mod):
    """Register a module if not already registered."""
    if mod not in _registered_modules:
        try:
            if hasattr(mod, "register"):
                mod.register()
                _registered_modules.add(mod)
        except Exception as e:
            print(f"[{addon_name}] Failed to register {mod.__name__}: {e}")

def unregister_module(addon_name, mod):
    """Unregister a module if currently registered."""
    if mod in _registered_modules:
        try:
            if hasattr(mod, "unregister"):
                mod.unregister()
                _registered_modules.discard(mod)
        except Exception as e:
            print(f"[{addon_name}] Failed to unregister {mod.__name__}: {e}")

def make_update_callback(addon_name, registry, prop_name):
    """Create an update callback for a module toggle property."""
    def update_func(self, context):
        mod = get_module_by_prop_name(registry, prop_name)
        if mod is None:
            return
        enabled = getattr(self, prop_name)
        if enabled:
            register_module(addon_name, mod)
        else:
            unregister_module(addon_name, mod)
    return update_func

def init_properties(pref_class, registry, addon_name):
    """Dynamically add properties to the preferences class based on registry."""
    # Ensure annotations dict exists
    if not hasattr(pref_class, "__annotations__"):
        pref_class.__annotations__ = {}

    # 1. Module properties
    for item in registry:
        pref_class.__annotations__[item["prop"]] = bpy.props.BoolProperty(
            name=item["name"],
            default=True,
            description=item.get("description", ""),
            update=make_update_callback(addon_name, registry, item["prop"])
        )
    
    # 2. Category toggle properties
    categories = set(item.get("category", "Uncategorized") for item in registry)
    for cat in categories:
        prop_name = f"show_category_{cat.replace(' ', '_').replace('/', '_').lower()}"
        pref_class.__annotations__[prop_name] = bpy.props.BoolProperty(
            name=cat,
            default=True # Default to expanded
        )

def register_initial_modules(addon_name, registry):
    """Register modules based on current preferences (or defaults)."""
    # Get preferences
    # Note: context.preferences might not be fully available during load, but usually is fine.
    # A safer way is checking if the addon is enabled, but for local addons:
    prefs = None
    try:
        prefs = bpy.context.preferences.addons.get(addon_name)
    except:
        pass
        
    for item in registry:
        prop_name = item["prop"]
        mod = item["module"]
        
        enabled = True
        if prefs and hasattr(prefs, "preferences"):
             enabled = getattr(prefs.preferences, prop_name, True)
        
        if enabled:
            register_module(addon_name, mod)

def unregister_all_modules(addon_name, registry):
    """Unregister all currently registered modules."""
    for item in reversed(registry):
        unregister_module(addon_name, item["module"])

def draw_registry_ui(layout, preference_instance, registry):
    """Helper to draw the registry UI with categories."""
    
    # Organize items by category
    categories = {}
    for item in registry:
        cat = item.get("category", "Uncategorized")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
        
    # Draw categories
    for cat in sorted(categories.keys()):
        items = categories[cat]
        box = layout.box()
        
        # Category Header with Toggle
        cat_prop = f"show_category_{cat.replace(' ', '_').replace('/', '_').lower()}"
        is_expanded = getattr(preference_instance, cat_prop, True)
        
        row = box.row()
        row.alignment = 'LEFT'
        icon = 'DOWNARROW_HLT' if is_expanded else 'RIGHTARROW'
        row.prop(preference_instance, cat_prop, icon=icon, text=cat, emboss=False)
        
        # Count Info
        sub = row.row()
        sub.alignment = 'RIGHT'
        sub.label(text=f"{len(items)} items")
        
        if is_expanded:
            col = box.column()
            col.use_property_split = False
            col.use_property_decorate = False  
            
            for item in items:
                col.prop(preference_instance, item["prop"], text=item["name"])
