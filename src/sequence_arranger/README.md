# Sequence Arranger

## Demo Link (x.com)


## Description
English:
Arrange two objects based on mathematical sequences (Prime Numbers or Fibonacci). Creates a Geometry Nodes setup that instances objects at positions determined by the sequence.

日本語:
数学的数列（素数またはフィボナッチ）に基づいて2つのオブジェクトを配置します。数列によって決定された位置にオブジェクトをインスタンス化するジオメトリノードセットアップを作成します。

## Download
English:
This is part of the Search Extension addon.
[Download](https://github.com/arthur-vr/SearchExtension/releases)

## How to use
English:
- Select 2 objects (Object A for sequence positions, Object B for non-sequence positions)
- Press F3 and search for `Sequence Arranger`
- Choose sequence type, count, and spacing
- A new object with Geometry Nodes modifier is created

日本語:
- 2つのオブジェクトを選択（オブジェクトA = 数列位置用、オブジェクトB = 非数列位置用）
- F3を押して `Sequence Arranger` を検索
- 数列タイプ、数、間隔を選択
- ジオメトリノードモディファイアを持つ新しいオブジェクトが作成されます

## Panel Description
English:
- **Sequence Type**: Prime Numbers or Fibonacci Sequence
- **Count**: Number of positions to generate (1-1000)
- **Spacing**: Distance between positions

日本語:
- **数列タイプ**: 素数 または フィボナッチ数列
- **数**: 生成する位置の数（1-1000）
- **間隔**: 位置間の距離

## Differences from other tools
English:
- **Mathematical Patterns**: Uses prime numbers and Fibonacci sequence for artistic arrangements
- **Geometry Nodes**: Non-destructive setup with adjustable parameters
- **Two-object System**: Different objects for sequence vs non-sequence positions

日本語:
- **数学的パターン**: 素数とフィボナッチ数列を使用したアーティスティックな配置
- **ジオメトリノード**: 調整可能なパラメータを持つ非破壊的セットアップ
- **2オブジェクトシステム**: 数列位置と非数列位置に異なるオブジェクトを使用

## Q&A
### English:
#### How does the sequence work?
##### For each position (1 to Count), if the number matches the sequence (is prime or is a Fibonacci number), Object A is placed. Otherwise, Object B is placed.

### 日本語:
#### 数列はどのように機能しますか？
##### 各位置（1からCount）について、その数が数列に一致する（素数またはフィボナッチ数）場合はオブジェクトAが配置されます。そうでない場合はオブジェクトBが配置されます。
