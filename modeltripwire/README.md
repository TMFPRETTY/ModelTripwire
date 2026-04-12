# ModelTripwire

> Safety evaluation, adversarial testing, benchmark gating, and regression tracking for LLMs and agentic systems.

ModelTripwire is an open source AI safety evaluation and red teaming framework for large language models and agentic AI systems. It helps researchers, engineers, and security-minded builders detect unsafe behavior, quantify failure modes, track benchmark performance, and analyze model risk through structured evaluations, adversarial testing, tripwire detection, and reporting.

Rather than making vague claims about whether a model is safe, ModelTripwire provides repeatable mechanisms to probe model behavior under realistic and adversarial conditions, capture outputs, score responses, trigger safety tripwires, persist runs, compare results over time, and generate interpretable reports.

---

## Why ModelTripwire exists

Safety work often breaks down in practice because teams lack one or more of these:
- repeatable datasets
- durable run records
- interpretable scoring
- explicit tripwires
- benchmark gates
- regression detection over time

ModelTripwire is built to make safety evaluation more operational.

Core use cases:
- jailbreak susceptibility testing
- prompt injection resilience analysis
- system prompt leakage checks
- policy violation detection
- tool misuse and agent safety evaluation
- benchmark-based milestone tracking
- regression detection across stored runs
- safe versus unsafe agent architecture comparison

---

## Project status

**Current status: Alpha foundation / early Alpha**

ModelTripwire now has a credible Alpha backbone:
- repeatable runs with durable run metadata
- stored run inspection and comparison
- named benchmark suites
- benchmark gate evaluation for Alpha readiness
- regression gates for benchmark-to-benchmark drift

What that means in plain English:
- **Alpha:** yes, this is fair
- **Beta:** not yet
- **RC / production-grade:** not yet

Current limitations:
- benchmark coverage is still small
- scoring and tripwires are still mostly rule-based
- provider hardening is still minimal
- multi-turn and tool-trace evaluation depth is still limited

---

## What you get today

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

## Key capabilities at a glance

| Capability | Status |
|---|---|
| Baseline dataset evaluation | Implemented |
| Mock provider | Implemented |
| OpenAI-style provider | Implemented |
| Anthropic-style provider | Implemented |
| Rule-based scoring | Implemented |
| Keyword tripwires | Implemented |
| Run persistence | Implemented |
| Run comparison | Implemented |
| Benchmark suites | Implemented |
| Alpha benchmark gates | Implemented |
| Regression gates | Implemented |
| Multi-turn benchmark packs | Planned |
| Judge-model scoring | Planned |
| CI release gates | Planned |

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

What the baseline run does:
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

### Current benchmark suite

- `alpha_core`  
  First-pass Alpha benchmark pack covering:
  - jailbreaks
  - prompt injection
  - leakage
  - unsafe tool requests
  - context robustness

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

Use benchmark gates to ask, “does this run meet the current Alpha threshold?”

```bash
modeltripwire benchmark-gate <run-id> --config configs/default.yaml
modeltripwire benchmark-report <run-id> --config configs/default.yaml --output-dir outputs/benchmark_reports
```

Current Alpha gate foundations include checks for:
- minimum mean refusal score
- maximum mean compliance score
- maximum mean tripwire count
- minimum benchmark pass rate
- per-case compliance/tripwire limits

### Regression gate

Use regression gates to ask, “did this candidate get worse than the baseline?”

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
```

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

## Current implemented phases

### Phase 1: README and project narrative
Implemented.

### Phase 2: Mock provider and dataset loader
Implemented.

### Phase 3: Baseline experiment
Implemented.

### Phase 4: Tripwires and simple scoring
Implemented.

### Phase 5: Real provider integrations
Implemented.

### Phase 6: Run metadata and comparison foundations
Implemented.

### Phase 7: Benchmark suite foundations
Implemented.

### Phase 8: Alpha benchmark gating foundations
Implemented.

### Phase 9: Regression gate foundations
Implemented.

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
- expand benchmark coverage
- add harder scenario packs and stricter suite thresholds
- improve per-scenario gate specificity
- add benchmark trend views across repeated runs

### To reach Beta
- stronger scorers beyond keyword heuristics
- richer tripwire logic and confidence handling
- multi-turn benchmark flows
- stronger provider reliability, retries, and normalization
- better comparative analytics across models and providers

### To reach release candidate
- frozen benchmark sets and release gates
- CI benchmark workflows
- clearer documentation and contributor guidance
- stronger reproducibility guarantees
- broader validation across real providers and benchmark suites

---

## Responsible use

ModelTripwire is designed for defensive research, system hardening, and safety evaluation. It should be used to improve safeguards, not to operationalize harmful behavior.

Included prompts reflect realistic adversarial patterns, but the framework is intentionally conservative about response handling, scoring, and reporting. Any use with external models should respect provider terms, legal boundaries, and responsible disclosure norms.

---

## License

See `LICENSE`.
