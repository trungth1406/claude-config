# Docs — obsidian-vault

All docs go through the `obsidian-vault` skill. Two tiers:

- **In-repo path, LOCAL-ONLY**: `CONTEXT.md`, `docs/adr/`, `docs/agents/` —
  agent inputs the engineering skills read on every run. They live at their
  conventional paths but are gitignored: docs are NEVER committed or pushed
  to a remote. Tickets and specs go to the tracker; docs stay on the machine.
- **In the vault**: prose — research, explainers, design writeups, reports —
  at `~/obsidian/Vaults/<project>/`, never inside the repo. An in-repo vault
  folder is a stale stub. Confirm the exact vault per project.

A skill's own report artifact keeps its format but lands in the project vault.
