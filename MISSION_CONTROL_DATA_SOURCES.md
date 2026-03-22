# MISSION_CONTROL_DATA_SOURCES.md

## Purpose
This document defines the data sources for each Mission Control V1 page/widget so the dashboard can be implemented from real room/agent/job/system state.

## Goal
Every V1 widget should have a clear source of truth.

Mission Control should prefer:
- real commands
- real state files
- real docs/registries
- generated JSON snapshots if needed

Mission Control should avoid:
- hand-maintained duplicate status text
- disconnected dashboard-only facts
- widgets that cannot be sourced reliably

## Data Source Types

### 1. Static / semi-static docs
Use for definitions, labels, room purposes, and registry data.

### 2. Dynamic command outputs
Use for runtime health, job state, and live system status.

### 3. Generated local snapshots
Use when the UI needs a stable JSON shape and the source is otherwise scattered.

## Canonical Static Sources

### `AGENT_REGISTRY.md`
Use for:
- agent names
- room mapping
- agent status class (`active`, `embedded`, `transitional`, `planned`, `retired`)
- mission text
- current jobs list
- skill associations
- approval boundary summaries

### `CHANNEL_ARCHITECTURE_PLAN.md`
Use for:
- room purpose text
- room ownership boundaries
- what belongs in each room
- permanent vs transitional room semantics

### `CHANNEL_MIGRATION_MAP.md`
Use for:
- room/channel IDs
- current vs future routing
- destination mapping for jobs

### `JOB_CATALOG.md`
Use for:
- planned/known job inventory
- long-form job purpose text
- migration/retirement decisions

### `MISSION_CONTROL_PLAN.md`
Use for:
- V1 scope and product intent

### `MISSION_CONTROL_WIREFRAMES.md`
Use for:
- UI layout mapping

## Canonical Dynamic Sources

### `openclaw status`
Use for:
- gateway status
- host/runtime health summary
- overall job/system counts when exposed
- system-level state for the System page

### Cron API / cron job data
Use for:
- job enabled/disabled state
- last run
- next run
- failure status
- run summaries
- delivery status

Relevant operations:
- `cron list`
- `cron runs <job>`
- `cron status` if useful

### Gateway/service status
Use for:
- whether the gateway/runtime is healthy
- whether Discord integrations appear reachable

### Local state files
Use for:
- specialized workflow state
- queue-like or watcher-specific information

Known examples:
- `.openclaw/signalandcircuit-mail-monitor-state.json`
- future workflow-specific JSON snapshots if created

## Recommended V1 Snapshot Layer
Mission Control V1 will likely be easiest to build if the UI reads from generated JSON snapshots instead of parsing markdown and shell commands on every page load.

### Suggested snapshots
Create these later as needed:
- `mission-control/rooms.json`
- `mission-control/agents.json`
- `mission-control/jobs.json`
- `mission-control/approvals.json`
- `mission-control/alerts.json`
- `mission-control/activity.json`
- `mission-control/system.json`

These should be derived from the canonical sources above, not manually edited.

## Widget-to-Source Mapping

### Overview → Global Health Strip
Fields needed:
- total active rooms
- total active agents
- pending approvals count
- open alerts count
- job failures count
- overall system health

Sources:
- rooms/agents: `AGENT_REGISTRY.md` + `CHANNEL_ARCHITECTURE_PLAN.md`
- approvals/alerts: generated snapshot or room-derived status later
- job failures: cron runs/list
- overall system health: `openclaw status`

### Overview → Needs Attention
Fields needed:
- top 2 to 5 high-priority items

Sources:
- initially: manually synthesized/generated summary from recent alerts + failing jobs + approvals
- later: `alerts.json` + `approvals.json` + selected room highlights

### Overview → Room Status Grid
Fields needed per room:
- room name
- status
- headline
- last update time
- optional badges (approvals/blockers/queue)

Sources:
- room definitions: `CHANNEL_ARCHITECTURE_PLAN.md`
- room/agent mapping: `AGENT_REGISTRY.md`
- headline/last update: generated room snapshot from recent room outputs
- status: synthesized from job health + alerts + recent room activity

### Overview → Recent Activity Feed
Fields needed:
- room
- title
- one-line summary
- timestamp
- priority

Sources:
- generated `activity.json`
- likely assembled from recent job outputs, room summaries, alerts, approvals

### Overview → Jobs Health Panel
Fields needed:
- job name
- room
- status
- last run
- next run
- recent failure count

Sources:
- cron list
- cron runs
- job/room mapping from `AGENT_REGISTRY.md` and `CHANNEL_MIGRATION_MAP.md`

### Overview → Approvals Waiting
Fields needed:
- title
- source room
- risk
- age
- decision type

Sources:
- V1 may require a small generated approvals snapshot, because approvals are not yet fully represented in a single canonical machine-readable store
- until then, this may be seeded from selected room updates or explicit approval-tracking data

### Overview → Alerts / Blockers
Fields needed:
- title
- source
- severity
- summary
- age

Sources:
- generated alerts snapshot
- job failures from cron
- system/runtime issues from `openclaw status`
- room-derived blocker summaries later

### Overview → Recommended Focus Today
Fields needed:
- 1 to 3 recommended actions

Sources:
- synthesized from needs-attention items
- should be generated from current room/job/alert/approval state, not manually authored

## Page-Level Source Mapping

### Rooms Page
Primary sources:
- `CHANNEL_ARCHITECTURE_PLAN.md`
- `AGENT_REGISTRY.md`
- generated room snapshot

### Agents Page
Primary sources:
- `AGENT_REGISTRY.md`

### Jobs Page
Primary sources:
- cron list
- cron runs
- `JOB_CATALOG.md`
- `AGENT_REGISTRY.md`

### Approvals Page
Primary sources:
- generated approvals snapshot
- explicit approval events later

### Activity Page
Primary sources:
- generated activity snapshot

### System Page
Primary sources:
- `openclaw status`
- gateway status
- generated system snapshot

## Suggested Snapshot Generation Strategy

### Phase 1
Use a lightweight script or command pipeline to generate JSON from:
- agent registry
- room definitions
- cron status/runs
- openclaw status

This can populate:
- agents
- rooms
- jobs
- system

### Phase 2
Add generated snapshots for:
- alerts
- activity
- approvals
- recommended focus

### Phase 3
Improve room-specific status derivation from live output and queues.

## Suggested File Ownership

### Workspace docs own
- definitions
- room purposes
- registry
- product intent

### Runtime commands own
- status
- health
- run history

### Snapshot layer owns
- UI-ready normalization
- denormalized card data
- latest activity summaries

## Reliability Rules
- Never let the dashboard invent status that does not trace back to a source.
- If a field cannot be sourced confidently, omit it or mark it unavailable.
- Prefer fewer trustworthy cards over many speculative ones.
- Keep the dashboard stable even if one optional source is temporarily missing.

## V1 Minimum Viable Data Set
Mission Control V1 can be useful with only:
- `AGENT_REGISTRY.md`
- `CHANNEL_ARCHITECTURE_PLAN.md`
- cron list/runs
- `openclaw status`

That is enough to build:
- rooms view
- agents view
- jobs health
- top-line system status

## Recommended Next Technical Step
After this document, the next useful artifact is:
- `MISSION_CONTROL_SNAPSHOT_SPEC.md`

That file should define the exact JSON shapes for:
- rooms.json
- agents.json
- jobs.json
- system.json
- alerts.json
- approvals.json
- activity.json
