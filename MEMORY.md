# MEMORY.md

## OpenClaw Mac mini / org direction
- Current direction is to migrate from the laptop-era experimental setup to a more intentional Mac mini deployment.
- Discord is the primary action surface; a future OpenClaw HQ dashboard will be the visibility/control layer.
- Planned permanent Discord rooms: command-center, ops-desk, support-inbox, caruso-growth, caruso-product, security-infra, and research-lab.
- Planned first-wave agents: ops-desk, caruso-growth, caruso-product, security-infra.
- Planned second-wave agents: research-lab, qa-review (embedded first), and signal-and-circuit-editor.
- Additional future layers: learning-loop and knowledge-base; strategy-director and finance-ops are later/optional.

## Planning artifacts created
- Prep docs now exist for the Mac mini deployment: OPENCLAW_ORG_BLUEPRINT.md, AGENT_RUNBOOKS.md, CUTOVER_CHECKLIST.md, DASHBOARD_SCHEMA_V1.md, and JOB_CATALOG.md.
- Custom operating skills created and packaged so far: caruso-growth, support-triage, command-center-digest, security-infra, caruso-product, research-lab, ops-desk, and qa-review.

## Operational decisions
- Use one Discord bot with multiple logical agents/rooms rather than separate Discord bots per agent.
- The gaming trends / video game news workflow was an experiment and should be retired rather than migrated to the Mac mini.
- QA should cover both content QA and code QA.
- Docker is not a day-one requirement for the Mac mini; install only if a real workflow needs it.
- VS Code is the recommended default IDE/editor to have available on the Mac mini for coding visibility and intervention.
- Signal and Circuit should likely have an editorial lookout agent that monitors for breaking or interesting gaming/news content, alerts the team when something looks worth covering, and helps route story creation to the right site persona instead of relying only on fixed schedules.
- There may already be code in the system intended to suppress low-value newsroom triggers; treat that as something for engineering review and threshold tuning, not as an assumption that the problem is already solved.
- Signal and Circuit also needs an AdSense-readiness pass: likely use an agent to audit the site for Google Publisher Policy compliance and site-quality issues such as originality, duplicate/replicated content, low-value pages, navigational/UX problems, privacy disclosures, and search-spam-style weaknesses before re-review.
- Added Signal and Circuit-specific operating skills for both AdSense readiness and traffic growth/editorial packaging.
- Created `SIGNAL_AND_CIRCUIT_ADSENSE_PLAN.md` as the concrete execution plan for Signal and Circuit AdSense readiness and parallel traffic-quality improvements.
- While waiting on the Mac mini, the active laptop-era cron jobs were re-enabled to maintain momentum; the retired gaming-trends workflow stayed disabled.
- Channel structure was prioritized before activating more agents. `CHANNEL_ARCHITECTURE_PLAN.md` and `CHANNEL_MIGRATION_MAP.md` now define the permanent room layout and how current jobs/channels should migrate.
- Live laptop routing has started moving toward the permanent structure already: command-center digest now points at `command-center`, Caruso growth jobs point at `caruso-growth`, and Signal and Circuit remains transitional for now.
- Starter cron jobs were added for `ops-desk`, `caruso-product`, `security-infra`, and `research-lab` so the permanent room structure is active on the laptop now, not just planned.
- `support-inbox` remains intentionally dependent on the real support-mail workflow rather than a placeholder room digest.
- Signal and Circuit should keep one strong combined operating room for now (using the current active channel) instead of splitting newsroom/growth/monetization too early.
- Added `SIGNAL_AND_CIRCUIT_LABELING_CONVENTION.md` to keep the combined room readable using labels like `[EMAIL]`, `[EDITORIAL]`, `[ADSENSE]`, `[GROWTH]`, `[HANDOFF]`, `[QA]`, and `[ALERT]` instead of creating more channels too early.
- A shared `engineering` Discord room was created on 2026-03-21 with channel id `1484988049229086850` to handle code work across Caruso, Signal and Circuit, OpenClaw automations, and platform/integration changes, instead of splitting engineering into multiple low-volume rooms too early.
- Important repo anchors for shared engineering work: Caruso lives at `/Users/jeremypretty/Documents/PM and QA/PM-and-QA-Combo-Fun`, Signal and Circuit lives at `/Users/jeremypretty/Documents/AI:ML/signal-and-circuit`, and OpenClaw/platform work lives at `/Users/jeremypretty/.openclaw/workspace`.
- Added repo-local `OPENCLAW_CONTEXT.md` pointer files to both the Caruso and Signal and Circuit repos so repo-bound room agents can find the canonical OpenClaw planning docs without duplicating the strategy layer.
- Mission Control is the intended future dashboard/control layer: overview-first, built on top of the existing room/agent/job system, not as a disconnected second system. `MISSION_CONTROL_PLAN.md` now defines the V1 scope and build order.
- `MISSION_CONTROL_WIREFRAMES.md` now defines the first-screen layout and main V1 page/widget structure for Mission Control.
- `MISSION_CONTROL_DATA_SOURCES.md` now defines the real source mapping for Mission Control V1 widgets/pages.
- `MISSION_CONTROL_SNAPSHOT_SPEC.md` now defines the JSON contract for Mission Control V1 snapshot files.
- Built a first visible Mission Control prototype in the workspace: static dashboard UI in `mission-control/`, snapshot generator script in `scripts/generate_mission_control_snapshots.py`, generated snapshot data in `mission-control/data/`, and a simple local web-server path for viewing it.
- Upgraded the prototype with scheduled snapshot refresh, smarter derived room headlines/activity/alerts, dedicated Rooms and Jobs pages, and a first-pass approvals/alerts derivation layer.
- Engineering now has `ENGINEERING_ROOM_GUIDE.md`, `ENGINEERING_WORKFLOW.md`, and starter recurring jobs for engineering status and engineering QA checks. Important limitation: this still does not magically create instant Discord conversational pickup for arbitrary posts; it creates the operating model and room cadence, not provider-side message listener behavior.
- Created `AGENT_REGISTRY.md` to formally define the active, embedded, transitional, planned, and retired agents/rooms for the current laptop system and upcoming Mac mini deployment.
