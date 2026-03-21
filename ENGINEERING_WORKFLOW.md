# ENGINEERING_WORKFLOW.md

## Purpose
This file defines how engineering and QA should operate across the OpenClaw system.

## Scope
Applies to:
- Caruso code and automation work
- Signal and Circuit site/editorial-system work
- OpenClaw automation and integration work
- infrastructure-adjacent implementation work

## Workflow Stages

### 1. Intake
Capture:
- system
- request
- reason
- constraints
- done criteria
- urgency

### 2. Triage
Decide:
- is this coding work, config work, automation work, or just a business question?
- does it belong in engineering at all?
- is it risky enough to need approval before changes are made?

### 3. Planning
For meaningful work, produce:
- short implementation plan
- likely files/systems touched
- obvious risks
- testing/review need

### 4. Execution
Do the implementation work.
Keep changes scoped to the actual request.
Avoid mixing unrelated cleanup into the same task unless it is clearly beneficial and low risk.

### 5. QA Review
Use QA review especially for:
- automation logic changes
- integrations
- state handling
- config changes
- user-visible output changes
- code that can create noisy loops, duplicate posting, or data risk

### 6. Handoff
Return one of:
- complete
- complete but test before use
- needs approval
- blocked
- needs revision

## QA Checklist In Engineering
Review for:
- correctness
- blast radius
- missing edge cases
- auth/secret/config handling
- duplicate-posting or retry-loop risk
- maintainability
- whether testing is needed

## Approval Boundary
Needs approval when work would:
- change public-facing behavior materially
- risk live workflows or data
- alter important security or remote-access posture
- send external communications automatically
- make deletions or destructive changes

## Room Cadence
Use the room for:
- new implementation intake
- active work tracking
- QA handoffs
- blocked-work visibility

Add light recurring summaries, but do not flood the room with meaningless status churn.
