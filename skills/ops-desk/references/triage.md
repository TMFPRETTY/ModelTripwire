# Ops Desk Triage

## Priority Order
In most situations, rank ops attention like this:
1. blockers to current execution
2. repeated failures or shared infra/auth issues
3. pending approvals that stop work
4. growing queues or stale items
5. optimization / cleanup items

## Stale Work Patterns
Surface stale work when:
- a task has no owner
- a queue item sits without movement past the expected cadence
- a follow-up was promised but not delivered
- approvals have been waiting long enough to affect timing

## Escalation Heuristic
Send to command-center when the issue is:
- cross-room
- time-sensitive
- risky
- dependent on Jeremy
- likely to affect the day’s priorities

Keep it in ops-desk when the issue is local, recoverable, and already has a clear owner.

## Compression Rule
If five alerts all reflect the same root problem, write one summary item naming the root problem and impact instead of five separate bullets.
