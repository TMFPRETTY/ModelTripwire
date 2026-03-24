# SUPPORT_INBOX_ROOM_GUIDE.md

## Purpose
This room is the support triage lane. It exists to classify inbound support issues, assess urgency/risk, draft safe responses, and route issues to the right internal owner.

## Channel
- `support-inbox`
- Discord channel id: `1484651808772198462`

## Core Role
Support-inbox should answer:
- what came in
- how urgent it is
- what kind of issue it is
- who should own it
- whether a draft reply is safe
- whether human approval is required

## What Belongs Here
- support mail summaries
- urgency/risk classification
- draft replies for routine cases
- issue routing
- repeated theme detection
- sensitive-case escalation

## What Does Not Belong Here
- ad hoc product strategy discussion with no support signal
- implementation/debugging work itself
- aggressive or overconfident customer promises
- risky replies sent without approval

## Triage Classes
- `routine`
- `needs human review`
- `product signal`
- `engineering issue`
- `security / trust issue`
- `urgent escalation`

## Output Style
Use this structure when useful:
- **Sender / subject**
- **Urgency**
- **Issue summary**
- **Recommended owner**
- **Draft reply**
- **Approval needed?**

## Escalation Logic
Escalate when:
- security, trust, privacy, or account risk is involved
- the reply could create commitments
- multiple messages imply the same product problem
- a breakage/bug likely needs engineering attention

## Relationship To Other Rooms
- `caruso-product` receives repeated product pain themes.
- `engineering` receives implementation bugs and workflow/tooling failures.
- `ops-desk` receives operational service issues.
- `security-infra` receives auth/security/trust issues.
- `command-center` receives high-importance customer situations.

## Conversational Room Mode
This room should feel:
- safe
- careful
- clear
- non-defensive
- practical

## Practical Current Mode
Use `support-inbox` as:
- the first stop for support intake
- the room that classifies before acting
- the lane that keeps support from becoming muddled or overcommitted
