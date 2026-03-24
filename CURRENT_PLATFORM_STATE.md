# CURRENT_PLATFORM_STATE.md

## Purpose
This file is the current truth snapshot for platform and operating state.

Use it when a room needs the latest shared context without relying on stale chat memory.

## Current state snapshot

### Platform posture
- Active operating docs now exist for the non gaming system, including registry, runbooks, room guides, safeguards, scorecards, job guide, live audit, and operating index.
- Cross room communication is the next major maturity area and is being formalized.

### Mac mini and cutover context
- Mac mini cutover work from the prior day is important enough that affected rooms should explicitly know about it.
- Engineering missing that context exposed a propagation problem between documentation and live room memory.
- Treat major cutovers as items that must be logged, handed off, and reflected in engineering relevant summaries.

### Signal and Circuit state
- Repo local paths were corrected to current machine reality.
- Live room session was reset after compaction and typing stall issues.
- Room remains more fragile than the others and should stay under watch.

### Command center state
- A scheduled morning digest had a non delivery incident.
- A later rerun delivered successfully.
- Treat command center as functional but worth monitoring for repeat delivery issues.

### Communication state
- The system now has strong docs, but communication enforcement is still being upgraded.
- Daily standup style communication is not yet reliable enough to assume.
- Engineering context sync should be treated as a required operating need.

### Current watchpoints
- Signal and Circuit session fragility
- cross room communication consistency
- engineering awareness of major operating changes
- command center delivery reliability if non delivery repeats

## How to use this file
Check this file before major work involving:
- platform state
- infrastructure changes
- cutovers
- room or workflow changes
- engineering work that depends on recent operating context

## Update rule
Update this file when:
- a major cutover happens
- current platform truth changes
- a major watchpoint appears or is resolved
- a room reset or live config change materially affects operations
