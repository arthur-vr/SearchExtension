---
title: "Implementation Guide - Read This First When Adding Features"
tags: ["implementation", "guide", "overview", "start"]
simhash: "03c3bf192553e031"
created: "2025-12-25"
---

# Implementation Guide

**When adding new features to this addon, read this first.**

## Available Rules

| Rule | What It Covers |
|------|----------------|
| spec-first-development | Write specification before coding |
| project-structure | Directory layout, where to start |
| operator-implementation | How to add operators, F3 registration, storage patterns |
| ui-constraints | UI philosophy (F3 search only, no panels) |
| post-implementation-checklist | What to do after implementation |

## Quick Start

1. Write spec in `.agent/specs/<feature>/` → see `spec-first-development.md`
2. Read `project-structure.md` → understand the codebase
3. Follow `operator-implementation.md` → implement your feature
4. Check `ui-constraints.md` → no side panels, F3 search only
5. Complete `post-implementation-checklist.md` → registry, README, build

## Core Concept

This addon is **search-driven**:
- Users press F3, search, and execute
- No persistent UI (no N-panel, no toolbars)
- Modal dialogs and popups only
