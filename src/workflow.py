from dotenv import load_dotenv

# pylint: disable=import-error
from langgraph.graph import StateGraph, END
# pylint: enable=import-error

from models.project_state import ProjectState
from edges import can_ask_questions, has_questions
from nodes.generate_questions import GenerateQuestions
from nodes.start_project import StartProject
from nodes.update_description import UpdateDescription

load_dotenv()

def build(is_debugging: bool = False):
    workflow = StateGraph(ProjectState)

    start_project = StartProject()
    update_description = UpdateDescription()
    generate_questions = GenerateQuestions()

    workflow.add_node("start_project", start_project.execute)
    workflow.add_node("update_description", update_description.execute)
    workflow.add_node("generate_questions", generate_questions.execute)

    workflow.set_entry_point("start_project")
    workflow.add_edge("start_project", "update_description")
    workflow.add_conditional_edges(
        "update_description",
        can_ask_questions.check,
        {
            "CONTINUE": "generate_questions",
            "FINISH": END,
        })
    workflow.add_conditional_edges(
        "generate_questions",
        has_questions.check,
        {
            "CONTINUE": "update_description",
            "FINISH": END,
        })

    return workflow.compile(debug=is_debugging)
