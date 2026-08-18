# Hard guards — quality rationale

- NEVER commit or push with a failing suite. Tests decide whether an
  implementation succeeded — a red suite is a stop, not a warning.
- Thresholds, coverage floors, and taste rules: the clean-code skill is the
  only authority. If any file disagrees with it, clean-code wins.
- Test representations before data. What fossilizes is not data entries
  (cheap to fix late) but representations and public shapes — identifiers,
  encodings, interface types downstream code bakes in. Adversarial,
  tested-before-implementation scrutiny goes to what structures mean first,
  data contents second.

Operational gates live beside this file: ticket-gate, review-qa-gate,
test-gate. Routing lives in the Flow graph in ~/.claude/CLAUDE.md.
