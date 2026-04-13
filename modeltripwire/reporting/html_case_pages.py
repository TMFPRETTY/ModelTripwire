from __future__ import annotations

import html
from pathlib import Path


def _render_scorecard(title: str, scorecard: dict | None) -> str:
    if not scorecard:
        return f"<div class=\"card\"><h2>{html.escape(title)}</h2><p>No scorecard available.</p></div>"
    return f"""
    <div class=\"card\">
      <h2>{html.escape(title)}</h2>
      <ul>
        <li><strong>Refusal:</strong> {html.escape(str(scorecard.get('refusal_score', 'n/a')))}</li>
        <li><strong>Compliance:</strong> {html.escape(str(scorecard.get('compliance_score', 'n/a')))}</li>
        <li><strong>Leakage:</strong> {html.escape(str(scorecard.get('leakage_score', 'n/a')))}</li>
        <li><strong>Harmfulness:</strong> {html.escape(str(scorecard.get('harmfulness_score', 'n/a')))}</li>
        <li><strong>Confidence:</strong> {html.escape(str(scorecard.get('confidence', 'n/a')))}</li>
        <li><strong>Risk flags:</strong> {html.escape(str(scorecard.get('risk_flags', [])))}</li>
        <li><strong>Notes:</strong> {html.escape(str(scorecard.get('notes', [])))}</li>
      </ul>
    </div>
    """


def write_case_detail_page(case_row: dict, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metadata = case_row.get("metadata", {}) or {}
    content = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(str(case_row.get('prompt_id', 'case')))} | ModelTripwire</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; background: #0b1020; color: #e8ecf3; }}
    .wrap {{ max-width: 900px; margin: 0 auto; padding: 32px 20px 48px; }}
    .card {{ background: #131a2e; border: 1px solid #24304d; border-radius: 16px; padding: 20px; margin-bottom: 20px; }}
    pre {{ white-space: pre-wrap; word-break: break-word; background: #0f1527; border: 1px solid #24304d; border-radius: 12px; padding: 14px; }}
    ul {{ margin: 10px 0 0 18px; }}
    li {{ margin: 6px 0; }}
    a {{ color: #8bb8ff; }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <div class=\"card\">
      <h1>{html.escape(str(case_row.get('prompt_name', case_row.get('prompt_id', 'case'))))}</h1>
      <ul>
        <li><strong>Prompt ID:</strong> {html.escape(str(case_row.get('prompt_id', 'n/a')))}</li>
        <li><strong>Scenario:</strong> {html.escape(str(case_row.get('scenario', 'n/a')))}</li>
        <li><strong>Category:</strong> {html.escape(str(case_row.get('category', 'n/a')))}</li>
        <li><strong>Benchmark suite:</strong> {html.escape(str(case_row.get('benchmark_suite', 'n/a')))}</li>
        <li><strong>Model:</strong> {html.escape(str(case_row.get('model_name', 'n/a')))}</li>
      </ul>
    </div>

    <div class=\"card\">
      <h2>Prompt</h2>
      <pre>{html.escape(str(case_row.get('prompt_text', '')))}</pre>
    </div>

    <div class=\"card\">
      <h2>Response</h2>
      <pre>{html.escape(str(case_row.get('response_text', '')))}</pre>
    </div>

    <div class=\"card\">
      <h2>Scores</h2>
      <ul>
        <li><strong>Refusal:</strong> {html.escape(str(case_row.get('refusal_score', 'n/a')))}</li>
        <li><strong>Compliance:</strong> {html.escape(str(case_row.get('compliance_score', 'n/a')))}</li>
        <li><strong>Leakage:</strong> {html.escape(str(case_row.get('leakage_score', 'n/a')))}</li>
        <li><strong>Harmfulness:</strong> {html.escape(str(case_row.get('harmfulness_score', 'n/a')))}</li>
        <li><strong>Evaluator mode:</strong> {html.escape(str(metadata.get('evaluator_mode', 'n/a')))}</li>
        <li><strong>Blend policy:</strong> {html.escape(str(metadata.get('blend_policy', {})))}</li>
      </ul>
    </div>

    {_render_scorecard('Rule scorecard', case_row.get('rule_scorecard'))}
    {_render_scorecard('Judge scorecard', case_row.get('judge_scorecard'))}
    {_render_scorecard('Blended scorecard', case_row.get('blended_scorecard'))}
  </div>
</body>
</html>
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
