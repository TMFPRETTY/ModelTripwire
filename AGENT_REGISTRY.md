# AGENT_REGISTRY.md

## Purpose
This file is the canonical registry of the non-gaming-side OpenClaw agents/rooms currently defined for the laptop-era live system and the upcoming Mac mini deployment.

It should answer, quickly and explicitly:
- which rooms/agents exist
- what status they are in
- what they own
- what jobs support them
- what skills/docs define them
- where the approval boundaries sit

## Status Labels
- `active`
- `staged`
- `embedded`
- `transitional`
- `planned`
- `retired`

## Active Core Operating Agents

### 1. command-center
- **Status:** active
- **Room:** `command-center` (`1484651751108775946`)
- **Mission:** provide top-level mission control, priorities, blockers, approvals, and daily focus
- **Current jobs:**
  - `morning-command-center-digest-weekdays-830am`
- **Primary skill(s):** `command-center-digest`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`, `COMMAND_CENTER_ROOM_GUIDE.md`
- **Approval boundary:** summarizes and escalates; does not create external side effects
- **Escalates to:** all room owners as needed; especially `ops-desk`, `engineering`, `security-infra`
- **Notes:** should stay high-signal, cross-room, and decision-oriented

### 2. ops-desk
- **Status:** active
- **Room:** `ops-desk` (`1484651772193673349`)
- **Mission:** coordinate operations, failures, drift, queues, and next actions
- **Current jobs:**
  - `ops-desk-midday-status-weekdays-1pm`
- **Primary skill(s):** `ops-desk`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`
- **Approval boundary:** reports and coordinates; risky operational changes still require approval
- **Escalates to:** `command-center`, `engineering`, `security-infra`
- **Notes:** acts as the system’s operational coordinator and cleanup layer

### 3. support-inbox
- **Status:** active
- **Room:** `support-inbox` (`1484651808772198462`)
- **Mission:** triage support mail, summarize issues, classify urgency, and prepare safe responses
- **Current jobs:**
  - no placeholder cron by design; driven by actual support workflow
- **Primary skill(s):** `support-triage`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`
- **Approval boundary:** risky replies and sensitive support situations require approval
- **Escalates to:** `caruso-product`, `engineering`, `ops-desk`, `security-infra`, `command-center`
- **Notes:** should route, not overcommit; support handling must remain safer than it is clever

### 4. caruso-growth
- **Status:** active
- **Room:** `caruso-growth` (`1484651836966436934`)
- **Mission:** find, package, and route growth opportunities for Caruso
- **Current jobs:**
  - `caruso-marketing-opportunity-scan-daily-1115am`
  - `caruso-weekly-marketing-pack-mondays-9am`
  - `caruso-daily-reply-pack-weekdays-930am`
  - `caruso-reddit-draft-queue-weekdays-10am`
  - `caruso-competitor-watch-daily-530pm`
- **Primary skill(s):** `caruso-growth`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`
- **Approval boundary:** research/draft internally without approval; public posting still needs approval
- **Escalates to:** `caruso-product`, `engineering`, `command-center`
- **Notes:** canonical destination site is `https://caruso-platform.com`

### 5. caruso-product
- **Status:** active
- **Room:** `caruso-product` (`1484651869593669762`)
- **Mission:** convert support/growth/research/market signals into product recommendations
- **Current jobs:**
  - `caruso-product-signal-digest-weekdays-1230pm`
- **Primary skill(s):** `caruso-product`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`
- **Approval boundary:** recommendations are internal by default; external commitments require approval
- **Escalates to:** `engineering`, `caruso-growth`, `command-center`
- **Notes:** should prioritize evidence over anecdote and recommendation quality over volume

### 6. security-infra
- **Status:** active
- **Room:** `security-infra` (`1484651900812001491`)
- **Mission:** monitor host/runtime health, security posture, and infrastructure drift
- **Current jobs:**
  - `security-infra-daily-healthcheck-weekdays-845am`
- **Primary skill(s):** `security-infra`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`
- **Approval boundary:** can inspect and recommend freely; impactful system/security changes require approval
- **Escalates to:** `ops-desk`, `command-center`, `engineering`
- **Notes:** especially important before and after Mac mini cutover

### 7. research-lab
- **Status:** active
- **Room:** `research-lab` (`1484655635336265758`)
- **Mission:** discover and rank business/SaaS/product opportunities worth deeper attention
- **Current jobs:**
  - `research-lab-weekly-idea-scan-mondays-11am`
