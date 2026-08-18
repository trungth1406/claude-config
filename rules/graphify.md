# Second brain — graphify + wikilinks

`graphify` extracts the code graph (`--code-only`, tree-sitter AST, free). The
graph exports into the Obsidian vault as browsable notes. Prose notes bridge to
code notes via `[[wikilinks]]` — Obsidian resolves them natively.

- **Querying**: prefer the `graphify` MCP server (10 tools, `token_budget`).
  CLI: `graphify query`, `graphify affected`, `graphify path`.
- **Writing**: when a vault note mentions a code symbol that has a generated
  note, write `[[SymbolName]]`. Methods: `[[dot-MethodName()]]`. The vault's
  `CONVENTIONS.md` has the naming table.
- **Freshness**: git hooks refresh the code graph on commit. The vault export
  is manual (`infra/second-brain.py`).
- **Developing neuron**: a vault note in `notes/` with `status:` frontmatter.
  Promoted by moving to `research/` or `adr/` and flipping the status.
- **Backend**: `claude-cli` only (community labeling). No API keys, ever.

Per-project details: `docs/agents/second-brain.md`.
