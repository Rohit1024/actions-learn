"""Classify normalized synthetic events, not raw gh-aw log parsing."""
import json
from pathlib import Path

DECISIONS = {
    "compiler_missing": ("local toolchain", "stop; obtain a reviewed compiler outside this exercise"),
    "reference_resolution_denied": ("compile dependency resolution", "stop; inspect reference access and installed-version support"),
    "model_auth_denied": ("engine authentication", "stop; inspect identity configuration without logging credentials"),
    "network_denied": ("agent network", "stop; compare required destination with reviewed allowlist"),
    "tool_unavailable": ("tool capability", "stop; report missing evidence or redesign the task"),
    "unsupported_claim": ("report quality", "review rubric failure before budgeting another sample"),
    "handler_limit": ("output policy", "stop; reduce proposal to reviewed operation count"),
    "cancelled_after_proposal": ("partial execution", "stop; inspect handler status and existing effects before retry"),
}


def classify(event):
    return DECISIONS.get(event["signal"], ("unknown", "stop; preserve evidence and investigate"))


if __name__ == "__main__":
    events = json.loads(Path(__file__).with_name("events.json").read_text())
    for event in events:
        boundary, next_step = classify(event)
        print(f"{event['id']}: {boundary} -> {next_step}")
    print("SYNTHETIC DIAGNOSTICS ONLY: no logs downloaded and no reruns requested")
