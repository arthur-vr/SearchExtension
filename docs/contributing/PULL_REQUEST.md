# Pull Request Guide / プルリクエストガイド

[English](#english) | [日本語](#日本語)

---

## English

### Before Submitting

1. **Ensure your branch is up to date with `dev`**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout your-branch
   git rebase dev
   ```

2. **Build and verify**
   ```bash
   cd bin && pnpm build
   ```

3. **Test your changes in Blender**
   - Install the built addon
   - Verify the feature works as expected
   - Check for any console errors

### PR Requirements

#### Required

- [ ] Descriptive title following commit convention: `<type>(<scope>): <description>`
- [ ] Clear description of changes
- [ ] Builds successfully (`cd bin && pnpm build`)
- [ ] Tested in Blender
- [ ] Targets `dev` branch (NOT `main`)

#### Highly Recommended

- [ ] **Video demonstration** of the feature/fix
- [ ] Screenshots if UI changes are involved
- [ ] Update relevant documentation
- [ ] Add/update operator README if applicable

### PR Title Format

Follow the same format as commit messages:

```
feat(nanobanana_texture_gen): add atlas generation mode
fix(add_camera): handle scene without camera
docs(contributing): add PR guidelines
```

### PR Description Template

Use this template for your PR description:

```markdown
## Summary
[Brief description of what this PR does]

## Changes
- [Change 1]
- [Change 2]
- [Change 3]

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Testing
[Describe how you tested the changes]

## Screenshots/Video
[Attach screenshots or video demonstration]

## Related Issues
Closes #[issue number]

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have tested my changes in Blender
- [ ] I have updated the documentation accordingly
- [ ] My changes generate no new warnings
```

### Video Demonstration

We **strongly encourage** including a video demonstration. This helps:

- Reviewers understand the changes quickly
- Document the feature for future reference
- Catch UI/UX issues early

**Recommended tools:**
- OBS Studio (free)
- Windows Game Bar (Win+G)
- LICEcap (for GIFs)

### Review Process

1. **Automated checks**: Build verification
2. **Code review**: Maintainer reviews code changes
3. **Testing**: Maintainer tests in Blender if needed
4. **Feedback**: Address any requested changes
5. **Merge**: PR is merged to `dev`

---

## 日本語

### 提出前に

1. **ブランチが`dev`の最新状態であることを確認**
   ```bash
   git checkout dev
   git pull origin dev
   git checkout your-branch
   git rebase dev
   ```

2. **ビルドと確認**
   ```bash
   cd bin && pnpm build
   ```

3. **Blenderで変更をテスト**
   - ビルドしたアドオンをインストール
   - 機能が期待通りに動作することを確認
   - コンソールエラーがないか確認

### PR要件

#### 必須

- [ ] コミット規約に従った説明的なタイトル: `<type>(<scope>): <description>`
- [ ] 変更の明確な説明
- [ ] ビルド成功 (`cd bin && pnpm build`)
- [ ] Blenderでテスト済み
- [ ] `dev`ブランチをターゲット（`main`ではない）

#### 強く推奨

- [ ] 機能/修正の**動画デモンストレーション**
- [ ] UI変更がある場合はスクリーンショット
- [ ] 関連ドキュメントの更新
- [ ] 該当する場合はオペレーターREADMEの追加/更新

### PRタイトル形式

コミットメッセージと同じ形式に従います：

```
feat(nanobanana_texture_gen): アトラス生成モードを追加
fix(add_camera): カメラのないシーンを処理
docs(contributing): PRガイドラインを追加
```

### PR説明テンプレート

PR説明には以下のテンプレートを使用：

```markdown
## 概要
[このPRが何をするかの簡単な説明]

## 変更点
- [変更1]
- [変更2]
- [変更3]

## 変更の種類
- [ ] 新機能
- [ ] バグ修正
- [ ] ドキュメント更新
- [ ] リファクタリング
- [ ] その他（説明してください）

## テスト
[変更をどのようにテストしたか説明]

## スクリーンショット/動画
[スクリーンショットまたは動画デモを添付]

## 関連イシュー
Closes #[イシュー番号]

## チェックリスト
- [ ] コードはプロジェクトのスタイルガイドラインに従っている
- [ ] Blenderで変更をテストした
- [ ] ドキュメントを適切に更新した
- [ ] 変更で新しい警告は発生しない
```

### 動画デモンストレーション

動画デモンストレーションを含めることを**強く推奨**します。これにより：

- レビュアーが変更を素早く理解できる
- 将来の参照のために機能をドキュメント化
- UI/UXの問題を早期に発見

**推奨ツール：**
- OBS Studio（無料）
- Windows Game Bar（Win+G）
- LICEcap（GIF用）

### レビュープロセス

1. **自動チェック**: ビルド検証
2. **コードレビュー**: メンテナがコード変更をレビュー
3. **テスト**: 必要に応じてメンテナがBlenderでテスト
4. **フィードバック**: リクエストされた変更に対応
5. **マージ**: PRが`dev`にマージ
