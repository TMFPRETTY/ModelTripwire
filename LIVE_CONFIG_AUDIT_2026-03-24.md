# LIVE_CONFIG_AUDIT_2026-03-24.md

## Purpose
This document records a live audit of the current non-gaming room/job setup against the documented operating model.

Audit date: 2026-03-24

## What Was Checked
- active cron jobs via OpenClaw cron list
- live session bindings visible in agent session stores
- recent known problem areas in Signal & Circuit
- alignment against:
  - `AGENT_REGISTRY.md`
  - `AGENT_RUNBOOKS.md`
  - room guide docs

## High-Level Result
Overall shape is good.
The non-gaming side now has a much tighter documented operating model and the live cron setup mostly aligns with it.

However, a few mismatches or risk notes remain.

## Confirmed Live Job Coverage
### command-center
- `morning-command-center-digest-weekdays-830am`

### ops-desk
- `ops-desk-midday-status-weekdays-1pm`

### security-infra
- `security-infra-daily-healthcheck-weekdays-845am`

### engineering / qa-review
- `engineering-midday-intake-status-weekdays-2pm`
- `engineering-qa-review-check-weekdays-215pm`

### caruso-growth
- `caruso-marketing-opportunity-scan-daily-1115am`
- `caruso-weekly-marketing-pack-mondays-9am`
- `caruso-daily-reply-pack-weekdays-930am`
- `caruso-reddit-draft-queue-weekdays-10am`
- `caruso-competitor-watch-daily-530pm`

### caruso-product
- `caruso-product-signal-digest-weekdays-1230pm`

### research-lab
- `research-lab-weekly-idea-scan-mondays-11am`

### signal-and-circuit
- `signalandcircuit-reddit-draft-queue-weekdays-10am`
- conversational room binding exists for Discord channel `1484556120025727127`

## Confirmed Live Room Binding Notes
### Signal & Circuit
- Live room binding exists at session key:
  - `agent:signal-and-circuit:discord:channel:1484556120025727127`
- Current session id after reset:
  - `4ae18b6a-7363-4ae2-ba00-e1aa2bdd0ce2`
- Workspace context is correctly bound to:
  - `/Users/tmfprettybot/Documents/AI:ML/signal-and-circuit`

### Signal & Circuit thread spillover
Additional Signal & Circuit thread sessions exist for at least:
- `1485744420598059029`
- `1485845441580105750`

This is not inherently bad, but it means Signal & Circuit operational state can spread across room thread sessions if not watched.

## Mismatches / Risks Found

### 1. Command-center delivery issue
- The latest `morning-command-center-digest-weekdays-830am` run had:
  - `lastRunStatus: ok`
  - `lastDeliveryStatus: not-delivered`
  - `lastDelivered: false`

Interpretation:
- the job itself ran, but the final post did not land in the room
- this is not catastrophic, but it is operationally important because command-center is a top-level summary lane

Recommendation:
- watch the next command-center run closely
- if it repeats, treat as an ops-desk + command-center delivery issue

### 2. Signal & Circuit cron job session key oddity
- `signalandcircuit-reddit-draft-queue-weekdays-10am` had been using:
  - `sessionKey: agent:main:main`
- It has now been normalized to:
  - `sessionKey: agent:codex:main`

Interpretation:
- this mismatch was real, not just cosmetic
- it is now fixed, which reduces one source of unnecessary inconsistency around the most fragile room

Recommendation:
- keep the normalized session key unless a future intentional routing decision requires otherwise

### 3. Signal & Circuit session still shows context pressure risk
- The reset helped, but the live Signal & Circuit room record already shows:
  - `contextTokens: 16000`
  - `compactionCount: 1`

Interpretation:
- the room is cleaner than before, but still sitting on a relatively tight context ceiling
- this room remains the most likely to regress into typing-then-stop behavior if overloaded again

Recommendation:
- keep routing implementation work cleanly out to `engineering`
- avoid turning the room into a mixed editorial + support + debugging sludge bucket

### 4. Support-inbox has docs but no live recurring job
Interpretation:
- this is not necessarily a bug
- it matches the intent that support should be driven by real mailbox workflow rather than filler posts

Recommendation:
- treat this as intentional until a real support automation is ready

## Alignment Verdict By Room
- `command-center` — mostly aligned, but delivery issue needs watching
- `ops-desk` — aligned
- `support-inbox` — aligned as a room model; no recurring cron by design
- `caruso-growth` — aligned
- `caruso-product` — aligned
- `security-infra` — aligned
- `research-lab` — aligned
- `signal-and-circuit` — aligned in structure, but still the highest-risk room operationally
- `engineering` — aligned
- `qa-review` — aligned as embedded function

## Bottom Line
The docs and the live configuration are now much closer than they were before.

The main remaining operational watchpoints are:
1. command-center delivery reliability
2. Signal & Circuit session fragility
3. the odd Signal & Circuit cron session-key inconsistency

None of these invalidate the operating model, but they are the places most likely to cause practical drift.
ate the operating model, but the remaining two watchpoints are the places most likely to cause practical drift.
