# Changelog

## 0.2.0-beta.1

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
- Current OpenAI `beta_core` results still show meaningful failures in phishing escalation and trust-buildup sensitive export scenarios
- Scoring/tripwire calibration was improved to better distinguish real unsafe assistance from safe denials and generic reasoning explanations

### Automation
- Added `CI` workflow for tests plus `beta_core` mock smoke validation
- Added `Release Readiness` workflow for repeated benchmark trials and trend-report artifact generation

### Framing
- ModelTripwire is now best described as a framework Beta candidate rather than a blanket claim that tested providers already pass the Beta benchmark bar
