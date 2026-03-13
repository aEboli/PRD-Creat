#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-${CODEX_HOME:-$HOME/.codex}/skills}"
FORCE_FLAG="${2:-}"
REPO_URL="${REPO_URL:-https://github.com/aEboli/PRD-Creat.git}"
BRANCH="${BRANCH:-main}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required to install prd-creater." >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
DEST_DIR="${TARGET_DIR%/}/prd-creater"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TMP_DIR"
mkdir -p "$TARGET_DIR"

if [ -e "$DEST_DIR" ]; then
  if [ "$FORCE_FLAG" != "--force" ]; then
    echo "Target already exists: $DEST_DIR" >&2
    echo "Re-run with '--force' as the second argument to overwrite it." >&2
    exit 1
  fi
  rm -rf "$DEST_DIR"
fi

cp -R "$TMP_DIR/skills/prd-creater" "$DEST_DIR"

echo
echo "[OK] Installed prd-creater to $DEST_DIR"
echo "[TIP] Example prompt: Use \$prd-creater to turn this feature brief into a PRD."
