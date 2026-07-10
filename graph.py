from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from agents.ingestion import ingestion_node
from agents.planner import planner_node
from agents.synthesizer import synthesizer_node
from agents.auditor import auditors_node
from agents.validator import validator_node, validation

from state import AuditState
from utils.llm import llm

load_dotenv()

graph = StateGraph(AuditState)

graph.add_node("Transcription Ingestion", ingestion_node)
graph.add_node("Compliance Planner", planner_node)
graph.add_node("Specialized Auditors", auditors_node)
graph.add_node("Report Synthesizer", synthesizer_node)
graph.add_node("Adversarial Validator", validator_node)

graph.add_edge(START, "Transcription Ingestion")

graph.add_edge("Transcription Ingestion", "Compliance Planner")
graph.add_edge("Compliance Planner", "Specialized Auditors")
graph.add_edge("Specialized Auditors", "Report Synthesizer")
graph.add_edge("Report Synthesizer", "Adversarial Validator")

graph.add_conditional_edges(
    "Adversarial Validator",
    validation,
    {
        "invalid": "Compliance Planner",
        "valid": END
    }
)

app = graph.compile()