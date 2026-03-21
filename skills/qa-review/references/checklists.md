# QA Review Checklists

## Content QA Checklist
Ask:
- Is it correct?
- Is it clear?
- Is it missing important context?
- Is the confidence level appropriate?
- Is the urgency or priority calibrated correctly?
- Is it too noisy, repetitive, or bloated?
- Does it need explicit approval language?

## Code QA Checklist
Ask:
- Does the change match the request?
- What could break?
- What happens on bad input or missing state?
- Could this create duplicate posting, retry loops, or silent failure?
- Are secrets, auth, or config handled safely?
- Is the code understandable and maintainable enough?
- Should it be tested before use?

## Review Outcome Heuristics
- **PASS:** good enough, low risk, no material issues
- **PASS_WITH_EDITS:** mostly fine, minor fixes improve clarity/safety
- **TEST_BEFORE_USE:** likely fine, but behavior should be exercised first
- **NEEDS_APPROVAL:** acceptable draft/change, but human signoff is required
- **REWORK:** material issues need revision
- **BLOCK:** unsafe, broken, or inappropriate to proceed

## Escalation Rule
If the issue could cause external embarrassment, customer harm, security exposure, or operational breakage, do not bury it in minor notes. Make the risk explicit.
