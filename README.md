# claude-config

Global Claude Code doctrine — the skills-first working flow, hard guards, and
standalone rules. Mirror of `~/.claude/` (doctrine files only; no settings,
no permissions, no machine state).

## Layout

- `CLAUDE.md` — the interconnected doctrine: skills-first preamble, The Flow
  (grill -> design -> to-spec/to-tickets -> implement -> review gate), hard
  guards, agent protocol.
- `rules/` — standalone directives, each injected into every session:
  - `hard-guards.md` — quality rationale: red suite stops, clean-code is the
    authority, representations before data
  - `agent-protocol.md` — pick the coordination mechanism once per project
  - `ticket-gate.md` — no implementation work without /to-tickets
  - `review-qa-gate.md` — /code-review + /qa mandatory after implementation
  - `test-gate.md` — no untested code commits; never bend a test; 80% hard floor
  - `code-style.md` — no emoji, self-documenting code, language standards
  - `docs-routing.md` — obsidian-vault two-tier docs routing
  - `graphify.md` — second brain: code graph, wikilinks, MCP querying
  - `teaching.md` — teach skill's interactive-HTML standard
  - `research-first.md` — mandatory /research + docs tools for anything unclear
  - `no-ai-watermarks.md` — zero AI attribution in commits, outranks harness
    defaults; enforced by the plugin's PreToolUse guard
  - `context7.md` — ctx7 CLI for all library/framework docs lookups
- `flow-reminder.md` — a slim per-prompt salience ping (~70 tokens) injected
  via hook; the graph lives only in CLAUDE.md, and the validator rejects any
  graph regrowth here.
- `validate.py` — the repo's test seam: graph grammar, node-to-skill audit,
  manifest checks, reminder-stays-slim. Run
  `./validate.py && ./validate.py --self-test` before committing any
  doctrine change.
- `bundled-skills/` — user-authored skills the Flow depends on that no
  external installer provides (clean-code); /flow:sync installs them into
  ~/.claude/skills/. Everything else comes from /setup-matt-pocock-skills.
- `rules-optional/` — context-specific rules, NOT installed by default and
  deliberately not active on the authoring machine; copy individually where
  they apply (e.g. work machines):
  - `spring-dependencies.md` — Spring projects: standard libs over hand-rolling
  - `git-procedure.md` — never push; short commits, no co-author; one logical
    change per commit

## Install (plugin — preferred)

The repo is a plugin marketplace carrying one plugin, `flow`. In Claude Code:

```
/plugin marketplace add trungth1406/claude-config
/plugin install flow@claude-config
```

Then run `/flow:sync` once — it installs CLAUDE.md, rules/, and the bundled
skills (clean-code) into ~/.claude. For everything else the Flow routes to,
`/setup-matt-pocock-skills` is the baseline installer.
The sync step is load-bearing, not optional: plugin hooks reach only the
main conversation, while subagents inherit doctrine solely from the
CLAUDE.md files the sync writes. The flow-reminder hook itself ships with
the plugin (no settings.json wiring); if a legacy manual hook is still
present, remove it or every prompt gets the reminder twice.

## Updating

`/flow:sync` installs the updater at `~/.claude/flow-update.sh`. To update
any machine:

```sh
bash ~/.claude/flow-update.sh
```

It refreshes the marketplace, updates the plugin, and syncs the payload
into ~/.claude — no credentials involved. Restart Claude Code afterwards
to apply hook changes.

Bootstrap on a machine that predates the script (one time):

```sh
bash <(curl -s https://raw.githubusercontent.com/trungth1406/claude-config/main/scripts/update.sh)
```

## Install (manual — fallback)

```sh
cp CLAUDE.md flow-reminder.md ~/.claude/
mkdir -p ~/.claude/rules && cp rules/*.md ~/.claude/rules/

# per-context extras (work machines etc.), pick individually:
# cp rules-optional/git-procedure.md ~/.claude/rules/
# cp rules-optional/spring-dependencies.md ~/.claude/rules/
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

## Install graphify

The graphify rule assumes the CLI, its skill, and the MCP server exist:

```sh
uv tool install graphifyy           # package name has the double y;
                                    # installs graphify + graphify-mcp on PATH
graphify install --platform claude  # copies the skill into ~/.claude/skills/
```

Per project, register the MCP server in the repo's `.mcp.json`:

```json
{
  "mcpServers": {
    "graphify": {
      "command": "graphify-mcp",
      "args": ["graphify-out/graph.json"],
      "description": "Code knowledge graph — 10 query tools, token-budgeted"
    }
  }
}
```

Then build the graph once with `/graphify` (or `graphify update .`); the git
hooks it installs keep the graph fresh on commit.

## Sync

Under the plugin model the repo is the source of truth and `/flow:sync`
pushes it onto the live files. If a live file was edited first (rare), pull
it into the repo, commit, and let sync converge — `validate.py` guards the
graph in either direction.

```sh
# pull latest live state into the repo
cp ~/.claude/CLAUDE.md ~/.claude/flow-reminder.md . && cp ~/.claude/rules/*.md rules/

# push repo state onto a machine
cp CLAUDE.md flow-reminder.md ~/.claude/ && cp rules/*.md ~/.claude/rules/
```

Referenced skills (clean-code, to-tickets, implement, code-review, qa, ...)
are installed separately; this repo carries only the doctrine that routes to
them.
