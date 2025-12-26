import bpy
import hashlib
import os
import tempfile
from datetime import datetime
from .._commons.constants import ADDON_LABEL_SUFFIX, ADDON_NAME
from .external_storage import (
    RenderSaveImageExternalStorage,
    KEY_NAME_INPUT,
    KEY_SET_ACTIVE,
    KEY_AUTO_REPEAT,
    KEY_AUTO_REPEAT_INTERVAL,
    KEY_RESOLUTION_LEVEL,
    KEY_SAMPLE_LEVEL,
    KEY_USE_JPEG_FORMAT,
    KEY_JPEG_QUALITY_LEVEL,
    KEY_IMAGE_HASHES,
)

_SCENE_AUTO_RENDER_PROP = f"{ADDON_NAME.lower()}_auto_render_enabled"
_AUTO_RENDER_TIMER_HANDLERS = {}
_AUTO_RENDER_SCENE_CONFIGS = {}
_AUTO_RENDER_MIN_INTERVAL = 0.5

_STORAGE_INSTANCE = None


def _get_persistent_storage():
    global _STORAGE_INSTANCE
    if _STORAGE_INSTANCE is None:
        _STORAGE_INSTANCE = RenderSaveImageExternalStorage()
    return _STORAGE_INSTANCE


_QUALITY_LEVEL_MIN = 1
_QUALITY_LEVEL_MAX = 10
_JPEG_QUALITY_MULTIPLIER = 10


def register_scene_properties():
    if hasattr(bpy.types.Scene, _SCENE_AUTO_RENDER_PROP):
        return

    setattr(
        bpy.types.Scene,
        _SCENE_AUTO_RENDER_PROP,
        bpy.props.BoolProperty(
            name=f"{ADDON_NAME} Auto Render",
            description="Automatically repeat Render & Save on a timer",
            default=False,
            update=_handle_auto_render_toggle,
        ),
    )


def unregister_scene_properties():
    _stop_all_auto_render_timers()
    if hasattr(bpy.types.Scene, _SCENE_AUTO_RENDER_PROP):
        delattr(bpy.types.Scene, _SCENE_AUTO_RENDER_PROP)


def _handle_auto_render_toggle(scene, _context):
    if not _scene_supports_auto_render(scene):
        return

    if _is_scene_auto_render_enabled(scene):
        if not _AUTO_RENDER_SCENE_CONFIGS.get(scene.name):
            _set_scene_auto_render_enabled(scene, False)
            return
        _start_auto_render_timer(scene)
    else:
        _stop_auto_render_timer(scene)


def _scene_supports_auto_render(scene):
    return hasattr(bpy.types.Scene, _SCENE_AUTO_RENDER_PROP)


def _is_scene_auto_render_enabled(scene):
    return bool(getattr(scene, _SCENE_AUTO_RENDER_PROP, False))


def _set_scene_auto_render_enabled(scene, value):
    if _scene_supports_auto_render(scene):
        setattr(scene, _SCENE_AUTO_RENDER_PROP, bool(value))


def _configure_scene_auto_render(scene, image_name, interval, set_active, quality_config=None):
    if not _scene_supports_auto_render(scene):
        return

    _AUTO_RENDER_SCENE_CONFIGS[scene.name] = {
        "image_name": image_name,
        "interval": max(interval, _AUTO_RENDER_MIN_INTERVAL),
        KEY_SET_ACTIVE: bool(set_active),
        "quality": quality_config or {},
    }

    if _is_scene_auto_render_enabled(scene):
        _set_scene_auto_render_enabled(scene, False)

    _set_scene_auto_render_enabled(scene, True)


def _stop_auto_render_timer(scene_or_name):
    scene_name = scene_or_name if isinstance(scene_or_name, str) else scene_or_name.name
    handler = _AUTO_RENDER_TIMER_HANDLERS.pop(scene_name, None)
    if handler:
        try:
            if bpy.app.timers.is_registered(handler):
                bpy.app.timers.unregister(handler)
        except Exception:
            pass


def _stop_all_auto_render_timers():
    for handler in list(_AUTO_RENDER_TIMER_HANDLERS.values()):
        try:
            if bpy.app.timers.is_registered(handler):
                bpy.app.timers.unregister(handler)
        except Exception:
            pass
    _AUTO_RENDER_TIMER_HANDLERS.clear()
    _AUTO_RENDER_SCENE_CONFIGS.clear()


