"""
Represents the main workflow.

This module defines the structure and behavior of a planning workflow.
It contains methods to add nodes, edges, and conditional edges to the workflow,
as well as set the entry point and compile the workflow.

Attributes:
    app: The compiled workflow application.
"""

from dotenv import load_dotenv
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.state import StateGraph
from langgraph.graph import END

from models.project_state import ProjectState
from nodes import start_project, update_description # , query_user, has_answers

load_dotenv()

def build(is_debugging: bool = False) -> CompiledGraph:
    """
    Builds and returns a compiled workflow graph.

    Returns:
        CompiledGraph: The compiled workflow graph.
    """
    workflow = StateGraph(ProjectState)

    workflow.add_node("start_project", start_project.create)
    workflow.add_node("execute_analysis", update_description.create)
    # workflow.add_node("query_user", query_user.create)
    # workflow.add_node("generate_report", AnalysisCrew(is_debugging).generate_report)

    workflow.set_entry_point("start_project")
    workflow.add_edge("start_project", "execute_analysis")
    # workflow.add_edge("execute_analysis", "query_user")
    # workflow.add_conditional_edges(
    #     "query_user",
    #     has_answers.create,
    #     {
    #         "CONTINUE": "execute_analysis",
    #         "FINISH": "generate_report",
    #     })
    # workflow.add_edge("generate_report", END)
    workflow.add_edge("execute_analysis", END)

    return workflow.compile(debug=is_debugging)
