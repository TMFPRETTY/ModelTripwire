# OPENCLAW_ORG_BLUEPRINT.md

## Purpose
This document is the canonical operating blueprint for the Mac mini OpenClaw deployment. It defines the rooms, agents, responsibilities, boundaries, and operating rules so machine setup is execution rather than redesign.

## Deployment Goal
Run OpenClaw as a stable always-on operating layer for:
- command visibility
- inbox and ops handling
- Caruso growth and product support
- security and infrastructure monitoring
- later research, editorial, and knowledge workflows

Primary action surface: Discord.
Future visual surface: OpenClaw HQ dashboard.

## Core Principles
- Discord is the operational interface.
- The dashboard is the visibility and control layer, not the primary typing surface.
- Agents should summarize, draft, route, and escalate.
- External actions require explicit approval unless pre-authorized.
- First optimize reliability and clarity; sophistication comes second.
- Launch in waves. Avoid turning on every automation at once.

## Permanent Discord Channel Plan
- `command-center` — `1484651751108775946`
- `ops-desk` — `1484651772193673349`
- `support-inbox` — `1484651808772198462`
- `caruso-growth` — `1484651836966436934`
- `caruso-product` — `1484651869593669762`
- `security-infra` — `1484651900812001491`
- `research-lab` — `1484655635336265758`

## Existing/Related Channels Already Used
- gaming news channel — `1484556422384717985`
- support alerts channel — `1484558242381168670`
- Signal and Circuit mail monitor channel — `1484600889506533576`
- Caruso marketing channel — `1484611501842104510`

## Operating Rooms

### 1. Command Center
Purpose:
- daily executive summary
- system-wide visibility
- top alerts, blockers, priorities
- handoff point across agents

Inputs:
- summaries from all active rooms
- job failures
- approval requests
- urgent inbox/security/product/growth events

Outputs:
- morning digest
- notable event summaries
- launch/health snapshots
- cross-room escalation notices

Human expectation:
- read this first to understand what matters today

### 2. Ops Desk
Purpose:
- operations workflow management
- task routing and triage
- queue hygiene and follow-ups
- watchdog for automation health

Inputs:
- job statuses
- agent summaries
- failed runs
- recurring task outputs

Outputs:
- ops summaries
- action queues
- incident notes
- “needs approval” packets

### 3. Support Inbox
Purpose:
- triage inbound support mail
- summarize issues
- prepare draft responses
- classify urgency and owner

Inputs:
- Gmail / Workspace inboxes
- thread commands
- support mailbox integrations

Outputs:
- email summaries
- thread-per-message workflows
- recommended replies
- escalation flags

### 4. Growth Room
Purpose:
- marketing opportunities
- channel/reddit/community research
- content and campaign ideas
- competitor watch

Primary destination brand:
- `https://caruso-platform.com`

Outputs:
- opportunity scans
- reply packs
- weekly marketing packs
- draft content suggestions
- competitor movement notes

### 5. Product Lab
Purpose:
- product ideas
- customer signal synthesis
- feature recommendations
- product feedback clustering

Outputs:
- recommendation memos
- issue/theme summaries
- product backlog candidates
- positioning/feature insight notes

### 6. Security Office / Security & Infra
Purpose:
- host hardening
- system exposure review
- software/update posture
- OpenClaw runtime health monitoring

Outputs:
- security alerts
- drift reports
- hardening recommendations
- update advisories
- risk summaries

### 7. Research Lab
Purpose:
- weekly idea scans
- deep-dive memos
- idea scorecards and ranking
- new SaaS/business exploration

Outputs:
- ranked idea reports
- deep-dive research notes
- market maps
- recommendation briefs

### 8. Newsroom / Signal and Circuit Editorial Desk (later wave)
Purpose:
- monitor gaming/news signals
- decide what is worth covering
- route worthwhile stories to site personas
- accelerate article generation workflow

Outputs:
- story picks
- coverage recommendations
- editorial routing suggestions
- draft article support materials

## Agent Waves

### First-Wave Agents
- ops-desk
- caruso-growth
- caruso-product
- security-infra

### Second-Wave Agents
- research-lab
- qa-review (embedded first, separate later if needed)
- signal-and-circuit-editor

### Later Layers
- learning-loop
- knowledge-base
- strategy-director
- finance-ops

## Shared Agent Rules
All agents should:
- summarize before sprawling
- escalate exceptions, not every detail
- keep outputs structured and scannable
- avoid external side effects without approval
- post to the channel that best matches ownership
- route cross-functional items to command-center when broadly important

## Approval Boundary
Allowed without approval:
- research
- summaries
- categorization/tagging
- internal memos
- draft replies
- queue maintenance inside approved systems
- internal Discord reporting

Requires approval:
- sending email replies unless explicitly delegated
- public posting
- changing production automations materially
- deleting data
- spending money
- changing security posture in a risky way
- granting new permissions / integrating new external services

## Escalation Rules
Escalate to command-center when:
- an item affects multiple rooms
- a deadline/blocker impacts execution today
- there is a system failure or auth break
- human approval is needed
- a security issue is material
- a support message is urgent/high-risk

Escalate directly within the room when:
- issue is local and owned by that room
- no approval is needed
- no other team/room is affected

## Dashboard Relationship
Discord remains the action layer.
Dashboard becomes the visual operating system with:
- room status
- queue visibility
- approval board
- recent activity
- system health
- standups and handoffs

## Success Criteria For Initial Deployment
The Mac mini deployment is “good” when:
- OpenClaw runs stably on the Mac mini
- Discord routing works reliably
- first-wave agents post useful, consistent updates
- key automations can be paused/resumed cleanly
- failures are visible quickly
- approvals are explicit and easy to act on
- no critical workflow depends on fragile manual memory

## Near-Term Launch Sequence
1. Bring up platform and connectivity.
2. Restore/verify Discord and auth.
3. Enable command-center digest.
4. Enable ops-desk.
5. Enable support-inbox.
6. Enable one growth workflow.
7. Enable product and security workflows.
8. Observe for drift before expanding.

## Open Questions To Resolve During Prep
- Which automations should remain laptop-only vs move to Mini?
- Which inboxes are fully approved for draft-only vs send-capable workflows?
- Which jobs should announce to Discord vs only write dashboard state?
- What level of remote administration is acceptable for the Mini?
- What backup/recovery target is preferred for config, logs, and state?
- Which alerts should be quiet outside waking hours?
