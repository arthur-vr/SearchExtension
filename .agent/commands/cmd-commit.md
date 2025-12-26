# Commit Command

## Usage

Use this command to have the AI automatically generate commit messages based on the current changes.

## Instructions for AI

When this command is invoked:

1.  **Read the convention**: Follow the commit message format defined in `docs/contributing/COMMIT_CONVENTION.md`
2.  **Analyze changes**: Run `git diff --staged` (or `git diff` if nothing is staged) to understand what has been changed
3.  **Generate commit message**: Create a commit message following the Conventional Commits format
4.  **Language**: All commit messages MUST be written in English
5.  **Execute commit**: Propose the `git commit -m "..."` command for user approval

## Example Workflow

```bash
# AI will run this to see changes
git diff --staged

# AI will then propose a commit like:
git commit -m "feat(component_name): add new feature description"
```

## Notes

- If changes span multiple logical units, suggest splitting into multiple commits
- Always include a meaningful scope in parentheses
- Use imperative mood ("add" not "added", "fix" not "fixed")