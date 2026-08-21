---
name: neuron
description: Persist thinking as graphs via the neurons MCP tools. Mandatory on every task; during discussion, the moment something becomes clear, write it to the graph. Re-orient with summary after any compaction or session start.
---

# neuron

Thinking survives compaction as graphs. Notes die with context; shape does not.

## Establish — any new task or idea

- `new_graph` per idea cluster. Root node = the ask.
- Nearest neighbors answer: what is it, how, where, what applies.
- Every node pre-plans ~5 levels ahead from itself — a rolling lookahead,
  per node, never flat tiers from root. Total depth unbounded.

## Update — the moment something is clear

- Confirmed → `reinforce` (or repeat the same link).
- Corrected → add the replacement, `supersede` the old. Never delete.
- New thought → `add_node` + `link` to what raised it.
- Not now, not wrong → `park`; `unpark` wakes it.

## Bind agents to the Flow

- A node's `stage` = its Flow position; `skills` = what fires next. An agent
  bound to a node reads both against the CLAUDE.md Flow graph and invokes
  that skill.
- A task built on existing idea nodes gets a NEW graph, bridged back (bridge
  nodes both ways), and runs the same Flow loop. Retrace = follow bridges.
- Topology is unlimited: graphs link graphs. Split near ~30 nodes.

## Re-orient — after compaction or session start

- `summary` first, always. Then `show` (depth 1), `path`, `search`.
- Never dump a whole graph into context.

## Finish

- `settle` when concluded; `reopen` wakes it.
- `consolidate` before risky operations; the owner also consolidates on
  thresholds, quiet, and shutdown.
