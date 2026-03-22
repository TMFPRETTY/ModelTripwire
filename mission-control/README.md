# Mission Control Local Preview

## Refresh snapshots manually
```bash
cd /Users/jeremypretty/.openclaw/workspace
python3 scripts/generate_mission_control_snapshots.py
```

## Serve locally
```bash
cd /Users/jeremypretty/.openclaw/workspace
bash scripts/serve_mission_control.sh
```

Then open:
- <http://127.0.0.1:8765/mission-control/>
- <http://127.0.0.1:8765/mission-control/rooms.html>
- <http://127.0.0.1:8765/mission-control/jobs.html>

## Current structure
- `index.html` → overview
- `rooms.html` → room list
- `room.html?id=<room-slug>` → room detail
- `jobs.html` → jobs list
- `data/*.json` → generated snapshots
