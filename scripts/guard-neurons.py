#!/usr/bin/env python3
"""PreToolUse guard: blocks git commit if no neurons graph was touched.

Checks the neurons db modified time against the session start. If the db
hasn't been written to this session, the commit is blocked with guidance.
Only fires on git commit commands (same pattern as guard-commit.py).
"""
import json
import os
import sys
import time
from pathlib import Path


def main():
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    if tool != "Bash":
        return

    cmd = data.get("tool_input", {}).get("command", "")
    if "git commit" not in cmd:
        return

    if "FLOW_SKIP_NEURON_CHECK=1" in cmd:
        return

    home = Path.home()
    cwd = os.environ.get("PWD", os.getcwd())
    project = Path(cwd).name if cwd else "default"
    candidates = [
        home / ".claude" / "neurons" / project / "neurons.db",
        home / ".claude" / "neurons" / "neurons.db",
    ]

    db = None
    for c in candidates:
        if c.exists():
            db = c
            break

    if db is None:
        print("BLOCKED: no neurons graph exists for this project.", file=sys.stderr)
        print("The neuron skill is mandatory: establish a thinking graph", file=sys.stderr)
        print("before committing. Use /neuron or the neurons MCP tools.", file=sys.stderr)
        print("Override: prefix FLOW_SKIP_NEURON_CHECK=1.", file=sys.stderr)
        sys.exit(2)

    db_mtime = db.stat().st_mtime
    age = time.time() - db_mtime
    if age > 7200:
        print("BLOCKED: neurons db hasn't been touched this session.", file=sys.stderr)
        print(f"Last write: {int(age // 60)} minutes ago ({db})", file=sys.stderr)
        print("Write to your thinking graph before committing.", file=sys.stderr)
        print("Override: prefix FLOW_SKIP_NEURON_CHECK=1.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
