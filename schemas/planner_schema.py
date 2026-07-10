from typing import List
from pydantic import BaseModel, Field


class GeneralNote(BaseModel):
    """
    General observations discussed during the meeting that are
    not directly mapped to a specific control.
    """

    note: str = Field(
        ...,
        description="Important meeting note."
    )


class PlannedControl(BaseModel):
    """
    Control selected for auditing.
    """

    control_id: str = Field(...)

    control_name: str = Field(...)

    reason: str = Field(
        ...,
        description="Why this control should be audited."
    )

    transcript_evidence: List[str] = Field(
        default_factory=list
    )


class PlannerOutput(BaseModel):

    framework: str

    general_notes: List[GeneralNote] = Field(default_factory=list)

    planned_controls: List[PlannedControl] = Field(default_factory=list)