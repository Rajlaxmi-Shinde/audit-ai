import json
from pathlib import Path
from state import AuditState


def ingestion_node(state: AuditState):
    """
    Reads:
    1. Meeting transcript (.txt)
    2. Audit checklist (.json)

    Returns both in Python dictionary format.
    """

    print("=" * 60)
    print("📥 INGESTION NODE")
    print("=" * 60)

    # -----------------------------
    # Read Transcript
    # -----------------------------
    transcript_path = Path(state["transcript_path"])

    with open(transcript_path, "r", encoding="utf-8") as file:
        transcript = file.read()

    print(f"✅ Transcript Loaded ({len(transcript)} characters)")

    # -----------------------------
    # Read Audit Checklist
    # -----------------------------
    checklist_path = Path(state["checklist_path"])

    with open(checklist_path, "r", encoding="utf-8") as file:
        checklist = json.load(file)

    print(
        f"✅ Checklist Loaded ({checklist['framework']})"
    )

    print(
        f"Total Controls : {checklist['total_controls']}"
    )

    print("=" * 60)

    return {
        "transcript": transcript,
        "audit_checklist": checklist
    }