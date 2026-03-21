# CHANNEL_MIGRATION_MAP.md

## Purpose
This is the practical mapping of current/legacy Discord destinations to the intended Mac mini-era room structure.

## Current Active / Known Channels

### command-center (planned permanent)
- `1484651751108775946`
- target for top-level digests and cross-room summaries

### ops-desk (planned permanent)
- `1484651772193673349`
- target for operational coordination and failure/watchdog output

### support-inbox (planned permanent)
- `1484651808772198462`
- target for support triage

### caruso-growth (planned permanent)
- `1484651836966436934`
- target for Caruso marketing/growth workflows

### caruso-product (planned permanent)
- `1484651869593669762`
- target for product synthesis

### security-infra (planned permanent)
- `1484651900812001491`
- target for security/runtime work

### research-lab (planned permanent)
- `1484655635336265758`
- target for research workflows

## Transitional / Legacy Destinations

### legacy support alerts
- `1484558242381168670`
- status: temporary / migrate away

### Signal and Circuit mail/editorial channel
- `1484600889506533576`
- status: active transitional room
- likely remains in use until a more explicit newsroom decision is made

### legacy Caruso marketing channel
- `1484611501842104510`
- status: active transitional room
- target destination for its workflows should become `caruso-growth`

## Job-by-Job Target Routing

### morning-command-center-digest-weekdays-830am
- current: Discord `1484624715590144010`
- future target: `command-center` `1484651751108775946`
- action: migrate destination at cutover

### signalandcircuit-mail-monitor-every-2m
- current: Discord `1484600889506533576`
- future target: keep as-is temporarily pending newsroom/channel decision
- action: review later

### caruso-weekly-marketing-pack-mondays-9am
- current: Discord `1484611501842104510`
- future target: `caruso-growth` `1484651836966436934`
- action: migrate destination at cutover

### caruso-reddit-draft-queue-weekdays-10am
- current: Discord `1484611501842104510`
- future target: `caruso-growth` `1484651836966436934`
- action: migrate destination at cutover

### caruso-daily-reply-pack-weekdays-930am
- current: Discord `1484611501842104510`
- future target: `caruso-growth` `1484651836966436934`
- action: migrate destination at cutover

### caruso-competitor-watch-every-6h
- current: Discord `1484611501842104510`
- future target: `caruso-growth` `1484651836966436934`
- action: migrate destination at cutover

### caruso-marketing-opportunity-scan-every-4h
- current: Discord `1484611501842104510`
- future target: `caruso-growth` `1484651836966436934`
- action: migrate destination at cutover

### gaming-trends-video-game-news-every-2h
- current: retired
- future target: none
- action: do not migrate

## Suggested Near-Term Rules
- Keep legacy channels alive only as long as needed to avoid disruption.
- Prefer new work to route to the permanent room structure once cutover happens.
- Do not move Signal and Circuit editorial routing until that site’s newsroom structure is decided.
- Do not create overlapping rooms for the same function.

## Newly Activated Starter Room Jobs

### ops-desk
- `ops-desk-midday-status-weekdays-1pm`
- destination: `1484651772193673349`
- purpose: operational coordination / health / blockers

### caruso-product
- `caruso-product-signal-digest-weekdays-1230pm`
- destination: `1484651869593669762`
- purpose: product signal synthesis and recommendations

### security-infra
- `security-infra-daily-healthcheck-weekdays-845am`
- destination: `1484651900812001491`
- purpose: runtime and infrastructure health visibility

### research-lab
- `research-lab-weekly-idea-scan-mondays-11am`
- destination: `1484655635336265758`
- purpose: weekly ranked opportunity scan

## Intentionally Deferred

### support-inbox
- permanent room is defined
- no new starter cron was created yet because the more important support path is still the actual mailbox integration / triage workflow rather than a fake placeholder digest

## Next Decision Still Open
Signal and Circuit needs a final room decision:
- one dedicated newsroom room?
- one editorial room plus one monetization/growth room?
- keep the current room and formalize it?
