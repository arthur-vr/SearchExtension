import bpy
from . import operator
from . import ui
from . import localization


def menu_func(self, context):
    self.layout.operator(operator.NanoBananaTextureGenOperator.bl_idname)


def register():
    # 0. Register translations
    localization.register()
    
    # 1. Register PropertyGroups first (required for CollectionProperty)
    bpy.utils.register_class(ui.NanoBananaFileRefItem)
    bpy.utils.register_class(ui.NanoBananaImageRefItem)

    # 2. Register properties that use PropertyGroups
    ui.register_properties()

    # 3. Register operators
    bpy.utils.register_class(operator.NanoBananaShowMessageOperator)
    bpy.utils.register_class(operator.NanoBananaFocusCameraOperator)
    bpy.utils.register_class(operator.NanoBananaAddCameraOperator)
    bpy.utils.register_class(operator.NanoBananaRenderCameraOperator)
    bpy.utils.register_class(operator.NanoBananaToggleWorkbenchOperator)
    bpy.utils.register_class(operator.NanoBananaSettingsOperator)
    bpy.utils.register_class(operator.NanoBananaApplyBakeOperator)
    bpy.utils.register_class(operator.NanoBananaCreatePromptTextOperator)
    bpy.utils.register_class(operator.NanoBananaOpenTextEditorOperator)
    bpy.utils.register_class(operator.NanoBananaTextureGenOperator)
    bpy.utils.register_class(operator.NanoBananaCopyPromptOperator)
    bpy.utils.register_class(operator.NanoBananaLoadPromptOperator)
    bpy.utils.register_class(operator.NanoBananaDeleteHistoryOperator)
    bpy.utils.register_class(operator.NanoBananaClearAllHistoryOperator)
    # List management operators
    bpy.utils.register_class(operator.NanoBananaAddFileRefOperator)
    bpy.utils.register_class(operator.NanoBananaRemoveFileRefOperator)
    bpy.utils.register_class(operator.NanoBananaAddImageRefOperator)
    bpy.utils.register_class(operator.NanoBananaRemoveImageRefOperator)

    # 4. Register panels
    bpy.utils.register_class(operator.NanoBananaHistoryPanel)

    # 5. Register menu
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    # Unregister menu
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    # Unregister panels
    bpy.utils.unregister_class(operator.NanoBananaHistoryPanel)

    # Unregister operators (reverse order)
    bpy.utils.unregister_class(operator.NanoBananaRemoveImageRefOperator)
    bpy.utils.unregister_class(operator.NanoBananaAddImageRefOperator)
    bpy.utils.unregister_class(operator.NanoBananaRemoveFileRefOperator)
    bpy.utils.unregister_class(operator.NanoBananaAddFileRefOperator)
    bpy.utils.unregister_class(operator.NanoBananaClearAllHistoryOperator)
    bpy.utils.unregister_class(operator.NanoBananaDeleteHistoryOperator)
    bpy.utils.unregister_class(operator.NanoBananaLoadPromptOperator)
    bpy.utils.unregister_class(operator.NanoBananaCopyPromptOperator)
    bpy.utils.unregister_class(operator.NanoBananaTextureGenOperator)
    bpy.utils.unregister_class(operator.NanoBananaOpenTextEditorOperator)
    bpy.utils.unregister_class(operator.NanoBananaCreatePromptTextOperator)
    bpy.utils.unregister_class(operator.NanoBananaApplyBakeOperator)
    bpy.utils.unregister_class(operator.NanoBananaSettingsOperator)
    bpy.utils.unregister_class(operator.NanoBananaToggleWorkbenchOperator)
    bpy.utils.unregister_class(operator.NanoBananaRenderCameraOperator)
    bpy.utils.unregister_class(operator.NanoBananaAddCameraOperator)
    bpy.utils.unregister_class(operator.NanoBananaFocusCameraOperator)
    bpy.utils.unregister_class(operator.NanoBananaShowMessageOperator)

    # Unregister properties
    ui.unregister_properties()

    # Unregister PropertyGroups last
    bpy.utils.unregister_class(ui.NanoBananaImageRefItem)
    bpy.utils.unregister_class(ui.NanoBananaFileRefItem)
    
    # Unregister translations
    localization.unregister()
