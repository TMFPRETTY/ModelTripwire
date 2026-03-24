# AGENT_SCORECARDS.md

## Purpose
This file defines a lightweight health model for the non-gaming agents/rooms so they can be judged consistently.

Status labels should help answer:
- is this room healthy?
- is it drifting?
- is it noisy?
- is it blocked?
- what should happen next?

## Shared Scorecard Labels
- `HEALTHY`
- `DRIFTING`
- `NOISY`
- `BLOCKED`
- `WATCH`

## How To Use Them
### HEALTHY
Use when:
- outputs are landing
- outputs are useful
- room ownership is clear
- failures are rare or contained

### DRIFTING
Use when:
- behavior no longer matches room purpose
- prompts/jobs are producing lower-fit outputs
- ownership or handoff lines are getting muddy

### NOISY
Use when:
- posts are repetitive
- posts are low-value to review
- signal-to-noise is too low
- the room/job creates more burden than utility

### BLOCKED
Use when:
- delivery is failing
- auth/runtime prevents useful operation
- a room cannot perform its intended role
- human approval is the hard stop for materially important work

### WATCH
Use when:
- things are mostly working
- but recent evidence suggests elevated risk
- or the next 1 to 3 runs should be watched before calling it healthy again

---

## Current Non-Gaming Scorecards

### command-center
- **Status:** WATCH
- **Why:** room model is strong, but the latest morning digest run finished `ok` and still did not deliver
- **Promote to HEALTHY when:** next 2 scheduled/manual digests deliver cleanly
- **Downgrade to BLOCKED when:** another digest run finishes without delivery
- **Next action:** watch next command-center deliveries closely and escalate if non-delivery repeats

### ops-desk
- **Status:** HEALTHY
- **Why:** job coverage and room purpose align; no current delivery/drift issue surfaced in audit
- **Downgrade to WATCH when:** repeated failures or low-value generic summaries show up
- **Next action:** keep monitoring for drift rather than change anything now

### support-inbox
- **Status:** HEALTHY
- **Why:** room definition is clear and the lack of recurring cron currently appears intentional
- **Downgrade to DRIFTING when:** support work starts leaking into unrelated rooms without routing discipline
- **Next action:** leave as-is until a real support automation is introduced

### caruso-growth
- **Status:** HEALTHY
- **Why:** multiple active jobs, clear room ownership, no current delivery problems surfaced
- **Downgrade to NOISY when:** opportunity/reply/reddit outputs become repetitive or weak-fit
- **Next action:** periodically sample quality, but no immediate intervention needed

### caruso-product
- **Status:** HEALTHY
- **Why:** room purpose and active digest align well
- **Downgrade to DRIFTING when:** weak evidence starts being overstated repeatedly
- **Next action:** keep the recommendation quality bar high

### security-infra
- **Status:** HEALTHY
- **Why:** daily check is active and currently delivering
- **Downgrade to WATCH when:** runtime risk reporting becomes shallow or misses repeated failures
- **Next action:** keep evidence-based posture

### research-lab
- **Status:** HEALTHY
- **Why:** room scope is clear and the weekly scan is aligned with that purpose
- **Downgrade to NOISY when:** the room turns into generic idea sludge
- **Next action:** maintain selectivity over volume

### signal-and-circuit
- **Status:** WATCH
- **Why:** room docs are now much better and the odd cron session key was fixed, but this room still has the highest recent history of compaction/context fragility and mixed-lane overload
- **Promote to HEALTHY when:** room interactions and next scheduled outputs remain stable without typing-stall regressions
- **Downgrade to BLOCKED when:** typing-then-stop behavior returns on ordinary work
- **Next action:** keep implementation work routed out to `engineering` quickly and avoid mixed-lane sludge

### engineering
- **Status:** HEALTHY
- **Why:** room role is explicit and QA relationship is well defined
- **Downgrade to DRIFTING when:** engineering work starts closing without clear QA or approval boundaries
- **Next action:** preserve implementation-vs-review discipline

### qa-review
- **Status:** HEALTHY
- **Why:** role and verdict structure are explicit and aligned with engineering flow
- **Downgrade to NOISY when:** QA becomes ritual boilerplate without real verdict value
- **Next action:** keep verdicts concrete and evidence-based

## Practical Rule
A room can have good docs and still be `WATCH` or `BLOCKED` if the live system misbehaves.
The scorecard is about operational reality, not just document quality.
