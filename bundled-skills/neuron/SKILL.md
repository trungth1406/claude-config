---
name: neuron
description: Persist the shape of thinking as small graphs via the neurons MCP tools. Use when a discussion, task, or idea cluster has structure worth keeping across compaction - form a graph, capture and link thoughts, reinforce what discussion confirms, supersede what it corrects, re-orient with summary after any context loss.
---

# Neuron — thinking that survives compaction

The neurons MCP server holds many small thinking-graphs in machine-local
storage. The graph is not notes; it is the SHAPE of the thinking — what
was decided, what was corrected, what connects to what. Context windows
die; the graph does not.

## When to form a graph

Create one graph per idea cluster the moment it shows structure worth
keeping — a design discussion, a debugging arc, a research question:

    new_graph {graph: "outbox-design", title: "Outbox delta consolidation"}

Do NOT form graphs for one-shot questions or mechanical edits. A graph
that will never be re-read is noise. Optional project tag groups graphs.

## Capture as you think

Add a node when a thought lands, link it immediately to what raised it:

    add_node {graph, id: "per-kind-keying", kind: "decision",
              title: "Outbox keys by component kind, last-wins"}
    link {graph, from: "why-reinsert-everything", to: "per-kind-keying",
          label: "answered-by"}

- id: short kebab, byte-exact identity, unique per graph
- kind is free vocabulary: idea, question, decision, knowledge, risk,
  correction — whatever the thought is
- content: only when the title cannot carry the meaning alone
- stage / skills: set when the node sits in the Flow (see below)

## Reinforce, never restate

When discussion re-confirms an existing thought, do not add a duplicate:

    reinforce {graph, id: "per-kind-keying"}

Repeating a link with the same from/to/label bumps its weight the same
way. Weight and reinforced counts ARE the graph's memory of conviction.

## Correct by supersession

Wrong beliefs are never deleted — they are outweighed:

    add_node {graph, id: "graph-first", kind: "correction",
              title: "In-memory graph is the truth; SQL is consolidation"}
    supersede {graph, old: "sql-centric-core", by: "graph-first"}

The superseded node stays visible with a forwarding address. The history
of being wrong is part of the thinking.

Set aside without judging: park {graph, id} — not now, not wrong.
Wake it later with unpark.

## Re-orient after compaction

First call after any context loss, before re-reading anything:

    summary {graph}

Frontier = freshest active thoughts (where you were). Top = most
reinforced (what matters). Counts tell the graph's health. Then walk
only what you need:

    show {graph, node, depth: 1}     — neighborhood, budget-capped
    path {graph, from, to}           — how two thoughts connect
    search {query}                   — "where did we think about X", all graphs

NEVER dump a whole graph into context. The budgets exist so re-reading
thinking costs a paragraph, not a session.

## Keep graphs neuron-sized

Near ~30 nodes, split: create a sibling graph and add a bridge node in
each naming the other (kind: "bridge", title naming the sibling graph
id). Search spans all graphs, so bridges are findable from both sides.

## Bind to the Flow

A node's stage names its Flow position (grilled, specced, ticketed,
implemented, reviewed); skills lists what fires next (to-tickets,
implement, code-review). Working a node = read its stage, invoke its
skill. The doctrine graph routes the work; the neuron graph remembers it.

## Settle

When the thinking concludes: settle {graph}. It leaves the active list
but stays searchable forever; reopen wakes it. Before risky operations,
consolidate {} forces everything dirty into long-term storage — though
the owner already consolidates on thresholds, quiet, and shutdown.
