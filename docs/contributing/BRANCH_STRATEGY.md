# Branch Strategy / ブランチ戦略

[English](#english) | [日本語](#日本語)

---

## English

### Branch Types

| Branch Type | Pattern | Description | Target |
|:------------|:--------|:------------|:-------|
| Main | `main` | Production releases only | Protected |
| Development | `dev` | Integration branch | PR target |
| Release | `releases/v*` | Version management | From dev |
| Feature | `feature/*` | New features | → dev |
| Fix | `fix/*` | Bug fixes | → dev |
| Hotfix | `hotfix/*` | Critical production fixes | → main & dev |
| Docs | `docs/*` | Documentation only | → dev |

### Branch Naming Convention

Feature and fix branches should follow this format:

```
<type>/<short-description>
```

#### Examples

✅ **Good Examples:**
- `feature/ai-texture-generation`
- `feature/add-camera-operator`
- `fix/uv-layout-export-crash`
- `fix/gemini-api-timeout`
- `docs/contributing-guide`
- `hotfix/critical-render-bug`

❌ **Bad Examples:**
- `my-feature` (missing type prefix)
- `feature/fix-something-and-add-new-thing` (multiple purposes)
- `feature/wip` (not descriptive)
- `Feature/CamelCase` (use lowercase with hyphens)

### Workflow

```
1. Fork the repository
2. Create a feature branch from `dev`
3. Work on your changes
4. Submit PR to `dev`
5. After review and merge, `dev` is periodically merged to `main`
6. Version tags are created from `releases/*` branches
```

### Protected Branches

- **`main`**: Direct pushes disabled. Only accepts PRs from `dev` or `hotfix/*`.
- **`dev`**: Direct pushes disabled. Accepts PRs from feature/fix branches.

### Version Management

Versions are managed through `releases/*` branches:

```
releases/v1.0.0
releases/v1.1.0
releases/v2.0.0
```

When a release is ready:
1. Create a release branch from `dev`: `releases/v1.2.0`
2. Final testing and fixes on the release branch
3. Merge to `main` and tag the version
4. Merge back to `dev` if hotfixes were applied

---

## 日本語

### ブランチの種類

| ブランチタイプ | パターン | 説明 | ターゲット |
|:--------------|:---------|:-----|:-----------|
| メイン | `main` | プロダクションリリースのみ | 保護 |
| 開発 | `dev` | 統合ブランチ | PRターゲット |
| リリース | `releases/v*` | バージョン管理 | devから |
| フィーチャー | `feature/*` | 新機能 | → dev |
| 修正 | `fix/*` | バグ修正 | → dev |
| ホットフィックス | `hotfix/*` | 重大な本番修正 | → main & dev |
| ドキュメント | `docs/*` | ドキュメントのみ | → dev |

### ブランチ命名規則

フィーチャーブランチと修正ブランチは以下の形式に従います：

```
<タイプ>/<短い説明>
```

#### 例

✅ **良い例：**
- `feature/ai-texture-generation`
- `feature/add-camera-operator`
- `fix/uv-layout-export-crash`
- `fix/gemini-api-timeout`
- `docs/contributing-guide`
- `hotfix/critical-render-bug`

❌ **悪い例：**
- `my-feature` (タイププレフィックスがない)
- `feature/fix-something-and-add-new-thing` (複数の目的)
- `feature/wip` (説明的でない)
- `Feature/CamelCase` (小文字とハイフンを使用)

### ワークフロー

```
1. リポジトリをフォーク
2. `dev`からフィーチャーブランチを作成
3. 変更を加える
4. `dev`へPRを提出
5. レビューとマージ後、`dev`は定期的に`main`にマージされる
6. バージョンタグは`releases/*`ブランチから作成
```

### 保護されたブランチ

- **`main`**: 直接プッシュ無効。`dev`または`hotfix/*`からのPRのみ受け付け。
- **`dev`**: 直接プッシュ無効。feature/fixブランチからのPRを受け付け。

### バージョン管理

バージョンは`releases/*`ブランチで管理されます：

```
releases/v1.0.0
releases/v1.1.0
releases/v2.0.0
```

リリース準備ができたら：
1. `dev`からリリースブランチを作成: `releases/v1.2.0`
2. リリースブランチで最終テストと修正
3. `main`にマージしてバージョンをタグ付け
4. ホットフィックスが適用された場合は`dev`にマージバック
