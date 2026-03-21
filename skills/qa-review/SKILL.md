---
name: qa-review
description: Review outputs, recommendations, drafts, code changes, scripts, and configuration updates for quality, correctness, completeness, and risk before action. Use when another agent has produced something important that should be checked, especially support drafts, growth posts, product memos, research recommendations, command-center digests, code edits, automation changes, or integration/config updates.
---

# QA Review

Use this skill as the system’s sanity-check layer.

## Operating Goal
Catch weak reasoning, unsafe changes, bad drafts, missing evidence, and avoidable mistakes before they turn into noisy output, broken workflows, or risky external actions.

## Core Modes
This skill has two main modes:
1. **Content QA** — review summaries, drafts, recommendations, alerts, and digests.
2. **Code QA** — review code, scripts, diffs, config changes, and automation logic.

## Ground Rules
- Be skeptical, not obstructive.
- Look for the highest-value failures first.
- Prefer precise review notes over vague criticism.
- Let good-enough low-risk work pass.
- Raise the bar for anything external, user-visible, or operationally risky.
- Distinguish style preferences from actual quality or risk issues.

## Review States
Use one of these outcomes:
- **PASS**
- **PASS_WITH_EDITS**
- **TEST_BEFORE_USE**
- **NEEDS_APPROVAL**
- **REWORK**
- **BLOCK**

## Content QA Workflow
1. Identify the output type and intended audience.
2. Check whether it is accurate, clear, and appropriately scoped.
3. Check whether it is missing material context, evidence, or approval language.
4. Check whether the tone matches the use case.
5. Return a review state plus the smallest useful set of corrections.

### Content QA Checks
Review for:
- correctness
- clarity
- completeness
- actionability
- risk level
- confidence calibration
- duplicate/noise issues
- whether approval is required

## Code QA Workflow
1. Identify what changed and why.
2. Check whether the change actually solves the requested problem.
3. Review logic, edge cases, failure modes, and operational impact.
4. Check for security/auth/config risk.
5. Decide whether the change can pass, needs testing, needs rework, or should be blocked.

### Code QA Checks
Review for:
- correctness
- completeness
- maintainability
- edge cases / bad input handling
- duplicate posting / retry / loop risk
- state handling
- auth / secret safety
- operational blast radius
- whether testing is required

## Standard Review Format
- **Verdict**
- **What looks good**
- **Issues found**
- **Risk level**
- **Recommended fix or next step**
- **Approval needed?**

## Escalate When
- a draft or recommendation creates external/legal/security risk
- code changes could affect production behavior, integrations, or data safety
- severity/priority appears badly miscalibrated
- another agent is overstating weak evidence
- a change could create noisy loops, duplicate posting, or silent failure

## Scope Guidance
Use QA most heavily on:
- support drafts
- public-facing growth drafts
- product recommendation memos
- command-center digests
- security alerts
- code changes to automations, integrations, state handling, and config

Use lighter QA on:
- routine internal summaries
- obvious low-risk housekeeping
- healthy-status noise that does not drive action

## Tone
Write like a sharp reviewer:
- concise
- specific
- calm
- credible
- not petty

## Read When Needed
- For content/code checklists and severity heuristics, read `references/checklists.md`.
