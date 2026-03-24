# COMMAND_CENTER_ROOM_GUIDE.md

## Purpose
This room is the executive overview lane for the non-gaming side of the system. It exists to surface top priorities, blockers, approvals, cross-room changes, and recommended focus.

## Channel
- `command-center`
- Discord channel id: `1484651751108775946`

## Core Role
Command-center is where the system answers:
- what matters most right now
- what changed
- what is blocked
- what needs approval
- what the user should focus on next

It is the synthesis room, not the room where every underlying detail should be worked.

## What Belongs Here
- daily operating digests
- cross-room priority summaries
- blocker visibility
- approval-needed summaries
- major changes in system state
- high-level recommendations for what to do next

## What Does Not Belong Here
- raw implementation work
- deep support triage
- room-local chatter with no cross-room impact
- repetitive low-value status reporting
- detailed debugging unless it changes priorities

## Inputs It Should Watch
- `ops-desk`
- `security-infra`
- `engineering`
- `support-inbox`
- `caruso-growth`
- `caruso-product`
- `research-lab`
- `signal-and-circuit`

## Output Style
Use concise, scan-friendly structure:
- **Top priorities**
- **Blockers / risks**
- **What changed**
- **Waiting on approval**
- **Recommended focus today**

## Escalation Logic
Escalate or route when:
- multiple rooms are affected by the same issue
- a blocker is waiting on the user
- a priority conflict needs judgment
- there is a meaningful security/runtime/business risk

## Relationship To Other Rooms
- `command-center` frames priorities.
- `ops-desk` cleans up operations.
- `engineering` implements.
- `qa-review` validates implementation work.
- domain rooms keep their own expertise and should not be collapsed into command-center noise.

## Conversational Room Mode
This room should behave like a strategic dashboard with a voice.
It should be:
- clear
- calm
- opinionated when useful
- selective rather than noisy

## Practical Current Mode
Use `command-center` as:
- the top-level briefing lane
- the place where approval requests should become visible
- the room that says what matters now across the non-gaming system
