# ROOMS_AND_WORKFLOW_SPEC.md

## Purpose
This is the canonical operating spec for room ownership, agent roles, and the engineering -> QA workflow.

## Room Ownership

### command-center
- Channel role: executive overview, priorities, blockers, cross-room visibility
- Owning agent: `command-center`

### ops-desk
- Channel role: operations coordination, queue health, failures, follow-ups, workflow visibility
- Owning agent: `ops-desk`

### support-inbox
- Channel role: support triage, reply drafting, escalation
- Owning agent: `support-inbox`

### caruso-growth
- Channel role: growth opportunities, campaigns, community/reddit drafts, distribution ideas
- Owning agent: `caruso-growth`

### caruso-product
- Channel role: product synthesis, recommendations, packaging/roadmap signals
- Owning agent: `caruso-product`

### security-infra
- Channel role: infra health, runtime posture, auth/update/risk monitoring
- Owning agent: `security-infra`

### research-lab
- Channel role: opportunity discovery, research scans, market analysis
- Owning agent: `research-lab`

### signal-and-circuit
- Channel role: newsroom/editorial/system needs for Signal and Circuit
- Owning agent: `signal-and-circuit`

### engineering
- Channel role: implementation lane for code, debugging, config, automation, integrations, and QA coordination
- Owning agent: `engineering`

### qa-review
- Workflow role: review authority for engineering-impact work
- Owning agent: `qa-review`
- Note: QA may operate as an embedded lane within engineering, but the role is distinct and should be treated as a separate review function.

## Core Routing Principle
- Business/functional rooms define needs in their domain.
- Engineering owns implementation once the work becomes code/config/script/integration work.
- QA owns validation before engineering-impact work is considered truly done.
- Final results return to the owning room, command-center, or the requesting context as appropriate.

## Cross-Room Handoff Rules

### Signal and Circuit -> Engineering
Use when a request requires:
- code changes
- site fixes
- automation work
- tooling/debugging
- integration work

### Caruso Product / Growth -> Engineering
Use when a request requires:
- implementation
- workflow/tooling changes
- automation
- scripts/config work
- instrumentation or landing-page/build changes

### Ops / Security -> Engineering
Use when an issue requires:
- code/config changes
- runtime fixes
- engineering-impact automation repair

### Engineering -> QA
Use when the work includes:
- code changes
- config changes
- automation logic
- integrations
- state handling
- risky prompt/workflow changes
- anything likely to create duplicate posting, silent failure, auth breakage, or operational risk

## Engineering Operating Model
Engineering should be a live working room.

That means:
- it should respond to direct messages in-channel
- it can be told to inspect other rooms for context
- it can gather requirements from other channels before implementing
- implementation status should still be tracked back in engineering
- coding work should not be declared complete without QA/approval/intentional stop

## QA Operating Model
QA is not optional ceremony.
QA is the gate between “implemented” and “done.”

### QA verdicts
- `PASS`
- `PASS_WITH_EDITS`
- `TEST_BEFORE_USE`
- `NEEDS_APPROVAL`
- `REWORK`
- `BLOCK`

## Required Workflow

### Default loop
Engineering -> QA -> Engineering (if needed) -> QA -> Done/Approval

### Completion rule
A task is complete only when one of these is true:
- QA passed it
- explicit human approval was given
- the work was intentionally stopped

## State Labels
Use these labels when useful:
- `INTAKE`
- `PLANNING`
- `IN_PROGRESS`
- `NEEDS_QA`
- `REWORK`
- `TESTING`
- `NEEDS_APPROVAL`
- `BLOCKED`
- `DONE`

## Memory / Continuity Rule
When the operating model changes in a meaningful way, update:
- this file for the canonical spec
- daily memory notes for what changed
- long-term memory summaries when the pattern is durable

## Current Intent
This workspace should operate as:
- a set of domain rooms with clear owners
- a live engineering room that can intake and act conversationally
- a QA-gated implementation flow
- a system where other rooms can hand work into engineering, and engineering can inspect those rooms for context before acting
