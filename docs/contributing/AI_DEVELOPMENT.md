# AI Development Guide / AI開発ガイド

[English](#english) | [日本語](#日本語)

---

## English

This project is **fully AI-driven**. This guide helps AI agents and developers using AI assistants contribute effectively.

### Supported AI Agents

This project includes rule files compatible with multiple AI agents:

| Agent | Rule File |
|:------|:----------|
| Gemini | `GEMINI.md` |
| Claude | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| Cline | `.clinerules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Generic | `AGENTS.md` |

### Project Structure Knowledge

AI agents should be aware of:

```
├── bin/                  # Build scripts and output
├── releases/             # Release zip files
├── src/                  # Source code (Blender addon)
│   ├── __init__.py       # Main addon registration
│   ├── _commons/         # Shared utilities and constants
│   └── <operator_name>/  # Each operator has its own folder
│       ├── __init__.py   # Operator registration
│       └── README.md     # (if exists) Operator documentation
├── docs/
│   └── contributing/     # This guide
└── .agent/               # Agent-specific rules and commands
    ├── root-rules.md     # Root rules for all agents
    ├── rules/            # Searchable rules database
    ├── commands/         # Custom commands
    └── workflows/        # Automated workflows
```

### AI Agent Workflow

#### 1. Understanding Context

Before making changes:

1. **Read the root rules**: `.agent/root-rules.md`
2. **Search for relevant rules**:
   ```bash
   cd bin && pnpm cli search-rule --query "your topic" --tags "blender,api"
   ```
3. **Check operator README**: If modifying an operator, read its `README.md` first

#### 2. Making Changes

1. **Follow the branch strategy**: Create appropriate feature/fix branches
2. **Use atomic commits**: One logical change per commit
3. **Write descriptive messages**: Follow the commit convention
4. **Build after changes**:
   ```bash
   cd bin && pnpm build
   ```

#### 3. Adding Rules

When you discover something important (a fix, a pattern, a gotcha):

```bash
cd bin && pnpm cli add-rule --name "rule-name" --title "Rule Title" --tags "tag1,tag2" --content "Rule content..."
```

**Rule naming guidelines:**
- English only
- Use hyphens (e.g., `blender-uv-bake-vertex-color`)
- Single responsibility per rule
- Descriptive and searchable

#### 4. Submitting Work

1. Ensure build passes
2. Write clear PR description
3. Include video demonstration if possible
4. Reference any rules you added

### Best Practices for AI Agents

#### Do ✅

- Read existing code before modifying
- Check for operator README files
- Use the rule search system
- Make atomic, focused commits
- Document discoveries as rules
- Test in Blender before submitting

#### Don't ❌

- Make changes without understanding context
- Skip the build step
- Create overly complex commits
- Ignore existing patterns and conventions
- Forget to update documentation

### WorkTree Recommendation

For parallel development, use Git WorkTree:

```bash
# Create a new worktree for your feature
git worktree add ../feature/my-feature dev

# Work in the new directory
cd ../feature/my-feature

# When done, clean up
git worktree remove ../feature/my-feature
```

This allows:
- Multiple features in parallel
- Clean separation of work
- Easy context switching

---

## 日本語

このプロジェクトは**完全にAI駆動**です。このガイドはAIエージェントとAIアシスタントを使用する開発者が効果的に貢献できるようにします。

### サポートされているAIエージェント

このプロジェクトには複数のAIエージェントと互換性のあるルールファイルが含まれています：

| エージェント | ルールファイル |
|:------------|:--------------|
| Gemini | `GEMINI.md` |
| Claude | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| Cline | `.clinerules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| 汎用 | `AGENTS.md` |

### プロジェクト構造の理解

AIエージェントが把握すべき内容：

```
├── bin/                  # ビルドスクリプトと出力
├── releases/             # リリースzipファイル
├── src/                  # ソースコード（Blenderアドオン）
│   ├── __init__.py       # メインアドオン登録
│   ├── _commons/         # 共有ユーティリティと定数
│   └── <operator_name>/  # 各オペレーターは独自のフォルダ
│       ├── __init__.py   # オペレーター登録
│       └── README.md     # (存在する場合) オペレータードキュメント
├── docs/
│   └── contributing/     # このガイド
└── .agent/               # エージェント固有のルールとコマンド
    ├── root-rules.md     # すべてのエージェント用のルートルール
    ├── rules/            # 検索可能なルールデータベース
    ├── commands/         # カスタムコマンド
    └── workflows/        # 自動化されたワークフロー
```

### AIエージェントワークフロー

#### 1. コンテキストの理解

変更を加える前に：

1. **ルートルールを読む**: `.agent/root-rules.md`
2. **関連ルールを検索**：
   ```bash
   cd bin && pnpm cli search-rule --query "トピック" --tags "blender,api"
   ```
3. **オペレーターREADMEを確認**: オペレーターを変更する場合、まずその`README.md`を読む

#### 2. 変更を加える

1. **ブランチ戦略に従う**: 適切なfeature/fixブランチを作成
2. **アトミックなコミット**: 1つの論理的な変更につき1コミット
3. **説明的なメッセージ**: コミット規約に従う
4. **変更後にビルド**：
   ```bash
   cd bin && pnpm build
   ```

#### 3. ルールの追加

重要なこと（修正、パターン、注意点）を発見した場合：

```bash
cd bin && pnpm cli add-rule --name "rule-name" --title "ルールタイトル" --tags "tag1,tag2" --content "ルール内容..."
```

**ルール命名ガイドライン：**
- 英語のみ
- ハイフンを使用（例：`blender-uv-bake-vertex-color`）
- ルールごとに単一の責任
- 説明的で検索可能

#### 4. 作業の提出

1. ビルドが通ることを確認
2. 明確なPR説明を書く
3. 可能な限り動画デモを含める
4. 追加したルールがあれば参照

### AIエージェントのベストプラクティス

#### すべきこと ✅

- 変更前に既存コードを読む
- オペレーターREADMEファイルを確認
- ルール検索システムを使用
- アトミックで焦点を絞ったコミット
- 発見をルールとしてドキュメント化
- 提出前にBlenderでテスト

#### してはいけないこと ❌

- コンテキストを理解せずに変更
- ビルドステップをスキップ
- 過度に複雑なコミットを作成
- 既存のパターンと規約を無視
- ドキュメントの更新を忘れる

### WorkTreeの推奨

並行開発には、Git WorkTreeを使用：

```bash
# 機能用の新しいworktreeを作成
git worktree add ../feature/my-feature dev

# 新しいディレクトリで作業
cd ../feature/my-feature

# 完了したらクリーンアップ
git worktree remove ../feature/my-feature
```

これにより：
- 複数の機能を並行して開発
- 作業のクリーンな分離
- 簡単なコンテキスト切り替え
