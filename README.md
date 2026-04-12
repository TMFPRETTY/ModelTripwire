<div align="center">

# ModelTripwire

### Safety evaluation, adversarial testing, benchmark gates, and regression tracking for LLMs and agentic systems

[![Status: Alpha Foundation](https://img.shields.io/badge/status-alpha_foundation-2563eb)](#project-status)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](#installation)
[![License](https://img.shields.io/badge/license-see%20LICENSE-111827)](#license)
[![Benchmarks](https://img.shields.io/badge/benchmarks-alpha__core-7c3aed)](#benchmark-workflow)
[![Gates](https://img.shields.io/badge/gates-alpha%20%2B%20regression-059669)](#alpha-gate-workflow)

*Operational safety evaluation with durable runs, benchmark suites, pass/fail gates, and regression-aware reporting.*

</div>

---

## Table of contents

- [Why ModelTripwire](#why-modeltripwire)
- [Project status](#project-status)
- [Alpha release](#alpha-release)
- [Why it stands out](#why-it-stands-out)
- [Feature highlights](#feature-highlights)
- [Architecture overview](#architecture-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quickstart](#quickstart)
- [Benchmark workflow](#benchmark-workflow)
- [Run tracking and comparison workflow](#run-tracking-and-comparison-workflow)
- [Alpha gate workflow](#alpha-gate-workflow)
- [Repeated trials and benchmark trends](#repeated-trials-and-benchmark-trends)
- [Example workflow](#example-workflow)
- [Sample output](#sample-output)
- [Safe vs unsafe agent demo](#safe-vs-unsafe-agent-demo)
- [Project structure](#project-structure)
- [Roadmap from here](#roadmap-from-here)
- [Contributing](#contributing)
- [Responsible use](#responsible-use)
- [License](#license)

---

## Why ModelTripwire

ModelTripwire is an open source AI safety evaluation and red teaming framework for large language models and agentic AI systems. It helps researchers, engineers, and security-minded builders detect unsafe behavior, quantify failure modes, track benchmark performance, and analyze model risk through structured evaluations, adversarial testing, tripwire detection, and reporting.

Rather than making vague claims about whether a model is safe, ModelTripwire provides repeatable mechanisms to:
- probe model behavior under realistic and adversarial conditions
- capture outputs and score behavior consistently
- trigger interpretable safety tripwires
- persist runs and inspect history over time
- benchmark milestone readiness
- detect regressions between stored benchmark runs

This repo is aimed at teams who want safety evaluation to feel more like engineering and less like hand-wavy commentary.

---

## Project status

> **Current status: Alpha foundation / early Alpha**

ModelTripwire now has a credible Alpha backbone:
- repeatable runs with durable run metadata
- stored run inspection and comparison
- named benchmark suites
- benchmark gate evaluation for Alpha readiness
- regression gates for benchmark-to-benchmark drift
- repeated benchmark trials and trend summaries across stored runs

**Plain-English maturity read:**
- **Alpha:** complete / ready to present as an Alpha release
- **Beta:** not yet
- **RC / production-grade:** not yet

**Current limitations:**
- scoring and tripwires are still mostly rule-based
- provider hardening is still minimal
- multi-turn and tool-trace evaluation depth is still limited
- broader provider validation is still needed before Beta claims

---

## Alpha release

ModelTripwire is now in a strong Alpha-release state.

### What is included in Alpha
- adversarial benchmark suites for core and extended safety scenarios
- scenario-aware reporting and benchmark breakdowns
- durable run storage with run IDs, labels, hashes, and git commit capture
- benchmark gate evaluation for milestone readiness
- regression gates for benchmark-to-benchmark drift
- repeated benchmark trials and trend summaries across stored runs
- markdown, JSON, CSV, and chart-based reporting outputs

### What Alpha means here
Alpha means the project now has a credible benchmark-driven evaluation loop, not just one-off prompt testing.

It is strong enough for:
- internal model safety validation
- adversarial benchmark iteration
- release-gate experimentation
- comparing repeated runs over time

It is not yet claiming:
- Beta-grade scorer sophistication
- production-hardened provider orchestration
- fully mature multi-turn agent evaluation
- final release-candidate stability guarantees

---

## Why it stands out

A lot of AI safety tooling can produce outputs. Far fewer tools give you a clean path from **evaluation** to **decision**.

ModelTripwire stands out because it combines:
- **durable run records** instead of ephemeral notebook output
- **benchmark suites** instead of one-off prompt pokes
- **Alpha pass/fail gates** instead of vague interpretation
- **regression gates** instead of “it seems worse than before”
- **human-readable markdown reports** alongside machine-friendly exports

The goal is not just to test a model once. The goal is to build a workflow that can support release quality judgments over time.

---

## Feature highlights

### Evaluation framework
- prompt dataset loading
- batch evaluation runner
- provider abstraction for mock, OpenAI-style, and Anthropic-style backends
- scenario-aware prompt metadata

### Safety analysis
- rule-based scoring
- keyword-driven tripwires
- scenario breakdowns
- benchmark breakdowns
- notable failure extraction

### Run management
- persistent run IDs and run labels
- config hash capture
- dataset hash capture
- git commit capture when available
- SQLite-backed run/result persistence

### Reporting
- JSON and CSV exports
- markdown reports
- category and scenario charts
- run comparison reports
- benchmark gate reports
- regression gate reports

### Benchmarking
- named benchmark suites
- Alpha benchmark pack support
- benchmark pass/fail gates
- regression gates between benchmark runs

---

## Architecture overview

```text
Dataset / Benchmark Suite
        -> Runner
        -> Provider
        -> Response
        -> Scoring
        -> Tripwires
        -> Storage
        -> Reports / Charts / Gates
```

Main components:
- `providers/` model backends
- `evals/` dataset loading and orchestration
- `scoring/` scoring logic and future judge scaffolding
- `tripwires/` unsafe behavior detection logic
- `storage/` SQLite persistence and exports
- `reporting/` summaries, markdown reports, comparison reports, charts
- `agents/` safe and unsafe agent demos
- `experiments/` reproducible experiment entry points
- `benchmarks.py` benchmark suite registry
- `benchmark_gates.py` benchmark pass/fail logic
- `regression_gates.py` benchmark drift/regression logic

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or simply:

```bash
pip install -e .
```

If you plan to use external APIs:

```bash
cp .env.example .env
```

---

## Configuration

Default configuration lives in:

```bash
configs/default.yaml
```

Supported config areas include:
- provider type and model name
- API key environment variable names
- dataset path
- output directory
- SQLite path
- enabled tripwires
- scoring settings
- reporting title and research question

---

## Quickstart

The fastest way to get momentum is the local mock baseline:

```bash
python scripts/run_baseline.py
```

You can also use the CLI directly:

```bash
modeltripwire run-baseline --config configs/default.yaml
modeltripwire run-dataset data/prompts/baseline_adversarial_prompts.json --config configs/default.yaml
modeltripwire generate-report outputs/latest/results.json --output-dir outputs/report_regen
```

**What the baseline run does:**
- loads the baseline adversarial dataset
- runs prompts against the configured provider
- scores responses
- evaluates tripwires
- persists a run record
- exports JSON and CSV
- writes a markdown report
- generates charts

---

## Benchmark workflow

ModelTripwire includes benchmark suite support for milestone-driven evaluation.

### Available benchmark commands

```bash
modeltripwire list-benchmarks
modeltripwire run-benchmark alpha_core --config configs/default.yaml
modeltripwire benchmark-report <run-id> --config configs/default.yaml --output-dir outputs/benchmark_reports
modeltripwire benchmark-gate <run-id> --config configs/default.yaml
```

### Current benchmark suites

**`alpha_core`**  
First-pass Alpha benchmark pack covering:
- jailbreaks
- prompt injection
- leakage
- unsafe tool requests
- context robustness

**`alpha_extended`**  
Stronger Alpha-hardening pack covering:
- social engineering escalation
- audit-pretext extraction
- bulk sensitive export requests
- late-turn policy drift
- reasoning exposure probes
- research-pretext harmful assistance

### Benchmark prompt metadata

Benchmark prompts can carry:
- benchmark suite name
- scenario
- difficulty
- tags
- expected risk type

---

## Run tracking and comparison workflow

### Run inspection

```bash
modeltripwire list-runs --config configs/default.yaml
modeltripwire show-run <run-id> --config configs/default.yaml
```

### Run comparison

```bash
modeltripwire compare-runs <baseline-run-id> <candidate-run-id> --config configs/default.yaml --output-dir outputs/compare
```

Each run can persist:
- run ID
- run label
- provider type
- model name
- dataset path
- dataset hash
- config path
- config hash
- git commit
- started/completed timestamps

---

## Alpha gate workflow

### Benchmark gate

Use benchmark gates to ask, **“does this run meet the current Alpha threshold?”**

```bash
modeltripwire benchmark-gate <run-id> --config configs/default.yaml
modeltripwire benchmark-report <run-id> --config configs/default.yaml --output-dir outputs/benchmark_reports
```

Current Alpha gate foundations include checks for:
- minimum mean refusal score
- maximum mean compliance score
- maximum mean tripwire count
- minimum benchmark pass rate
- per-case compliance and tripwire limits
- per-scenario thresholds for refusal, compliance, and tripwire counts

### Regression gate

Use regression gates to ask, **“did this candidate get worse than the baseline?”**

```bash
modeltripwire regression-gate <baseline-run-id> <candidate-run-id> --config configs/default.yaml
modeltripwire regression-report <baseline-run-id> <candidate-run-id> --config configs/default.yaml --output-dir outputs/regression_reports
```

Current regression checks include:
- refusal score drop
- compliance score increase
- tripwire count increase
- pass-rate drop
- scenario-level drift summary

---

## Repeated trials and benchmark trends

ModelTripwire now supports running repeated benchmark trials and summarizing trend stability across recent stored runs.

### Repeated benchmark trials

```bash
modeltripwire run-benchmark-trials alpha_core --trials 3 --config configs/default.yaml
modeltripwire run-benchmark-trials alpha_extended --trials 3 --config configs/default.yaml
```

### Benchmark trend summaries

```bash
modeltripwire benchmark-trends alpha_core --limit 10 --config configs/default.yaml --output-dir outputs/benchmark_trends
modeltripwire benchmark-trends alpha_extended --limit 10 --config configs/default.yaml --output-dir outputs/benchmark_trends
```

Trend summaries roll up:
- pass rate stability across repeated runs
- average refusal, compliance, and tripwire metrics
- scenario-level pass fractions across recent runs
- recent benchmark run history in one report

---

## Example workflow

```bash
# 1. Run a benchmark
modeltripwire run-benchmark alpha_core --config configs/default.yaml

# 2. Inspect stored runs
modeltripwire list-runs --config configs/default.yaml

# 3. Gate a benchmark run
modeltripwire benchmark-gate <run-id> --config configs/default.yaml

# 4. Compare two benchmark runs
modeltripwire regression-gate <baseline-run-id> <candidate-run-id> --config configs/default.yaml

# 5. Run repeated trials and inspect trend stability
modeltripwire run-benchmark-trials alpha_extended --trials 3 --config configs/default.yaml
modeltripwire benchmark-trends alpha_extended --limit 3 --config configs/default.yaml
```

---

## Sample output

### Example benchmark gate result

```json
{
  "suite_name": "alpha_core",
  "passed": true,
  "checks": {
    "min_mean_refusal_score": true,
    "max_mean_compliance_score": true,
    "max_mean_tripwire_count": true,
    "min_pass_rate": true
  }
}
```

### Example regression gate result

```json
{
  "suite_name": "alpha_core",
  "passed": true,
  "deltas": {
    "refusal_drop": 0.0,
    "compliance_increase": 0.0,
    "tripwire_increase": 0.0,
    "pass_rate_drop": 0.0
  }
}
```

This is the shape of output intended to support milestone decisions, not just exploratory inspection.

---

## Safe vs unsafe agent demo

The repo includes a small architectural demo:
- `UnsafeAgent` forwards user input directly to the provider
- `SafeAgent` applies input checks, output checks, and structured logging

Run it with:

```bash
modeltripwire demo-agents --config configs/default.yaml
```

This demo is intentionally simple, but it helps illustrate how surrounding architecture changes safety outcomes even when the underlying model stays the same.

---

## Project structure

```text
modeltripwire/
  README.md
  pyproject.toml
  .env.example
  configs/
    default.yaml
  modeltripwire/
    __init__.py
    cli.py
    config.py
    logging_utils.py
    benchmark_runner.py
    benchmarks.py
    benchmark_gates.py
    regression_gates.py
    models/
      __init__.py
      schemas.py
    providers/
      __init__.py
      base.py
      openai_provider.py
      anthropic_provider.py
      mock_provider.py
    evals/
      __init__.py
      runner.py
      dataset_loader.py
    redteam/
      __init__.py
      prompts.py
      mutators.py
    scoring/
      __init__.py
      rules.py
      judge.py
    tripwires/
      __init__.py
      base.py
      rules.py
    storage/
      __init__.py
      sqlite_store.py
      export.py
    reporting/
      __init__.py
      summaries.py
      markdown_report.py
      charts.py
      compare.py
    agents/
      __init__.py
      unsafe_agent.py
      safe_agent.py
      filters.py
    experiments/
      __init__.py
      baseline_safety_stress_test.py
  data/
    prompts/
      baseline_adversarial_prompts.json
    benchmarks/
      alpha_core.json
  outputs/
  notebooks/
    baseline_analysis.ipynb
  scripts/
    run_baseline.py
  tests/
    test_tripwires.py
    test_scoring.py
    test_runner.py
    test_runs.py
    test_cli_runs.py
    test_benchmarks.py
    test_benchmark_gates.py
    test_regression_gates.py
```

---

## Roadmap from here

### To strengthen Alpha
- add benchmark trend views across repeated runs
- tighten scenario thresholds further with real-provider evidence
- add repeated-trial support for score stability
- expand failure analysis and benchmark comparison summaries

### To reach Beta
- stronger scorers beyond keyword heuristics
- richer tripwire logic and confidence handling
- multi-turn benchmark flows
- stronger provider reliability, retries, and normalization
- better comparative analytics across models and providers

### After Alpha
- calibrate gates against real-provider variability
- add repeated-trial stability thresholds
- strengthen failure analysis and richer benchmark comparisons
- expand benchmark packs further for tougher release gating

### To reach release candidate
- frozen benchmark sets and release gates
- CI benchmark workflows
- clearer documentation and contributor guidance
- stronger reproducibility guarantees
- broader validation across real providers and benchmark suites

---

## Contributing

Contributions are welcome, especially in these areas:
- new benchmark packs
- more realistic adversarial datasets
- stronger tripwire logic
- judge-based scoring
- provider integrations
- comparison and reporting improvements
- CI and reproducibility workflows

If you contribute, favor:
- small, testable changes
- benchmark-aware additions
- explicit reporting and reproducibility
- defensive and responsible safety framing

## Responsible use

ModelTripwire is designed for defensive research, system hardening, and safety evaluation. It should be used to improve safeguards, not to operationalize harmful behavior.

Included prompts reflect realistic adversarial patterns, but the framework is intentionally conservative about response handling, scoring, and reporting. Any use with external models should respect provider terms, legal boundaries, and responsible disclosure norms.

---

## License

See `LICENSE`.
