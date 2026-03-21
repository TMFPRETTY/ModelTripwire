# Security Infra Checklists

## Mac Mini Baseline Checklist
Use this when bringing up the dedicated OpenClaw host.

### Host baseline
- confirm hostname/computer name
- confirm intended always-on role
- confirm local admin and remote administration path
- confirm disk encryption
- confirm power/sleep settings support headless uptime

### Network / remote access
- confirm firewall posture
- confirm sharing settings are intentional
- confirm Tailscale or chosen remote path works
- confirm reachability from the expected operator environment

### OpenClaw runtime
- confirm `openclaw status`
- confirm gateway health
- confirm logs are accessible
- confirm config/workspace are in expected locations
- confirm critical jobs can be paused/resumed cleanly

### Integrations
- confirm Discord routing
- confirm Google/Gmail/GCP auth state where needed
- confirm any required local CLIs are installed and usable
- confirm there are no hidden laptop-only dependencies

## Severity Guide
- **Critical:** normal operation or safe remote management is materially broken
- **High:** important service risk or meaningful exposure needs prompt action
- **Normal:** should be fixed soon but not emergency-level
- **Low:** housekeeping, cleanup, or optimization item

## Reporting Rule
Do not dump raw settings lists unless requested. Compress findings into:
- what is healthy
- what is risky
- what changed
- what should happen next
