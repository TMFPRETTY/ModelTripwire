---
name: security-infra
description: Review host security, infrastructure health, OpenClaw runtime posture, update state, remote access exposure, and operational drift for a machine running OpenClaw. Use when preparing a new host, hardening a Mac mini or server, checking version/update posture, reviewing remote access, diagnosing repeated service failures, or producing security/infrastructure summaries for the security-infra room.
---

# Security Infra

Use this skill to turn security and infrastructure checks into actionable operational guidance.

## Operating Goal
Keep the OpenClaw host stable, reachable, reasonably hardened, and free of obvious configuration drift or silent failure.

## Ground Rules
- Prefer evidence over vague concern.
- Distinguish actual risk from cosmetic warning noise.
- Do not make disruptive system changes without approval.
- Treat remote access, auth, and always-on reliability as first-class concerns.
- When recommending a fix, say why it matters and how urgent it is.
- If a problem is cross-room or threatens normal operation, escalate to command-center.

## Core Check Areas
Review some or all of these depending on the task:
1. host identity and intended role
2. update posture
3. remote access path and exposure
4. firewall/sharing/security settings
5. OpenClaw runtime health
6. gateway status and job health
7. auth/integration drift
8. backup/logging/observability readiness

## Workflow
1. Establish scope: baseline hardening, health check, incident review, or pre-cutover audit.
2. Gather concrete status/evidence.
3. Group findings into:
   - healthy
   - watch items
   - risks
   - blockers
4. Rank by practical impact.
5. Recommend the smallest sensible next actions.
6. Mark which changes require approval.

## Output Format
- **Status**
- **Risk**
- **Evidence**
- **Recommended action**
- **Urgency** (`low`, `normal`, `high`, `critical`)
- **Approval needed?**

## Escalate Immediately When
- OpenClaw or gateway repeatedly fails to start
- remote administration path breaks
- auth/config drift disables important workflows
- updates are critically overdue with meaningful exposure
- there is evidence of material exposure or compromise
- multiple jobs fail because of a shared infrastructure issue

## Change Discipline
Without approval, this skill may:
- inspect status
- summarize posture
- compare current state to intended state
- recommend remediations
- prepare action plans

Without approval, this skill should not:
- change firewall/SSH/remote access settings in a risky way
- disable important services
- delete logs/state
- perform disruptive remediation

## Mac Mini Launch Focus
For the Mac mini cutover, pay extra attention to:
- always-on power/sleep behavior
- remote access reliability
- Tailscale or equivalent remote path
- software update posture
- OpenClaw status and gateway health
- logging and backup readiness
- whether laptop-era hidden dependencies still exist

## Read When Needed
- For launch-specific checklists and severity/risk heuristics, read `references/checklists.md`.
