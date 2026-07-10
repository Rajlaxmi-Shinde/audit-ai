import logging

from langchain_core.messages import HumanMessage
from pydantic import ValidationError

from prompts.auditor_prompt import AUDITOR_PROMPT
from schemas.auditor_schema import AuditorOutput
from state import AuditState

from utils.llm import llm

logger = logging.getLogger(__name__)


def auditors_node(state: AuditState):

    logger.info("=" * 60)
    logger.info("AUDITOR STARTED")
    logger.info("=" * 60)

    transcript = state["transcript"]
    audit_plan = state["audit_plan"]

    structured_llm = llm.with_structured_output(AuditorOutput)

    prompt = f"""
{AUDITOR_PROMPT}

Meeting Transcript

{transcript}

Planned Controls

{audit_plan}
"""

    try:

        response = structured_llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        logger.info(
            "Auditor generated %s findings.",
            len(response.audit_findings)
        )

        return {
            "audit_findings": response.model_dump()
        }

    except ValidationError as e:

        logger.exception("Schema validation failed.")

        raise RuntimeError(
            "Auditor output validation failed."
        ) from e

    except Exception as e:

        logger.exception("Auditor failed.")

        raise RuntimeError(
            "Unexpected error in Auditor."
        ) from e