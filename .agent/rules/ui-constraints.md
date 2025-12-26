---
title: "UI Constraints and Rules"
tags: ["ui", "constraints", "blender", "addon", "rules"]
simhash: "0262b2192545ec3f"
created: "2025-12-25"
---

# UI Constraints (NEVER Rules)\n\nThis addon has strict UI constraints due to its "search-based operator launcher" philosophy:\n\n## NEVER Do These\n\n- **NEVER use side panels (N-panel)** - All features must be accessible via search (F3)\n- **NEVER create persistent UI elements** - No toolbars, no permanent panels\n- **Modal dialogs only** - Use popup dialogs, invoke popups, or modal operators\n- **No menus in header/topbar** - Keep the UI minimal and search-driven\n\n## Core Concept\n\nThe core concept: Users press F3, search for the operator, and interact via modal/popup only.