# CHANNEL_ARCHITECTURE_PLAN.md

## Purpose
This document defines the Discord room/channel structure for the OpenClaw Mac mini era so jobs, agents, approvals, and discussions land in the right places.

## Operating Principle
Get the rooms right before adding more active agents.

Discord is the main action surface. Each channel should have a clear ownership boundary and a clear reason to exist. Avoid overlap, duplicate reporting, and “misc dump” rooms.

## Channel Design Rules
- One room = one main operational purpose.
- Command-center is for top-level visibility, not every event.
- Room-local details should stay in the room that owns them.
- Approvals should be obvious and easy to act on.
- QA stays embedded at first unless review volume proves it needs its own visible room.
- Retire experiment channels instead of letting them linger.

## Planned Permanent Rooms

### 1. command-center
**Channel ID:** `1484651751108775946`

**Purpose:**
- top-level daily visibility
- executive summary
- cross-room blockers
- priorities and watchlist
- high-value handoff point

**Should receive:**
- morning digest
- major blockers
- major approvals waiting
- meaningful cross-room alerts
- major system health issues

**Should not receive:**
- routine room-local chatter
- every successful run
- raw draft content

---

### 2. ops-desk
**Channel ID:** `1484651772193673349`

**Purpose:**
- operational coordination
- queue/watchdog activity
- failures, drift, stale work
- migration/cutover tracking

**Should receive:**
- repeated job failures
- queue backlog notes
- stale follow-ups
- infra/auth blockers that affect workflows
- status about what is active, paused, or retired

**Should not receive:**
- every marketing/content idea
- every support email by default
- raw research dumps

---

### 3. support-inbox
**Channel ID:** `1484651808772198462`

**Purpose:**
- support mailbox triage
- summaries of inbound issues
- draft replies
- escalation of risky support situations

**Should receive:**
- new support summaries
- thread-per-issue workflows
- urgency classification
- recommended replies
- approval-needed flags for sensitive replies

**Should not receive:**
- non-support operational chatter
- product memo writing unless tied to support signal

---

### 4. caruso-growth
**Channel ID:** `1484651836966436934`

**Purpose:**
- Caruso marketing, distribution, and community opportunity work

**Should receive:**
- marketing opportunity scans
- reply packs
- Reddit draft queues
- competitor watch updates
- campaign/content suggestions
- growth-related approvals

**Should not receive:**
- product backlog memos
- security alerts
- unrelated inbox traffic

---

### 5. caruso-product
**Channel ID:** `1484651869593669762`

**Purpose:**
- product signal synthesis and recommendation work

**Should receive:**
- product recommendation memos
- feature/theme clustering
- support/growth/research themes that imply product action
- backlog candidates and prioritization notes

**Should not receive:**
- generic growth chatter
- room-local support operations unless they point to product insight

---

### 6. security-infra
**Channel ID:** `1484651900812001491`

**Purpose:**
- host/runtime/security monitoring
- hardening, drift, remote access, and update posture

**Should receive:**
- security summaries
- infrastructure alerts
- runtime health changes
- update/hardening recommendations
- cutover hardening checklist progress

**Should not receive:**
- routine editorial or growth content
- non-security room chatter

---

### 7. research-lab
**Channel ID:** `1484655635336265758`

**Purpose:**
- idea scans
- deep-dive opportunity research
- scorecards and market maps

**Should receive:**
- weekly idea scans
- ranked opportunity lists
- deep-dive research memos
- exploratory business/product opportunities

**Should not receive:**
- day-to-day ops chatter
- routine support traffic

### 8. engineering
**Channel ID:** `1484988049229086850`

**Purpose:**
- shared implementation lane for code work across Caruso, Signal and Circuit, OpenClaw automations, and platform/integration changes
- engineering requests, debugging, implementation planning, and code QA coordination

**Should receive:**
- coding requests
- bugfix/debugging work
- implementation plans
- code review / QA notes
- automation or integration change discussions
- thread-based work for Caruso, Signal and Circuit, platform/OpenClaw, and infra/automation

**Should not receive:**
- general product strategy without implementation work
- generic growth content
- routine room-local chatter with no engineering action

## Embedded / Cross-Cutting Functions

### QA Review
**Initial form:** embedded, not its own room

**How it works:**
- reviews outputs inside the owning room
- reviews code/config changes in context
- uses verdicts like PASS / PASS_WITH_EDITS / TEST_BEFORE_USE / NEEDS_APPROVAL / REWORK / BLOCK

**Escalate to visible room later only if:**
- review volume becomes high
- approval/review state becomes hard to track
- dashboard later needs a dedicated QA lane

### Command approvals
**Initial form:** embedded in owning room, surfaced to command-center when high-value or blocking

## Signal and Circuit Room Recommendation
Signal and Circuit currently has active mail monitoring in Discord channel `1484600889506533576`.

Recommended direction:
- keep the current operational/editorial Discord area active for now
- later decide whether Signal and Circuit gets one dedicated newsroom room or a split between:
  - editorial/newsroom
  - adsense/growth/monetization

For now, the most important thing is to avoid mixing Signal and Circuit editorial work into Caruso rooms.

## Legacy / Existing Channels

### support alerts channel
**Channel ID:** `1484558242381168670`
Current status:
- legacy support workflow destination
- keep temporarily if needed until support-inbox cutover is complete

### Signal and Circuit mail monitor channel
**Channel ID:** `1484600889506533576`
Current status:
- active
- keep during transition
- later decide whether it becomes the permanent newsroom/support/editorial room for that site

### Caruso marketing channel
**Channel ID:** `1484611501842104510`
Current status:
- active legacy destination for Caruso workflows
- likely temporary until routing moves to `caruso-growth`

## Retired / Do Not Use
- gaming news channel — `1484556422384717985`
- do not migrate or revive

## Migration Map

### Move these to `command-center`
- morning command-center digest

### Move these to `ops-desk`
- future failure watches
- cutover status summaries
- “what is active/paused/broken” summaries

### Move these to `support-inbox`
- support mailbox triage workflows currently using legacy support alert destinations

### Move these to `caruso-growth`
- caruso marketing opportunity scan
- caruso weekly marketing pack
- caruso daily reply pack
- caruso Reddit draft queue
- caruso competitor watch

### Keep temporarily where they are until dedicated decision
- Signal and Circuit mail monitor / editorial flow

## Immediate Setup Priorities
1. confirm the permanent channels exist and are the intended rooms
2. map each currently active job to its future room
3. identify which legacy channels remain transitional only
4. prevent retired experiments from coming along
5. move jobs in a controlled order during cutover

## Definition of Good Channel Architecture
A good setup makes it obvious:
- where a given workflow belongs
- where to look for a specific type of work
- what is urgent vs local
- where approvals should happen
- what rooms are temporary versus permanent
