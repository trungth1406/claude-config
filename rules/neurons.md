# Neurons — the thinking graph binds every agent

- Every task gets a thinking graph (neurons MCP, /neuron skill). During
  discussion, the moment something becomes clear, write it to the graph.
- Spawned agents too: before building, re-orient on the relevant graph
  (summary, search); while working, write clarity back (add_node, link,
  set_stage). An agent that cannot reach the neurons tools says so in its
  report instead of silently skipping.
- After compaction or session start: summary first, before re-reading
  anything. Never dump a whole graph into context.

HOW (subagents must follow these steps):
1. Load tools: ToolSearch "select:mcp__neurons__summary,mcp__neurons__add_node,
   mcp__neurons__add_nodes,mcp__neurons__link,mcp__neurons__set_stage,
   mcp__neurons__supersede,mcp__neurons__reinforce,mcp__neurons__search"
2. Orient: call summary on the graph named in your prompt (or search to
   find it). If no graph exists for this work, create one with new_graph.
3. During work: every decision -> add_node + link; every stage change ->
   set_stage; every correction -> supersede. A thin graph = failure.
4. Before finishing: set_stage on your root task node to pr-open or done.
5. If ToolSearch returns nothing (tools unavailable): state "neurons tools
   unreachable" in your final report. Do not silently skip.