def _start_auto_render_timer(scene):
    if not _scene_supports_auto_render(scene):
        return

    config = _AUTO_RENDER_SCENE_CONFIGS.get(scene.name)
    if not config:
        _set_scene_auto_render_enabled(scene, False)
        return

    image_name = config.get("image_name", "")
    if not image_name:
        _set_scene_auto_render_enabled(scene, False)
        return

    _stop_auto_render_timer(scene)

    scene_name = scene.name

    def _timer():
        current_scene = bpy.data.scenes.get(scene_name)
        if not current_scene or not _is_scene_auto_render_enabled(current_scene):
            _stop_auto_render_timer(scene_name)
            return None

        current_config = _AUTO_RENDER_SCENE_CONFIGS.get(scene_name)
        if not current_config:
            _set_scene_auto_render_enabled(current_scene, False)
            _stop_auto_render_timer(scene_name)
            return None

        current_image_name = current_config.get("image_name", "")
        if not current_image_name:
            _set_scene_auto_render_enabled(current_scene, False)
            _stop_auto_render_timer(scene_name)
            return None

        current_interval = max(current_config.get("interval", 1.0), _AUTO_RENDER_MIN_INTERVAL)
        current_set_active = bool(current_config.get(KEY_SET_ACTIVE, True))
        current_quality = current_config.get("quality", {})

        try:
            _perform_render_operation(
                current_scene,
                None,
                current_image_name,
                current_set_active,
                quality_config=current_quality,
            )
        except Exception as exc:
            print(f"[searchExtension] Auto Render failed: {exc}")
            _set_scene_auto_render_enabled(current_scene, False)
            _stop_auto_render_timer(scene_name)
            return None

        return current_interval

    first_interval = max(config.get("interval", 1.0), _AUTO_RENDER_MIN_INTERVAL)
    bpy.app.timers.register(_timer, first_interval=first_interval)
    _AUTO_RENDER_TIMER_HANDLERS[scene_name] = _timer


def _normalize_quality_level(value):
    try:
        level = int(value)
    except (TypeError, ValueError):
        return _QUALITY_LEVEL_MAX

    return max(_QUALITY_LEVEL_MIN, min(_QUALITY_LEVEL_MAX, level))


def _get_image_extension(file_format):
    if not file_format:
        return "png"

    fmt = file_format.lower()
    if fmt == "jpeg":
        return "jpg"
    return fmt


