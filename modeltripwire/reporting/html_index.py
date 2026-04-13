from __future__ import annotations

import html
from pathlib import Path


def write_html_index(run_cards: list[dict], path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cards_html = "".join(
        f"""
        <a class=\"card\" href=\"{html.escape(card['href'])}\">
          <div class=\"top\">
            <span class=\"pill {html.escape(card.get('status_class', 'status-neutral'))}\">{html.escape(card.get('status', 'n/a'))}</span>
            <span class=\"muted\">{html.escape(card.get('completed_at', 'n/a'))}</span>
          </div>
          <h2>{html.escape(card.get('title', 'Run'))}</h2>
          <p class=\"muted\">run_id={html.escape(card.get('run_id', 'n/a'))}</p>
          <ul>
            <li><strong>Benchmark:</strong> {html.escape(card.get('benchmark_suite', 'n/a'))}</li>
            <li><strong>Model:</strong> {html.escape(card.get('model_name', 'n/a'))}</li>
            <li><strong>Cases:</strong> {html.escape(str(card.get('total_cases', 'n/a')))}</li>
          </ul>
        </a>
        """
        for card in run_cards
    ) or '<p class="muted">No runs available.</p>'

    content = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>ModelTripwire Report Hub</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; background: #0b1020; color: #e8ecf3; }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 48px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }}
    .card {{ display: block; text-decoration: none; color: inherit; background: #131a2e; border: 1px solid #24304d; border-radius: 16px; padding: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.25); }}
    .top {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; }}
    .pill {{ display: inline-block; padding: 8px 12px; border-radius: 999px; font-weight: 700; }}
    .status-ship {{ background: #123a2a; color: #7ef0b0; }}
    .status-review {{ background: #4a3510; color: #ffd36b; }}
    .status-block {{ background: #4a1717; color: #ff9a9a; }}
    .status-neutral {{ background: #23304f; color: #d7def0; }}
    .muted {{ color: #9eb0d1; }}
    ul {{ margin: 10px 0 0 18px; }}
    li {{ margin: 6px 0; }}
    @media (max-width: 800px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <h1>ModelTripwire Report Hub</h1>
    <p class=\"muted\">HTML index for recent runs and operator reports.</p>
    <div class=\"grid\">{cards_html}</div>
  </div>
</body>
</html>
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path
