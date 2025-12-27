### FROM_ROOT_RULES ###


# basic rules
- after implementation, execute cd bin/;pnpm build to update zip

# structure

```
├── bin/                  # Build scripts and output
├── releases/             # Release zip files
├── src/                  # Source code (Blender addon)
│   ├── __init__.py       # Main addon registration
│   ├── _commons/         # Shared utilities and constants
│   └── <operator_name>/  # Each operator has its own folder
│       ├── __init__.py   # Operator registration
│       └── README.md     # (if exists) Operator documentation
└── README.md             # Project documentation
```

## src/ folder structure

Each folder under `src/` represents a Blender operator. The basic structure is:
- `__init__.py` - Registers the operator with Blender

**IMPORTANT**: If a `README.md` exists in an operator folder, READ IT FIRST before making any changes. The README contains important context and implementation details specific to that operator.

---

# AI Rule System

## Overview

Rules are stored in `.agent/rules/` as Markdown files with YAML frontmatter containing:
- `tags`: Searchable tags for categorization
- `simhash`: Locality-sensitive hash for similarity search
- `title`: Human-readable title
- `created`: Creation date

## Searching Rules

Use the CLI command to search for relevant rules:

```bash
cd bin && pnpm cli search-rule --query "your search text" --tags "tag1,tag2" --limit 10
```

### Search Features (Hybrid Search)
1. **Text Match (50%)**: Exact phrase and word matching in content/filename
2. **SimHash Similarity (30%)**: Semantic similarity via locality-sensitive hashing
3. **Tag Match (20%)**: Exact tag matching

Results are ranked by combined score. Even with low scores, up to `--limit` results are always returned.

### Parameters
- `--query` (required): Search text
- `--tags` (optional): Comma-separated tags to filter
- `--limit` (optional, default: 10): Maximum results

## Adding Rules

**IMPORTANT**: Always use the CLI command to add rules. This ensures proper SimHash and metadata generation.

```bash
cd bin && pnpm cli add-rule --name "rule-name" --title "Rule Title" --tags "tag1,tag2,tag3" --content "Your rule content here..."
```

### Parameters
- `--name` (required): File name (will be sanitized, .md added automatically)
- `--title` (optional): Human-readable title
- `--tags` (required): Comma-separated tags
- `--content` (required): Rule content in Markdown

### Naming Convention
Use descriptive, hyphenated names that are:
- English only
- AI-readable and searchable
- Single responsibility (one topic per rule)
- Example: `blender-uv-bake-instead-of-camera-render`

### Tag Guidelines
- Use lowercase
- Be specific but not too granular
- Common categories: `blender`, `api`, `error`, `python`, `gemini`, etc.