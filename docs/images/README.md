# ModelTripwire README Images

This folder is for tracked README screenshots and visual examples.

Suggested image set:
- `dashboard.png` — HTML dashboard / report hub
- `run-report.png` — single run HTML operator report
- `case-drilldown.png` — HTML case detail page

Suggested capture source files:
- `outputs/html_reports/index.html`
- `outputs/html_reports/report_<run_id>.html`
- `outputs/html_reports/report_<run_id>_cases/<prompt_id>.html`

Suggested local flow on macOS:
1. Generate reports:
   - `python3 -m modeltripwire.cli run-benchmark beta_core --config configs/default.yaml`
   - `python3 -m modeltripwire.cli html-dashboard --config configs/default.yaml --output-dir outputs/html_reports`
2. Open the HTML files in a browser.
3. Capture screenshots with `screencapture` or normal macOS screenshots.
4. Save final cropped images into this folder using the filenames above.

Keep images reasonably cropped and readable for GitHub README display.
