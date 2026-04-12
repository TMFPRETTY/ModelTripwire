from pathlib import Path

from modeltripwire.config import load_config
from modeltripwire.experiments.baseline_safety_stress_test import run_baseline_experiment


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    result = run_baseline_experiment(config, project_root)

    print("ModelTripwire baseline complete")
    print(f"Output directory: {result['output_dir']}")
    print()
    for item in result["results"]:
        print(f"[{item.prompt_case.category}] {item.prompt_case.name}")
        print(f"  response: {item.provider_response.content}")
        print(
            "  scores:",
            {
                "refusal": item.scorecard.refusal_score,
                "compliance": item.scorecard.compliance_score,
                "leakage": item.scorecard.leakage_score,
                "harmfulness": item.scorecard.harmfulness_score,
            },
        )
        print(f"  tripwires: {[match.name for match in item.tripwires_triggered]}\n")
