# DASHBOARD_SCHEMA_V1.md

## Purpose
This document defines the V1 conceptual schema for the future OpenClaw HQ dashboard. The goal is a practical control plane first, with room for later “digital office” presentation on top.

## Product Direction
Visual tone:
- serious dark-mode mission control
- subtle office metaphor
- dashboard as operating system
- Discord remains the execution surface

## Top-Level Navigation
- Overview
- Rooms
- Standup
- Approvals
- Agents
- Activity
- System

## Primary Rooms / Lanes
- Command Center
- Ops Desk
- Support Inbox
- Growth Room
- Product Lab
- Security Office
- Research Lab
- Newsroom
- Meeting Room / Standup Room
- Approval Board
- QA Review (initially embedded, later optional room)

## Core Data Objects

### Agent
Represents a logical worker or workflow persona.

Fields:
- `id`
- `name`
- `slug`
- `roomId`
- `status` (`idle`, `running`, `waiting`, `blocked`, `error`, `paused`)
- `summary`
- `ownerType` (`system`, `human`, `hybrid`)
- `lastActiveAt`
- `currentJobId` (nullable)
- `capabilities` (array)
- `approvalRequiredByDefault` (boolean)

### Room
Represents a Discord room / operational domain.

Fields:
- `id`
- `name`
- `slug`
- `kind` (`command`, `ops`, `support`, `growth`, `product`, `security`, `research`, `editorial`, `approvals`, `meeting`)
- `discordChannelId` (nullable)
- `status`
- `headline`
- `priority`
- `agentIds` (array)

### Workflow
Represents an ongoing process with one or more jobs.

Fields:
- `id`
- `name`
- `roomId`
- `status` (`healthy`, `warning`, `blocked`, `paused`)
- `summary`
- `jobIds` (array)
- `queueDepth` (nullable)
- `lastRunAt`
- `nextRunAt`

### Job
Represents a scheduled or triggered execution unit.

Fields:
- `id`
- `name`
- `workflowId`
- `roomId`
- `scheduleType` (`cron`, `interval`, `manual`, `event`)
- `scheduleExpr` (nullable)
- `status` (`active`, `paused`, `running`, `failed`, `disabled`)
- `lastRunAt`
- `lastResult`
- `nextRunAt`
- `failureCountRecent`
- `destinationType` (`discord`, `dashboard`, `mixed`)
- `destinationRef` (nullable)

### Update
Represents a meaningful message/event emitted by an agent or workflow.

Fields:
- `id`
- `roomId`
- `agentId` (nullable)
- `jobId` (nullable)
- `kind` (`summary`, `alert`, `recommendation`, `approval_request`, `result`, `digest`)
- `title`
- `body`
- `priority` (`low`, `normal`, `high`, `urgent`)
- `createdAt`
- `linkRef` (nullable)
- `actionState` (`info`, `needs_review`, `approved`, `rejected`, `resolved`)

### QueueItem
Represents work awaiting triage/action.

Fields:
- `id`
- `roomId`
- `sourceType` (`email`, `job_failure`, `idea`, `mention`, `task`, `alert`)
- `sourceRef`
- `title`
- `status` (`new`, `triaged`, `in_progress`, `waiting`, `done`, `ignored`)
- `priority`
- `ownerAgentId` (nullable)
- `createdAt`
- `updatedAt`

### Approval
Represents a bounded decision requiring explicit human input.

Fields:
- `id`
- `roomId`
- `requestedByAgentId` (nullable)
- `title`
- `summary`
- `riskLevel` (`low`, `medium`, `high`)
- `decisionType` (`send`, `post`, `change_config`, `spend`, `delete`, `other`)
- `status` (`pending`, `approved`, `rejected`, `expired`)
- `requestedAt`
- `resolvedAt` (nullable)
- `contextLinks` (array)

### Standup
Represents a timed standup/reporting collection.

Fields:
- `id`
- `date`
- `status` (`draft`, `published`)
- `summary`
- `entryIds` (array)

### StandupEntry
Represents one room or agent contribution to a standup.

Fields:
- `id`
- `standupId`
- `roomId`
- `agentId` (nullable)
- `yesterday`
- `today`
- `blockers`
- `priority`

### Alert
Represents a high-importance condition.

Fields:
- `id`
- `roomId`
- `severity` (`warning`, `critical`)
- `title`
- `summary`
- `sourceType`
- `sourceRef`
- `status` (`open`, `acknowledged`, `resolved`)
- `createdAt`
- `resolvedAt` (nullable)

### ChannelMapping
Represents where a room or agent announces.

Fields:
- `id`
- `roomId`
- `agentId` (nullable)
- `provider` (`discord`)
- `channelId`
- `threadMode` (`none`, `per_item`, `per_run`)
- `enabled`

### SystemHealthSnapshot
Represents periodic machine/runtime health.

Fields:
- `id`
- `capturedAt`
- `hostLabel`
- `gatewayStatus`
- `openclawStatus`
- `activeJobCount`
- `failedJobCount`
- `notes`

## Likely Later Objects
- `Persona`
- `Idea`
- `KnowledgeArtifact`
- `MemoryLink`
- `Site`
- `Campaign`

## Relationship Summary
- a Room has many Agents
- a Room has many Workflows
- a Workflow has many Jobs
- an Agent emits many Updates
- a Room contains many QueueItems
- a Room can have many Approvals and Alerts
- Standup aggregates StandupEntries from Rooms/Agents

## V1 Widget Set

### Status Summary
Shows:
- active rooms
- healthy/warning/blocked counts
- pending approvals
- alerts

### Queue List
Shows:
- top queue items by room
- priority and age
- owner/agent

### Approval Queue
Shows:
- pending approvals
- risk levels
- what action is waiting

### Recent Activity Feed
Shows:
- latest updates across rooms
- alerts, summaries, recommendations

### Alert Banner
Shows:
- urgent failures or risks requiring attention

### Agent Card
Shows:
- agent status
- current task
- last activity
- room

### Room Card
Shows:
- room health
- headline
- queue depth
- last update

### Standup Summary
Shows:
- today’s standup rollup
- blockers
- priorities

### Recommendation Widget
Shows:
- product/growth/research recommendations awaiting review

### Workflow Health
Shows:
- next run
- last result
- recent failures

### Channel Link
Shows:
- direct link between dashboard object and Discord destination

### System Health Grid
Shows:
- host health
- gateway state
- active job count
- failures

## V1 Rules
- every dashboard card should map to a real underlying object
- every alert should have a source
- every approval should have bounded decision context
- avoid storing giant blobs when a compact summary + source link is enough
- optimize for triage clarity over visual cleverness

## Suggested First API/State Priorities
1. Rooms
2. Agents
3. Jobs
4. Updates
5. Approvals
6. Alerts
7. Queue items
8. System snapshots

## Definition of a Good Dashboard
A good dashboard lets Jeremy answer, at a glance:
- what matters right now?
- what is blocked?
- what needs my approval?
- which agents are healthy?
- what changed since I last looked?
