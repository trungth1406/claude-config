# claude-config

Global Claude Code doctrine — the skills-first working flow, hard guards, and
standalone rules. Mirror of `~/.claude/` (doctrine files only; no settings,
no permissions, no machine state).

## Layout

- `CLAUDE.md` — the interconnected doctrine: skills-first preamble, The Flow
  (grill -> design -> to-spec/to-tickets -> implement -> review gate), hard
  guards, agent protocol.
- `rules/` — standalone directives, each injected into every session:
  - `ticket-gate.md` — no implementation work without /to-tickets
  - `review-qa-gate.md` — /code-review + /qa mandatory after implementation
  - `test-gate.md` — no untested code commits; never bend a test; 80% hard floor
  - `code-style.md` — no emoji, self-documenting code, language standards
  - `docs-routing.md` — obsidian-vault two-tier docs routing
  - `graphify.md` — second brain: code graph, wikilinks, MCP querying
  - `teaching.md` — teach skill's interactive-HTML standard
  - `context7.md` — ctx7 CLI for all library/framework docs lookups
- `flow-reminder.md` — condensed flow, injected on every prompt via hook.

## Install on a new machine

```sh
cp CLAUDE.md flow-reminder.md ~/.claude/
mkdir -p ~/.claude/rules && cp rules/*.md ~/.claude/rules/
```

Wire the per-prompt reminder hook into `~/.claude/settings.json`:

```json
"hooks": {
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "cat ~/.claude/flow-reminder.md 2>/dev/null || true"
        }
      ]
    }
  ]
}
```

`CLAUDE.md` and `rules/*.md` load automatically; only the hook needs wiring.

## Sync

Live files are the source of truth; this repo is the mirror.

```sh
# pull latest live state into the repo
cp ~/.claude/CLAUDE.md ~/.claude/flow-reminder.md . && cp ~/.claude/rules/*.md rules/

# push repo state onto a machine
cp CLAUDE.md flow-reminder.md ~/.claude/ && cp rules/*.md ~/.claude/rules/
```

Referenced skills (clean-code, to-tickets, implement, code-review, qa, ...)
are installed separately; this repo carries only the doctrine that routes to
them.
