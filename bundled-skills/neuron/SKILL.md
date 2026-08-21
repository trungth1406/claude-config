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
- Plan to ~5 only where knowledge is settled; stop early at a genuine open
  question — a question node terminates lookahead, discussion grows past it.

## Update — actively, throughout work

Agents must write to the graph during work, not just at establishment:
- Decision made → `add_node` (kind: decision) + `link` to what raised it.
- File created or API shaped → `set_stage` on the task node.
- Confirmed → `reinforce` (or repeat the same link).
- Corrected → add the replacement, `supersede` the old. Never delete.
- Lesson learned → `add_node` (kind: knowledge) + `link`.
- Not now, not wrong → `park`; `unpark` wakes it.

A thin graph means an agent silently worked. That is a failure.

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
