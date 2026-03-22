# MISSION_CONTROL_OFFICE_WIREFRAMES.md

## Purpose
This document defines the first wireframe layout for Mission Control Office Mode.

## Goal
Office Mode should let Jeremy view the system as a staffed digital headquarters:
- rooms feel like spaces
- agents feel like staff
- handoffs are visible
- standups / QA / approvals appear as conference spaces

## MVP Layout

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Mission Control / Office Mode                                           │
│ System health | Staff on duty | Alerts | Approvals                      │
├──────────────────────────────────────────────────────────────────────────┤
│ Command Center        │ Standup Room          │ Approval Board           │
│ top priorities        │ daily rollup          │ pending decisions        │
├───────────────────────┼───────────────────────┼──────────────────────────┤
│ Ops Desk              │ Engineering Bay       │ QA Review Room           │
│ failures / drift      │ coding work           │ pass / rework / block    │
├───────────────────────┼───────────────────────┼──────────────────────────┤
│ Growth Room           │ Product Lab           │ Security Office          │
│ campaigns / replies   │ recommendations       │ infra/risk               │
├───────────────────────┼───────────────────────┼──────────────────────────┤
│ Research Lab          │ Signal & Circuit      │ Support Inbox            │
│ idea scans            │ newsroom              │ triage / drafts          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Card Types

### Staffed room card
Should show:
- room name
- status
- headline
- staff/agents present
- badge counts (alerts / approvals / queue)

### Conference room card
Used for:
- Standup Room
- QA Review Room
- Approval Board

Should show:
- function
- current queue / pending items
- linked source rooms

## Presence Display
Each room card can show a simple "staff present" strip using agent names/titles.

Examples:
- Command Center → command-center
- Engineering Bay → engineering, qa-review
- Signal & Circuit Newsroom → signal-and-circuit

## Handoff Indicators
Office Mode should later show simple text/lines for important handoffs:
- Signal and Circuit -> Engineering
- Engineering -> QA Review Room
- Product Lab -> Engineering
- Ops Desk -> Security Office

The MVP can start with textual badges instead of animated movement.

## First Office Mode Page Sections
- top health strip
- office grid
- current handoffs
- recommended focus

## Initial Recommendation
Build Office Mode as a separate page/tab first:
- `office.html`

That keeps the normal dashboard intact while allowing the richer metaphor to develop safely.
