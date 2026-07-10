from typing import List
from pydantic import BaseModel, Field


class AuditFinding(BaseModel):
    """
    Audit finding for one mapped control.
    """

    control_id: str = Field(
        ...,
        description="Control or clause identifier."
    )

    control_name: str = Field(
        ...,
        description="Control title."
    )

    observation: str = Field(
        ...,
        description="Audit observation."
    )

    objective_evidence: str = Field(
        ...,
        description="Objective evidence from transcript."
    )

    finding: str = Field(
        ...,
        description="One of C, NC or S."
    )

    recommendation: str = Field(
        ...,
        description="Recommendation if required."
    )


class AuditorOutput(BaseModel):

    audit_findings: List[AuditFinding]