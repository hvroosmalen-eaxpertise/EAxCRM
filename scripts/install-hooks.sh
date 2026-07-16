#!/usr/bin/env sh
# Installs the ea-code-validator pre-commit hook into .git/hooks/pre-commit.
#
# Idempotent: if the hook already exists and was written by this installer
# (recognised by a marker line), it is overwritten.  If it exists but was
# written by someone/something else, the installer refuses and prints the
# intended contents so the user can merge manually.

set -eu

repo_root=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$repo_root" ]; then
    echo "Not inside a git repository." >&2
    exit 1
fi

hook_path="$repo_root/.git/hooks/pre-commit"
marker='# ea-code-validator hook -- managed by scripts/install-hooks'
body="#!/usr/bin/env sh
$marker
python .opencode/skills/ea-code-validator/cli.py --changed
"

if [ -f "$hook_path" ]; then
    if ! grep -qF "$marker" "$hook_path"; then
        echo "Refusing to overwrite existing $hook_path (not managed by this installer)."
        echo ""
        echo "Intended contents:"
        printf '%s' "$body"
        exit 1
    fi
fi

printf '%s' "$body" > "$hook_path"
chmod +x "$hook_path"
echo "Installed pre-commit hook at $hook_path"
