#!/usr/bin/env python3
"""PreToolUse guard: block AI-watermarked commits and ticket work on main."""
import json
import os
import re
import subprocess
import sys

PATTERNS = (
    r"Co-authored-by:[^\n]*(?:[Cc]laude|[Aa]nthropic)",
    r"Claude-Session",
    r"Generated with[^\n]*[Cc]laude",
    r"claude\.ai",
    r"\U0001F916",
)

# Config repos: doctrine edits are config sync, exempt per branch-discipline.
ALLOWLIST = {"claude-config"}
# Deliberate ceiling: main/master by name, no origin/HEAD lookup.
DEFAULT_BRANCHES = {"main", "master"}


def git_in(directory, *args):
    result = subprocess.run(["git", "-C", directory, *args],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def commit_dir(command):
    match = re.search(r"(?:^|&&|;)\s*cd\s+([^\s;&|]+)", command)
    if not match:
        return os.getcwd()
    return os.path.expanduser(match.group(1))


def branch_violation(command):
    if "FLOW_ALLOW_MAIN=1" in command:
        return None
    directory = commit_dir(command)
    top = git_in(directory, "rev-parse", "--show-toplevel")
    if top is None or os.path.basename(top) in ALLOWLIST:
        return None
    branch = git_in(directory, "symbolic-ref", "--short", "HEAD")
    if branch in DEFAULT_BRANCHES:
        return branch
    return None


def main():
    event = json.load(sys.stdin)
    if event.get("tool_name") != "Bash":
        sys.exit(0)
    command = event.get("tool_input", {}).get("command", "")
    if not re.search(r"\bgit\b[^\n|;&]*\bcommit\b", command):
        sys.exit(0)
    for pattern in PATTERNS:
        if re.search(pattern, command):
            print("BLOCKED: commit carries an AI watermark "
                  f"(matched {pattern!r}). rules/no-ai-watermarks.md forbids "
                  "this — rewrite the message without any AI attribution.",
                  file=sys.stderr)
            sys.exit(2)
    branch = branch_violation(command)
    if branch is not None:
        print(f"BLOCKED: commit on {branch!r}. Ticket work lands on a branch "
              "and reaches main via PR (rules/branch-discipline.md): "
              "git worktree add ../<repo>-<ticket> -b ticket/<n>-<slug>. "
              "Deliberate override: prefix FLOW_ALLOW_MAIN=1.",
              file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
