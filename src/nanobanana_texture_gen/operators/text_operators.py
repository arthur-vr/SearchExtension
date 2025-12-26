"""Text and prompt editing operators."""

import bpy
import time
from bpy.props import StringProperty, EnumProperty
from bpy.types import Operator
from ..._commons.constants import ADDON_LABEL_SUFFIX


class NanoBananaShowMessageOperator(Operator):
    """Simple operator to show messages."""
    bl_idname = "nanobanana.show_message"
    bl_label = "NanoBanana Message" + ADDON_LABEL_SUFFIX
    bl_options = {'INTERNAL'}

    message_type: EnumProperty(
        name="Type",
        items=[
            ('INFO', "Info", ""),
            ('WARNING', "Warning", ""),
            ('ERROR', "Error", ""),
        ],
        default='INFO'
    )

    message: StringProperty(
        name="Message",
        default=""
    )

    def execute(self, context):
        self.report({self.message_type}, self.message)
        return {'FINISHED'}


class NanoBananaCreatePromptTextOperator(Operator):
    """Create a new Text datablock for prompt editing."""
    bl_idname = "nanobanana.create_prompt_text"
    bl_label = "Create Prompt Text" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text_name = f"NanoBanana_Prompt_{int(time.time())}"
        text_block = bpy.data.texts.new(text_name)
        text_block.write("# Enter your prompt here\n# Lines starting with # are ignored\n\n")

        # Open in new window
        try:
            bpy.ops.wm.window_new()
            new_window = context.window_manager.windows[-1]
            new_screen = new_window.screen

            # Change the area to TEXT_EDITOR
            for area in new_screen.areas:
                area.type = 'TEXT_EDITOR'
                # Need to use timer to set text after area type change
                def set_text():
                    for a in new_screen.areas:
                        if a.type == 'TEXT_EDITOR':
                            a.spaces.active.text = text_block
                            return None
                    return None
                bpy.app.timers.register(set_text, first_interval=0.1)
                break

            self.report({'INFO'}, f"Created: {text_name}")
        except Exception as e:
            self.report({'WARNING'}, f"Created: {text_name} (Could not open window: {e})")

        return {'FINISHED'}


class NanoBananaOpenTextEditorOperator(Operator):
    """Open a Text datablock in a new Text Editor window."""
    bl_idname = "nanobanana.open_text_editor"
    bl_label = "Open in Text Editor" + ADDON_LABEL_SUFFIX
    bl_options = {'REGISTER', 'UNDO'}

    text_name: StringProperty(
        name="Text Name",
        default=""
    )

    def execute(self, context):
        if not self.text_name or self.text_name not in bpy.data.texts:
            self.report({'WARNING'}, "No text selected")
            return {'CANCELLED'}

        text_block = bpy.data.texts[self.text_name]
        text_name = self.text_name

        # Open in new window
        try:
            bpy.ops.wm.window_new()
            new_window = context.window_manager.windows[-1]
            new_screen = new_window.screen

            # Change the area to TEXT_EDITOR
            for area in new_screen.areas:
                area.type = 'TEXT_EDITOR'
                # Need to use timer to set text after area type change
                def set_text():
                    for a in new_screen.areas:
                        if a.type == 'TEXT_EDITOR':
                            if text_name in bpy.data.texts:
                                a.spaces.active.text = bpy.data.texts[text_name]
                            return None
                    return None
                bpy.app.timers.register(set_text, first_interval=0.1)
                break

            self.report({'INFO'}, f"Opened: {text_name}")
        except Exception as e:
            self.report({'WARNING'}, f"Could not open window: {e}")

        return {'FINISHED'}
