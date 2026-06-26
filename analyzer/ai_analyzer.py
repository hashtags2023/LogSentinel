"""
LogSentinel — AI Triage Analyzer
Sends detected findings to Claude for SOC-style triage reporting.
"""

import os
import json
from datetime import datetime
import anthropic
from dotenv import load_dotenv

load_dotenv()


def _get_client():
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError(
            "[!] ANTHROPIC_API_KEY not set. Add it to your .env file."
        )
    return anthropic.Anthropic(api_key=key)


def build_prompt(findings: list[dict]) -> str:
    """Formats findings into a structured prompt for Claude."""
    lines = []
    for i, f in enumerate(findings, 1):
        lines.append(f"[{i}] {f.get('severity','?')} — {f['title']}")
        lines.append(f"     Category: {f.get('category','Unknown')}")
        lines.append(f"     Detail: {f.get('description','')}")
        evidence = f.get("evidence", [])
        if evidence:
            lines.append(f"     Evidence (up to 2 lines):")
            for e in evidence[:2]:
                lines.append(f"       > {e[:120]}")
        lines.append("")

    findings_text = "\n".join(lines)

    return f"""You are a senior SOC analyst reviewing automated threat detection results.

The following {len(findings)} finding(s) were detected in a security log analysis:

{findings_text}

Write a concise SOC triage report with exactly these four sections:

## Threat Summary
One paragraph. Overall threat picture — is this active attack, reconnaissance, insider threat, or noise?

## Critical & High Priority
For each CRITICAL or HIGH finding: what it means in practice, attacker's likely next step, and whether immediate action is needed.

## Watch List
MEDIUM and INFO findings worth monitoring but not yet urgent.

## Recommended Actions
Exactly 3 prioritized actions. Be specific — include commands, config changes, or tool names where relevant.

Be direct. No filler. Assume a technical analyst audience."""


def analyze_findings(findings: list[dict]) -> str:
    """
    Takes LogSentinel findings and returns an AI triage report string.
    Only calls the API when there are actual findings.
    """
    if not findings:
        return "No findings to analyze."

    # Only send HIGH and above to the AI to keep token usage low
    # Still pass all findings for context but filter evidence on low-severity
    prioritized = []
    for f in findings:
        entry = {k: v for k, v in f.items() if k != "evidence"}
        if f.get("severity") in ("CRITICAL", "HIGH"):
            entry["evidence"] = f.get("evidence", [])[:2]
        prioritized.append(entry)

    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=700,
        messages=[{"role": "user", "content": build_prompt(prioritized)}]
    )
    return message.content[0].text


def save_ai_report(findings: list[dict], ai_report: str, log_source: str) -> str:
    """Saves findings + AI triage report to a JSON file in /reports."""
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/ai_triage_{timestamp}.json"

    output = {
        "generated_at": datetime.now().isoformat(),
        "log_source": log_source,
        "finding_count": len(findings),
        "severity_breakdown": {
            sev: sum(1 for f in findings if f.get("severity") == sev)
            for sev in ("CRITICAL", "HIGH", "MEDIUM", "INFO")
        },
        "findings": findings,
        "ai_triage_report": ai_report,
    }

    with open(filename, "w") as fp:
        json.dump(output, fp, indent=2)

    return filename