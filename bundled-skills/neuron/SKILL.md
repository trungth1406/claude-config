---
name: neuron
description: The thinking graph. Use on every task, every agent, every session. Load the neurons MCP tools first (ToolSearch), orient on the relevant graph (summary/search), establish if none exists (new_graph + add_nodes), write every decision/correction/lesson during work (add_node, link, set_stage, supersede, reinforce), close with set_stage on the root. A session without graph writes is incomplete. After compaction or session start, summary first.
---

# neuron

## Load

```
ToolSearch "select:mcp__neurons__summary,mcp__neurons__add_node,
mcp__neurons__add_nodes,mcp__neurons__new_graph,mcp__neurons__link,
mcp__neurons__set_stage,mcp__neurons__supersede,mcp__neurons__reinforce,
mcp__neurons__search,mcp__neurons__settle,mcp__neurons__park,
mcp__neurons__unpark,mcp__neurons__consolidate,mcp__neurons__export"
```

If unavailable: state "neurons tools unreachable" in the first message.

## Orient

`summary` on the graph named in the prompt, or `search` to find it.
No graph exists → `new_graph`.

## Establish

Root node = the task. Neighbors: what, how, where, applies.
~5 levels ahead per node where knowledge is settled; stop at open
questions. One `add_nodes` call.

## During work

| event | action |
|---|---|
| decision made | `add_node` (decision) + `link` |
| file or API shaped | `set_stage` on task node |
| belief corrected | `add_node` replacement + `supersede` old |
| lesson learned | `add_node` (knowledge) + `link` |
| confirmed again | `reinforce` |
| not now, not wrong | `park` |

## Close

`set_stage` root → final state. `settle` if concluded.

## After compaction

`summary` first. Then `show`, `path`, `search`. Never dump a whole graph.

## Topology

Task on existing ideas → new graph, bridge nodes both ways.
Graphs link graphs.
