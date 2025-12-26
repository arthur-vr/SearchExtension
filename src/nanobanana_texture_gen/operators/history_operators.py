"""History-related operators and panel."""

import bpy
import datetime
from bpy.props import IntProperty
from bpy.types import Operator
from ..._commons.constants import ADDON_LABEL_SUFFIX
from .storage_utils import get_persistent_storage, format_reference_info
from ..external_storage import KEY_PROMPT, KEY_MODEL_VERSION, KEY_SEED, KEY_REFERENCE_INFO


class NanoBananaCopyPromptOperator(Operator):
    """Copy prompt from history."""
    bl_idname = "nanobanana.copy_prompt"
    bl_label = "Copy Prompt" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    history_index: IntProperty(default=0)

    def execute(self, context):
        storage = get_persistent_storage()
        history = storage.get_prompt_history()

        if 0 <= self.history_index < len(history):
            entry = history[self.history_index]
            context.window_manager.clipboard = entry.get('prompt', '')
            self.report({'INFO'}, "Prompt copied to clipboard")
        else:
            self.report({'ERROR'}, "Invalid history index")

        return {'FINISHED'}


class NanoBananaLoadPromptOperator(Operator):
    """Load prompt from history into current settings."""
    bl_idname = "nanobanana.load_prompt"
    bl_label = "Load Prompt" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    history_index: IntProperty(default=0)

    def execute(self, context):
        storage = get_persistent_storage()
        history = storage.get_prompt_history()

        if 0 <= self.history_index < len(history):
            entry = history[self.history_index]
            storage.update({
                KEY_PROMPT: entry.get('prompt', ''),
                KEY_MODEL_VERSION: entry.get('model_version', 'gemini-2.5-flash-image'),
                KEY_SEED: entry.get('seed', 0),
            })
            self.report({'INFO'}, "Prompt loaded")
        else:
            self.report({'ERROR'}, "Invalid history index")

        return {'FINISHED'}


class NanoBananaDeleteHistoryOperator(Operator):
    """Delete a history entry."""
    bl_idname = "nanobanana.delete_history"
    bl_label = "Delete History Entry" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    history_index: IntProperty(default=0)

    def execute(self, context):
        storage = get_persistent_storage()
        if storage.delete_history_entry(self.history_index):
            self.report({'INFO'}, "History entry deleted")
        else:
            self.report({'ERROR'}, "Could not delete history entry")

        return {'FINISHED'}


class NanoBananaClearAllHistoryOperator(Operator):
    """Clear all prompt history."""
    bl_idname = "nanobanana.clear_all_history"
    bl_label = "Clear All History" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        storage = get_persistent_storage()
        storage.clear_all_history()
        self.report({'INFO'}, "All history cleared")
        return {'FINISHED'}


class NanoBananaHistoryPanel(bpy.types.Panel):
    """Panel to show full prompt history."""
    bl_label = "NanoBanana Prompt History" + ADDON_LABEL_SUFFIX
    bl_idname = "VIEW3D_PT_nanobanana_history"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'NanoBanana'

    def draw(self, context):
        layout = self.layout
        storage = get_persistent_storage()
        history = storage.get_prompt_history()

        if not history:
            layout.label(text="No history yet", icon='INFO')
            return

        # Header with clear button
        row = layout.row()
        row.label(text=f"Total: {len(history)} entries", icon='DOCUMENTS')
        row.operator("nanobanana.clear_all_history", text="Clear All", icon='TRASH')

        layout.separator()

        # Show all history entries
        for i, entry in enumerate(history):
            box = layout.box()
            col = box.column(align=True)

            # Show full prompt
            prompt_text = entry.get('prompt', '')
            # Split into lines if too long
            max_chars = 60
            if len(prompt_text) > max_chars:
                lines = [prompt_text[j:j+max_chars] for j in range(0, len(prompt_text), max_chars)]
                for line in lines[:3]:  # Show max 3 lines
                    col.label(text=line)
                if len(lines) > 3:
                    col.label(text="...")
            else:
                col.label(text=prompt_text, icon='TEXT')

            # Show negative prompt if exists
            neg_prompt = entry.get('negative_prompt', '')
            if neg_prompt:
                col.label(text=f"Negative: {neg_prompt[:40]}...", icon='CANCEL')

            # Show metadata
            meta_row = col.row(align=True)
            meta_row.scale_y = 0.8
            model = entry.get('model_version', '').replace('gemini-', '')
            seed = entry.get('seed', 0)
            timestamp = entry.get('timestamp', 0)
            time_str = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            meta_row.label(text=f"{model} | Seed: {seed} | {time_str}", icon='INFO')

            ref_label, ref_path = format_reference_info(entry.get(KEY_REFERENCE_INFO))
            if ref_label:
                col.label(text=f"Ref: {ref_label}", icon='IMAGE_DATA')
                if ref_path:
                    shortened = ref_path if len(ref_path) <= 90 else f"...{ref_path[-87:]}"
                    col.label(text=shortened, icon='FILE_FOLDER')

            # Action buttons
            btn_row = col.row(align=True)
            load_op = btn_row.operator("nanobanana.load_prompt", text="Load", icon='IMPORT')
            load_op.history_index = i
            copy_op = btn_row.operator("nanobanana.copy_prompt", text="Copy", icon='COPYDOWN')
            copy_op.history_index = i
            delete_op = btn_row.operator("nanobanana.delete_history", text="Delete", icon='X')
            delete_op.history_index = i
