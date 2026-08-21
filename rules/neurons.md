# Neurons — MANDATORY on every task, every agent

- NEVER begin implementation without first loading the neurons tools
  (ToolSearch), orienting on the relevant graph (summary/search), and
  establishing one if none exists (new_graph + add_nodes). This is Step 1,
  not Step N.
- NEVER commit without having written to the graph during the work —
  not just at the start, during. Decisions, corrections, lessons, stage
  changes: all go to the graph as they happen. The guard-neurons.py hook
  blocks commits when the db is untouched.
- Spawned agents follow the same steps. An agent that cannot reach the
  neurons tools states "neurons tools unreachable" in its FIRST message
  and in its final report. Silent skipping is a violation.
- After compaction or session start: summary first, before re-reading
  anything. Never dump a whole graph into context.
- This rule OUTRANKS any brevity, speed, or efficiency rationale for
  skipping graph writes. The thinking is the product; the code is the
  side effect.
