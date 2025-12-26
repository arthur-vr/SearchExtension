# Commit Convention / コミット規約

[English](#english) | [日本語](#日本語)

---

## English

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Language Policy

**All commit messages must be written in English.** This ensures consistency across the codebase and makes the commit history accessible to all contributors.

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|:-----|:------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Code style changes (formatting, no code change) |
| `refactor` | Code refactoring (no feature or fix) |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `build` | Build system or dependency changes |
| `ci` | CI configuration changes |
| `chore` | Other changes that don't modify src |

### Scope

The scope should be the name of the operator or component affected:

- `nanobanana_texture_gen`
- `add_camera`
- `save_uv_layout`
- `preferences`
- `commons`
- `build`

### Examples

✅ **Good Commit Messages:**

```
feat(nanobanana_texture_gen): add vertex color bake mode

- Added VERTEX_COLOR as a new bake type option
- Implemented preview button for vertex bake
- Updated UI panel with toggle control
```

```
fix(add_camera): handle missing active camera gracefully

Previously the operator would crash if no active camera was set.
Now it displays a user-friendly error message.

Closes #42
```

```
docs(contributing): add branch strategy guide
```

```
refactor(commons): extract localization utilities
```

❌ **Bad Commit Messages:**

```
fixed stuff
```

```
WIP
```

```
update
```

```
feat: added new feature for the texture generation thing that does stuff
```

### AI Agent Guidelines

When using AI agents for development:

1. **Be descriptive**: AI agents should generate detailed commit messages
2. **Reference context**: Include relevant issue numbers or PR references
3. **Atomic commits**: One logical change per commit
4. **Body for complex changes**: Explain "why" in the body, not just "what"

---

## 日本語

このプロジェクトは [Conventional Commits](https://www.conventionalcommits.org/) 仕様に従います。

### 言語ポリシー

**すべてのコミットメッセージは英語で記述してください。** これにより、コードベース全体の一貫性が保たれ、すべてのコントリビューターがコミット履歴を理解しやすくなります。

### コミットメッセージの形式

```
<タイプ>(<スコープ>): <説明>

[オプションの本文]

[オプションのフッター]
```

### タイプ

| タイプ | 説明 |
|:------|:-----|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `style` | コードスタイルの変更（フォーマット、コード変更なし） |
| `refactor` | コードリファクタリング（機能追加やバグ修正なし） |
| `perf` | パフォーマンス改善 |
| `test` | テストの追加または更新 |
| `build` | ビルドシステムまたは依存関係の変更 |
| `ci` | CI設定の変更 |
| `chore` | srcを変更しないその他の変更 |

### スコープ

スコープは影響を受けるオペレーターまたはコンポーネントの名前にします：

- `nanobanana_texture_gen`
- `add_camera`
- `save_uv_layout`
- `preferences`
- `commons`
- `build`

### 例

✅ **良いコミットメッセージ：**（英語で記述）

```
feat(nanobanana_texture_gen): add vertex color bake mode

- Added VERTEX_COLOR as a new bake type option
- Implemented preview button for vertex bake
- Updated UI panel with toggle control
```

```
fix(add_camera): handle missing active camera gracefully

Previously the operator would crash if no active camera was set.
Now it displays a user-friendly error message.

Closes #42
```

```
docs(contributing): add branch strategy guide
```

```
refactor(commons): extract localization utilities
```

❌ **悪いコミットメッセージ：**

```
修正                           # NG: 日本語で書かれている
```

```
WIP
```

```
更新                           # NG: 日本語で書かれている
```

```
feat: テクスチャ生成のための新機能を追加した   # NG: 日本語で書かれている
```

### AIエージェント向けガイドライン

AIエージェントを使用した開発の場合：

1. **説明的に**: AIエージェントは詳細なコミットメッセージを生成すべき
2. **コンテキストを参照**: 関連するイシュー番号やPR参照を含める
3. **アトミックなコミット**: 1つの論理的な変更につき1コミット
4. **複雑な変更には本文を**: 本文で「何を」ではなく「なぜ」を説明
