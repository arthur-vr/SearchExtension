"""Localization support for NanoBanana addon.

Uses Blender's built-in translation system.
"""

import bpy

# Translation context
TRANSLATION_CONTEXT = "NanoBanana"

# Translation dictionary: {locale: {(context, key): translated_string}}
translations_dict = {
    "ja_JP": {
        # UI Labels
        ("*", "Bake"): "ベイク",
        ("*", "Camera"): "カメラ",
        ("*", "References"): "参照",
        ("*", "Prompt"): "プロンプト",
        ("*", "Settings"): "設定",
        ("*", "History"): "履歴",
        
        # Bake section
        ("*", "No Mesh Selected"): "メッシュが選択されていません",
        ("*", "Include:"): "含める:",
        ("*", "Preview"): "プレビュー",
        
        # Camera section
        ("*", "Workbench Mode"): "Workbenchモード",
        ("*", "Active:"): "アクティブ:",
        ("*", "Focus View"): "ビューにフォーカス",
        ("*", "Render to Image"): "画像にレンダリング",
        ("*", "No Active Camera"): "アクティブカメラがありません",
        ("*", "No Cameras in Scene"): "シーンにカメラがありません",
        ("*", "Add Camera"): "カメラを追加",
        
        # References section
        ("*", "File Paths"): "ファイルパス",
        ("*", "Blender Images"): "Blender画像",
        
        # Prompt section
        ("*", "Use Text Editor"): "テキストエディターを使用",
        ("*", "Open in Text Editor"): "テキストエディターで開く",
        
        # Common
        ("*", "Texture Prefix"): "テクスチャ接頭辞",
        ("*", "Append Timestamp"): "タイムスタンプを追加",
        ("*", "Add Image Node"): "イメージノードを追加",
        ("*", "Seed"): "シード",
        ("*", "Generate"): "生成",
        
        # Messages
        ("*", "Texture generation complete!"): "テクスチャ生成が完了しました！",
        ("*", "Generation already in progress. Please wait..."): "生成中です。お待ちください...",
        ("*", "No reference images provided."): "参照画像がありません。",
        ("*", "API Key is not set."): "APIキーが設定されていません。",
        
        # History
        ("*", "Copy"): "コピー",
        ("*", "Load"): "読み込み",
        ("*", "Delete"): "削除",
        ("*", "Clear All"): "すべてクリア",
        ("*", "No history yet"): "履歴がありません",
    }
}


def get_text(text):
    """Get translated text based on current Blender locale.
    
    Args:
        text: Original English text
        
    Returns:
        str: Translated text or original if no translation found
    """
    try:
        # Get current Blender locale
        locale = bpy.app.translations.locale
        
        if locale in translations_dict:
            # Try to find translation with wildcard context
            key = ("*", text)
            if key in translations_dict[locale]:
                return translations_dict[locale][key]
        
        return text
    except:
        return text


# Shorthand alias
_ = get_text


def register():
    """Register translations with Blender."""
    try:
        bpy.app.translations.register(__name__, translations_dict)
    except:
        pass  # Translations may already be registered or not supported


def unregister():
    """Unregister translations from Blender."""
    try:
        bpy.app.translations.unregister(__name__)
    except:
        pass
