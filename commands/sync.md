---
description: Install the doctrine (CLAUDE.md + rules + bundled skills) into ~/.claude, overriding local copies
---

Sync the flow doctrine from this plugin into the live ~/.claude directory.
The plugin payload is the source of truth: install everything, overriding
existing local copies.

1. Install with override: copy "${CLAUDE_PLUGIN_ROOT}/CLAUDE.md" to
   ~/.claude/CLAUDE.md, "${CLAUDE_PLUGIN_ROOT}/rules/"*.md into
   ~/.claude/rules/, and each skill directory under
   "${CLAUDE_PLUGIN_ROOT}/bundled-skills/" into ~/.claude/skills/ (create
   directories if missing). Only .md files from rules/. NEVER copy
   rules-optional/ — those install only by explicit per-machine choice.
2. Report per file: overwritten (changed), already current, or new.
3. Run python3 "${CLAUDE_PLUGIN_ROOT}/validate.py" and report its output —
   advisory, not a gate: the files above are already installed either way.
   If it reports missing skills, tell the user to run
   /setup-matt-pocock-skills for the baseline and list what else is missing.
4. Install or update the neurons layer: run
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/install-neurons.sh" and report its
   output. It pulls the latest neurons release binary (platform-aware),
   installs it, and registers the MCP server if absent - idempotent, and
   it skips gracefully when gh or claude are unavailable.
5. Inspect ~/.claude/settings.json for a legacy manual UserPromptSubmit hook
   that cats a flow-reminder file. If present, warn: the plugin hook now
   injects the reminder, so every prompt is being double-injected. Recommend
   removing the manual hook, but do not edit settings.json without the
   user's explicit confirmation.
