# MISSION_CONTROL_SNAPSHOT_SPEC.md

## Purpose
This document defines the JSON snapshot shapes for Mission Control V1 so the dashboard can consume a stable, UI-friendly data layer.

## Goal
Normalize the current OpenClaw room/agent/job/system state into a small set of generated JSON files.

These snapshot files should:
- be derived from canonical docs and live command outputs
- avoid duplicating source-of-truth logic in the frontend
- make the UI implementation simple and predictable

## Snapshot Directory
Recommended directory:
- `mission-control/`

Recommended files:
- `mission-control/rooms.json`
- `mission-control/agents.json`
- `mission-control/jobs.json`
- `mission-control/system.json`
- `mission-control/alerts.json`
- `mission-control/approvals.json`
- `mission-control/activity.json`
- `mission-control/overview.json`

## Common Conventions

### Timestamps
Use ISO-8601 strings in UTC.

Examples:
- `2026-03-21T22:10:00Z`
- `2026-03-21T22:10:00.123Z`

### Status enums
Preferred values:
- `healthy`
- `warning`
- `blocked`
- `quiet`
- `active`
- `paused`
- `planned`
- `error`

### Priority enums
Preferred values:
- `low`
- `normal`
- `high`
- `urgent`

### IDs
Use stable string IDs whenever possible:
- room slug for rooms
- agent slug/name for agents
- cron job ID for jobs
- generated IDs for alerts/approvals/activity items

## 1. rooms.json

### Purpose
Provide card-ready room state for the Rooms page and the Overview room grid.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "rooms": [
    {
      "id": "command-center",
      "name": "command-center",
      "channelId": "1484651751108775946",
      "status": "healthy",
      "headline": "Morning digest delivered; no major blockers.",
      "lastUpdateAt": "2026-03-21T13:30:00Z",
      "agents": ["command-center"],
      "badges": {
        "approvals": 0,
        "alerts": 0,
        "queue": 0
      },
      "kind": "command"
    }
  ]
}
```

### Required fields per room
- `id`
- `name`
- `channelId` (nullable if no Discord room exists)
- `status`
- `headline`
- `lastUpdateAt` (nullable)
- `agents` (array)
- `badges` object
- `kind`

## 2. agents.json

### Purpose
Provide agent status/metadata for the Agents page.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "agents": [
    {
      "id": "caruso-growth",
      "name": "caruso-growth",
      "status": "active",
      "roomId": "caruso-growth",
      "mission": "Find, package, and route growth opportunities for Caruso.",
      "jobs": [
        "ee105b50-2e8e-463b-b9a4-bcc165a21a3d"
      ],
      "skills": ["caruso-growth"],
      "approvalBoundary": "Public posting requires approval.",
      "phase": "active"
    }
  ]
}
```

### Required fields per agent
- `id`
- `name`
- `status`
- `roomId` (nullable)
- `mission`
- `jobs`
- `skills`
- `approvalBoundary`
- `phase`

## 3. jobs.json

### Purpose
Provide normalized job state for the Jobs page and Overview health panel.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "jobs": [
    {
      "id": "148c5073-5be0-40cc-8cbc-79f062a18191",
      "name": "morning-command-center-digest-weekdays-830am",
      "roomId": "command-center",
      "status": "active",
      "enabled": true,
      "lastRunAt": "2026-03-21T13:30:00Z",
      "nextRunAt": "2026-03-22T13:30:00Z",
      "lastResult": "ok",
      "recentFailureCount": 0,
      "summary": "Morning digest posted successfully.",
      "destination": {
        "type": "discord",
        "channelId": "1484651751108775946"
      }
    }
  ]
}
```

### Required fields per job
- `id`
- `name`
- `roomId` (nullable)
- `status`
- `enabled`
- `lastRunAt` (nullable)
- `nextRunAt` (nullable)
- `lastResult` (`ok`, `warning`, `failed`, `unknown`)
- `recentFailureCount`
- `summary`
- `destination`

## 4. system.json

### Purpose
Provide top-level system/runtime health for the System page and Overview health strip.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "system": {
    "overallStatus": "healthy",
    "hostLabel": "Jeremy’s MacBook Pro",
    "gatewayStatus": "running",
    "runtime": "openclaw",
    "activeJobCount": 12,
    "failingJobCount": 1,
    "warningCount": 2,
    "notes": [
      "Signal and Circuit mail monitor was recently repaired."
    ]
  }
}
```

### Required fields
- `generatedAt`
- `system.overallStatus`
- `system.hostLabel`
- `system.gatewayStatus`
- `system.runtime`
- `system.activeJobCount`
- `system.failingJobCount`
- `system.warningCount`
- `system.notes`