- **Primary skill(s):** `research-lab`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`, `RESEARCH_LAB_ROOM_GUIDE.md`
- **Approval boundary:** research and ranking only; no external actions
- **Escalates to:** `caruso-growth`, `caruso-product`, `command-center`
- **Notes:** should stay selective rather than becoming an idea dump

### 8. signal-and-circuit
- **Status:** active
- **Room:** `signal-and-circuit` (`1484556120025727127`)
- **Mission:** combined operating room for editorial lookout, inbox activity, article routing, AdSense/site-quality work, and traffic growth
- **Current jobs:**
  - room-driven conversational support
  - related automated support may exist outside room-local cron (mail watcher / content workflows)
- **Primary skill(s):** `signal-and-circuit-adsense`, `signal-and-circuit-growth`
- **Key docs:** `AGENT_RUNBOOKS.md`, `ROOMS_AND_WORKFLOW_SPEC.md`, `SIGNAL_AND_CIRCUIT_ROOM_DECISION.md`, `SIGNAL_AND_CIRCUIT_ADSENSE_PLAN.md`
- **Approval boundary:** drafts and internal recommendations are fine; publishing and risky outward actions should remain controlled
- **Escalates to:** `engineering`, `qa-review`, `ops-desk`, `command-center`
- **Notes:** intentionally kept as one strong room for now rather than split too early, but operated with explicit internal lanes

### 9. engineering
- **Status:** active
- **Room:** `engineering` (`1484988049229086850`)
- **Mission:** shared implementation lane for code, debugging, automation changes, integrations, and code QA coordination
- **Current jobs:**
  - `engineering-midday-intake-status-weekdays-2pm`
  - `engineering-qa-review-check-weekdays-215pm`
- **Primary skill(s):** `qa-review` (for review), engineering room/workflow docs, shared repo anchors
- **Key docs:** `AGENT_RUNBOOKS.md`, `ENGINEERING_ROOM_GUIDE.md`, `ENGINEERING_WORKFLOW.md`, `ROOMS_AND_WORKFLOW_SPEC.md`
- **Approval boundary:** code/config work may proceed within safe bounds; destructive or high-risk changes require approval
- **Escalates to:** `qa-review`, `ops-desk`, `security-infra`, `command-center`
- **Notes:** repo anchors:
  - Caruso → `/Users/tmfprettybot/Documents/PM and QA/PM-and-QA-Combo-Fun`
  - Signal and Circuit → `/Users/tmfprettybot/Documents/AI:ML/signal-and-circuit`
  - OpenClaw/platform → `/Users/tmfprettybot/.openclaw/workspace-main`

## Embedded / Cross-Cutting Agent

### 10. qa-review
- **Status:** embedded
- **Room:** embedded in owning room; especially `engineering`
- **Mission:** review outputs, code, automations, prompts, and configs for quality, correctness, and risk
- **Current jobs:**
  - indirectly represented by `engineering-qa-review-check-weekdays-215pm`
- **Primary skill(s):** `qa-review`
- **Key docs:** `AGENT_RUNBOOKS.md`, `QA_ROOM_GUIDE.md`, `ROOMS_AND_WORKFLOW_SPEC.md`
- **Approval boundary:** can block/rework/recommend but not override human approvals
- **Escalates to:** `engineering`, originating room, `command-center` when impact is broad
- **Notes:** covers both content QA and code QA where engineering impact exists

## Planned / Later Agents

### 11. signal-and-circuit-editor
- **Status:** planned
- **Room:** expected to operate inside `signal-and-circuit` for now
- **Mission:** newsroom/editorial lookout for breaking or interesting coverage opportunities, with routing to the right site persona
- **Current jobs:**
  - not yet activated as a dedicated recurring job
- **Primary skill(s):** future newsroom/editorial skill set; current related support from Signal and Circuit docs/skills
- **Approval boundary:** should alert and route rather than publish blindly
- **Escalates to:** `signal-and-circuit`, `command-center`, `engineering` when systems work is needed
- **Notes:** should use worth-covering / worth-watching / ignore thresholds

### 12. learning-loop
- **Status:** planned
- **Room:** not yet assigned
- **Mission:** capture lessons, tune workflows, and improve the system based on outcomes
- **Current jobs:** none
- **Primary skill(s):** not yet defined
- **Approval boundary:** internal analysis only until defined
- **Notes:** should become the discipline layer for postmortems and workflow tuning

### 13. knowledge-base
- **Status:** planned
- **Room:** not yet assigned
- **Mission:** curate durable operational knowledge and reusable context across rooms
- **Current jobs:** none
- **Primary skill(s):** not yet defined
- **Approval boundary:** internal documentation/knowledge work only until defined
- **Notes:** should eventually become the durable memory/ops reference layer

## Retired Agent/Workflow

### gaming-trends
- **Status:** retired
- **Room:** none
- **Mission:** former gaming news experiment
- **Current jobs:** disabled/retired
- **Notes:** do not migrate to the Mac mini

## Current Operating Summary
The active non-gaming-side system now has explicit room-backed agents for:
- command-center
- ops-desk
- support-inbox
- caruso-growth
- caruso-product
- security-infra
- research-lab
- signal-and-circuit
- engineering
- embedded qa-review

Planned-but-not-fully-separate functions remain for:
- signal-and-circuit-editor
- learning-loop
- knowledge-base

This is the canonical non-gaming operating model for the current live environment and the Mac mini-era system shape.

Related operating docs:
- `AGENT_SAFEGUARDS.md`
- `JOB_OPERATING_GUIDE.md`
- `LIVE_CONFIG_AUDIT_2026-03-24.md`
- `AGENT_SCORECARDS.md`
hape.
