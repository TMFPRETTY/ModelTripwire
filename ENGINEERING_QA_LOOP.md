# ENGINEERING_QA_LOOP.md

## Purpose
This document defines the closed-loop workflow between engineering and QA for code, automation, integration, and configuration work.

## Core Rule
A task is not truly done when engineering finishes coding.
A task is done when it has either:
- passed QA,
- been explicitly approved,
- or been intentionally stopped.

## Workflow

### 1. Intake
Engineering receives a request.
Capture:
- system
- task
- why it matters
- constraints
- done criteria
- urgency

### 2. Plan
Engineering creates a short implementation plan when needed.
Include:
- likely files/systems touched
- obvious risks
- whether testing is needed
- whether QA should be mandatory

### 3. Execute
Engineering implements the change.
Possible outputs:
- code change
- config change
- automation change
- script update
- workflow/prompt adjustment with engineering impact

### 4. QA Review
QA reviews the result.

QA checks for:
- correctness
- completeness
- edge cases
- config/auth safety
- retry / duplicate / loop risk
- maintainability
- user-visible risk
- whether testing is needed before use

### 5. QA Verdict
QA returns one of:
- `PASS`
- `PASS_WITH_EDITS`
- `TEST_BEFORE_USE`
- `NEEDS_APPROVAL`
- `REWORK`
- `BLOCK`

## Routing Rules

### If QA returns `PASS`
- mark item ready / done
- hand back to originating room if needed

### If QA returns `PASS_WITH_EDITS`
- engineering applies the specified small edits
- optionally return to QA if the edits materially affect the outcome

### If QA returns `TEST_BEFORE_USE`
- run or request the required test
- return to QA or mark ready pending successful test

### If QA returns `NEEDS_APPROVAL`
- surface the item for human approval
- do not continue automatically into risky deployment/use

### If QA returns `REWORK`
- route back to engineering
- include exact failure reasons and requested fixes
- engineering revises and returns it to QA

### If QA returns `BLOCK`
- stop progression
- surface the risk clearly
- require a new approach or explicit human decision

## State Labels
Use these labels where helpful:
- `INTAKE`
- `PLANNING`
- `IN_PROGRESS`
- `NEEDS_QA`
- `REWORK`
- `TESTING`
- `NEEDS_APPROVAL`
- `BLOCKED`
- `DONE`

## When QA Is Mandatory
QA should automatically review:
- automation logic
- integration changes
- state-file handling
- prompt/workflow changes that affect live outputs
- config changes with operational impact
- code that may create duplicate posting, silent failures, auth breakage, or destructive behavior

## When Lightweight QA Is Enough
Lighter QA is acceptable for:
- tiny low-risk copy/format changes
- internal-only notes with no operational impact
- safe refactors with clearly bounded scope

## Relationship To Rooms
- originating business room defines the need
- engineering implements
- QA validates
- engineering reworks if needed
- final result returns to the owning room or command-center when appropriate

Examples:
- Signal and Circuit identifies a site/tooling need -> engineering implements -> QA reviews -> result returns to Signal and Circuit if approved
- Caruso product or growth identifies a workflow/tooling/build need -> engineering implements -> QA reviews -> result returns to the owning Caruso room if approved
- Ops or security finds an implementation/config issue -> engineering implements -> QA reviews before the work is considered done

## Bottom Line
The intended loop is:

Engineering → QA → Engineering (if needed) → QA → Done/Approval

Not one-pass coding and hope.

For this workspace, treat that loop as the default for code work, automation work, config changes, integration changes, and other engineering-impact changes.