## 5. alerts.json

### Purpose
Provide bounded, high-signal alerts/blockers for Overview and Alerts views.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "alerts": [
    {
      "id": "alert-signal-mail-monitor",
      "title": "Signal and Circuit mail monitor needed channel remap",
      "roomId": "signal-and-circuit",
      "severity": "warning",
      "summary": "Old room ID caused Unknown Channel failures until remapped.",
      "createdAt": "2026-03-21T21:00:00Z",
      "status": "open",
      "sourceType": "job",
      "sourceRef": "4cfe0675-b283-433d-bcaf-432a08706980"
    }
  ]
}
```

### Required fields per alert
- `id`
- `title`
- `roomId` (nullable)
- `severity`
- `summary`
- `createdAt`
- `status`
- `sourceType`
- `sourceRef` (nullable)

## 6. approvals.json

### Purpose
Provide a central list of things waiting on Jeremy.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "approvals": [
    {
      "id": "approval-example-1",
      "title": "Review support reply draft",
      "roomId": "support-inbox",
      "risk": "medium",
      "decisionType": "send",
      "summary": "Customer reply drafted; needs human approval before sending.",
      "requestedAt": "2026-03-21T20:00:00Z",
      "status": "pending"
    }
  ]
}
```

### Required fields per approval
- `id`
- `title`
- `roomId` (nullable)
- `risk`
- `decisionType`
- `summary`
- `requestedAt`
- `status`

## 7. activity.json

### Purpose
Provide a normalized recent-activity feed for the Overview and Activity pages.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "activity": [
    {
      "id": "activity-1",
      "roomId": "caruso-growth",
      "kind": "recommendation",
      "title": "Caruso opportunity scan posted",
      "summary": "Three medium-fit opportunities surfaced for Jira/TestRail discussions.",
      "priority": "normal",
      "at": "2026-03-21T19:00:00Z",
      "sourceType": "job",
      "sourceRef": "ee105b50-2e8e-463b-b9a4-bcc165a21a3d"
    }
  ]
}
```

### Required fields per activity item
- `id`
- `roomId`
- `kind`
- `title`
- `summary`
- `priority`
- `at`
- `sourceType`
- `sourceRef` (nullable)

## 8. overview.json

### Purpose
Provide a precomputed overview payload so the homepage can render without recomputing cross-file state in the client.

### Shape
```json
{
  "generatedAt": "2026-03-21T22:10:00Z",
  "overview": {
    "globalHealth": {
      "systemStatus": "healthy",
      "activeRooms": 9,
      "activeAgents": 8,
      "pendingApprovals": 1,
      "openAlerts": 2,
      "failingJobs": 0
    },
    "needsAttention": [
      {
        "title": "Review Signal and Circuit P0 remediation handoff",
        "roomId": "signal-and-circuit",
        "priority": "high"
      }
    ],
    "recommendedFocus": [
      "Hand the P0 engineering backlog from Signal and Circuit to engineering.",
      "Review whether support-inbox now receives support mail cleanly."
    ]
  }
}
```

### Required fields
- `generatedAt`
- `overview.globalHealth`
- `overview.needsAttention`
- `overview.recommendedFocus`

## Derivation Rules

### rooms.json
Derived from:
- `CHANNEL_ARCHITECTURE_PLAN.md`
- `AGENT_REGISTRY.md`
- generated room status/headline logic

### agents.json
Derived from:
- `AGENT_REGISTRY.md`

### jobs.json
Derived from:
- cron list
- cron runs
- `AGENT_REGISTRY.md`
- `CHANNEL_MIGRATION_MAP.md`

### system.json
Derived from:
- `openclaw status`
- optional system/gateway checks

### alerts.json
Derived from:
- failing jobs
- important blocker states
- significant room-level warnings

### approvals.json
Derived from:
- explicit approval-tracking data or generated room summaries

### activity.json
Derived from:
- recent job outputs
- room summaries
- alert/approval events

### overview.json
Derived from:
- all the above snapshots

## Implementation Guidance
- Generate snapshots server-side or via a workspace script.
- Do not make the frontend parse markdown directly if a generated snapshot exists.
- Keep each file small, focused, and cacheable.
- Regenerate snapshots on a timer or on-demand.

## V1 Minimum Needed First
The first implementable set can be just:
- `rooms.json`
- `agents.json`
- `jobs.json`
- `system.json`
- `overview.json`

That is enough for a useful V1.

## Next Step
After this spec, the next practical artifact is:
- `MISSION_CONTROL_IMPLEMENTATION_PLAN.md`

That should define:
- what stack to use
- where the code should live
- how snapshots get generated
- how the first end-to-end prototype should be built
