"""Main texture generation operator."""

import bpy
import os
from bpy.props import StringProperty, IntProperty, EnumProperty, BoolProperty
from bpy.types import Operator
from ..._commons.constants import ADDON_LABEL_SUFFIX
from ..external_storage import (
    KEY_API_KEY,
    KEY_PROMPT,
    KEY_SEED,
    KEY_MODEL_VERSION,
    KEY_CUSTOM_MODEL_NAME,
    KEY_TEXTURE_PREFIX,
    KEY_APPEND_TIMESTAMP,
    KEY_USE_ACTIVE_OBJ,
    KEY_USE_WORKBENCH,
)
from ..image_utils import ensure_image_file
from ..generation_manager import start_generation, is_generation_running
from .storage_utils import get_persistent_storage


class NanoBananaTextureGenOperator(Operator):
    """Generate texture using NanoBanana (Gemini) with bake + references."""
    bl_idname = "nanobanana.generate_texture"
    bl_label = "NanoBanana" + ADDON_LABEL_SUFFIX
    bl_description = "Generate texture using NanoBanana (Gemini) from reference images"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    # =========================================================================
    # Properties
    # =========================================================================
    texture_prefix: StringProperty(
        name="Texture Prefix",
        description="Base name used for generated texture",
        default="nanobanana_texture",
    )

    append_timestamp: BoolProperty(
        name="Append Timestamp",
        description="Append timestamp to generated texture names",
        default=True,
    )

    prompt: StringProperty(
        name="Prompt",
        description="Text prompt for texture generation (short)",
        default="",
    )

    use_text_editor: BoolProperty(
        name="Use Text Editor",
        description="Use Blender Text datablock for longer prompts",
        default=False,
    )

    prompt_text: StringProperty(
        name="Prompt Text",
        description="Name of Blender Text datablock to use as prompt",
        default="",
    )

    seed: IntProperty(
        name="Seed",
        description="Random seed (0 for random)",
        default=0,
        min=0
    )

    bake_mode: EnumProperty(
        name="Bake Mode",
        description="Type of bake to use for reference",
        items=[
            ("VERTEX_COLOR", "Vertex Color", "Bake vertex colors (useful for ID maps/guides)"),
            ("COMBINED", "Combined", "Bake everything (lighting, materials, shadows)"),
            ("DIFFUSE", "Diffuse", "Bake only diffuse color"),
            ("NORMAL", "Normal", "Bake normal map"),
        ],
        default="COMBINED"
    )

    use_active_object_bake: BoolProperty(
        name="Bake Active Object",
        description="Include vertex color bake of active object as reference",
        default=True,
    )

    apply_to_object: BoolProperty(
        name="Add Image Node",
        description="After generation, add the texture as an Image Node to the active object's material",
        default=False,
    )

    show_bake_section: BoolProperty(
        name="Show Bake Section",
        description="Expand Bake section",
        default=False,
    )

    show_camera_section: BoolProperty(
        name="Show Camera Section",
        description="Expand Camera section",
        default=False,
    )

    # =========================================================================
    # Execute
    # =========================================================================
    def execute(self, context):
        return self._execute_uv_base(context)

    # =========================================================================
    # Execute - UV Base Mode
    # =========================================================================
    def _execute_uv_base(self, context):
        storage = self._ensure_storage()
        wm = context.window_manager

        # Load Global Settings
        api_key = storage.get(KEY_API_KEY, "")
        model_version = storage.get(KEY_MODEL_VERSION, "gemini-2.5-flash-image")
        custom_model_name = storage.get(KEY_CUSTOM_MODEL_NAME, "")

        if not api_key:
            self.report({'ERROR'}, "API Key is not set. Please configure in Settings.")
            return {'CANCELLED'}

        if is_generation_running():
            self.report({'WARNING'}, "Generation already in progress. Please wait...")
            return {'CANCELLED'}

        # Collect References
        temp_files_to_cleanup = []
        source_obj = context.active_object
        image_paths = []
        reference_info_details = []

        # A. Active Object Reference (Optional - skip if no image found)
        if source_obj and source_obj.type == 'MESH' and self.use_active_object_bake:
            self.report({'INFO'}, f"Checking reference image from '{source_obj.name}'...")

            active_image = None
            if source_obj.data.materials and source_obj.data.materials[0]:
                mat = source_obj.data.materials[0]
                if mat.use_nodes:
                    if mat.node_tree.nodes.active and mat.node_tree.nodes.active.type == 'TEX_IMAGE':
                        active_image = mat.node_tree.nodes.active.image

                    if not active_image:
                        for node in mat.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                if node.inputs['Base Color'].is_linked:
                                    link = node.inputs['Base Color'].links[0]
                                    if link.from_node.type == 'TEX_IMAGE':
                                        active_image = link.from_node.image
                                break

            if active_image:
                try:
                    img_path, created_temp = ensure_image_file(active_image, name_hint=f"ref_bake_{source_obj.name}")
                    if created_temp:
                        temp_files_to_cleanup.append(img_path)

                    saved_ref_path = storage.save_baked_reference(
                        img_path,
                        object_name=source_obj.name,
                        name_hint=self.texture_prefix
                    )

                    image_paths.append(img_path)
                    reference_info_details.append({
                        "type": "BAKE",
                        "object_name": source_obj.name,
                        "path": saved_ref_path or img_path,
                        "saved_path": saved_ref_path or ""
                    })
                    self.report({'INFO'}, f"Added bake reference from '{source_obj.name}'")
                except Exception as e:
                    self.report({'WARNING'}, f"Could not use object reference: {str(e)}")
            else:
                self.report({'INFO'}, f"No bake image on '{source_obj.name}', skipping object reference")

        # B. File References
        for item in wm.nanobanana_file_refs:
            if not item.filepath:
                continue
            abs_path = bpy.path.abspath(item.filepath)
            if not os.path.exists(abs_path):
                self.report({'WARNING'}, f"Image file not found: {abs_path}")
                continue

            saved_ref_path = storage.save_baked_reference(
                abs_path,
                object_name=os.path.basename(abs_path),
                name_hint=self.texture_prefix
            )
            image_paths.append(abs_path)
            reference_info_details.append({
                "type": "FILE",
                "object_name": os.path.basename(abs_path),
                "path": saved_ref_path or abs_path,
                "saved_path": saved_ref_path or ""
            })

        # C. Blender Image References
        for item in wm.nanobanana_image_refs:
            if not item.image_name:
                continue
            image = bpy.data.images.get(item.image_name)
            if not image:
                self.report({'WARNING'}, f"Image '{item.image_name}' not found, skipping")
                continue

            try:
                img_path, created_temp = ensure_image_file(image, name_hint=self.texture_prefix or image.name)
            except Exception as e:
                self.report({'ERROR'}, f"Could not export image '{item.image_name}': {str(e)}")
                return {'CANCELLED'}

            if created_temp:
                temp_files_to_cleanup.append(img_path)

            saved_ref_path = storage.save_baked_reference(
                img_path,
                object_name=image.name,
                name_hint=self.texture_prefix
            )
            image_paths.append(img_path)
            reference_info_details.append({
                "type": "IMAGE",
                "object_name": image.name,
                "path": saved_ref_path or img_path,
                "saved_path": saved_ref_path or ""
            })

        if not image_paths:
            self.report({'ERROR'}, "No reference images provided. Select an object or add reference images.")
            return {'CANCELLED'}

        return self._start_generation(
            context, storage, api_key, model_version, custom_model_name,
            reference_info_details, source_obj, temp_files_to_cleanup
        )

    # =========================================================================
    # Common Generation Start
    # =========================================================================
    def _start_generation(self, context, storage, api_key, model_version, custom_model_name,
                          reference_info_details, source_obj, temp_files):

        actual_model = custom_model_name if model_version == "CUSTOM" else model_version
        if model_version == "CUSTOM" and not custom_model_name.strip():
            self.report({'ERROR'}, "Custom model name is required in Settings.")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Starting generation with {actual_model}...")

        # Get prompt from text editor or direct input
        if self.use_text_editor:
            if not self.prompt_text or self.prompt_text not in bpy.data.texts:
                self.report({'ERROR'}, "Please select a valid Text datablock for the prompt.")
                return {'CANCELLED'}
            text_block = bpy.data.texts[self.prompt_text]
            prompt = text_block.as_string().strip()
            # Remove comment lines starting with #
            lines = [line for line in prompt.split('\n') if not line.strip().startswith('#')]
            prompt = '\n'.join(lines).strip()
        else:
            prompt = self.prompt.strip()

        if not prompt:
            self.report({'ERROR'}, "Prompt is required.")
            return {'CANCELLED'}

        combined_reference_info = {
            "mode": "UV_BASE",
            "count": len(reference_info_details),
            "details": reference_info_details,
            "object_name": reference_info_details[0]["object_name"] if reference_info_details else "None",
            "path": reference_info_details[0]["path"] if reference_info_details else ""
        }

        history_info = {
            'prompt': prompt,
            'model_version': actual_model,
            'seed': self.seed,
            'reference_info': combined_reference_info
        }

        # Persist settings
        storage.update({
            KEY_PROMPT: self.prompt,
            KEY_SEED: self.seed,
            KEY_TEXTURE_PREFIX: self.texture_prefix,
            KEY_APPEND_TIMESTAMP: self.append_timestamp,
            KEY_USE_ACTIVE_OBJ: self.use_active_object_bake,
        })

        try:
            start_generation(
                api_key=api_key,
                model=actual_model,
                prompt=prompt,
                image_references=reference_info_details,
                source_obj=source_obj if self.apply_to_object else None,
                temp_files=temp_files,
                texture_prefix=self.texture_prefix,
                append_timestamp=self.append_timestamp,
                history_info=history_info
            )
        except RuntimeError as e:
            self.report({'WARNING'}, str(e))
            return {'CANCELLED'}

        self.report({'INFO'}, f"Texture generation started in background...")
        return {'FINISHED'}

    # =========================================================================
    # Draw UI - Unified Sectioned Layout
    # =========================================================================
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        # Settings Button
        row = layout.row()
        row.operator("nanobanana.settings", icon='PREFERENCES', text="Settings (API Key & Model)")
        layout.separator()

        # === Section 1: Bake ===
        self._draw_bake_section(context, layout)

        # === Section 2: Camera ===
        self._draw_camera_section(context, layout)

        # === Section 3: References ===
        self._draw_references_section(context, layout, wm)

        layout.separator()

        # === Apply to Object Option ===
        row = layout.row()
        row.prop(self, "apply_to_object")
        # Disable if no active mesh (user requirement)
        if not context.active_object or context.active_object.type != 'MESH':
            row.enabled = False
            self.apply_to_object = False  # Force disable logic

        layout.separator()

        # === Output Config ===
        col = layout.column(align=True)
        col.prop(self, "texture_prefix")
        col.prop(self, "append_timestamp")

        layout.separator()

        # === Prompt Section ===
        box = layout.box()
        box.label(text="Prompt", icon='TEXT')

        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(self, "use_text_editor", text="Use Text Editor", toggle=True)

        if self.use_text_editor:
            row = col.row(align=True)
            row.prop_search(self, "prompt_text", bpy.data, "texts", text="")
            row.operator("nanobanana.create_prompt_text", text="", icon='ADD')

            # Open in Text Editor button
            if self.prompt_text and self.prompt_text in bpy.data.texts:
                row = col.row(align=True)
                op = row.operator("nanobanana.open_text_editor", text="Open in Text Editor", icon='TEXT')
                op.text_name = self.prompt_text

                # Show preview of text content
                text_block = bpy.data.texts[self.prompt_text]
                preview = text_block.as_string()[:100]
                if len(text_block.as_string()) > 100:
                    preview += "..."
                col.label(text=f"Preview: {preview[:50]}", icon='INFO')
        else:
            col.prop(self, "prompt", text="")

        layout.separator()
        layout.prop(self, "seed")

        # History
        self._draw_history(context)

    def _draw_bake_section(self, context, layout):
        """Draw Bake section UI (collapsible)."""
        box = layout.box()

        # Collapsible header
        row = box.row()
        row.prop(self, "show_bake_section",
                 icon='TRIA_DOWN' if self.show_bake_section else 'TRIA_RIGHT',
                 icon_only=True, emboss=False)
        row.label(text="Bake", icon='RENDER_RESULT')

        if not self.show_bake_section:
            return

        obj = context.active_object
        col = box.column(align=True)

        if obj and obj.type == 'MESH':
            row = col.row(align=True)
            row.prop(self, "use_active_object_bake", text=f"Include: {obj.name}", toggle=True)

            if self.use_active_object_bake:
                row = col.row(align=True)
                row.prop(self, "bake_mode", text="")
                op = row.operator("nanobanana.apply_bake_preview", text="Preview", icon='VPAINT_HLT')
                op.bake_mode = self.bake_mode
        else:
            col.label(text="No Mesh Selected", icon='INFO')

    def _draw_camera_section(self, context, layout):
        """Draw Camera section UI (collapsible)."""
        box = layout.box()

        # Collapsible header
        row = box.row()
        row.prop(self, "show_camera_section",
                 icon='TRIA_DOWN' if self.show_camera_section else 'TRIA_RIGHT',
                 icon_only=True, emboss=False)
        row.label(text="Camera", icon='CAMERA_DATA')

        if not self.show_camera_section:
            return

        scene = context.scene
        col = box.column(align=True)

        # Workbench mode toggle (persistent)
        storage = self._ensure_storage()
        use_workbench = storage.get(KEY_USE_WORKBENCH, True)

        row = col.row(align=True)
        icon = 'CHECKBOX_HLT' if use_workbench else 'CHECKBOX_DEHLT'
        op = row.operator("nanobanana.toggle_workbench", text="Workbench Mode", icon=icon, depress=use_workbench)

        col.separator()

        # Check if ANY cameras exist in scene (not just active camera)
        cameras_in_scene = [obj for obj in bpy.data.objects if obj.type == 'CAMERA']

        if scene.camera:
            col.label(text=f"Active: {scene.camera.name}", icon='CHECKMARK')

            row = col.row(align=True)
            row.operator("nanobanana.focus_camera", text="Focus View", icon='ZOOM_SELECTED')
            row.operator("nanobanana.render_camera", text="Render to Image", icon='RENDER_STILL')
        else:
            # No active camera (even if others exist, provide option to add/set)
            if cameras_in_scene:
                col.label(text="No Active Camera", icon='ERROR')
                col.label(text=f"{len(cameras_in_scene)} camera(s) in scene", icon='INFO')
            else:
                col.label(text="No Cameras in Scene", icon='ERROR')

            # Show Add Camera button in all cases where active is missing
            col.operator("nanobanana.add_camera", text="Add Camera", icon='ADD')


    def _draw_references_section(self, context, layout, wm):
        """Draw References section UI."""
        box = layout.box()
        box.label(text="References", icon='IMGDISPLAY')

        # File Refs
        sub_box = box.box()
        row = sub_box.row()
        row.label(text=f"File Paths ({len(wm.nanobanana_file_refs)})")
        row.operator("nanobanana.add_file_ref", text="", icon='ADD')
        for i, item in enumerate(wm.nanobanana_file_refs):
            ref_row = sub_box.row(align=True)
            ref_row.prop(item, "filepath", text="")
            remove_op = ref_row.operator("nanobanana.remove_file_ref", text="", icon='X')
            remove_op.index = i

        # Image Refs
        sub_box = box.box()
        row = sub_box.row()
        row.label(text=f"Blender Images ({len(wm.nanobanana_image_refs)})")
        row.operator("nanobanana.add_image_ref", text="", icon='ADD')
        for i, item in enumerate(wm.nanobanana_image_refs):
            ref_row = sub_box.row(align=True)
            ref_row.prop_search(item, "image_name", bpy.data, "images", text="")
            remove_op = ref_row.operator("nanobanana.remove_image_ref", text="", icon='X')
            remove_op.index = i


    def _draw_history(self, context):
        from .storage_utils import format_reference_info
        from ..external_storage import KEY_REFERENCE_INFO

        layout = self.layout
        storage = self._ensure_storage()
        history = storage.get_prompt_history(limit=None)

        # Always show history section
        box = layout.box()
        row = box.row()
        row.prop(context.window_manager, "nanobanana_show_history",
                icon='TRIA_DOWN' if context.window_manager.nanobanana_show_history else 'TRIA_RIGHT',
                icon_only=True, emboss=False)
        row.label(text=f"Prompt History ({len(history)})")

        if context.window_manager.nanobanana_show_history:
            if not history:
                box.label(text="No history yet", icon='INFO')
            else:
                for i, entry in enumerate(history):
                    history_box = box.box()
                    col = history_box.column(align=False)

                    prompt_text = entry.get('prompt', '')
                    if len(prompt_text) > 50:
                        prompt_text = prompt_text[:50] + "..."
                    col.label(text=prompt_text, icon='TEXT')

                    col.separator(factor=0.5)

                    meta_row = col.row(align=True)
                    meta_row.scale_y = 0.8
                    model = entry.get('model_version', '').replace('gemini-', '')
                    meta_row.label(text=f"{model}", icon='INFO')

                    col.separator(factor=0.5)

                    btn_row = col.row(align=True)
                    load_op = btn_row.operator("nanobanana.load_prompt", text="Load", icon='IMPORT')
                    load_op.history_index = i
                    copy_op = btn_row.operator("nanobanana.copy_prompt", text="Copy", icon='COPYDOWN')
                    copy_op.history_index = i
                    delete_op = btn_row.operator("nanobanana.delete_history", text="", icon='X')
                    delete_op.history_index = i

    def invoke(self, context, event):
        self._load_transient_settings()
        return context.window_manager.invoke_props_dialog(self, width=450)

    def _ensure_storage(self):
        # Always use singleton storage to ensure consistency
        return get_persistent_storage()

    def _load_transient_settings(self):
        storage = self._ensure_storage()
        self.prompt = storage.get(KEY_PROMPT, "")
        self.seed = storage.get(KEY_SEED, 0)
        self.texture_prefix = storage.get(KEY_TEXTURE_PREFIX, "nanobanana_texture")
        self.append_timestamp = storage.get(KEY_APPEND_TIMESTAMP, True)
        self.use_active_object_bake = storage.get(KEY_USE_ACTIVE_OBJ, True)
