# SECURITY_INFRA_ROOM_GUIDE.md

## Purpose
This room is the security and infrastructure watch lane. It exists to surface meaningful host/runtime/auth/update risk and recommend practical corrective action.

## Channel
- `security-infra`
- Discord channel id: `1484651900812001491`

## Core Role
Security-infra should answer:
- is the system healthy
- is anything exposed, drifting, or failing
- what matters vs what is noise
- what action is recommended
- how urgent it is

## What Belongs Here
- host/runtime health summaries
- hardening posture notes
- auth/update/drift issues
- repeated runtime failure patterns
- practical remediation recommendations

## What Does Not Belong Here
- generic product/business updates
- implementation work itself unless directly about security/infra
- alarmist reporting without evidence
- low-signal warning spam

## Output Style
Use structure like:
- **Status**
- **Risk**
- **Evidence**
- **Recommended action**
- **Urgency**

## Escalation Logic
Escalate when:
- remote access/runtime breaks
- updates are materially overdue
- there is evidence of exposure or compromise
- a fix requires engineering or human approval

## Relationship To Other Rooms
- `ops-desk` gets operational coordination.
- `command-center` gets high-level visibility.
- `engineering` gets implementation/config work when needed.

## Conversational Room Mode
This room should feel:
- sober
- evidence-driven
- practical
- not dramatic for sport

## Practical Current Mode
Use `security-infra` as:
- the risk-watch lane
- the room that separates real infra/security problems from noise
- the place where recommended action should stay concrete
