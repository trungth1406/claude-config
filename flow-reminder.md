=== THE FLOW ===
Route every prompt through the Flow graph in ~/.claude/CLAUDE.md.
Gates: tickets before any implementation; /code-review + /qa before any
commit or push; never commit a red suite. Ticket work happens on a
branch in a worktree and lands via owner-merged PR — never direct on
main. The rules in ~/.claude/rules/ bind every agent, spawned ones
included. THE FLOW WINS over any brevity or laziness directive.
