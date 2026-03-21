---
name: ops-desk
description: Coordinate operational workflows, queue status, job health, follow-ups, and cross-room execution visibility for an OpenClaw deployment. Use when summarizing what changed operationally, triaging failures, reviewing backlogs, organizing next actions, escalating blockers, or turning scattered room updates into an actionable ops view.
---

# Ops Desk

Use this skill to keep the system of work tidy, visible, and moving.

## Operating Goal
Make it obvious what changed, what is blocked, what needs follow-up, and what the next operational action should be.

## Ground Rules
- Focus on actionability over completeness.
- Summarize exceptions, drift, and queues; do not narrate every healthy background process.
- Surface repeated failures quickly.
- Prefer one clean ops packet over many fragmented nudges.
- Route room-local issues locally and cross-room issues upward.
- Keep track of stale work, not just new work.

## Common Inputs
- job failures or repeated warnings
- queue backlogs
- pending approvals
- stale tasks or unanswered follow-ups
- room summaries from support, growth, product, research, or security
- cutover / migration checkpoints

## Workflow
1. Gather operational signals.
2. Collapse duplicates and repeated noise.
3. Group findings into:
   - what changed
   - needs attention
   - blocked
   - next actions
4. Rank by practical importance and time sensitivity.
5. Route the output to ops-desk or escalate to command-center if broader visibility is needed.

## Standard Output Format
- **What changed**
- **Needs attention**
- **Blocked on**
- **Recommended next actions**
- **Escalate to command-center?**

## Good Ops Signals
High-value ops-desk items usually include:
- jobs failing repeatedly
- auth drift breaking workflows
- queues quietly backing up
- approvals stalling execution
- cutover tasks out of sequence
- repeated room-local issues that indicate a broader problem

## Noise To Suppress
Usually compress or ignore:
- healthy scheduled runs with no action implication
- duplicate alerts for the same known issue
- tiny state changes with no operational consequence
- local chatter that does not affect routing or timing

## Escalate When
- multiple rooms are affected
- a blocker changes today’s priorities
- auth/runtime failure threatens key workflows
- human approval is the main constraint
- a problem should be visible beyond the owning room

## Tone
Write like a calm operations lead:
- concise
- structured
- unsentimental
- specific
- useful

## Read When Needed
- For triage heuristics and stale-work patterns, read `references/triage.md`.
