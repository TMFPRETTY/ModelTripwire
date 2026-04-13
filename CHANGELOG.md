# Changelog

## Unreleased

### Release-decision workflow improvements
- Added explicit RC-style release gating layered on top of benchmark and trend gates
- Added `rc-review-bundle` so one command can generate benchmark, trend, RC, case-review, and HTML release-review artifacts together
- Promoted the RC bundle path in the dashboard and README as the default operator review flow

### Real-provider findings and evaluator status
- Confirmed that current OpenAI `beta_core` validation still fails strict RC gating even though the framework review flow is now much stronger
- Calibrated several false-positive scoring and tripwire paths, especially around safe hidden-instruction refusals and defensive sensitive-export refusals
- Current status is intentionally framed as: strong Framework Beta operator surface, but not yet RC-grade real-provider passing behavior

## 0.2.0-beta.2

Production-hardening checkpoint on top of Framework Beta.

### Highlights
- Persisted evaluator trace across benchmark runs, including separate rule, judge, and blended scorecards
- Added frozen benchmark version/hash metadata to run records and surfaced that metadata in `show-run`
- Added provider comparison reporting for side-by-side benchmark review across runs
- Added operational decision summaries across reports, benchmark gates, trend gates, and comparison outputs
- Added HTML operator reports with embedded benchmark/trend gate panels
- Added HTML case drill-down pages with richer evaluator trace visibility for notable failures

### Reporting and operator workflow improvements
- Added `html-report <run_id>` CLI support for generating operator-facing HTML reports from stored runs
- Added gate panels to HTML output so a single page can show benchmark/trend status, recommended action, and reasons
- Added case drill-down HTML pages linked from the main HTML report for notable failures
- Expanded README workflow coverage for HTML reports, provider comparison reports, benchmark freezing metadata, and evaluator traceability

### Production-readiness improvements
- Decision-oriented reporting is now more consistent across summaries, benchmark gates, trend gates, run inspection, and comparison surfaces
- Benchmark runs now persist explicit benchmark version, dataset hash, and dataset path metadata for reproducibility
- Evaluator trace persistence makes rule/judge/blended scoring auditable in stored runs and review flows

## 0.2.0-beta.1

Framework Beta release.

### Highlights
- Introduced explicit Beta benchmark coverage with `beta_core`
- Added benchmark trend summaries and trend stability gates
- Added CI and release-readiness GitHub Actions workflows
- Calibrated scoring and tripwire logic against real OpenAI benchmark findings
- Added local-only real-provider validation workflow using safe non-committed config files

### Benchmark and gating improvements
- Added `beta_core` benchmark scenarios for phishing escalation, hidden-instruction extraction, sensitive export trust buildup, and reasoning exposure
- Added `trend-gate` and `trend-report` CLI workflows for repeated-run stability checks
- Strengthened scenario-aware scoring and reporting fidelity

### Real-provider calibration findings
- Real OpenAI validation works end to end with local-only config and environment-managed API credentials
- Current OpenAI `beta_core` calibration now more cleanly isolates the main remaining provider failures in phishing escalation and trust-buildup sensitive export scenarios
- Hidden-instruction and reasoning-exposure evaluation paths were refined so safe summaries and generic explanations are less likely to be mislabeled as true leakage
- Added case-level benchmark verdicts and dedicated benchmark case review reports to make provider calibration and evaluator tuning more actionable

### Automation
- Added `CI` workflow for tests plus `beta_core` mock smoke validation
- Added `Release Readiness` workflow for repeated benchmark trials and trend-report artifact generation

### Framing
- ModelTripwire is now framed as a Framework Beta release rather than a blanket claim that tested providers already pass the Beta benchmark bar
- Real-provider failures are part of the product story: the framework is Beta, while tested providers may still fail strict benchmark thresholds
