# MISSION_CONTROL_WIREFRAMES.md

## Purpose
This document defines the wireframe structure for Mission Control V1 so the dashboard can be implemented from a concrete layout rather than a loose concept.

## Design Goal
Mission Control should let Jeremy understand the state of the system in under a minute.

The first screen should answer:
- what matters right now?
- what is healthy vs blocked?
- what needs my attention?
- what changed recently?

## General Layout Principles
- dark mode
- high signal density without clutter
- readable at a glance
- cards should summarize, not dump logs
- the overview page should feel like a control surface, not a spreadsheet

## V1 Navigation
Top navigation:
- Overview
- Rooms
- Agents
- Jobs
- Approvals
- Activity
- System

## Primary Screen: Overview

### Wireframe structure

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Mission Control                                                    │
│ Global health | Active rooms | Alerts | Approvals | Job failures   │
├─────────────────────────────────────────────────────────────────────┤
│ Needs Attention                                                    │
│ - 2 to 5 highest-priority items                                    │
├───────────────────────┬─────────────────────────────────────────────┤
│ Room Status Grid      │ Recent Activity                             │
│ command-center        │ [room] title / summary / time              │
│ ops-desk              │ [room] title / summary / time              │
│ support-inbox         │ [room] title / summary / time              │
│ caruso-growth         │ ...                                         │
│ caruso-product        │                                             │
│ security-infra        │                                             │
│ research-lab          │                                             │
│ signal-and-circuit    │                                             │
│ engineering           │                                             │
├───────────────────────┴─────────────────────────────────────────────┤
│ Jobs Health                                                        │
│ failing / warning / next up / recently run                         │
├───────────────────────┬─────────────────────────────────────────────┤
│ Approvals Waiting     │ Alerts / Blockers                           │
│ pending decisions     │ urgent issues and blockers                  │
├───────────────────────┴─────────────────────────────────────────────┤
│ Recommended Focus Today                                            │
│ - 1 to 3 suggested actions                                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Overview Sections

### 1. Global Health Strip
Purpose:
- give instant top-level status

Contents:
- total active rooms
- total active agents
- pending approvals count
- open alerts count
- jobs failing count
- system health status (`healthy`, `warning`, `blocked`)

Display style:
- compact stat pills/cards across the top

### 2. Needs Attention
Purpose:
- show the 2 to 5 highest-priority things Jeremy should care about immediately

Examples:
- engineering blocked on X
- security issue needs approval
- Signal and Circuit has AdSense blocker
- support issue requires reply

Rules:
- only show items with real urgency or consequence
- this should not become a duplicate of recent activity

### 3. Room Status Grid
Purpose:
- visualize the operating rooms as the main units of work

Show one card per room:
- room name
- status (`healthy`, `warning`, `blocked`, `quiet`)
- short headline
- last update time
- optional badges: approvals / blockers / queue

Initial rooms:
- command-center
- ops-desk
- support-inbox
- caruso-growth
- caruso-product
- security-infra
- research-lab
- signal-and-circuit
- engineering

Card style:
- 3 columns desktop / stacked mobile
- color status accent only, not giant color blocks

### 4. Recent Activity Feed
Purpose:
- show the latest meaningful cross-room updates

Each item should include:
- room
- title
- one-line summary
- timestamp
- priority badge if needed

Rules:
- omit low-value healthy chatter
- prefer digest/recommendation/alert-style items
- cap feed length on overview

### 5. Jobs Health Panel
Purpose:
- show job execution health without making users read the cron system directly

Subsections:
- failing now
- warning / noisy
- next scheduled
- recently completed

Each row:
- job name
- room
- status
- last run
- next run
- failure count recent

Rules:
- sort failures first
- keep successful routine jobs visually compressed

### 6. Approvals Waiting
Purpose:
- central place for things that need Jeremy’s decision

Each item:
- title
- source room
- risk level
- age
- decision type

Rules:
- only bounded approvals
- avoid vague “review this maybe” clutter

