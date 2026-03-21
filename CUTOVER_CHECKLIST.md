# CUTOVER_CHECKLIST.md

## Purpose
This is the Mac mini arrival and cutover checklist. Goal: restore service cleanly, verify basics, then re-enable automation in controlled waves.

## Phase 0 — Before Arrival
- [ ] Confirm intended Mac mini role: dedicated always-on OpenClaw host.
- [ ] Decide hostname.
- [ ] Decide local admin/remote administration model.
- [ ] Decide Tailscale naming and access policy.
- [ ] Decide backup destination for config/state/logs.
- [ ] Prepare canonical docs in workspace.
- [ ] Inventory accounts, tokens, and auth dependencies.
- [ ] Confirm which automations remain paused until validation.

## Phase 1 — Unbox / Base Machine Setup
- [ ] Power on and complete macOS setup.
- [ ] Apply system updates.
- [ ] Set computer name / hostname.
- [ ] Configure power settings for always-on behavior.
- [ ] Disable sleep if appropriate for headless operation.
- [ ] Enable needed remote access path(s).
- [ ] Install Tailscale if using.
- [ ] Verify remote reachability.

## Phase 2 — Security / Baseline
- [ ] Confirm login/security settings.
- [ ] Enable disk encryption if not already enabled.
- [ ] Review firewall and sharing settings.
- [ ] Confirm software update policy.
- [ ] Review startup/login items.
- [ ] Record baseline security posture.

## Phase 3 — OpenClaw Install / Restore
- [ ] Install/verify OpenClaw runtime.
- [ ] Restore workspace to expected location.
- [ ] Restore OpenClaw config.
- [ ] Restore or recreate required local dependencies.
- [ ] Verify `openclaw status` works.
- [ ] Verify gateway state.
- [ ] Verify logs are writable and discoverable.

## Phase 4 — Auth / Integrations
- [ ] Verify Discord bot/app configuration.
- [ ] Verify Discord channel allowlist/config.
- [ ] Re-auth any Google / Gmail / GCP integrations as needed.
- [ ] Verify project-level cloud access still works.
- [ ] Verify any required local CLIs (`gcloud`, `gog`, etc.).
- [ ] Verify website/domain/API credentials inventory against reality.

## Phase 5 — Messaging / Routing Validation
- [ ] Send a test message into each primary Discord room.
- [ ] Confirm replies/threads behave as expected.
- [ ] Confirm support-inbox destination works.
- [ ] Confirm command-center destination works.
- [ ] Confirm one failure/alert path can be observed end-to-end.

## Phase 6 — Job Validation Before Re-Enable
For each job:
- [ ] confirm purpose
- [ ] confirm schedule
- [ ] confirm destination channel
- [ ] confirm auth dependency
- [ ] confirm expected output format
- [ ] dry-run if possible
- [ ] verify logging/observability

## Phase 7 — Re-Enable In Waves

### Wave 1
- [ ] command-center digest
- [ ] ops-desk basics
- [ ] support-inbox core triage
- [ ] one Caruso growth workflow

### Wave 2
- [ ] caruso-product workflows
- [ ] security-infra checks
- [ ] additional growth jobs

### Wave 3
- [ ] research-lab workflows
- [ ] newsroom/editorial workflows
- [ ] higher-volume or experimental automations

## Phase 8 — Observe / Stabilize
- [ ] Watch logs after first scheduled runs.
- [ ] Confirm no duplicate posting.
- [ ] Confirm rate/volume is acceptable.
- [ ] Confirm thread/approval flows are understandable.
- [ ] Adjust schedules if they are too noisy.
- [ ] Record issues in ops notes.

## Phase 9 — Finalize
- [ ] Mark laptop-era paused jobs as migrated, replaced, or retired.
- [ ] Update inventory docs with current auth/machine reality.
- [ ] Commit workspace changes.
- [ ] Document lessons learned from cutover.

## Rollback Plan
If the deployment behaves badly:
- pause jobs first
- preserve logs and config
- reduce to command-center + one validated workflow
- fix auth/routing issues before re-expansion
- avoid partial “sort of working” production state

## Definition of Done
Cutover is complete when:
- the Mac mini is the trusted host
- command-center and core rooms receive expected updates
- critical auth and routing paths are stable
- first-wave jobs run successfully on schedule
- failures are visible and diagnosable
- the laptop is no longer the hidden dependency
