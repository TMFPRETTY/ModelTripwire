# MISSION_CONTROL_OFFICE_MODE.md

## Purpose
This document defines the humanized / spatial "Office Mode" layer for Mission Control.

Office Mode is not a replacement for the operational dashboard. It is a richer visual presentation layer built on top of the same real rooms, agents, jobs, approvals, and activity.

## Core Idea
Mission Control already has the right operational structure:
- rooms
- agents
- jobs
- approvals
- alerts
- activity

Office Mode should make that system feel more like:
- a staffed digital office
- a newsroom / control center
- a set of rooms where work actually happens
- agents as role-based staff rather than abstract background jobs

## Principle
**Same system, different presentation.**

That means:
- every office room maps to a real room or workflow lane
- every "person" maps to a real agent role
- every conference/standup/review room maps to a real operational state or handoff
- Office Mode should never invent a fake world detached from the real system state

## What Office Mode Should Feel Like
- calm
- cinematic but useful
- modern dark-mode operations center
- like a digital headquarters
- more human and spatial than the flat dashboard

Avoid:
- cartoonish gimmicks
- fake activity unrelated to real system state
- too much motion or novelty that obscures meaning

## Layer Model

### Layer 1 — Operational Dashboard
This is the current Mission Control foundation:
- Overview
- Rooms
- Jobs
- Agents
- Approvals
- System

### Layer 2 — Office Mode
This adds:
- rooms as spaces
- agents as staff/personas
- work movement between rooms
- conference/standup/review spaces
- stronger visual identity

## Rooms As Spaces
The current operating rooms can be presented as physical spaces:

### Command Center
Function:
- mission control
- top priorities
- blockers
- cross-room visibility

### Ops Desk
Function:
- operator coordination desk
- queue/watchdog/failure triage

### Support Inbox
Function:
- inbox handling desk
- reply drafting / escalation area

### Growth Room
Function:
- campaign wall / distribution room
- opportunity review space

### Product Lab
Function:
- product strategy room
- synthesis / prioritization space

### Security Office
Function:
- infra/security monitoring room
- incident/risk station

### Research Lab
Function:
- idea scanning / market analysis room

### Signal and Circuit Newsroom
Function:
- newsroom / editorial desk
- inbox + editorial lookout + monetization planning for now

### Engineering Bay
Function:
- implementation room
- coding/debugging/integration work

## Shared / Conference Spaces
In addition to the main rooms, Office Mode should introduce special spaces that represent real cross-room workflows.

### Standup Room
Purpose:
- daily cross-room summary
- blockers
- what each room is focused on today

Maps to:
- command-center summaries
- future standup rollups

### QA Review Room
Purpose:
- where engineering hands work to QA
- where pass/rework/block decisions happen

Maps to:
- `qa-review`
- engineering <-> QA loop state

### Approval Board / Approval Room
Purpose:
- where pending human decisions are visible

Maps to:
- approvals data
- command-center and room-specific approval requests

### Handoff Room
Purpose:
- where one room hands work to another
- especially useful for:
  - Signal and Circuit -> engineering
  - product -> engineering
  - ops -> security/engineering

Maps to:
- explicit handoff items
- cross-room tasks

## Agents As People / Staff
Office Mode should represent agents more like staff cards or presence tiles than abstract software labels.

Each agent card should include:
- display name
- role title
- current room
- current work focus
- status
- optional avatar/icon

## Suggested Staff Presentation

### command-center
- role: Chief of Staff / Control Lead
- default room: Command Center

### ops-desk
- role: Operations Coordinator
- default room: Ops Desk

### caruso-growth
- role: Growth Strategist
- default room: Growth Room

### caruso-product
- role: Product Analyst / Product Strategist
- default room: Product Lab

### security-infra
- role: Security & Infrastructure Officer
- default room: Security Office

### research-lab
- role: Research Analyst / Scout
- default room: Research Lab

### engineering
- role: Engineer / Implementation Team
- default room: Engineering Bay

### qa-review
- role: QA Reviewer
- default room: QA Review Room (or embedded with Engineering Bay visually)

### signal-and-circuit
- role: Newsroom Editor / Site Operator
- default room: Signal and Circuit Newsroom

### support-inbox
- role: Support Triage Lead
- default room: Support Inbox

## Presence Model
Office Mode should later be able to show:
- where an agent "is"
- what room currently owns their attention
- whether a handoff is in progress

Possible presence states:
- `working in room`
- `waiting`
- `in review`
- `in standup`
- `blocked`
- `handoff pending`

This should be based on real workflow state where possible, not random animation.

## Visual Concepts

### Option A — Grid of named rooms
A map-like dashboard with room cards laid out spatially.

### Option B — Floorplan view
A stylized office/newsroom/control-floor visual layout.

### Option C — Hybrid
Operational overview page + Office Mode toggle.

Recommended approach:
- start with **Hybrid**
- keep current overview
- add an **Office Mode** view/tab later

## Initial Office Mode MVP
The first Office Mode version should include:
- room cards that feel like spaces
- agent/staff tiles inside rooms
- standup room card
- QA review room card
- approval board card
- handoff indicators between rooms

This should be enough to communicate the metaphor without overbuilding.

## How It Maps To Real Data
Office Mode should still use:
- `rooms.json`
- `agents.json`
- `jobs.json`
- `alerts.json`
- `approvals.json`
- `activity.json`
- later standup/handoff snapshots

## Future Snapshot Additions For Office Mode
Likely useful later:
- `presence.json`
- `handoffs.json`
- `standups.json`
- `room-layout.json`

## Interaction Ideas
Later, Office Mode could allow:
- click a room to open its detail view
- click an agent to view status/current work
- click a handoff to trace work from source room to destination room
- click QA Review Room to see pending pass/rework items

## Risks To Avoid
- fake presence unrelated to actual work
- too much motion/noise
- making the dashboard slower or less legible
- turning useful status into decorative fiction

## Definition of Success
Office Mode is successful when:
- the system feels more alive and understandable
- Jeremy can intuitively grasp where work is happening
- cross-room interactions are easier to see
- the richer metaphor improves clarity rather than reducing it

## Immediate Next Step
After this concept doc, the next likely artifact is:
- `MISSION_CONTROL_OFFICE_WIREFRAMES.md`

That should define the actual spatial/floorplan-style screen layout for Office Mode V1.
