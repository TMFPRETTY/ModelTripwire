# MISSION_CONTROL_IMPLEMENTATION_PLAN.md

## Purpose
This document defines the practical implementation path for a first visible Mission Control dashboard prototype.

## V1 Technical Approach
Build Mission Control V1 as a lightweight static dashboard powered by generated JSON snapshots.

## Why This Approach
- fast to ship
- low operational complexity
- easy to open locally on the laptop or Mac mini
- keeps source-of-truth logic in snapshot generation instead of the frontend
- can later be upgraded into a richer app without throwing away the data contract

## Stack
### Frontend
- static HTML
- vanilla CSS
- vanilla JavaScript

### Data generation
- Python snapshot generator script
- reads workspace docs and runtime command outputs

### Snapshot output location
- `mission-control/data/`

### UI location
- `mission-control/`

## Initial Files
- `mission-control/index.html`
- `mission-control/styles.css`
- `mission-control/app.js`
- `mission-control/data/*.json`
- `scripts/generate_mission_control_snapshots.py`

## Data Sources For Prototype
- `AGENT_REGISTRY.md`
- fixed room definitions from current architecture docs
- `cron list` JSON
- `openclaw status` text
- optional `.openclaw/signalandcircuit-mail-monitor-state.json`

## First Prototype Scope
The first prototype should render:
- global health strip
- needs attention
- room status grid
- recent activity
- jobs health
- alerts / blockers
- agents view summary

## Not Required For Prototype
- live bidirectional controls
- editing jobs from the UI
- perfect approvals pipeline
- real auth/login
- charting

## Regeneration Model
Snapshots can be regenerated:
- manually via script
- later by cron or button

## Suggested Command
```bash
python3 scripts/generate_mission_control_snapshots.py
```

## How To View
Serve the workspace or the `mission-control` directory with a local static file server.

Simple option:
```bash
python3 -m http.server 8000
```
Then open:
- `http://localhost:8000/mission-control/`

## Future Upgrade Path
Later, Mission Control can become:
- a React/Next app
- a local app served by OpenClaw
- a richer dashboard with drilldowns and controls

But the snapshot contract should remain useful either way.
