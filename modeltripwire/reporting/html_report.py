from __future__ import annotations

import html
from pathlib import Path

from modeltripwire.models.schemas import ExperimentSummary


def _render_kv_list(items: dict) -> str:
    if not items:
        return "<li>None</li>"
    return "".join(
        f"<li><strong>{html.escape(str(key))}</strong>: {html.escape(str(value))}</li>"
        for key, value in items.items()
    )


def _render_failure_list(failures: list[dict], case_links: dict[str, str] | None = None) -> str:
    if not failures:
        return "<li>No notable failures</li>"
    case_links = case_links or {}
    return "".join(
        "<li>"
        + (
            f"<a href=\"{html.escape(case_links[item.get('prompt_id', '')])}\"><strong>{html.escape(str(item.get('prompt_id', 'n/a')))}</strong></a>"
            if item.get('prompt_id', '') in case_links
            else f"<strong>{html.escape(str(item.get('prompt_id', 'n/a')))}</strong>"
        )
        + f" ({html.escape(str(item.get('scenario', 'n/a')))} / {html.escape(str(item.get('category', 'n/a')))}), "
        + f"tripwires={html.escape(str(item.get('tripwire_count', 0)))}, "
        + f"severity={html.escape(str(item.get('max_severity', 0)))}"
        + "</li>"
        for item in failures
    )


def _render_simple_list(items: list[str]) -> str:
    if not items:
        return "<li>None</li>"
    return "".join(f"<li>{html.escape(str(item))}</li>" for item in items)


def _render_gate_panel(title: str, gate_result: dict | None) -> str:
    if not gate_result:
        return f"<div class=\"card\"><h2>{html.escape(title)}</h2><p class=\"muted\">No gate data available.</p></div>"
    decision = gate_result.get("decision_summary", {})
    return (
        f"<div class=\"card\">"
        f"<h2>{html.escape(title)}</h2>"
        f"<p><strong>Status:</strong> {html.escape(str(decision.get('status', 'n/a')))}</p>"
        f"<p><strong>Recommended action:</strong> {html.escape(str(decision.get('recommended_action', 'n/a')))}</p>"
        f"<p><strong>Reasons:</strong></p>"
        f"<ul>{_render_simple_list(decision.get('reasons', []))}</ul>"
        f"</div>"
    )


def write_html_report(
    summary: ExperimentSummary,
    path: str | Path,
    benchmark_gate: dict | None = None,
    trend_gate: dict | None = None,
    case_links: dict[str, str] | None = None,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status = summary.decision_summary.get("status", "n/a")
    status_class = {
        "SHIP": "status-ship",
        "REVIEW_REQUIRED": "status-review",
        "DO_NOT_SHIP": "status-block",
    }.get(status, "status-neutral")

    metrics_html = "".join(
        f'<div class="metric"><div class="metric-label">{html.escape(key)}</div><div class="metric-value">{html.escape(str(value))}</div></div>'
        for key, value in summary.aggregate_metrics.items()
    )

    content = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(summary.title)} | ModelTripwire</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; background: #0b1020; color: #e8ecf3; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 48px; }}
    .hero {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 24px; }}
    .card {{ background: #131a2e; border: 1px solid #24304d; border-radius: 16px; padding: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.25); }}
    .status-pill {{ display: inline-block; padding: 8px 12px; border-radius: 999px; font-weight: 700; }}
    .status-ship {{ background: #123a2a; color: #7ef0b0; }}
    .status-review {{ background: #4a3510; color: #ffd36b; }}
    .status-block {{ background: #4a1717; color: #ff9a9a; }}
    .status-neutral {{ background: #23304f; color: #d7def0; }}
    h1, h2, h3 {{ margin-top: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }}
    ul {{ margin: 10px 0 0 18px; }}
    li {{ margin: 6px 0; }}
    .muted {{ color: #9eb0d1; }}
    .metrics {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }}
    .metric {{ background: #0f1527; border: 1px solid #24304d; border-radius: 12px; padding: 14px; }}
    .metric-label {{ color: #9eb0d1; font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }}
    .metric-value {{ font-size: 24px; font-weight: 700; margin-top: 6px; }}
    @media (max-width: 800px) {{ .hero, .grid, .metrics {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <div class=\"hero\">
      <div class=\"card\">
        <h1>{html.escape(summary.title)}</h1>
        <p class=\"muted\">{html.escape(summary.research_question)}</p>
        <div class=\"status-pill {status_class}\">{html.escape(status)}</div>
        <p><strong>Recommended action:</strong> {html.escape(str(summary.decision_summary.get('recommended_action', 'n/a')))}</p>
        <p><strong>Reasons:</strong></p>
        <ul>{_render_simple_list(summary.decision_summary.get('reasons', []))}</ul>
      </div>
      <div class=\"card\">
        <h2>Run metadata</h2>
        <ul>
          <li><strong>Run ID:</strong> {html.escape(summary.run_id or 'n/a')}</li>
          <li><strong>Run label:</strong> {html.escape(summary.run_label or 'n/a')}</li>
          <li><strong>Benchmark suite:</strong> {html.escape(summary.benchmark_suite or 'mixed/unspecified')}</li>
          <li><strong>Models:</strong> {html.escape(', '.join(summary.model_names))}</li>
          <li><strong>Total cases:</strong> {summary.total_cases}</li>
        </ul>
      </div>
    </div>

    <div class=\"card\" style=\"margin-bottom: 20px;\">
      <h2>Aggregate metrics</h2>
      <div class=\"metrics\">{metrics_html}</div>
    </div>

    <div class=\"grid\" style=\"margin-bottom: 20px;\">
      {_render_gate_panel('Benchmark gate', benchmark_gate)}
      {_render_gate_panel('Trend gate', trend_gate)}
    </div>

    <div class=\"grid\">
      <div class=\"card\">
        <h2>Scenario breakdown</h2>
        <ul>{_render_kv_list(summary.scenario_breakdown)}</ul>
      </div>
      <div class=\"card\">
        <h2>Benchmark breakdown</h2>
        <ul>{_render_kv_list(summary.benchmark_breakdown)}</ul>
      </div>
      <div class=\"card\">
        <h2>Tripwire summary</h2>
        <ul>{_render_kv_list(summary.tripwire_summary)}</ul>
      </div>
      <div class=\"card\">
        <h2>Notable failures</h2>
        <ul>{_render_failure_list(summary.notable_failures, case_links=case_links)}</ul>
      </div>
      <div class=\"card\">
        <h2>Limitations</h2>
        <ul>{_render_simple_list(summary.limitations)}</ul>
      </div>
      <div class=\"card\">
        <h2>Next steps</h2>
        <ul>{_render_simple_list(summary.next_steps)}</ul>
      </div>
    </div>
  </div>
</body>
</html>
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
