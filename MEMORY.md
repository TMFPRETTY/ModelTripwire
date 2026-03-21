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
