# CROSS_ROOM_HANDOFF_STANDARD.md

## Purpose
This file defines the standard handoff format for meaningful changes that affect more than one room.

A handoff is required when one room changes reality for another room.

## Use a handoff for
- cutovers
- deploys
- infra changes
- room routing changes
- recurring job changes
- session resets
- incidents and recoveries
- repo path or workspace anchor changes
- anything engineering must know before acting safely

## Required fields
Every cross room handoff should include:
- **Change**
- **Why it matters**
- **Affected rooms**
- **Action requested**
- **Urgency**
- **Approval needed?**
- **Source of truth**

## Standard template
**Change:**

**Why it matters:**

**Affected rooms:**

**Action requested:**

**Urgency:**

**Approval needed?:**

**Source of truth:**

## Routing rule
Post or deliver the handoff to:
- the room that needs to act
- `ops-desk` if the change affects operation or delivery
- `command-center` if the change affects priorities, blockers, or multiple rooms
- `engineering` if implementation, deployment, config, automation, or debugging implications exist

## Non negotiable rule
If a change affects engineering reality and engineering did not receive a handoff, the communication process failed.

## Good handoff example
**Change:** Signal and Circuit room session was reset to a fresh session after repeated typing stall behavior.

**Why it matters:** prior context was degraded and unreliable. New work should not assume the old room session state.

**Affected rooms:** `signal-and-circuit`, `engineering`, `ops-desk`

**Action requested:** engineering should treat future Signal and Circuit work as coming from a fresh room session and rely on current docs rather than stale room memory.

**Urgency:** medium

**Approval needed?:** no

**Source of truth:** `LIVE_CONFIG_AUDIT_2026-03-24.md`, `CURRENT_PLATFORM_STATE.md`
