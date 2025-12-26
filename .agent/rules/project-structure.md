---
title: "Project Structure and Getting Started"
tags: ["structure", "blender", "addon", "guide"]
simhash: "83e3b6192445de71"
created: "2025-12-25"
---

# Project Structure\n\n## Getting Started\n\nWhen adding new functionality, **always start by reading `src/__init__.py`** to understand the module registration pattern.\n\n## Directory Layout\n\n```\n├── bin/                  # Build scripts and output\n├── releases/             # Release zip files\n├── src/                  # Source code (Blender addon)\n│   ├── __init__.py       # Main addon registration (START HERE)\n│   ├── _commons/         # Shared utilities and constants\n│   │   └── constants.py  # ADDON_NAME, ADDON_VERSION, etc.\n│   └── <operator_name>/  # Each operator has its own folder\n│       ├── __init__.py   # Operator registration\n│       └── README.md     # (if exists) READ FIRST\n└── README.md\n```\n\n## Important Notes\n\n- If a `README.md` exists in an operator folder, **READ IT FIRST**\n- After implementation, run: `cd bin/; pnpm build`