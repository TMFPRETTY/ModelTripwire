# ModelTripwire

ModelTripwire is an open source AI safety evaluation and red teaming framework for large language models and agentic AI systems. It helps researchers, engineers, and security minded builders detect unsafe behavior, quantify failure modes, and analyze model risk through structured evaluations, adversarial testing, tripwire detection, and reporting.

Rather than making vague claims about whether a model is safe, ModelTripwire provides repeatable mechanisms to probe model behavior under realistic and adversarial conditions, capture outputs, score responses, trigger safety tripwires, and generate interpretable reports. It is designed for research, system validation, guardrail development, and comparative model evaluation.

## Project status

**Current status: Alpha foundation / early Alpha**

ModelTripwire now has a credible Alpha backbone:
- repeatable runs with durable run metadata
- stored run inspection and comparison
- named benchmark suites
- benchmark gate evaluation for Alpha readiness
- regression gates for benchmark-to-benchmark drift

That said, this is **not Beta yet**. The current system is still limited by:
- small benchmark coverage
- mostly rule-based scoring and tripwires
- minimal provider hardening
- limited multi-turn and tool-trace evaluation depth

The practical read is:
- **Alpha:** yes, with a real benchmark/gate/regression foundation
- **Beta:** not yet
- **RC / production-grade:** definitely not yet

## Why this exists

Safety claims are often qualitative, inconsistent, and difficult to reproduce. ModelTripwire is built to make safety evaluation more operational: configurable datasets, modular providers, explicit tripwires, repeatable scoring, durable storage, and exportable reporting.

Core use cases include:
- jailbreak susceptibility testing
- prompt injection resilience analysis
- policy violation and leakage detection
- safe versus unsafe agent architecture comparison
- evidence driven safety reporting and system hardening

## Key capabilities

- Batch evaluation harness for prompt datasets
- Provider abstraction for OpenAI style, Anthropic style, and mock providers
- Baseline adversarial prompt library and prompt mutators
- Rule based safety scoring plus LLM-as-judge scaffold
- Configurable tripwire detection with severity levels
- SQLite persistence and CSV/JSON exports
- Run metadata tracking with run IDs, config hashes, dataset hashes, and git commit capture
- Benchmark suite support for Alpha-style safety packs
- Markdown summaries, comparison reports, and chart generation
- Safe versus unsafe agent demo for architecture comparison

## Architecture overview

```text
Dataset -> Runner -> Provider -> Response
                     -> Scoring
                     -> Tripwires
                     -> Storage
                     -> Reporting
```

Main components:
- `providers/`: model backends
- `evals/`: dataset loading and orchestration
- `scoring/`: rule scoring and judge scaffolding
- `tripwires/`: unsafe behavior detection
- `storage/`: SQLite and export logic
- `reporting/`: summaries, markdown reports, charts
- `agents/`: safe and unsafe agent demo implementations
- `experiments/`: reproducible experiment entry points

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or with requirements style tooling:

```bash
pip install -e .
```

## Configuration

Copy the environment template if you plan to use external APIs:

```bash
cp .env.example .env
```

Default configuration lives in `configs/default.yaml`.

Supported config fields include:
- provider type
- model name
- API key env var names
- dataset path
- output directory
- enabled tripwires
- scorer settings

## Quickstart

The simplest momentum-first path is the local mock baseline run:

```bash
python scripts/run_baseline.py
```

CLI entry points are also available:

```bash
modeltripwire run-baseline --config configs/default.yaml
modeltripwire run-dataset data/prompts/baseline_adversarial_prompts.json --config configs/default.yaml
modeltripwire generate-report outputs/latest/results.json --output-dir outputs/report_regen
modeltripwire list-benchmarks
modeltripwire run-benchmark alpha_core --config configs/default.yaml
modeltripwire list-runs --config configs/default.yaml
modeltripwire show-run <run-id> --config configs/default.yaml
modeltripwire compare-runs <baseline-run-id> <candidate-run-id> --config configs/default.yaml --output-dir outputs/compare
modeltripwire demo-agents --config configs/default.yaml
```

Running `python scripts/run_baseline.py` will:
- load the baseline adversarial dataset
- run every prompt against the mock provider
- print prompt-by-prompt results to the console
- score responses and trigger tripwires
- create a persistent run record with a run ID and run label
- save outputs into `outputs/latest/`

## Benchmark suites

ModelTripwire now includes benchmark suite support for milestone-driven evaluation work.

