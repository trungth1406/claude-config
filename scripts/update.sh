#!/usr/bin/env bash
# flow-update: one-shot plugin update. Public repo - no credentials needed.
set -euo pipefail

command -v claude >/dev/null || { echo "claude CLI is required" >&2; exit 1; }

claude plugin marketplace update claude-config
claude plugin update flow@claude-config

CACHE=$(ls -td "$HOME"/.claude/plugins/cache/claude-config/flow/*/ 2>/dev/null | head -1)
[ -n "$CACHE" ] || { echo "plugin cache not found - is flow installed?" >&2; exit 1; }
echo "Syncing payload from ${CACHE}"

cp "${CACHE}CLAUDE.md" "$HOME/.claude/CLAUDE.md"
mkdir -p "$HOME/.claude/rules"
cp "${CACHE}rules/"*.md "$HOME/.claude/rules/"
if [ -d "${CACHE}bundled-skills" ]; then
  mkdir -p "$HOME/.claude/skills"
  cp -R "${CACHE}bundled-skills/." "$HOME/.claude/skills/"
fi
cp "${CACHE}scripts/update.sh" "$HOME/.claude/flow-update.sh"

# Payload ships from a validated commit; this run is a local sanity echo.
python3 "${CACHE}validate.py" || \
  echo "validator reported issues above - missing skills? run /setup-matt-pocock-skills"

echo "Done. Restart Claude Code to apply updated hooks."
