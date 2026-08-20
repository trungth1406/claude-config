# Branch discipline — ticket work never lands on main directly

- Any implementation work driven by a ticket (/implement) starts on a NEW
  branch in a NEW git worktree: `git worktree add ../<repo>-<ticket> -b
  ticket/<n>-<slug>`. Never implement on main/master.
- Landing is a PR the owner merges: push the branch, open the PR with the
  code-review + qa evidence in the description, and STOP — merging is the
  owner's act, on GitHub, always.
- Exempt: doctrine/config repos (claude-config) — rule edits and payload
  sync are config work, not implementation, and stay direct-to-main.
- Mechanical enforcement: the flow plugin's guard blocks `git commit` while
  on main/master unless the repo is allowlisted or the command carries
  FLOW_ALLOW_MAIN=1 (deliberate, visible override).
- The review/qa gates are unchanged — they run before the PR opens; the PR
  is the landing protocol, not a replacement for the gates.
