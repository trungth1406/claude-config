#!/usr/bin/env python3
"""PreToolUse guard: block git commits carrying AI attribution watermarks."""
import json
import re
import sys

PATTERNS = (
    r"Co-authored-by:[^\n]*(?:[Cc]laude|[Aa]nthropic)",
    r"Claude-Session",
    r"Generated with[^\n]*[Cc]laude",
    r"claude\.ai",
    r"\U0001F916",
)


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
    sys.exit(0)


if __name__ == "__main__":
    main()
