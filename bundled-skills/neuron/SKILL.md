---
name: neuron
description: The thinking graph. MANDATORY on every task — no exceptions, no deferral. Fires BEFORE any implementation begins and DURING work, not after. A session without graph writes is a failed session.
---

# neuron — MANDATORY, not optional

Every task, every agent, every session. No exceptions.

## Step 1 — load the tools (FIRST action, before anything else)

ToolSearch "select:mcp__neurons__summary,mcp__neurons__add_node,
mcp__neurons__add_nodes,mcp__neurons__new_graph,mcp__neurons__link,
mcp__neurons__set_stage,mcp__neurons__supersede,mcp__neurons__reinforce,
mcp__neurons__search,mcp__neurons__settle,mcp__neurons__park,
mcp__neurons__unpark,mcp__neurons__consolidate,mcp__neurons__export"

If ToolSearch returns nothing: state "neurons tools unreachable" in your
very first message. Do not silently continue.

## Step 2 — orient (BEFORE reading code or files)

- `summary` on the graph named in your prompt, or `search` to find it.
- If no graph exists for this work: `new_graph` immediately.

## Step 3 — establish (BEFORE implementation starts)

- Root node = the task. Nearest neighbors: what, how, where, what applies.
- Pre-plan ~5 levels ahead per node where knowledge is settled.
- Stop at open questions — a question node terminates lookahead.
- Use `add_nodes` for the establishment burst (one call).

## Step 4 — write DURING work, not after

Every decision made → `add_node` (decision) + `link`.
Every file created or API shaped → `set_stage` on the task node.
Every correction → `supersede` the old belief. Never delete.
Every lesson learned → `add_node` (knowledge) + `link`.
Every confirmation → `reinforce`.
Park what is not-now-not-wrong → `park`.

These are not suggestions. A thin graph means the agent silently
worked. That is a failure — the thinking is lost on compaction.

## Step 5 — close

- `set_stage` on root task node to the final state (pr-open, shipped).
- `settle` if the thinking concluded.

## Re-orient after compaction or session start

`summary` first, always. Then `show`, `path`, `search` as needed.
NEVER dump a whole graph into context.

## Topology

- One graph per idea cluster. Split near ~30 nodes.
- Task on existing ideas → NEW graph, bridged back (bridge nodes both
  ways). Retrace = follow bridges.
- Graphs link graphs. No cap on topology.
