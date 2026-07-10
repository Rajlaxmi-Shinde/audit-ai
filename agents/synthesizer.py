from utils.llm import llm

import logging
import os
from datetime import datetime

from state import AuditState
from utils.docx_generator import generate_docx

logger = logging.getLogger(__name__)


def synthesizer_node(state: AuditState):
    """
    Report Synthesizer

    Responsibilities:
    -----------------
    1. Collect planner notes
    2. Collect auditor findings
    3. Prepare report data
    4. Generate DOCX report
    """

    logger.info("=" * 60)
    logger.info("REPORT SYNTHESIZER STARTED")
    logger.info("=" * 60)

    try:

        framework = state.get("framework", "")

        notes = state.get("general_notes", [])

        findings = state.get("audit_findings", {}).get(
            "audit_findings",
            []
        )

        report_data = {

            "company_name": "",

            "audit_date": datetime.today().strftime("%d-%m-%Y"),

            "iso_reference": framework,

            "internal_audit_report": "",

            "notes": notes,

            "findings": findings,
        }

        os.makedirs("output", exist_ok=True)

        report_name = (
            f"audit_report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        )

        report_path = os.path.join(
            "output",
            report_name,
        )

        generate_docx(
            report_data=report_data,
            output_path=report_path,
        )

        logger.info("Report generated successfully.")
        logger.info("Saved at: %s", report_path)

        return {

            "report_data": report_data,

            "report_path": report_path,

        }

    except Exception as e:

        logger.exception(
            "Failed to generate audit report."
        )

        raise RuntimeError(
            "Synthesizer execution failed."
        ) from e