# STANDUP_AND_SYNC_MODEL.md

## Purpose
This file defines the communication rhythm that should keep rooms aligned without creating chatter theater.

The system should not depend on agents casually remembering what happened yesterday.
It should depend on structured updates.

## Core principle
Standup is not freeform agent banter.
Standup is structured communication.

## Daily rhythm

### 1. Morning cross room standup
Purpose:
- what changed since yesterday
- what is blocked
- what needs attention today
- what major handoffs are pending

Primary output destination:
- `command-center`

Key contributors:
- `ops-desk`
- `engineering`
- `security-infra`
- `signal-and-circuit`
- `caruso-growth`
- `caruso-product`
- `support-inbox` when relevant
- `research-lab` only when there is real signal

Output structure:
- **What changed since yesterday**
- **Current blockers**
- **Waiting on whom**
- **Needs attention today**
- **Cross room handoffs**

### 2. Engineering context sync
Purpose:
- ensure engineering sees the implementation relevant reality of the system
- avoid engineering operating from stale room memory

Primary output destination:
- `engineering`

What it should include:
- major operating changes since yesterday
- platform or infra changes
- cutovers
- deployment state changes
- room resets that affect implementation work
- job or routing changes that affect engineering
- pending QA relevant items

Output structure:
- **Major changes engineering must know**
- **Active blockers**
- **Implementation requests**
- **QA and review needs**
- **Source docs to trust**

## Room responsibility model
- `command-center` owns top level synthesis
- `ops-desk` owns operational change visibility and follow through
- `engineering` owns implementation reality
- domain rooms own domain signal
- `qa-review` owns validation posture for engineering impact work

## What not to do
- do not make every room talk every day just to prove life
- do not flood engineering with all room chatter
- do not treat chat history as the only continuity layer
- do not assume a room knows a major change unless it was logged or handed off

## Minimum communication standard
For major changes, the system should produce all of these:
- changelog entry
- current state update if needed
- cross room handoff if another room is affected
- standup visibility if it matters today
- engineering sync visibility if implementation reality changed

## Recommended jobs
- `daily-cross-room-standup`
- `engineering-context-sync`

These should be treated as high value communication infrastructure, not optional niceties.