Current suite:
- `alpha_core`: a first-pass Alpha benchmark pack covering jailbreaks, prompt injection, leakage, tool misuse, and context robustness.

Useful commands:
- `modeltripwire list-benchmarks`
- `modeltripwire run-benchmark alpha_core --config configs/default.yaml`
- `modeltripwire benchmark-report <run-id> --config configs/default.yaml --output-dir outputs/benchmark_reports`
- `modeltripwire benchmark-gate <run-id> --config configs/default.yaml`
- `modeltripwire regression-report <baseline-run-id> <candidate-run-id> --config configs/default.yaml --output-dir outputs/regression_reports`
- `modeltripwire regression-gate <baseline-run-id> <candidate-run-id> --config configs/default.yaml`

Benchmark prompts can carry:
- benchmark suite name
- scenario
- difficulty
- tags

## Run tracking and comparison

ModelTripwire now records each experiment run with:
- run ID and run label
- provider type and model name
- dataset path and dataset hash
- config path and config hash
- git commit when available
- start and completion timestamps

Useful commands:
- `modeltripwire list-runs --config configs/default.yaml`
- `modeltripwire show-run <run-id> --config configs/default.yaml`
- `modeltripwire compare-runs <baseline-run-id> <candidate-run-id> --config configs/default.yaml --output-dir outputs/compare`

This makes it possible to inspect prior runs and generate markdown comparison reports between two stored runs.

## Current implemented phases

### Phase 1: README and project narrative
Implemented. The repo documents the purpose, architecture, quickstart, and responsible-use framing.

### Phase 2: Mock provider and dataset loader
Implemented. The repository includes a runnable mock provider plus JSON dataset loading for adversarial prompt cases. The loader accepts datasets that use either `prompt_text` or `prompt` as the prompt field.

### Phase 3: Baseline experiment
Implemented. `python scripts/run_baseline.py` runs an end-to-end mock evaluation and saves outputs in `outputs/latest/`.

### Phase 4: Tripwires and simple scoring
Implemented. Each response is evaluated with rule-based scoring and keyword tripwires, then persisted into exports and SQLite.

### Phase 5: Real provider integrations
Implemented as modular provider adapters for OpenAI-style and Anthropic-style APIs, gated by environment variables.

### Phase 6: Run metadata and comparison foundations
Implemented. Baseline and dataset runs now persist run metadata in SQLite, summaries include run identifiers, and the CLI can list, inspect, and compare stored runs.

### Phase 7: Benchmark suite foundations
Implemented. Benchmark-aware prompt metadata, an initial `alpha_core` benchmark suite, and CLI support for listing and running benchmark packs are now in place.

### Phase 8: Alpha benchmark gating foundations
Implemented. Benchmark thresholds can now be evaluated against stored benchmark runs, with pass/fail gate output and markdown gate reports.

### Phase 9: Regression gate foundations
Implemented. Stored benchmark runs can now be compared with explicit regression limits and pass/fail regression gates, plus markdown regression reports.

## Baseline experiment

The included baseline experiment is titled:

**Baseline Safety Stress Test of General Purpose LLMs Under Adversarial Prompting**

Research question:

**How consistently do general purpose LLMs resist common adversarial prompt patterns across jailbreak, injection, leakage, escalation, and agent misuse scenarios?**

The experiment:
- loads 10 baseline adversarial prompts
- runs prompts against a configured provider
- scores responses
- applies tripwires
- stores structured results
- exports JSON and CSV
- generates markdown summaries and charts

## Safe versus unsafe agent demo

The demo contrasts two agent architectures:
- `UnsafeAgent`: forwards user input directly to the provider
- `SafeAgent`: applies input filtering, policy checks, output filtering, and structured logging

This is intentionally simple, but useful for illustrating why architecture matters even when the underlying model is unchanged.

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
    benchmark_runner.py
    benchmarks.py
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
- better comparative analytics across models/providers

### To reach release candidate
- frozen benchmark sets and release gates
- CI benchmark workflows
- clearer documentation and contributor guidance
- stronger reproducibility guarantees
- broader validation across real providers and benchmark suites

## Ethical use and limitations

ModelTripwire is designed for defensive research, system hardening, and safety evaluation. It should be used to improve safeguards, not to operationalize harmful behavior. Included prompts reflect realistic adversarial patterns, but the framework is intentionally conservative about response handling, scoring, and reporting. Any use with external models should respect provider terms, legal boundaries, and responsible disclosure norms.
