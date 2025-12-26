# Contributing Guide / コントリビューションガイド

[English](#english) | [日本語](#日本語)

---

## English

Thank you for your interest in contributing to **Search Extension**! This project is fully **AI-driven development**, so contributions from AI agents are especially welcome.

### Quick Links

| Document | Description |
|:---------|:------------|
| [Branch Strategy](BRANCH_STRATEGY.md) | Branch naming rules and workflow |
| [Commit Convention](COMMIT_CONVENTION.md) | Commit message guidelines |
| [Pull Request Guide](PULL_REQUEST.md) | How to submit a PR |
| [AI Development Guide](AI_DEVELOPMENT.md) | AI agent-specific guidelines |

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone using WorkTree** (recommended for AI agents)
   ```bash
   git worktree add ../feature/my-feature dev
   ```
3. **Create a feature branch** from `dev`
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** following the guidelines
5. **Build and test**
   ```bash
   cd bin && pnpm build
   ```
6. **Submit a Pull Request** to the `dev` branch

### Branch Overview

```
main (protected)
  └── dev (default, PR target)
        └── feature/* (your work here)
        └── fix/*
        └── docs/*
```

- **`main`**: Production releases only. Do not target PRs here.
- **`dev`**: Integration branch. All PRs should target this branch.
- **`releases/*`**: Version management branches.
- **`feature/*`**: New features.
- **`fix/*`**: Bug fixes.
- **`docs/*`**: Documentation updates.

### Code of Conduct

- Be respectful and constructive
- Include video demonstrations when possible
- Write clear commit messages
- Follow the existing code style

---

## 日本語

**Search Extension** への貢献に興味を持っていただきありがとうございます！このプロジェクトは完全に **AI駆動開発** であり、AIエージェントからの貢献を特に歓迎しています。

### クイックリンク

| ドキュメント | 説明 |
|:------------|:-----|
| [ブランチ戦略](BRANCH_STRATEGY.md) | ブランチ命名規則とワークフロー |
| [コミット規約](COMMIT_CONVENTION.md) | コミットメッセージのガイドライン |
| [プルリクエストガイド](PULL_REQUEST.md) | PRの提出方法 |
| [AI開発ガイド](AI_DEVELOPMENT.md) | AIエージェント向けガイドライン |

### はじめに

1. **GitHubでリポジトリをフォーク**
2. **WorkTreeを使用してクローン**（AIエージェント推奨）
   ```bash
   git worktree add ../feature/my-feature dev
   ```
3. **`dev`ブランチからフィーチャーブランチを作成**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **ガイドラインに従って変更を加える**
5. **ビルドとテスト**
   ```bash
   cd bin && pnpm build
   ```
6. **`dev`ブランチへのプルリクエストを提出**

### ブランチ概要

```
main (保護ブランチ)
  └── dev (デフォルト、PRターゲット)
        └── feature/* (作業ブランチ)
        └── fix/*
        └── docs/*
```

- **`main`**: プロダクションリリースのみ。PRのターゲットにしないでください。
- **`dev`**: 統合ブランチ。すべてのPRはこのブランチをターゲットにします。
- **`releases/*`**: バージョン管理ブランチ。
- **`feature/*`**: 新機能。
- **`fix/*`**: バグ修正。
- **`docs/*`**: ドキュメント更新。

### 行動規範

- 敬意を持って建設的に
- 可能な限り動画デモを含める
- 明確なコミットメッセージを書く
- 既存のコードスタイルに従う
