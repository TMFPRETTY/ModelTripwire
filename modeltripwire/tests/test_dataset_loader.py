from pathlib import Path

from modeltripwire.evals.dataset_loader import load_prompt_dataset


def test_dataset_loader_reads_baseline_file() -> None:
    project_root = Path(__file__).resolve().parent.parent
    dataset = load_prompt_dataset(project_root / "data" / "prompts" / "baseline_adversarial_prompts.json")
    assert len(dataset) == 10
    assert dataset[0].id == "baseline-001"
