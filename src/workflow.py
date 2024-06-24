from dotenv import load_dotenv

# pylint: disable=import-error
from langgraph.graph import StateGraph, END
# pylint: enable=import-error

from .models.project_state import ProjectState
from .nodes import start_project_node, update_description_node, generate_questions_node # , query_user, has_answers
from .edges import has_questions

load_dotenv()

def build(is_debugging: bool = False):
    workflow = StateGraph(ProjectState)

    workflow.add_node("start_project", start_project_node.create)
    workflow.add_node("update_description", update_description_node.create)
    workflow.add_node("generate_questions", generate_questions_node.create)

    workflow.set_entry_point("start_project")
    workflow.add_edge("start_project", "update_description")
    workflow.add_edge("update_description", "generate_questions")
    workflow.add_conditional_edges(
        "generate_questions",
        has_questions.create,
        {
            "CONTINUE": "update_description",
            "FINISH": END,
        })

    return workflow.compile(debug=is_debugging)
