from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd

from modeltripwire.models.schemas import EvaluationResult


def generate_all_charts(results: Iterable[EvaluationResult], output_dir: str | Path) -> list[Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "category": item.prompt_case.category,
            "tripwire_count": item.tripwire_count,
            "refusal_score": item.scorecard.refusal_score,
            "compliance_score": item.scorecard.compliance_score,
            "max_severity": item.max_severity,
        }
        for item in results
    ]
    frame = pd.DataFrame(rows)
    if frame.empty:
        return []

    paths = []

    chart1 = output / "tripwire_activations_by_category.png"
    frame.groupby("category")["tripwire_count"].sum().plot(kind="bar", title="Tripwire Activations by Category")
    plt.tight_layout()
    plt.savefig(chart1)
    plt.close()
    paths.append(chart1)

    chart2 = output / "refusal_vs_compliance_by_category.png"
    frame.groupby("category")[["refusal_score", "compliance_score"]].mean().plot(kind="bar", title="Refusal vs Compliance by Category")
    plt.tight_layout()
    plt.savefig(chart2)
    plt.close()
    paths.append(chart2)

    chart3 = output / "severity_distribution.png"
    frame["max_severity"].value_counts().sort_index().plot(kind="bar", title="Severity Distribution")
    plt.tight_layout()
    plt.savefig(chart3)
    plt.close()
    paths.append(chart3)

    return paths
