# OPERATIONS_CHANGELOG.md

## Purpose
This file is the canonical short form log of meaningful operating changes across the non gaming system.

Use it for changes that other rooms may need to know about, including:
- infrastructure cutovers
- room ownership changes
- live job changes
- session resets
- repo path corrections
- delivery issues
- meaningful workflow or safeguard changes

Keep entries short, factual, and easy to skim.

## Entry format
### YYYY MM DD
- Change:
- Why it matters:
- Affected rooms:
- Source docs:

---

### 2026 03 24
- Change: Signal and Circuit repo local OpenClaw context was corrected to current machine paths and a repo local `MEMORY.md` was added.
- Why it matters: fixes a major source of bad path assumptions and startup read failures.
- Affected rooms: `signal-and-circuit`, `engineering`
- Source docs: repo local `OPENCLAW_CONTEXT.md`, repo local `MEMORY.md`

- Change: Caruso repo local OpenClaw context was corrected to current machine paths and a repo local `MEMORY.md` was added.
- Why it matters: reduces stale path assumptions and improves repo local continuity.
- Affected rooms: `caruso-product`, `caruso-growth`, `engineering`
- Source docs: repo local `OPENCLAW_CONTEXT.md`, repo local `MEMORY.md`

- Change: Signal and Circuit room session was reset to a fresh session id after compaction and typing stall issues.
- Why it matters: reduces inherited context fragility in the live room.
- Affected rooms: `signal-and-circuit`, `engineering`, `ops-desk`
- Source docs: `LIVE_CONFIG_AUDIT_2026-03-24.md`

- Change: Signal and Circuit cron job session key inconsistency was fixed from `agent:main:main` to `agent:codex:main`.
- Why it matters: removes one avoidable live config mismatch in the most fragile room.
- Affected rooms: `signal-and-circuit`, `ops-desk`
- Source docs: `LIVE_CONFIG_AUDIT_2026-03-24.md`, `JOB_OPERATING_GUIDE.md`

- Change: Non gaming operating docs were expanded with runbooks, room guides, safeguards, scorecards, job guide, creation checklist, and operating system index.
- Why it matters: gives the system a clearer shared operating model and stronger documentation backbone.
- Affected rooms: all major non gaming rooms
- Source docs: `AGENT_RUNBOOKS.md`, room guides, `AGENT_SAFEGUARDS.md`, `AGENT_SCORECARDS.md`, `JOB_OPERATING_GUIDE.md`, `NEW_AGENT_AND_JOB_CHECKLIST.md`, `OPERATING_SYSTEM_INDEX.md`

- Change: Command center experienced a transient non delivery on a scheduled digest, but a later manual rerun delivered successfully.
- Why it matters: command center delivery is functional, but should still be watched for recurrence.
- Affected rooms: `command-center`, `ops-desk`
- Source docs: `LIVE_CONFIG_AUDIT_2026-03-24.md`, `AGENT_SCORECARDS.md`

- Change: Mac mini cutover and related work from the prior day was not consistently visible in engineering room context.
- Why it matters: exposed a communication propagation gap between docs, room sessions, and cross room updates.
- Affected rooms: `engineering`, `command-center`, `ops-desk`, all impacted domain rooms
- Source docs: this changelog, `CURRENT_PLATFORM_STATE.md`, `CROSS_ROOM_HANDOFF_STANDARD.md`
