# Docs — obsidian-vault

All docs go through the `obsidian-vault` skill. Two tiers:

- **In-repo, versioned with the code**: `CONTEXT.md` (domain glossary) and
  `docs/adr/` — agent inputs the engineering skills read on every run.
- **In the vault**: prose — research, explainers, design writeups, reports —
  at `~/obsidian/Vaults/<project>/`, never inside the repo. An in-repo vault
  folder is a stale stub. Confirm the exact vault per project.

A skill's own report artifact keeps its format but lands in the project vault.

Exception: the claude-config doctrine repo keeps research/ in-repo — the
doctrine's evidence is versioned with the doctrine it justified.
