import logging
from langgraph.types import interrupt

from state import AuditState
from utils.llm_json import call_structure_llm
from prompts.validator_prompt import VALIDATOR_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def validator_node(state: AuditState)-> AuditState:
    """
    Advarsarial Validator
        Validate the drafted report.

    Parameters: 
        raw_transcript: str
        report_data   : dict

    Return:
        validation_result: dict
    """

    logger.info("="*60)
    logger.info("ADVERSARIAL VALIDATOR RUNNING")
    logger.info("="*60)

    transcript = state["transcript"]
    report = state["report_data"]

    user_content = f"""
        RAW TRANSCRIPT
        --------------
        {transcript}

        DRAFT aUDIT REPORT
        ------------------
        {report}
    """

    result: ValidatorOutput = call_structure_llm(
        VALIDATOR_SYSTEM_PROMPT,
        user_content,
        ValidatorOutput,
        "validator"
    )

    # State full validator output
    state["validation_result"] = result.model_dump()

    logger.info("Validation Result")
    logger.info(state["validation_result"])

    # Pause graph for human review
    human_response = interrupt(
        {
            "validation_result": state["validation_result"]
        }
    )

    # Resume starts here:
    state["is_valid"] = human_response.get("is_valid", False)
    state["user_validation_notes"] = human_response.get("user_validation_notes", "")

    logger_info(f"Human Decision: {state["is_valid"]}")

    return state

def validation(state: AuditState):
    """
    This function taking validation from user
    """
    if state["is_valid"]: 
        return "valid"
    return "invalid"

def collect_human_review(validation_result: dict)-> dict:
    """
    CLI Human Review
    """
    print("\n")
    print("="*70)
    print("VALIDATION RESULT")
    print("="*70)

    print(validation_result)

    defects = validation_result.get("defects_found", [])

    if len(defects) == 0:
        print("\nNo Validation defects found.\n")
    else:
        for i, defect in enumerate(defects, start=1):
            print(f"\nIssues {i}")
            print("-"*50)

            print("Type: ", defect.get("defect_type", "N/A"))

            print("Problem: ", defect.get("defect_type", "N/A"))

            print("Required Fix: ", defect.get("required_fix", "N/A"))
    
    print("\n")

    choice = input("Approve Report? (y/n): ").strip().lower()

    if choice=="y":
        return {
            "is_valid": True,
            "user_validation_notes": ""
        }
    
    notes = input("\nEnter Improvement Notes:\n")

    return {
        "is_valid": False,
        "user_validation_notes": notes
    }