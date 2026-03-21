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
