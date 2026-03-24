# NEW_AGENT_AND_JOB_CHECKLIST.md

## Purpose
This file is the creation gate for new non gaming agents, rooms, and recurring jobs.

Its purpose is simple:
new agents and jobs should not be added casually, vaguely, or without safeguards.

This checklist should be used before any new room, agent, or recurring automation is treated as live.

## Rule
If a proposed room, agent, or job cannot pass this checklist, it is not ready.
It can stay planned or draft, but it should not be treated as production ready.

---

## Part 1. New room or agent checklist

### Identity and ownership
Confirm all of these:
- [ ] clear name
- [ ] clear room or operating scope
- [ ] clear mission
- [ ] clear list of what it owns
- [ ] clear list of what it does not own
- [ ] clear relationship to other rooms

### Documentation
Confirm all of these exist or are explicitly planned before go live:
- [ ] registry entry in `AGENT_REGISTRY.md`
- [ ] runbook coverage in `AGENT_RUNBOOKS.md`
- [ ] room guide if it owns a room
- [ ] approval boundary is documented
- [ ] escalation paths are documented

### Routing discipline
Confirm all of these:
- [ ] implementation work routes to `engineering`
- [ ] behavior changing implementation routes through `qa-review`
- [ ] cross room escalation path is clear
- [ ] command center visibility is defined when relevant
- [ ] ops desk involvement is defined for failures or drift when relevant

### Safety boundary
Confirm all of these:
- [ ] no destructive behavior by default
- [ ] no stealth external action
- [ ] no public posting without approval unless intentionally designed and approved
- [ ] no unsupported commitments
- [ ] no risky customer or partner communication without approval

### Operational readiness
Confirm all of these:
- [ ] clear output format
- [ ] clear notion of what good output looks like
- [ ] clear definition of noise or drift
- [ ] clear way to pause or disable the room workflow if needed
- [ ] known owner for follow up when it misbehaves

---

## Part 2. New recurring job checklist

### Job identity
Confirm all of these:
- [ ] clear job name
- [ ] clear owner room
- [ ] clear destination channel or target
- [ ] clear schedule
- [ ] clear purpose

### Prompt and output quality
Confirm all of these:
- [ ] prompt reflects the real room mission
- [ ] prompt does not ask the agent to pretend it verified things it cannot verify
- [ ] prompt defines useful structure for the output
- [ ] prompt discourages filler and fake certainty
- [ ] prompt has a clear approval boundary when external action is implied

### Delivery and control
Confirm all of these:
- [ ] destination is correct
- [ ] delivery mode is intentional
- [ ] job can be paused or disabled easily
- [ ] repeated failure path is known
- [ ] delivery success can be checked after runs

### Risk review
Confirm all of these:
- [ ] job will not create unwanted external side effects
- [ ] job will not spam a room
- [ ] job will not duplicate another active workflow without reason
- [ ] job will not produce likely junk at the chosen cadence
- [ ] any auth or state dependency is understood

### Technical hygiene
Confirm all of these:
- [ ] session binding is intentional
- [ ] model choice is intentional
- [ ] timeout is reasonable
- [ ] likely failure modes are known
- [ ] a human can explain why this job deserves to exist

---

## Part 3. Go live decision labels

Use one of these labels for every proposed room, agent, or job:
- `READY`
- `READY WITH WATCHPOINTS`
- `DRAFT ONLY`
- `BLOCKED`

### READY
Use when the checklist is satisfied and the risk is acceptable.

### READY WITH WATCHPOINTS
Use when the checklist mostly passes but the first few runs should be watched closely.

### DRAFT ONLY
Use when the concept is good but the safeguards or docs are not complete.

### BLOCKED
Use when the proposal has unclear ownership, unsafe behavior, no approval boundary, or weak operational logic.

---

## Part 4. Fast rejection rules
Do not launch a new room or job if any of these are true:
- ownership is vague
- it duplicates an existing room without a strong reason
- approval boundaries are unclear
- it can create external effects without intentional control
- it has no easy pause or stop path
- it is mostly vibe and no operating logic
- it adds more review burden than likely value

---

## Part 5. Post launch watchpoints
For the first few live runs, check:
- [ ] did it deliver
- [ ] was it useful
- [ ] was it too noisy
- [ ] did it create confusion about room ownership
- [ ] did it require stronger approval boundaries than expected
- [ ] did it expose any routing or QA gaps

If the answer looks bad, downgrade it quickly instead of letting bad automation become normal.

## Bottom line
A new agent or job should earn its place.

The standard is not just can we make it run.
The standard is should this exist, can it be trusted, and will it improve the system instead of making it noisier or riskier.
