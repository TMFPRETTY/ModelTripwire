from __future__ import annotations

from pathlib import Path


def _format_tripwires(tripwires: list[dict]) -> str:
    if not tripwires:
        return "- No tripwires triggered"
    return "\n".join(
        f"- **{item['name']}** | severity={item['severity']} | confidence={item.get('confidence', 'n/a')} | match_type={item.get('match_type', 'n/a')} | evidence={item['evidence']}"
        for item in tripwires
    )


def _format_list(items: list[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def write_benchmark_case_review_report(
    gate_result: dict,
    results_by_prompt_id: dict[str, dict],
    path: str | Path,
    include_passed: bool = False,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    case_sections = []
    for case in gate_result["case_evaluations"]:
        if not include_passed and case["passed"] and case["score_confidence"] >= 0.75:
            continue

        result_row = results_by_prompt_id.get(case["prompt_id"], {})
        prompt_text = result_row.get("prompt_text", "")
        response_text = result_row.get("response_text", "")
        turns = result_row.get("metadata", {}).get("turns") or []
        turn_block = "\n".join(f"{idx + 1}. {turn}" for idx, turn in enumerate(turns)) or prompt_text or "n/a"

        calibration_action = "review"
        if "max_tripwire_count" in case["failure_reasons"] and case["compliance_score"] <= 0.1:
            calibration_action = "reduce false-positive tripwire sensitivity"
        elif "max_compliance_score" in case["failure_reasons"] and case["scenario"] in {"extended_phishing_escalation", "trust_buildup_sensitive_export"}:
            calibration_action = "treat as likely real provider weakness"
        elif case["passed"]:
            calibration_action = "keep as passing reference case"

        case_sections.append(
            f"""## {case['prompt_id']} - {case['prompt_name']}

- Verdict: {'PASS' if case['passed'] else 'FAIL'}
- Verdict summary: {case['verdict_summary']}
- Scenario: {case['scenario']}
- Expected risk type: {case['expected_risk_type']}
- Difficulty: {case.get('difficulty') or 'n/a'}
- Evaluation focus: {case.get('evaluation_focus') or []}
- Failure reasons: {case['failure_reasons'] or []}
- Recommended calibration action: {calibration_action}

### Prompt turns

{turn_block}

### Model response

{response_text or 'n/a'}

### Score breakdown

- Refusal: {case['refusal_score']}
- Compliance: {case['compliance_score']}
- Leakage: {case['leakage_score']}
- Harmfulness: {case['harmfulness_score']}
- Confidence: {case['score_confidence']}
- Risk flags: {case['risk_flags']}
- Evaluator mode: {result_row.get('metadata', {}).get('evaluator_mode', 'unknown')}
- Blend policy: {result_row.get('metadata', {}).get('blend_policy', {})}

### Evaluator trace

- Rule scorecard: {result_row.get('metadata', {}).get('rule_scorecard', 'n/a')}
- Judge scorecard: {result_row.get('metadata', {}).get('judge_scorecard', 'n/a')}
- Blended scorecard: {result_row.get('metadata', {}).get('blended_scorecard', 'n/a')}

### Score notes

{_format_list(case.get('score_notes', []))}

### Tripwire evidence

{_format_tripwires(case.get('tripwires', []))}

### Checks and thresholds

- Checks: {case['checks']}
- Thresholds: {case['thresholds']}
"""
        )

    content = f"""# Benchmark Case Review Report

## Benchmark context

- Suite: {gate_result['suite_name']}
- Title: {gate_result['title']}
- Run ID: {gate_result['run_id'] or 'n/a'}
- Run label: {gate_result['run_label'] or 'n/a'}
- Overall result: {'PASS' if gate_result['passed'] else 'FAIL'}

## Review focus

This report highlights failed and borderline benchmark cases to support provider calibration, scorer tuning, and tripwire review.

{chr(10).join(case_sections) or 'No failed or borderline cases to review.'}
"""
    output_path.write_text(content, encoding='utf-8')
    return output_path
