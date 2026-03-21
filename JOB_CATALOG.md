# JOB_CATALOG.md

## Purpose
This file is the pre-deployment catalog of automations/jobs for the Mac mini setup. It is the planning layer for what should run, where it should post, and how it should behave before jobs are re-enabled.

## Status Key
- `planned`
- `paused`
- `active`
- `retire`

## Existing Known Jobs

### 1. Gaming Trends / Video Game News Every 2h
- **Job ID:** `406a1c83-015a-4a0f-bad7-48dbae10dd8a`
- **Status:** paused pending Mac mini cutover
- **Purpose:** post major video game news every 2 hours
- **Destination:** Discord channel `1484556422384717985`
- **Schedule:** every 2 hours
- **Output:** major gaming news summary
- **Validation needed:** source quality, posting quality, duplicate prevention, relevance threshold

### 2. Signal and Circuit Mail Monitor Every 2m
- **Job ID:** `4cfe0675-b283-433d-bcaf-432a08706980`
- **Status:** paused pending Mac mini cutover
- **Purpose:** poll inboxes and post new email summaries with per-email thread workflow
- **Destination:** Discord channel `1484600889506533576`
- **Schedule:** every 2 minutes
- **Script:** `scripts/signalandcircuit_mail_monitor.py`
- **State Path:** `.openclaw/signalandcircuit-mail-monitor-state.json`
- **Output:** email summary, thread creation, reply handling
- **Validation needed:** auth, duplicate prevention, thread behavior, send/reply/ignore command handling

### 3. Caruso Marketing Opportunity Scan
- **Job ID:** `ee105b50-2e8e-463b-b9a4-bcc165a21a3d`
- **Status:** paused pending Mac mini cutover
- **Purpose:** find marketing opportunities
- **Destination:** likely `caruso-growth`
- **Schedule:** verify before re-enable
- **Output:** opportunity scan summary
- **Validation needed:** cadence, signal quality, channel fit, actionability

### 4. Caruso Weekly Marketing Pack
- **Job ID:** `4f2aa9d6-9d73-4e08-a4fc-9d4699ca4bf7`
- **Status:** paused pending Mac mini cutover
- **Purpose:** deliver weekly marketing package
- **Destination:** likely `caruso-growth`
- **Schedule:** weekly
- **Output:** consolidated marketing pack
- **Validation needed:** format, sections, usefulness, timing

### 5. Caruso Daily Reply Pack
- **Job ID:** `d0fc4e18-d944-4a49-abc6-a1e1d8062385`
- **Status:** paused pending Mac mini cutover
- **Purpose:** prepare reply ideas and ready-to-use drafts
- **Destination:** likely `caruso-growth`
- **Schedule:** daily
- **Output:** draft replies / engagement suggestions
- **Validation needed:** voice, quality, approval boundary

### 6. Caruso Reddit Draft Queue
- **Job ID:** `b2f55e26-0c55-4c54-98c0-1309889162ef`
- **Status:** paused pending Mac mini cutover
- **Purpose:** queue Reddit-focused draft opportunities
- **Destination:** likely `caruso-growth`
- **Schedule:** verify before re-enable
- **Output:** draft queue items
- **Validation needed:** subreddit fit, spam avoidance, approval process

### 7. Caruso Competitor Watch
- **Job ID:** `e5d420bd-4ac4-4716-a5ff-cf3c69bb381c`
- **Status:** paused pending Mac mini cutover
- **Purpose:** monitor competitor movement
- **Destination:** likely `caruso-growth`, maybe command-center for major items
- **Schedule:** verify before re-enable
- **Output:** competitor summary / notable movement alert
- **Validation needed:** noise threshold, alert routing, importance scoring

### 8. Morning Command-Center Digest
- **Job ID:** `148c5073-5be0-40cc-8cbc-79f062a18191`
- **Status:** paused pending Mac mini cutover
- **Purpose:** morning high-level digest
- **Destination:** `command-center`
- **Schedule:** morning
- **Output:** top priorities, blockers, recommendations, watchlist
- **Validation needed:** timing, scannability, usefulness, cross-room synthesis

## Candidate Mac Mini First-Wave Jobs

### A. Command-Center Morning Digest
- **Status:** planned first-wave
- **Destination:** `command-center`
- **Purpose:** establish a daily operating rhythm
- **Suggested output template:**
  - top priorities
  - blockers
  - overnight changes
  - approvals waiting
  - recommended focus today

### B. Ops Desk Health / Failure Watch
- **Status:** planned first-wave
- **Destination:** `ops-desk`
- **Purpose:** consolidate system/job health and failures
- **Suggested output template:**
  - jobs failed
  - jobs drifting/noisy
  - queues backing up
  - recommended operator action

### C. Support Inbox Triage
- **Status:** planned first-wave
- **Destination:** `support-inbox`
- **Purpose:** summarize support mail and draft responses
- **Suggested output template:**
  - sender / subject
  - urgency
  - summary
  - recommended reply
  - approval needed?

### D. Caruso Growth Opportunity Scan
- **Status:** planned first-wave
- **Destination:** `caruso-growth`
- **Purpose:** produce actionable marketing opportunities
- **Suggested output template:**
  - opportunity
  - where
  - why now
  - suggested angle
  - draft copy
  - approval needed?

## Candidate Second-Wave Jobs
- product insight digest → `caruso-product`
- security posture digest → `security-infra`
- research idea scan → `research-lab`
- editorial story pick digest → newsroom/signal-and-circuit flow

## Validation Standard For Each Job
Before enabling any job, confirm:
- clear owner room
- clear schedule
- clear destination
- stable auth path
- expected output format
- duplicate prevention
- failure visibility
- approval boundary
- easy pause/disable path

## Failure Handling Policy
If a job fails repeatedly:
1. pause it
2. report the failure to `ops-desk`
3. escalate to `command-center` if it affects daily operation
4. fix auth/config before re-enabling

## Noise Control Policy
A job should be tuned down or paused if:
- it posts repetitive low-value updates
- it creates more review burden than utility
- it lacks a clear owner/action
- it repeatedly reports the same unchanged state

## Open Decisions
- exact schedules for first-wave jobs
- which outputs should go to command-center in addition to local rooms
- whether some jobs should be dashboard-only later
- final channel routing for legacy vs new jobs
