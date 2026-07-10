import json
import logging

from langchain_core.messages import HumanMessage
from pydantic import ValidationError

from prompts.planner_prompt import PLANNER_PROMPT
from schemas.planner_schema import PlannerOutput
from state import AuditState
from utils.llm import llm

logger = logging.getLogger(__name__)


def planner_node(state: AuditState):

    logger.info("=" * 60)
    logger.info("COMPLIANCE PLANNER STARTED")
    logger.info("=" * 60)

    transcript = state["transcript"]
    checklist = state["audit_checklist"]

    structured_llm = llm.with_structured_output(PlannerOutput)

    prompt = f"""
{PLANNER_PROMPT}

==============================
AUDIT CHECKLIST
==============================

{json.dumps(checklist, indent=2)}

==============================
MEETING TRANSCRIPT
==============================

{transcript}
"""

    try:

        response = structured_llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        logger.info(
            "Planner selected %d controls.",
            len(response.planned_controls)
        )

        logger.info(
            "Planner extracted %d general notes.",
            len(response.general_notes)
        )

        return {
            "audit_plan": response.model_dump(),
            "general_notes": [
                note.model_dump()
                for note in response.general_notes
            ]
        }

    except ValidationError as e:

        logger.exception("Planner schema validation failed.")

        raise RuntimeError(
            "Planner returned an invalid response."
        ) from e

    except Exception as e:

        logger.exception("Planner execution failed.")

        raise RuntimeError(
            "Unexpected error in Planner."
        ) from e