# Render and Save Image

## Demo Link (x.com)


## Description
English:
Render the current scene and save it as a Blender image data-block (packed into the .blend file). Supports auto-repeat for continuous rendering and quality presets for quick previews.

日本語:
現在のシーンをレンダリングし、Blenderの画像データブロックとして保存します（.blendファイルにパック）。連続レンダリングのための自動繰り返しと、クイックプレビュー用の品質プリセットをサポートしています。

## Download
English:
This is part of the Search Extension addon.
[Download](https://github.com/arthur-vr/SearchExtension/releases)

## How to use
English:
- Press F3 and search for `Render and Save Image`
- Enter a custom name (optional) or leave blank for timestamped name
- Adjust quality settings if needed
- Enable Auto Repeat for continuous rendering at set intervals

日本語:
- F3を押して `Render and Save Image` を検索
- カスタム名を入力（オプション）、空白の場合はタイムスタンプ名
- 必要に応じて品質設定を調整
- 自動繰り返しを有効にして設定間隔で連続レンダリング

## Panel Description
English:
- **Name (optional)**: Custom name for the rendered image
- **Set as Active Image**: Automatically display in Image Editors
- **Quick Save Quality**:
  - Resolution Level (1-10): Render size scale (1=10%, 10=100%)
  - Sample Level (1-10): Cycles sample ratio
  - Use JPEG for Quick Saves: Compress as JPEG instead of PNG
  - JPEG Quality Level (1-10): Compression quality
- **Enable Auto Repeat**: Repeat rendering automatically (requires custom name)
- **Repeat Interval**: Seconds between automatic renders

日本語:
- **名前（オプション）**: レンダリング画像のカスタム名
- **アクティブ画像に設定**: Image Editorに自動表示
- **クイック保存品質**:
  - 解像度レベル (1-10): レンダーサイズスケール (1=10%, 10=100%)
  - サンプルレベル (1-10): Cyclesサンプル比率
  - クイック保存にJPEGを使用: PNGの代わりにJPEG圧縮
  - JPEG品質レベル (1-10): 圧縮品質
- **自動繰り返し有効**: 自動的にレンダリングを繰り返す（カスタム名必須）
- **繰り返し間隔**: 自動レンダー間の秒数

## Differences from other tools
English:
- **Packed Images**: Saves directly as Blender image data-block (no external files)
- **Auto Repeat**: Continuous rendering with configurable interval
- **Persistent Settings**: Settings are saved across Blender sessions
- **Smart Skip**: Detects unchanged renders to avoid redundant saves

日本語:
- **パック画像**: Blender画像データブロックとして直接保存（外部ファイルなし）
- **自動繰り返し**: 設定可能な間隔で連続レンダリング
- **永続設定**: Blenderセッション間で設定を保存
- **スマートスキップ**: 変更のないレンダーを検出して冗長な保存を回避
