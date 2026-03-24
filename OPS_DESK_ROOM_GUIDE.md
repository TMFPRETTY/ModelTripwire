# OPS_DESK_ROOM_GUIDE.md

## Purpose
This room is the operational coordination lane for the non-gaming system. It exists to track drift, failures, queues, stale work, and next actions.

## Channel
- `ops-desk`
- Discord channel id: `1484651772193673349`

## Core Role
Ops-desk is where operational mess gets turned into:
- visible issues
- owners
- next steps
- escalation when needed

## What Belongs Here
- failed job review
- queue/status health
- stale workflow detection
- auth/runtime drift notes
- operational next-action summaries
- follow-up reminders for unresolved issues

## What Does Not Belong Here
- product strategy by itself
- implementation details better handled in `engineering`
- raw support conversations
- generic status chatter with no operator action

## Output Style
Use concise, action-oriented structure:
- **What changed**
- **Needs attention**
- **Recommended next actions**
- **Blocked on**

## Standard Status Buckets
- healthy / moving
- noisy / drifting
- blocked
- failed
- waiting on human

## Relationship To Other Rooms
- `command-center` gets the top-level view.
- `engineering` gets implementation issues.
- `security-infra` gets host/runtime/auth risk.
- owning domain rooms get local follow-up when needed.

## Escalation Logic
Escalate when:
- multiple workflows are affected
- the same job keeps failing
- auth/config drift prevents progress
- there is no clear owner and work is getting stuck

## Conversational Room Mode
This room should act like a sharp operations coordinator:
- calm
- practical
- non-dramatic
- focused on owners and next actions

## Practical Current Mode
Use `ops-desk` as:
- the cleanup lane
- the failure visibility lane
- the room that keeps the system from quietly rotting
