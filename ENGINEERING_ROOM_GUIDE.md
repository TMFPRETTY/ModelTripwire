# ENGINEERING_ROOM_GUIDE.md

## Purpose
This room is the shared implementation lane for code, debugging, automation changes, integration work, and QA review across Caruso, Signal and Circuit, OpenClaw automations, and platform/infrastructure changes.

## Channel
- `engineering`
- Discord channel id: `1484988049229086850`

## Core Role
Engineering is where work moves from:
- idea
- bug report
- product request
- workflow need

into:
- implementation plan
- code change
- review
- testing
- handoff

## What Belongs Here
- coding requests
- bugfixes
- implementation planning
- debugging
- code review requests
- automation/integration changes
- config changes with engineering impact
- QA review of code and higher-risk outputs

## What Does Not Belong Here
- general growth brainstorming without implementation work
- product strategy discussion with no build component
- support triage by itself
- generic room-local chatter without engineering action

## Internal Lanes
Use threads or clearly labeled posts for these lanes:
- **Caruso**
- **Signal and Circuit**
- **OpenClaw / platform**
- **Infra / automation**
- **QA review**

## Active Room Ownership
Current intended room -> agent ownership:
- `engineering` -> `engineering`
- `signal-and-circuit` -> `signal-and-circuit`
- `command-center` -> `command-center`
- `ops-desk` -> `ops-desk`
- `support-inbox` -> `support-inbox`
- `caruso-growth` -> `caruso-growth`
- `caruso-product` -> `caruso-product`
- `security-infra` -> `security-infra`
- `research-lab` -> `research-lab`

Engineering is the implementation room, not the long-term owner of every request.
Other rooms can originate work, but engineering owns build/debug/integration execution once the work becomes implementation.

## Repo Anchors
Use these project roots when the request is about code in a specific system:
- **Caruso repo:** `/Users/jeremypretty/Documents/PM and QA/PM-and-QA-Combo-Fun`
- **Signal and Circuit repo:** `/Users/jeremypretty/Documents/AI:ML/signal-and-circuit`
- **OpenClaw workspace / platform:** `/Users/jeremypretty/.openclaw/workspace`

If a request in `engineering` names one of these systems, treat that repo/workspace as the default working context.

## How To Ask For Work
A good engineering request should include:
- **System:** Caruso / Signal and Circuit / OpenClaw / Infra
- **Problem or goal:** what needs to be built or fixed
- **Why:** the reason it matters
- **Constraints:** anything to avoid or preserve
- **Definition of done:** what success looks like
- **Urgency:** low / normal / high

## Recommended Request Template
- **System:**
- **Task:**
- **Why:**
- **Constraints:**
- **Done means:**
- **Urgency:**

## Engineering Workflow
1. Intake the request.
2. Clarify the real implementation task.
3. Decide whether the work belongs to Caruso, Signal and Circuit, platform, or infra.
4. Produce an implementation plan when needed.
5. Execute code/config/script changes.
6. Hand the result to QA review when appropriate.
7. Return status: ready, needs testing, needs approval, blocked, or complete.

## QA In Engineering
QA is part of the room’s operating model.

Use QA for:
- code review
- config review
- automation changes
- risky prompt/workflow changes
- high-value content/output review when engineering is involved

Rule of thumb:
- Engineering implements.
- QA reviews.
- Work is not complete just because engineering says the coding is done.
- A coding/config/automation task is complete only after QA passes it, explicit approval is given, or the work is intentionally stopped.

### QA verdicts
- `PASS`
- `PASS_WITH_EDITS`
- `TEST_BEFORE_USE`
- `NEEDS_APPROVAL`
- `REWORK`
- `BLOCK`

## Standard Status Labels
Use these labels in engineering threads/posts when useful:
- `INTAKE`
- `PLANNING`
- `IN PROGRESS`
- `NEEDS QA`
- `NEEDS APPROVAL`
- `BLOCKED`
- `DONE`

## Relationship To Other Rooms
- `caruso-product` decides product direction; `engineering` implements it.
- `signal-and-circuit` decides site/editorial/system needs; `engineering` implements them.
- `ops-desk` can escalate blocked implementation work here.
- `security-infra` can route engineering-impact fixes here when code/config work is required.
- `caruso-growth` can hand off landing pages, tooling, instrumentation, or automation tasks that require implementation.
- `support-inbox` can hand off bugs, fixes, and workflow/tooling issues that require engineering work.

When another room asks engineering to look at context from its own lane, engineering should use that room as the information source, then do the implementation work in engineering.

## Conversational Room Mode
The engineering room should behave like a live working room, not just a scheduled reporting lane.
That means:
- messages posted in the room should be picked up and answered
- engineering can be asked to look at other rooms for context or intake
- implementation can begin from requests originating in other rooms when engineering is explicitly directed to do so
- coding work should still be surfaced back through the engineering lane with QA review before completion

## Practical Current Mode
Use `engineering` as:
- the source-of-truth lane for engineering requests
- the place where implementation work should be tracked
- the place where coding and QA notes should land
- the room that coordinates with other rooms when implementation work depends on their context
