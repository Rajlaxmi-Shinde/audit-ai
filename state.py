from typing import Optional
from typing_extensions import TypedDict


class AuditState(TypedDict):
    """
    Shared state across all LangGraph nodes.
    """

    # ==========================================================
    # User Inputs
    # ==========================================================
    transcript_path: str
    checklist_path: str

    # ==========================================================
    # Ingestion Output
    # ==========================================================
    transcript: str
    audit_checklist: dict
    framework: Optional[str]

    # ==========================================================
    # Planner Output
    # ==========================================================
    audit_plan: dict
    general_notes: list[str]

    # ==========================================================
    # Auditor Output
    # ==========================================================
    audit_findings: dict

    # ==========================================================
    # Synthesizer Output
    # ==========================================================
    report_data: dict
    report_path: str

    # ==========================================================
    # Validator Output
    # ==========================================================
    validation_result: dict
    is_valid: bool
    user_validation_notes: str