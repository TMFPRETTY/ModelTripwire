# AGENT_REGISTRY.md

## Purpose
This file is the canonical registry of the OpenClaw agents/rooms currently defined for the laptop-era live system and the upcoming Mac mini deployment.

## Status Labels
- `active`
- `staged`
- `embedded`
- `transitional`
- `planned`
- `retired`

## First-Wave Active Agents

### 1. command-center
- **Status:** active
- **Room:** `command-center` (`1484651751108775946`)
- **Mission:** provide top-level mission control, priorities, blockers, approvals, and daily focus
- **Current jobs:**
  - `morning-command-center-digest-weekdays-830am`
- **Primary skill(s):** `command-center-digest`
- **Approval boundary:** summarizes and escalates; does not create external side effects
- **Notes:** should stay high-signal and avoid room-local noise

### 2. ops-desk
- **Status:** active
- **Room:** `ops-desk` (`1484651772193673349`)
- **Mission:** coordinate operations, failures, drift, queues, and next actions
- **Current jobs:**
  - `ops-desk-midday-status-weekdays-1pm`
- **Primary skill(s):** `ops-desk`
- **Approval boundary:** reports and coordinates; risky operational changes still require approval
- **Notes:** acts as the system’s operational coordinator

### 3. caruso-growth
- **Status:** active
- **Room:** `caruso-growth` (`1484651836966436934`)
- **Mission:** find, package, and route growth opportunities for Caruso
- **Current jobs:**
  - `caruso-marketing-opportunity-scan-every-4h`
  - `caruso-weekly-marketing-pack-mondays-9am`
  - `caruso-daily-reply-pack-weekdays-930am`
  - `caruso-reddit-draft-queue-weekdays-10am`
  - `caruso-competitor-watch-every-6h`
- **Primary skill(s):** `caruso-growth`
- **Approval boundary:** research/draft internally without approval; public posting still needs approval
- **Notes:** canonical destination site is `https://caruso-platform.com`

### 4. caruso-product
- **Status:** active
- **Room:** `caruso-product` (`1484651869593669762`)
- **Mission:** convert support/growth/research/market signals into product recommendations
- **Current jobs:**
  - `caruso-product-signal-digest-weekdays-1230pm`
- **Primary skill(s):** `caruso-product`
- **Approval boundary:** recommendations are internal by default; external commitments require approval
- **Notes:** should prioritize evidence over anecdote

### 5. security-infra
- **Status:** active
- **Room:** `security-infra` (`1484651900812001491`)
- **Mission:** monitor host/runtime health, security posture, and infrastructure drift
- **Current jobs:**
  - `security-infra-daily-healthcheck-weekdays-845am`
- **Primary skill(s):** `security-infra`
- **Approval boundary:** can inspect and recommend freely; impactful system/security changes require approval
- **Notes:** especially important before and after Mac mini cutover

### 6. research-lab
- **Status:** active
- **Room:** `research-lab` (`1484655635336265758`)
- **Mission:** discover and rank business/SaaS/product opportunities worth deeper attention
- **Current jobs:**
  - `research-lab-weekly-idea-scan-mondays-11am`
- **Primary skill(s):** `research-lab`
- **Approval boundary:** research and ranking only; no external actions
- **Notes:** should stay selective rather than becoming an idea dump

### 7. engineering
- **Status:** active
- **Room:** `engineering` (`1484988049229086850`)
- **Mission:** shared implementation lane for code, debugging, automation changes, integrations, and code QA coordination
- **Current jobs:**
  - `engineering-midday-intake-status-weekdays-2pm`
  - `engineering-qa-review-check-weekdays-215pm`
- **Primary skill(s):** `qa-review` (for review), engineering room/workflow docs, shared repo anchors
- **Approval boundary:** code/config work may proceed within safe bounds; destructive or high-risk changes require approval
- **Notes:** repo anchors:
  - Caruso → `/Users/jeremypretty/Documents/PM and QA/PM-and-QA-Combo-Fun`
  - Signal and Circuit → `/Users/jeremypretty/Documents/AI:ML/signal-and-circuit`
  - OpenClaw/platform → `/Users/jeremypretty/.openclaw/workspace`

## Embedded / Cross-Cutting Agents

### 8. qa-review
- **Status:** embedded
- **Room:** embedded in owning room; especially `engineering`
- **Mission:** review outputs, code, automations, prompts, and configs for quality, correctness, and risk
- **Current jobs:**
  - indirectly represented by `engineering-qa-review-check-weekdays-215pm`
- **Primary skill(s):** `qa-review`
- **Approval boundary:** can block/rework/recommend but not override human approvals
- **Notes:** covers both content QA and code QA

## Transitional / Special-Case Agents

### 9. support-inbox
- **Status:** transitional
- **Room:** `support-inbox` (`1484651808772198462`)
- **Mission:** triage support mail, summarize issues, and prepare safe responses
- **Current jobs:**
  - no placeholder cron by design
- **Primary skill(s):** `support-triage`
- **Approval boundary:** risky replies and sensitive support situations require approval
- **Notes:** depends on the real support mailbox workflow rather than fake room filler

### 10. signal-and-circuit
- **Status:** transitional
- **Room:** current active channel `1484600889506533576`
- **Mission:** combined operating room for editorial lookout, inbox activity, article routing, AdSense/site-quality work, and traffic growth
- **Current jobs:**
  - `signalandcircuit-mail-monitor-every-2m`
- **Primary skill(s):** `signal-and-circuit-adsense`, `signal-and-circuit-growth`
- **Approval boundary:** drafts and internal recommendations are fine; publishing and risky outward actions should remain controlled
- **Notes:** intentionally kept as one strong room for now rather than split too early

## Planned / Later Agents

### 11. signal-and-circuit-editor
- **Status:** planned
- **Room:** expected to operate inside `signal-and-circuit` for now
- **Mission:** newsroom/editorial lookout for breaking or interesting coverage opportunities, with routing to the right site persona
- **Current jobs:**
  - not yet activated as a dedicated recurring job
- **Primary skill(s):** future newsroom/editorial skill set; current related support from Signal and Circuit docs/skills
- **Approval boundary:** should alert and route rather than publish blindly
- **Notes:** should use worth-covering / worth-watching / ignore thresholds

### 12. learning-loop
- **Status:** planned
- **Room:** not yet assigned
- **Mission:** capture lessons, tune workflows, and improve the system based on outcomes
- **Current jobs:** none
- **Primary skill(s):** not yet defined
- **Approval boundary:** internal analysis only until defined

### 13. knowledge-base
- **Status:** planned
- **Room:** not yet assigned
- **Mission:** curate durable operational knowledge and reusable context across rooms
- **Current jobs:** none
- **Primary skill(s):** not yet defined
- **Approval boundary:** internal documentation/knowledge work only until defined

## Retired Agent/Workflow

### gaming-trends
- **Status:** retired
- **Room:** none
- **Mission:** former gaming news experiment
- **Current jobs:** disabled/retired
- **Notes:** do not migrate to the Mac mini

## Current Operating Summary
The active laptop system now has real room-backed agents for:
- command-center
- ops-desk
- caruso-growth
- caruso-product
- security-infra
- research-lab
- engineering
- embedded qa-review

Transitional rooms remain for:
- support-inbox
- signal-and-circuit

This is the live proving-ground version of the future Mac mini operating model.
