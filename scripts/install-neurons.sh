#!/usr/bin/env bash
# Install or update the neurons MCP binary from its GitHub release and
# register it with Claude Code. Idempotent; safe to run on every sync.
set -euo pipefail

REPO="trungth1406/neurons"
BIN_DIR="${NEURON_BIN_DIR:-$HOME/.cargo/bin}"
BIN="$BIN_DIR/neuron-mcp"

if ! command -v gh >/dev/null 2>&1; then
  echo "neurons: gh CLI not found - skipped (install gh and re-run /flow:sync)"
  exit 0
fi

latest=$(gh release view --repo "$REPO" --json tagName -q .tagName 2>/dev/null) || {
  echo "neurons: cannot read releases of $REPO (gh auth?) - skipped"
  exit 0
}
current="v$("$BIN" --version 2>/dev/null | awk '{print $2}')" || current="none"

if [ "$current" = "$latest" ]; then
  echo "neurons: binary already current ($latest)"
else
  case "$(uname -s)-$(uname -m)" in
    Darwin-arm64)  target="aarch64-apple-darwin" ;;
    Linux-x86_64)  target="x86_64-unknown-linux-gnu" ;;
    *) echo "neurons: no prebuilt binary for $(uname -s)-$(uname -m) - use cargo install --git https://github.com/$REPO"; exit 0 ;;
  esac
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  gh release download "$latest" --repo "$REPO" -p "*$target*" -D "$tmp"
  tar -xzf "$tmp"/neuron-mcp-*.tar.gz -C "$tmp"
  mkdir -p "$BIN_DIR"
  mv -f "$tmp/neuron-mcp" "$BIN"
  chmod +x "$BIN"
  echo "neurons: installed $("$BIN" --version) ($current -> $latest)"
fi

if command -v claude >/dev/null 2>&1; then
  if claude mcp list 2>/dev/null | grep -q "^neurons:"; then
    echo "neurons: MCP already registered"
  else
    claude mcp add neurons -- "$BIN" >/dev/null && echo "neurons: MCP registered (restart sessions to load)"
  fi
else
  echo "neurons: claude CLI not on PATH - register manually: claude mcp add neurons -- $BIN"
fi