def _compute_file_hash(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _apply_quality_overrides(scene, quality_config):
    if not quality_config:
        return {}

    overrides = {}
    render = scene.render

    overrides["resolution_percentage"] = render.resolution_percentage
    resolution_level = _normalize_quality_level(quality_config.get("resolution_level", _QUALITY_LEVEL_MAX))
    render.resolution_percentage = resolution_level * 10

    cycles_settings = getattr(scene, "cycles", None)
    if cycles_settings:
        overrides["cycles_samples"] = cycles_settings.samples
        sample_level = _normalize_quality_level(quality_config.get("sample_level", _QUALITY_LEVEL_MAX))
        sample_ratio = sample_level / float(_QUALITY_LEVEL_MAX)
        target_samples = max(1, int(overrides["cycles_samples"] * sample_ratio))
        cycles_settings.samples = target_samples

    image_settings = render.image_settings
    overrides["file_format"] = image_settings.file_format
    overrides["quality"] = image_settings.quality

    use_low_quality_format = bool(quality_config.get("use_low_quality_format", False))
    if use_low_quality_format:
        jpeg_level = _normalize_quality_level(quality_config.get("jpeg_quality_level", _QUALITY_LEVEL_MAX))
        image_settings.file_format = 'JPEG'
        image_settings.quality = min(100, jpeg_level * _JPEG_QUALITY_MULTIPLIER)
    overrides["used_low_quality_format"] = use_low_quality_format

    return overrides


def _restore_quality_settings(scene, overrides):
    if not overrides:
        return

    render = scene.render
    render.resolution_percentage = overrides.get("resolution_percentage", render.resolution_percentage)

    cycles_settings = getattr(scene, "cycles", None)
    if cycles_settings and "cycles_samples" in overrides:
        cycles_settings.samples = overrides["cycles_samples"]

    image_settings = render.image_settings
    if overrides.get("used_low_quality_format"):
        image_settings.file_format = overrides.get("file_format", image_settings.file_format)
        image_settings.quality = overrides.get("quality", image_settings.quality)

def _perform_render_operation(scene, screen, image_name, set_active, quality_config=None):
    temp_dir = tempfile.gettempdir()
    original_filepath = scene.render.filepath

    overrides = _apply_quality_overrides(scene, quality_config or {})
    image_settings = scene.render.image_settings
    temp_extension = _get_image_extension(image_settings.file_format)
    temp_file = os.path.join(temp_dir, f"{image_name}.{temp_extension}")

    try:
        scene.render.filepath = temp_file

        if hasattr(bpy.context, "temp_override"):
            with bpy.context.temp_override(scene=scene):
                bpy.ops.render.render(write_still=True)
        else:
            bpy.ops.render.render(write_still=True)

        if not os.path.exists(temp_file):
            raise RuntimeError("Render failed to create output file")

        storage = _get_persistent_storage()
        current_hash = _compute_file_hash(temp_file)
        previous_hash = storage.get_image_hash(image_name)
        image_exists = image_name in bpy.data.images
        already_fresh = image_exists and previous_hash == current_hash

        if already_fresh:
            rendered_image = bpy.data.images[image_name]
        else:
            if image_exists:
                rendered_image = bpy.data.images[image_name]
                rendered_image.filepath = temp_file
                rendered_image.reload()
                rendered_image.pack()
            else:
                rendered_image = bpy.data.images.load(temp_file, check_existing=False)
                rendered_image.name = image_name
                rendered_image.pack()

            storage.set_image_hash(image_name, current_hash)

        if set_active:
            _set_image_active(rendered_image, screen)

        try:
            os.remove(temp_file)
        except OSError:
            pass

        return rendered_image
    finally:
        scene.render.filepath = original_filepath
        _restore_quality_settings(scene, overrides)


def _set_image_active(rendered_image, screen):
    screens = []
    if screen:
        screens.append(screen)

    wm = bpy.context.window_manager if bpy.context else None
    if wm:
        for window in wm.windows:
            if window.screen and window.screen not in screens:
                screens.append(window.screen)

    for scr in screens:
        for area in scr.areas:
            if area.type == 'IMAGE_EDITOR':
                for space in area.spaces:
                    if space.type == 'IMAGE_EDITOR':
                        space.image = rendered_image
                        break

class SEARCHEXT_OT_render_save_image(bpy.types.Operator):
    """Render current scene and save as Blender image"""
    bl_idname = "search_extension.render_save_image"
    bl_label = "Render and Save Image" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    name_input: bpy.props.StringProperty(
        name="Name (optional)",
        description="Custom name for the rendered image. If empty, 'render' will be used",
        default=""
    )
    
    set_active: bpy.props.BoolProperty(
        name="Set as Active Image",
        description="Set the rendered image as active in image editors",
        default=True
    )

    auto_repeat: bpy.props.BoolProperty(
        name="Enable Auto Repeat",
        description="Repeat Render & Save automatically (requires a custom name)",
        default=False,
    )

    auto_repeat_interval: bpy.props.FloatProperty(
        name="Repeat Interval (Seconds)",
        description="Seconds between automatic Render & Save executions",
        default=1.0,
        min=_AUTO_RENDER_MIN_INTERVAL,
        soft_min=_AUTO_RENDER_MIN_INTERVAL,
        soft_max=60.0,
    )

    resolution_quality_level: bpy.props.IntProperty(
        name="Resolution Level",
        description="Render size scale where 1=10% and 10=100%",
        default=_QUALITY_LEVEL_MAX,
        min=_QUALITY_LEVEL_MIN,
        max=_QUALITY_LEVEL_MAX,
    )

    sample_quality_level: bpy.props.IntProperty(
        name="Sample Level",
        description="Lower sample count for faster renders (1=lowest, 10=full)",
        default=_QUALITY_LEVEL_MAX,
        min=_QUALITY_LEVEL_MIN,
        max=_QUALITY_LEVEL_MAX,
    )

    use_low_quality_format: bpy.props.BoolProperty(
        name="Use JPEG for Quick Saves",
        description="Export quick renders as compressed JPEG instead of PNG",
        default=False,
    )

    jpeg_quality_level: bpy.props.IntProperty(
        name="JPEG Quality Level",
        description="Compression level for JPEG outputs (1=low, 10=high)",
        default=8,
        min=_QUALITY_LEVEL_MIN,
        max=_QUALITY_LEVEL_MAX,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, KEY_NAME_INPUT)
        layout.prop(self, KEY_SET_ACTIVE)

        quality_box = layout.box()
        quality_box.label(text="Quick Save Quality")
        quality_box.prop(self, "resolution_quality_level")
        quality_box.prop(self, "sample_quality_level")
        quality_box.prop(self, "use_low_quality_format")
        if self.use_low_quality_format:
            quality_box.prop(self, "jpeg_quality_level")

        has_custom_name = bool(self.name_input.strip())

        auto_row = layout.row()
        auto_row.enabled = has_custom_name
        auto_row.prop(self, KEY_AUTO_REPEAT)

        if self.auto_repeat:
            interval_row = layout.row()
            interval_row.enabled = has_custom_name
            interval_row.prop(self, KEY_AUTO_REPEAT_INTERVAL)

    def execute(self, context):
        interval_value = max(float(self.auto_repeat_interval), _AUTO_RENDER_MIN_INTERVAL)
        self.auto_repeat_interval = interval_value
        self._persist_current_settings()

        quality_config = self._collect_quality_config()

        has_custom_name = bool(self.name_input.strip())
        if has_custom_name:
            image_name = self.name_input.strip()
            use_timestamp = False
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_name = f"render_{timestamp}"
            use_timestamp = True

        scene = context.scene
        screen = getattr(context, "screen", None)

        try:
            _perform_render_operation(
                scene,
                screen,
                image_name,
                self.set_active,
                quality_config=quality_config,
            )
        except RuntimeError as exc:
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        except Exception as exc:
            self.report({'ERROR'}, f"Render failed: {exc}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Rendered image saved as: {image_name}")

        if self.auto_repeat:
            if use_timestamp:
                self.report({'WARNING'}, "Auto repeat requires a custom name. Auto repeat skipped.")
            elif not _scene_supports_auto_render(scene):
                self.report({'WARNING'}, "Auto repeat is unavailable because scene properties are missing.")
            else:
                _configure_scene_auto_render(
                    scene,
                    image_name,
                    interval_value,
                    self.set_active,
                    quality_config=quality_config,
                )
                self.report({'INFO'}, f"Auto repeat enabled every {interval_value:.2f}s")
        elif _scene_supports_auto_render(scene) and _is_scene_auto_render_enabled(scene):
            _set_scene_auto_render_enabled(scene, False)

        return {'FINISHED'}

    def invoke(self, context, event):
        self._load_persistent_settings()
        return context.window_manager.invoke_props_dialog(self)

    def _ensure_storage(self):
        if not hasattr(self, "_storage") or self._storage is None:
            self._storage = _get_persistent_storage()
        return self._storage

    def _load_persistent_settings(self):
        storage = self._ensure_storage()
        stored_name = storage.get(KEY_NAME_INPUT, "") or ""
        stored_set_active = storage.get(KEY_SET_ACTIVE, True)
        stored_auto_repeat = storage.get(KEY_AUTO_REPEAT, False)
        stored_interval = storage.get(KEY_AUTO_REPEAT_INTERVAL, 1.0)
        stored_resolution = storage.get(KEY_RESOLUTION_LEVEL, _QUALITY_LEVEL_MAX)
        stored_sample = storage.get(KEY_SAMPLE_LEVEL, _QUALITY_LEVEL_MAX)
        stored_use_jpeg = storage.get(KEY_USE_JPEG_FORMAT, False)
        stored_jpeg_quality = storage.get(KEY_JPEG_QUALITY_LEVEL, 8)

        self.name_input = stored_name
        self.set_active = bool(stored_set_active)
        self.auto_repeat = bool(stored_auto_repeat)
        self.resolution_quality_level = _normalize_quality_level(stored_resolution)
        self.sample_quality_level = _normalize_quality_level(stored_sample)
        self.use_low_quality_format = bool(stored_use_jpeg)
        self.jpeg_quality_level = _normalize_quality_level(stored_jpeg_quality)
        try:
            self.auto_repeat_interval = max(float(stored_interval), _AUTO_RENDER_MIN_INTERVAL)
        except (TypeError, ValueError):
            self.auto_repeat_interval = 1.0

    def _persist_current_settings(self):
        storage = self._ensure_storage()
        try:
            interval_value = max(float(self.auto_repeat_interval), _AUTO_RENDER_MIN_INTERVAL)
        except (TypeError, ValueError):
            interval_value = 1.0

        storage.update({
            KEY_NAME_INPUT: self.name_input.strip(),
            KEY_SET_ACTIVE: bool(self.set_active),
            KEY_AUTO_REPEAT: bool(self.auto_repeat),
            KEY_AUTO_REPEAT_INTERVAL: interval_value,
            KEY_RESOLUTION_LEVEL: _normalize_quality_level(self.resolution_quality_level),
            KEY_SAMPLE_LEVEL: _normalize_quality_level(self.sample_quality_level),
            KEY_USE_JPEG_FORMAT: bool(self.use_low_quality_format),
            KEY_JPEG_QUALITY_LEVEL: _normalize_quality_level(self.jpeg_quality_level),
        })

    def _collect_quality_config(self):
        return {
            "resolution_level": _normalize_quality_level(self.resolution_quality_level),
            "sample_level": _normalize_quality_level(self.sample_quality_level),
            "use_low_quality_format": bool(self.use_low_quality_format),
            "jpeg_quality_level": _normalize_quality_level(self.jpeg_quality_level),
        }
