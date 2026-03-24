# OPERATING_SYSTEM_INDEX.md

## Purpose
This is the top level map of the non gaming agent operating system.

Use this file to answer:
- what documents define the system
- where to look for room ownership
- where to look for safeguards
- where to look for jobs and live audits
- where to update things when the system changes

This file is the navigation layer for the operating docs.

## Read This First If You Need...

### Room and agent overview
Start with:
- `AGENT_REGISTRY.md`

Use it for:
- what rooms and agents exist
- their status
- their mission
- current jobs
- key docs
- escalation relationships

### How each agent should behave
Start with:
- `AGENT_RUNBOOKS.md`

Use it for:
- mission
- owns and does not own
- inputs and outputs
- cadence
- approval boundaries
- escalation logic
- handoff rules
- fallback behavior

### How each room should behave
Start with the room guides:
- `COMMAND_CENTER_ROOM_GUIDE.md`
- `OPS_DESK_ROOM_GUIDE.md`
- `SUPPORT_INBOX_ROOM_GUIDE.md`
- `CARUSO_GROWTH_ROOM_GUIDE.md`
- `CARUSO_PRODUCT_ROOM_GUIDE.md`
- `SECURITY_INFRA_ROOM_GUIDE.md`
- `RESEARCH_LAB_ROOM_GUIDE.md`
- `SIGNAL_AND_CIRCUIT_ROOM_GUIDE.md`
- `ENGINEERING_ROOM_GUIDE.md`
- `QA_ROOM_GUIDE.md`

Use them for:
- what belongs in each room
- what does not belong there
- output style
- escalation logic
- relationship to other rooms
- practical room mode

### Cross room routing and workflow
Start with:
- `ROOMS_AND_WORKFLOW_SPEC.md`
- `ENGINEERING_WORKFLOW.md`

Use them for:
- ownership model
- cross room handoffs
- engineering routing
- QA expectations
- completion rules

### Safety and approval rules
Start with:
- `AGENT_SAFEGUARDS.md`

Use it for:
- baseline safety rules
- approval boundaries
- no guessing rules
- routing safeguards
- operational safeguards
- human trust safeguards

### Communication and change propagation
Start with:
- `OPERATIONS_CHANGELOG.md`
- `CURRENT_PLATFORM_STATE.md`
- `CROSS_ROOM_HANDOFF_STANDARD.md`
- `STANDUP_AND_SYNC_MODEL.md`
- `COMMUNICATION_RELIABILITY_PLAN.md`

Use them for:
- major change logging
- current shared truth
- cross room handoff rules
- standup and engineering sync structure
- communication failure prevention

### Creation gate for new rooms, agents, and jobs
Start with:
- `NEW_AGENT_AND_JOB_CHECKLIST.md`

Use it for:
- deciding if a new room or agent is ready
- deciding if a new recurring job is ready
- go live labels
- fast rejection rules
- first run watchpoints

### Live automation operating rules
Start with:
- `JOB_OPERATING_GUIDE.md`
- `JOB_CATALOG.md`

Use them for:
- what recurring jobs exist
- what each job is supposed to do
- what good output looks like
- failure modes
- schedules and destinations
- planning versus live operation

### Live system reality check
Start with:
- `LIVE_CONFIG_AUDIT_2026-03-24.md`
- `AGENT_SCORECARDS.md`

Use them for:
- whether the live setup matches the docs
- which rooms are healthy or under watch
- known mismatches
- current risk areas

---

## Recommended Reading Order For A New Operator
1. `AGENT_REGISTRY.md`
2. `ROOMS_AND_WORKFLOW_SPEC.md`
3. `AGENT_SAFEGUARDS.md`
4. `AGENT_RUNBOOKS.md`
5. relevant room guide
6. `JOB_OPERATING_GUIDE.md`
7. `LIVE_CONFIG_AUDIT_2026-03-24.md`
8. `AGENT_SCORECARDS.md`

## Recommended Update Rules

### If a new room or agent is added
Update:
- `NEW_AGENT_AND_JOB_CHECKLIST.md` if the standard changes
- `AGENT_REGISTRY.md`
- `AGENT_RUNBOOKS.md`
- the relevant room guide
- `ROOMS_AND_WORKFLOW_SPEC.md` if routing changes
- `AGENT_SAFEGUARDS.md` if the baseline safety model changes
- `OPERATING_SYSTEM_INDEX.md` if the doc map changes

### If a recurring job is added or changed
Update:
- `NEW_AGENT_AND_JOB_CHECKLIST.md` if the gate changes
- `JOB_CATALOG.md`
- `JOB_OPERATING_GUIDE.md`
- `LIVE_CONFIG_AUDIT_2026-03-24.md` when auditing live behavior
- `AGENT_SCORECARDS.md` if room health changes

### If a room starts drifting or failing
Check:
- `AGENT_SCORECARDS.md`
- `LIVE_CONFIG_AUDIT_2026-03-24.md`
- the relevant room guide
- the relevant runbook
- `AGENT_SAFEGUARDS.md`

Then decide whether to:
- tune
- pause
- reset
- reroute
- escalate

---

## Current Core Document Set
- `AGENT_REGISTRY.md`
- `AGENT_RUNBOOKS.md`
- `ROOMS_AND_WORKFLOW_SPEC.md`
- `AGENT_SAFEGUARDS.md`
- `NEW_AGENT_AND_JOB_CHECKLIST.md`
- `JOB_CATALOG.md`
- `JOB_OPERATING_GUIDE.md`
- `LIVE_CONFIG_AUDIT_2026-03-24.md`
- `AGENT_SCORECARDS.md`
- room guide documents
- engineering and QA specific guides

## Bottom line
This operating system should be understandable without relying on memory or tribal knowledge.

If a smart operator cannot find the rule, owner, safeguard, or workflow path in these docs, the system is still too implicit.
