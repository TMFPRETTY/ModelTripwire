# MISSION_CONTROL_PLAN.md

## Purpose
Mission Control is the visual dashboard/control layer for the OpenClaw operating system. It should sit on top of the real room/agent/job structure already running in Discord and in the workspace, not invent a disconnected second system.

## Product Goal
Give Jeremy a fast, trustworthy way to answer:
- what matters right now?
- which agents/rooms are active?
- what is healthy vs blocked?
- what needs approval?
- what changed recently?
- where should I look first?

## Core Principle
Mission Control should be a **visual layer over the real operating model**.

That means:
- rooms in Mission Control map to real Discord rooms
- agents map to the real agents in `AGENT_REGISTRY.md`
- jobs map to real cron jobs
- alerts/approvals map to real operational events
- status should come from live or near-live sources, not hand-maintained fiction

## V1 Philosophy
Start with a useful, boring, high-signal dashboard.

Do not start with:
- a giant bespoke data model for everything
- virtual office gimmicks
- overdesigned animations
- trying to mirror every Discord message in real time

Start with:
- one overview page
- room status cards
- job health
- approvals/alerts
- recent activity

## Naming
Working name:
- **Mission Control**

Acceptable alternates later:
- OpenClaw HQ
- Control Tower
- Ops Console

## V1 Scope

### Primary page: Overview
The overview page should be the first useful screen.

It should include:
1. system health summary
2. room status grid
3. agent status summary
4. job health panel
5. approvals waiting
6. alerts / blockers
7. recent activity feed
8. recommended attention section

### Secondary views for V1 or V1.1
- Rooms
- Agents
- Jobs
- Approvals
- Activity
- System

## V1 Page Structure

### 1. Overview
Purpose:
- answer what matters right now at a glance

Widgets:
- overall health strip
- room status cards
- pending approvals count/list
- active alerts/blockers
- latest meaningful updates
- recent job failures or warnings
- "needs attention" section

### 2. Rooms
Purpose:
- show each operating room and its current state

For each room show:
- name
- status
- headline/summary
- last update
- related agent(s)
- queue/attention indicator if available

### 3. Agents
Purpose:
- show the active/transitional/planned agent map

For each agent show:
- name
- room
- status
- mission
- current jobs
- approval boundary summary

### 4. Jobs
Purpose:
- see schedule/health/failure status quickly

For each job show:
- name
- room
- enabled/disabled
- last run
- next run
- status
- recent failure count

### 5. Approvals
Purpose:
- centralize things waiting on Jeremy

Show:
- title
- room/source
- risk level
- decision needed
- age

### 6. Activity
Purpose:
- see the latest meaningful events across rooms

Show:
- room
- event type
- title/summary
- timestamp
- priority

### 7. System
Purpose:
- see runtime health

Show:
- host status
- gateway state
- active job count
- failed job count
- last system snapshot

## Initial Room Set
Mission Control should include these current rooms:
- command-center
- ops-desk
- support-inbox
- caruso-growth
- caruso-product
- security-infra
- research-lab
- signal-and-circuit
- engineering

## Initial Agent Set
Use `AGENT_REGISTRY.md` as the starting source for:
- active agents
- embedded agents
- transitional agents
- planned agents
- retired agents

## Data Sources

### Static / semi-static sources
- `AGENT_REGISTRY.md`
- `CHANNEL_ARCHITECTURE_PLAN.md`
- `CHANNEL_MIGRATION_MAP.md`
- `JOB_CATALOG.md`
- `DASHBOARD_SCHEMA_V1.md`

### Live / dynamic sources
- cron/job status and run history
- `openclaw status`
- room/job outputs as summarized updates
- future local snapshot/state files

## Suggested Data Pipeline
V1 does not need a full backend database immediately.

Reasonable V1 approach:
1. use markdown docs as static definitions
2. use cron/status outputs as dynamic data
3. optionally generate lightweight JSON snapshots for the UI
4. add persistence later if needed

## Recommended V1 Objects
Mission Control should expose, at minimum:
- Room
- Agent
- Job
- Update
- Approval
- Alert
- SystemHealthSnapshot

These already align with `DASHBOARD_SCHEMA_V1.md`.

## Visual Direction
Mission Control should feel:
- dark mode
- serious
- operational
- calm
- trustworthy
- easy to scan

Think:
- control room
- operations dashboard
- executive/status board

Not:
- playful AI desktop
- fake sci-fi clutter

## UX Rules
- High signal over completeness.
- Important things should stand out without shouting.
- Each card should answer a real question.
- Avoid giant blobs of text.
- Avoid requiring Discord knowledge to understand the dashboard.
- Use room names and statuses consistently with the actual system.

## V1 Build Order

### Step 1
Finalize the object mapping from current docs/state into UI cards.

### Step 2
Create the overview page with fake/static data using the real schema.

### Step 3
Wire in live job/system status.

### Step 4
Wire in room/agent summaries.

### Step 5
Add approvals/alerts/activity.

### Step 6
Refine visual design only after the data view is useful.

## Out of Scope For V1
- advanced analytics
- long-term trend charts
- deep automation editing UI
- full chat inside the dashboard
- pixel-perfect “digital office” metaphor
- replacing Discord as the live work surface

## Definition of Success
Mission Control V1 is successful when Jeremy can open it and quickly understand:
- the state of the system
- which rooms are healthy or blocked
- what needs attention now
- which agents are active
- what jobs are failing or noisy
- what approvals are waiting

## Immediate Next Artifact
After this plan, the next likely step is:
- `MISSION_CONTROL_WIREFRAMES.md`

That should define the exact card layout of the Overview page before implementation starts.
