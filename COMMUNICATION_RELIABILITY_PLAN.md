# COMMUNICATION_RELIABILITY_PLAN.md

## Purpose
This file turns the communication problem into an operating plan.

## Problem statement
The system had improved docs, but engineering still missed important recent work, including Mac mini cutover context.
That means documentation alone is not enough.
The system needs reliable communication paths.

## Primary failure modes
- important changes only existed in chat memory
- major changes were not handed off to affected rooms
- standup style communication was assumed rather than enforced
- engineering room context was stale or incomplete
- session memory was trusted too much relative to canonical docs

## Communication safeguards to enforce
1. meaningful changes go into `OPERATIONS_CHANGELOG.md`
2. current shared truth goes into `CURRENT_PLATFORM_STATE.md`
3. cross room impacts use `CROSS_ROOM_HANDOFF_STANDARD.md`
4. daily standup follows `STANDUP_AND_SYNC_MODEL.md`
5. engineering relevant changes must be visible in engineering context sync
6. room sessions should be refreshed or reseeded after major operating changes when needed

## Implementation checklist
- [ ] maintain `OPERATIONS_CHANGELOG.md`
- [ ] maintain `CURRENT_PLATFORM_STATE.md`
- [ ] use handoff template for cross room changes
- [ ] add a real daily cross room standup job
- [ ] add a real engineering context sync job
- [ ] include source docs in major updates
- [ ] audit whether the live jobs actually deliver

## Success condition
A room should not have to rely on memory alone to understand major changes from the prior day.
If engineering misses a major cutover or reset, the communication system is still incomplete.
