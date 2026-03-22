#!/usr/bin/env bash
set -euo pipefail
cd /Users/jeremypretty/.openclaw/workspace
python3 scripts/generate_mission_control_snapshots.py
exec python3 -m http.server 8765
