#!/usr/bin/env bash
# flow-update: one-shot plugin update with a transient GitHub token.
# Usage: GH_TOKEN=github_pat_xxx bash flow-update.sh   (or run bare and
# paste the token at the hidden prompt). The token lives only in this
# process's environment - nothing is stored, nothing to log out.
set -euo pipefail

if [ -z "${GH_TOKEN:-}" ]; then
  read -rsp "GitHub token (input hidden): " GH_TOKEN
  echo
  export GH_TOKEN
fi

command -v gh >/dev/null || { echo "gh CLI is required" >&2; exit 1; }
command -v claude >/dev/null || { echo "claude CLI is required" >&2; exit 1; }

gh auth setup-git >/dev/null 2>&1 || true

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

unset GH_TOKEN
echo "Done. Restart Claude Code to apply updated hooks."