### 7. Alerts / Blockers
Purpose:
- show operationally important interruptions

Examples:
- gateway/runtime issue
- repeated job failure
- auth break
- security issue
- major cross-room blocker

Each item:
- title
- source
- severity
- short summary
- age

### 8. Recommended Focus Today
Purpose:
- close the loop by turning dashboard state into action

Format:
- 1 to 3 plain-language recommended actions

Examples:
- Review Signal and Circuit P0 backlog and hand P0 ENG items to engineering
- Approve or reject the pending support response draft
- Investigate the repeated Caruso growth search failures

## Secondary Screen Wireframes

### Rooms Page
```text
┌───────────────────────────────────────────────────────────────┐
│ Rooms                                                        │
├───────────────────────────────────────────────────────────────┤
│ [Filters: all / healthy / warning / blocked]                 │
├───────────────────────────────────────────────────────────────┤
│ command-center  | status | headline | last update | agents   │
│ ops-desk        | status | headline | last update | agents   │
│ ...                                                         │
└───────────────────────────────────────────────────────────────┘
```

Room detail view should show:
- room purpose
- linked agent(s)
- related jobs
- recent updates
- approvals/alerts tied to room

### Agents Page
```text
┌───────────────────────────────────────────────────────────────┐
│ Agents                                                       │
├───────────────────────────────────────────────────────────────┤
│ [Filters: active / transitional / planned / embedded]        │
├───────────────────────────────────────────────────────────────┤
│ agent | room | status | mission | current jobs               │
└───────────────────────────────────────────────────────────────┘
```

Agent detail should show:
- mission
- room
- status
- skills used
- approval boundary
- current jobs

### Jobs Page
```text
┌───────────────────────────────────────────────────────────────┐
│ Jobs                                                         │
├───────────────────────────────────────────────────────────────┤
│ [Filters: failing / warning / active / paused]               │
├───────────────────────────────────────────────────────────────┤
│ job | room | status | last run | next run | failures         │
└───────────────────────────────────────────────────────────────┘
```

### Approvals Page
```text
┌───────────────────────────────────────────────────────────────┐
│ Approvals                                                    │
├───────────────────────────────────────────────────────────────┤
│ title | room | risk | age | decision needed                  │
└───────────────────────────────────────────────────────────────┘
```

### Activity Page
```text
┌───────────────────────────────────────────────────────────────┐
│ Activity                                                     │
├───────────────────────────────────────────────────────────────┤
│ time | room | kind | summary                                 │
└───────────────────────────────────────────────────────────────┘
```

### System Page
```text
┌───────────────────────────────────────────────────────────────┐
│ System                                                       │
├───────────────────────────────────────────────────────────────┤
│ gateway status | host health | active jobs | failures        │
│ runtime notes | last snapshot | warnings                     │
└───────────────────────────────────────────────────────────────┘
```

## Status Language
Use consistent statuses across cards/pages:
- `healthy`
- `warning`
- `blocked`
- `quiet`
- `active`
- `paused`
- `planned`

## Priority Language
Use:
- `low`
- `normal`
- `high`
- `urgent`

## Visual Hierarchy Rules
- Needs Attention should sit above everything else except the top health strip.
- Rooms are the primary dashboard object, not individual messages.
- Jobs should be visible but secondary to room state.
- Approvals and alerts should be easy to scan without dominating the whole page when empty.
- Recent activity should summarize, not sprawl.

## Mobile / Narrow Layout
If the layout collapses:
1. global health strip
2. needs attention
3. approvals / alerts
4. room cards
5. recent activity
6. jobs

## Out of Scope For Wireframe Phase
- final visual styling details
- animation
- charting
- deep edit/create flows
- live chat UI

## Immediate Next Step
After the wireframes, the next useful artifact is:
- `MISSION_CONTROL_DATA_SOURCES.md`

That should define exactly what files, commands, or generated JSON power each widget/card in the V1 dashboard.
