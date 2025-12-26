# Save UV Layout to Image

## Demo Link (x.com)


## Description
English:
Export the UV layout of the active mesh as a Blender image. Supports fill-only mode (no edge lines) and optional preview plane creation.

日本語:
アクティブメッシュのUVレイアウトをBlender画像としてエクスポートします。塗りつぶしのみモード（エッジラインなし）とオプションのプレビュープレーン作成をサポートしています。

## Download
English:
This is part of the Search Extension addon.
[Download](https://github.com/arthur-vr/SearchExtension/releases)

## How to use
English:
- Select a mesh object with UV layers
- Press F3 and search for `Save UV Layout to Image`
- Configure resolution and options in the dialog
- The UV layout is created as a Blender image

日本語:
- UVレイヤーを持つメッシュオブジェクトを選択
- F3を押して `Save UV Layout to Image` を検索
- ダイアログで解像度とオプションを設定
- UVレイアウトがBlender画像として作成されます

## Panel Description
English:
- **Resolution**: Image resolution (512-8192)
- **Create Preview Plane**: Generate a plane displaying the UV layout with emission shader
- **Bake Alpha**: Export with alpha channel (transparency)
- **Show Edge Lines**: Include UV edge lines (OFF = fill only)

日本語:
- **解像度**: 画像解像度（512-8192）
- **プレビュープレーン作成**: Emissionシェーダーで表示するUVレイアウトプレーンを生成
- **アルファベイク**: アルファチャンネル（透明度）付きでエクスポート
- **エッジライン表示**: UVエッジラインを含める（OFF = 塗りつぶしのみ）

## Differences from other tools
English:
- **Fill-only Mode**: Generate UV mask without edge lines (unique feature)
- **Preview Plane**: Instantly visualize UV layout on a 3D plane
- **Packed Output**: Saves as Blender image data-block (no external files)

日本語:
- **塗りつぶしのみモード**: エッジラインなしのUVマスクを生成（独自機能）
- **プレビュープレーン**: 3DプレーンでUVレイアウトを即座に可視化
- **パック出力**: Blender画像データブロックとして保存（外部ファイルなし）
