#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
HOOK_PATH="$WORKSPACE_ROOT/.git/hooks/pre-push"
MODELTRIPWIRE_DIR="$WORKSPACE_ROOT/modeltripwire"
VERIFY_SCRIPT="$MODELTRIPWIRE_DIR/scripts/verify_repo_boundary.py"

mkdir -p "$(dirname "$HOOK_PATH")"

cat > "$HOOK_PATH" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

read -r local_ref local_sha remote_ref remote_sha || true

repo_root="$(git rev-parse --show-toplevel)"
modeltripwire_dir="$repo_root/modeltripwire"
verify_script="$modeltripwire_dir/scripts/verify_repo_boundary.py"

if [[ "$PWD" == "$modeltripwire_dir" ]] || [[ "$PWD" == "$modeltripwire_dir"/* ]]; then
  python3 "$verify_script"
fi
HOOK

chmod +x "$HOOK_PATH"

echo "Installed pre-push guardrail at $HOOK_PATH"
echo "It will run the ModelTripwire boundary check whenever a push is initiated from the modeltripwire directory."
