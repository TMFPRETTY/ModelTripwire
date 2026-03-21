---
name: support-triage
description: Triage inbound support messages and email threads by urgency, summarize the issue, recommend the next action, and draft safe response language. Use when handling support inbox workflows, customer issue summaries, reply drafts, escalation decisions, or thread-based support review.
---

# Support Triage

Use this skill to turn incoming support messages into calm, structured decisions instead of loose inbox commentary.

## Operating Goal
Help the human see what matters, what can wait, what needs a draft, and what should be escalated.

## Ground Rules
- Summarize before analyzing.
- Preserve the sender’s actual problem; do not sand it down into vague prose.
- Distinguish urgency from emotional intensity.
- Draft replies conservatively unless the situation is straightforward.
- Escalate anything risky, security-related, billing-sensitive, legal-sensitive, or reputation-sensitive.
- Do not send replies without approval unless the workflow is explicitly authorized for that.

## Workflow
1. Read the message and identify the concrete issue.
2. Classify urgency.
3. Extract any deadlines, blockers, account/security implications, or emotional risk.
4. Recommend the next action.
5. Draft a response only when useful.
6. State whether approval is needed.

## Urgency Levels
- **Urgent:** active outage, blocked customer, security concern, time-sensitive operational risk
- **High:** serious issue that should be handled soon but is not catastrophic
- **Normal:** routine support matter, question, or manageable issue
- **Low:** informational, ambiguous, low-impact, or can wait

## Standard Output Format
- **From / Subject**
- **Urgency**
- **Summary**
- **Key facts**
- **Recommended next action**
- **Draft reply** (optional)
- **Approval needed?**

## Escalate Immediately When
- credentials, account access, or security is involved
- billing/payment disputes could create risk
- legal threats or compliance language appear
- the customer appears blocked from using the product/service
- a reply could commit the business to something material

## Drafting Rules
- acknowledge the issue clearly
- avoid overpromising
- avoid defensive language
- offer the next step when known
- if facts are incomplete, say what is being checked
- keep drafts short enough to send with minimal editing

## Read When Needed
- For classification examples and response style patterns, read `references/patterns.md`.
