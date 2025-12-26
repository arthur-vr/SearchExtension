# NanoBanana (Texture Generation)

## Demo Link (x.com)

## Description
English:
NanoBanana is an AI-powered texture generation tool integrated directly into Blender. It supports UV-based generation, camera-view based generation, and tileable atlas generation using prompts.

日本語:
NanoBananaは、Blenderに直接統合されたAI駆動のテクスチャ生成ツールです。UVベースの生成、カメラビューベースの生成、およびプロンプトを使用したタイリング可能なアトラス生成をサポートしています。

## Download
English:
This is part of the Search Extension addon.
[Download](https://github.com/arthur-vr/SearchExtension/releases)

## How to use

English:
- Open the Image Editor.
- Access the `NanoBanana` tab in the sidebar (N-panel).
- Or search for `NanoBanana` in the F3 search menu.

日本語:
- 画像エディタを開きます。
- サイドバー（Nパネル）の `NanoBanana` タブにアクセスします。
- または、F3検索メニューで `NanoBanana` を検索します。

## Panel Description
![Panel](./images/demo_panel.png)

English:
- **UV Base Mode**: Generate textures based on UV bake.
- **Camera Base Mode**: Generate textures using the camera view.
- **Atlas Base Mode**: Generate tileable textures from prompts (presets available).
- **Settings**: Configure API Key and Model (Gemini).
- **History**: View, load, or copy previous prompts and generation settings.

日本語:
- **UV Base Mode**: UVベイクに基づいてテクスチャを生成します。
- **Camera Base Mode**: カメラビューを使用してテクスチャを生成します。
- **Atlas Base Mode**: プロンプトからタイリング可能なテクスチャを生成します（プリセットあり）。
- **Settings**: APIキーとモデル(Gemini)を設定します。
- **History**: 以前のプロンプトや生成設定を表示、ロード、コピーできます。

## Differences from other tools
English:
- **Direct AI Integration**: Uses `Google Gemini API` to generate textures directly within Blender.
- **Integrated Workflow**: Seamlessly bake, generate, and apply textures without external software.

日本語:
- **AI直接統合**: `Google Gemini API` を使用してBlender内で直接テクスチャを生成します。
- **統合ワークフロー**: 外部ソフトを使わずに、ベイク、生成、適用をシームレスに行えます。

## Q&A
### English:
#### Image generation takes time
##### Since it communicates with the Gemini API for generation, it relies on internet speed and API response times.

#### Quality of generated textures
##### It depends on the selected AI model and the input prompts/references. Try refining your prompts or using different reference images.

### 日本語:
#### 画像生成に時間がかかる
##### 生成のためにGemini APIと通信しているため、インターネット速度やAPIの応答時間に依存します。

#### 生成されたテクスチャの画質について
##### 選択したAIモデルや入力プロンプト、参照画像に依存します。プロンプトを調整するか、異なる参照画像を試してみてください。
