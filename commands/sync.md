---
description: Install or update the doctrine (CLAUDE.md + rules) into ~/.claude and verify consistency
---

Sync the flow doctrine from this plugin into the live ~/.claude directory.

1. Gate on the payload first: run python3 "${CLAUDE_PLUGIN_ROOT}/validate.py"
   and report its output verbatim. If it fails, stop before writing anything.
   When the failures are missing skills (fresh machine): the baseline fix is
   running /setup-matt-pocock-skills — derive the expected skill set from it
   rather than hand-listing. Whatever it does not cover comes from this
   plugin's bundled-skills/ (installed in step 3) or the tool installs in the
   README (graphify, the superpowers plugin for systematic-debugging).
2. Diff before writing: compare "${CLAUDE_PLUGIN_ROOT}/CLAUDE.md" against
   ~/.claude/CLAUDE.md and each "${CLAUDE_PLUGIN_ROOT}/rules/"*.md against its
   ~/.claude/rules/ counterpart. Report per file: will change, already
   current, or new.
3. Copy only then: "${CLAUDE_PLUGIN_ROOT}/CLAUDE.md" to ~/.claude/CLAUDE.md,
   "${CLAUDE_PLUGIN_ROOT}/rules/"*.md into ~/.claude/rules/, and each skill
   directory under "${CLAUDE_PLUGIN_ROOT}/bundled-skills/" into
   ~/.claude/skills/ (create directories if missing). Only .md files from
   rules/. NEVER copy rules-optional/ — those install only by explicit
   per-machine choice.
4. Inspect ~/.claude/settings.json for a legacy manual UserPromptSubmit hook
   that cats a flow-reminder file. If present, warn: the plugin hook now
   injects the reminder, so every prompt is being double-injected. Recommend
   removing the manual hook, but do not edit settings.json without the
   user's explicit confirmation.
