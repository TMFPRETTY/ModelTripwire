# ModelTripwire

ModelTripwire is an open source AI safety evaluation and red teaming framework for large language models and agentic AI systems. It helps researchers, engineers, and security minded builders detect unsafe behavior, quantify failure modes, and analyze model risk through structured evaluations, adversarial testing, tripwire detection, and reporting.

Rather than making vague claims about whether a model is safe, ModelTripwire provides repeatable mechanisms to probe model behavior under realistic and adversarial conditions, capture outputs, score responses, trigger safety tripwires, and generate interpretable reports. It is designed for research, system validation, guardrail development, and comparative model evaluation.

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
- Markdown summaries and chart generation
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

Run the baseline experiment with the mock provider:

```bash
modeltripwire run-baseline --config configs/default.yaml
```

Run a specific dataset:

```bash
modeltripwire run-dataset data/prompts/baseline_adversarial_prompts.json --config configs/default.yaml
```

Generate a report from prior results:

```bash
modeltripwire generate-report outputs/latest/results.json --output-dir outputs/report_regen
```

Run the safe versus unsafe agent demo:

```bash
modeltripwire demo-agents --config configs/default.yaml
```

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
  outputs/
  notebooks/
    baseline_analysis.ipynb
  scripts/
    run_baseline.py
  tests/
    test_tripwires.py
    test_scoring.py
    test_runner.py
```

## Future roadmap

- Additional provider integrations
- More robust mutators and multi turn attack chains
- Ensemble tripwire logic and policy packs
- Comparative dashboards across models and runs
- Statistical analysis helpers for repeated trials
- CI-ready benchmark workflows

## Ethical use and limitations

ModelTripwire is designed for defensive research, system hardening, and safety evaluation. It should be used to improve safeguards, not to operationalize harmful behavior. Included prompts reflect realistic adversarial patterns, but the framework is intentionally conservative about response handling, scoring, and reporting. Any use with external models should respect provider terms, legal boundaries, and responsible disclosure norms.
