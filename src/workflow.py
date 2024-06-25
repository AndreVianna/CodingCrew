from dotenv import load_dotenv

# pylint: disable=import-error
from langgraph.graph import StateGraph, END
# pylint: enable=import-error

from models.project_state import ProjectState
from edges import has_questions
from tasks.generate_questions_task import GenerateQuestionsTask
from tasks.start_project_task import StartProjectTask
from tasks.update_description_task import UpdateDescriptionTask

load_dotenv()

def build(is_debugging: bool = False):
    workflow = StateGraph(ProjectState)

    start_project = StartProjectTask()
    update_description = UpdateDescriptionTask()
    generate_questions = GenerateQuestionsTask()

    workflow.add_node("start_project", start_project.execute)
    workflow.add_node("update_description", update_description.execute)
    workflow.add_node("generate_questions", generate_questions.execute)

    workflow.set_entry_point("start_project")
    workflow.add_edge("start_project", "update_description")
    workflow.add_edge("update_description", "generate_questions")
    workflow.add_conditional_edges(
        "generate_questions",
        has_questions.check,
        {
            "CONTINUE": "update_description",
            "FINISH": END,
        })

    return workflow.compile(debug=is_debugging)
