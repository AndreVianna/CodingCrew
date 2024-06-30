from dotenv import load_dotenv

# pylint: disable=import-error
from langgraph.graph import StateGraph
# pylint: enable=import-error

from models import Run
from nodes import StartProject, UpdateDescription, GenerateQueries
from edges import CanAskQuestions, HasQuestions

load_dotenv()

def build(is_debugging: bool = False):
    workflow = StateGraph(Run)

    workflow.add_node(StartProject.name, StartProject.run)
    workflow.add_node(UpdateDescription.name, UpdateDescription.run)
    workflow.add_node(GenerateQueries.name, GenerateQueries.run)

    workflow.set_entry_point(StartProject.name)
    workflow.add_edge(StartProject.name, UpdateDescription.name)
    workflow.add_conditional_edges(UpdateDescription.name, CanAskQuestions.check)
    workflow.add_conditional_edges(GenerateQueries.name, HasQuestions.check)

    return workflow.compile(debug=is_debugging)
