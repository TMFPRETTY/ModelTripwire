# SIGNAL_AND_CIRCUIT_LABELING_CONVENTION.md

## Purpose
This file defines a simple labeling convention for the combined `signal-and-circuit` room so inbox activity, editorial work, AdSense work, growth, and engineering handoffs can coexist without becoming hard to scan.

## Room
- `signal-and-circuit`
- current active Discord channel: `1484600889506533576`

## Core Rule
Start top-level posts with a short uppercase label in brackets.

Examples:
- `[EMAIL]`
- `[EDITORIAL]`
- `[ADSENSE]`
- `[GROWTH]`
- `[HANDOFF]`
- `[QA]`
- `[ALERT]`

This keeps one room readable without prematurely splitting it into multiple channels.

## Labels To Use

### `[EMAIL]`
Use for:
- inbound mailbox summaries
- new business/editorial/contact messages
- thread-starting email notifications

Format:
- sender
- subject
- short summary
- recommended next action

Rule:
- if an email needs discussion or drafting, move the detailed work into a thread

### `[EDITORIAL]`
Use for:
- story-worthiness decisions
- article routing
- worthwhile coverage opportunities
- newsroom lookout findings
- persona/angle recommendations

Format:
- what happened
- why it matters
- worth covering / worth watching / ignore
- suggested angle/persona

### `[ADSENSE]`
Use for:
- site-quality audits
- policy/compliance findings
- originality/thin-content/duplicate-content issues
- trust/privacy/UX issues
- remediation planning

Format:
- issue or recommendation
- why it matters
- severity / priority
- whether it is editorial or engineering work

### `[GROWTH]`
Use for:
- readership/traffic opportunities
- packaging improvements
- follow-up article ideas
- distribution/community opportunities

Format:
- opportunity
- why it matters
- suggested action

### `[HANDOFF]`
Use for:
- moving implementation work to `engineering`
- moving a specific remediation item from planning to build

Format:
- system
- ticket/task
- why it matters
- done means
- destination room

Example:
`[HANDOFF] Engineering — Implement P0-1 consent-gated ad loading + CMP integration for Signal and Circuit.`

### `[QA]`
Use for:
- review outcomes
- pass / rework / block decisions
- readiness checks

Format:
- item reviewed
- verdict
- main issue(s)
- next step

### `[ALERT]`
Use for:
- urgent/high-importance issues only
- serious AdSense blockers
- major story opportunities with timing pressure
- operational breakage affecting the site workflow

Rule:
- do not overuse this label

## Threading Rules
- Use a **thread per email** when detailed response handling is needed.
- Use a **thread per implementation item** if the discussion gets long and will hand off to engineering.
- Keep the main room focused on summaries, decisions, and handoffs.
- Keep long drafting/debugging work inside threads or in `engineering` when code work is involved.

## Ownership Rules
- Editorial/content-side changes stay in `signal-and-circuit`.
- Code/site/template/config changes move to `engineering`.
- Shared items should name a primary owner and a supporting owner.

## Recommended Reading Flow
A human or agent scanning the room should be able to quickly distinguish:
- inbox activity via `[EMAIL]`
- publication decisions via `[EDITORIAL]`
- monetization/site-quality work via `[ADSENSE]`
- audience work via `[GROWTH]`
- implementation transfer via `[HANDOFF]`

## Bottom Line
One strong room is fine for now, as long as posts are labeled clearly and detailed work gets pushed into threads or engineering when appropriate.
