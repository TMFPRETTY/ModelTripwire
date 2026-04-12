from pathlib import Path

from modeltripwire.config import load_config
from modeltripwire.experiments.baseline_safety_stress_test import run_baseline_experiment


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    config = load_config(project_root / "configs/default.yaml")
    run_baseline_experiment(config, project_root)
