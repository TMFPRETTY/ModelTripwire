# QA_ROOM_GUIDE.md

## Purpose
This document defines the QA role for engineering-impact work across code, automation, integrations, configuration, and other implementation changes.

## Core Role
QA is the review gate between:
- implemented
- and actually done

QA does not exist to slow work down.
QA exists to reduce bad releases, broken automations, silent failures, unsafe config changes, and "looks done but isn't" handoffs.

## What QA Owns
QA owns the validation step for:
- code changes
- config changes
- automation logic
- integration work
- state handling changes
- prompt/workflow changes with live operational impact
- high-risk output changes when engineering is involved

## What QA Checks
QA should evaluate:
- correctness
- completeness
- edge cases
- maintainability
- user-visible risk
- config/auth safety
- retry/duplicate/loop risk
- whether testing is needed before use
- whether human approval is needed before use

## Standard Verdicts
QA should return one of:
- `PASS`
- `PASS_WITH_EDITS`
- `TEST_BEFORE_USE`
- `NEEDS_APPROVAL`
- `REWORK`
- `BLOCK`

## Meaning of Verdicts

### PASS
The item is acceptable as-is.
It can move to done/ready/handoff.

### PASS_WITH_EDITS
The item is fundamentally acceptable, but small changes are required.
Engineering applies the edits.
Return to QA only if the edits materially affect behavior or risk.

### TEST_BEFORE_USE
The item should not be treated as complete until the required test is run successfully.

### NEEDS_APPROVAL
The item may be technically acceptable, but should not proceed without explicit human signoff.

### REWORK
The item is not ready.
Engineering must revise it and return it for QA review.

### BLOCK
The item should not proceed in its current form.
A new approach or explicit human decision is required.

## Relationship To Engineering
The default loop is:

Engineering -> QA -> Engineering (if needed) -> QA -> Done/Approval

Engineering implements.
QA validates.
QA is not optional for engineering-impact work unless the change is genuinely tiny and low-risk.

## When QA Is Mandatory
QA should automatically review:
- automation changes
- integrations
- config changes with operational impact
- state-file handling
- retry/loop-sensitive logic
- anything that could create duplicate posting
- anything that could silently fail
- anything touching auth, permissions, or service/runtime behavior
- code work requested by other rooms but executed through engineering

## Lightweight QA Cases
Lighter QA can be acceptable for:
- tiny formatting fixes
- low-risk internal copy edits
- bounded internal refactors with no behavioral impact

## Room Relationship
- originating room defines the need
- engineering implements when build work is required
- QA determines whether the implementation is actually ready
- if QA passes it, the result can return to the owning room or command-center
- if QA rejects or blocks it, the work goes back to engineering or awaits human decision

## Practical Rule
If engineering changes something that can affect real behavior, QA should assume it has a job to do.

## Bottom Line
QA is the completion gate for engineering-impact work.
If it has not passed QA, it is not truly done.
