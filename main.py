import logging
import os
from dotenv import load_dotenv

from graph import app


# ==========================================================
# LOGGING CONFIGURATION
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# MAIN
# ==========================================================

def main():

    load_dotenv()

    print("=" * 70)
    print("AI COMPLIANCE AUDIT AGENT")
    print("=" * 70)

    # ------------------------------------------------------
    # Input Files
    # ------------------------------------------------------

    transcript_path = "sample_data/meeting_transcript.txt"

    checklist_path = "sample_data/audit_checklist.json"

    # ------------------------------------------------------
    # Validate Files
    # ------------------------------------------------------

    if not os.path.exists(transcript_path):
        raise FileNotFoundError(
            f"Transcript not found: {transcript_path}"
        )

    if not os.path.exists(checklist_path):
        raise FileNotFoundError(
            f"Checklist not found: {checklist_path}"
        )

    # ------------------------------------------------------
    # Initial State
    # ------------------------------------------------------

    initial_state = {

        # Input
        "transcript_path": transcript_path,
        "checklist_path": checklist_path,

        # Ingestion
        "transcript": "",
        "audit_checklist": {},
        "framework": "",

        # Planner
        "audit_plan": {},
        "general_notes": [],

        # Auditor
        "audit_findings": {},

        # Synthesizer
        "report_data": {},
        "report_path": "",

        # Validator
        "validation_result": {}

    }

    # ------------------------------------------------------
    # Execute Graph
    # ------------------------------------------------------

    try:

        logger.info("Starting AI Audit Workflow...")

        result = app.invoke(initial_state)

        logger.info("Workflow Completed Successfully.")

        print("\n" + "=" * 70)
        print("AUDIT REPORT GENERATED SUCCESSFULLY")
        print("=" * 70)

        print(f"\nReport Location : {result['report_path']}")

    except Exception as e:

        logger.exception("Workflow Failed")

        print("\nWorkflow Failed.")

        print(e)


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()