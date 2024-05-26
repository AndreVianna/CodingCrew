"""Planning workflow."""

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from workflows.planning.states import PlanningState
from workflows.planning.nodes import PlanningNodes
from crews.planning.crew import PlanningCrew

load_dotenv()

class PlaningWorkflow():

    def __init__(self):
        nodes = PlanningNodes()
        workflow = StateGraph(PlanningState)

        workflow.add_node("start_project", nodes.start_project)
        workflow.add_node("analyse_description", PlanningCrew().kickoff)
        workflow.add_node("query_user", nodes.query_user)

        workflow.set_entry_point("start_project")
        workflow.add_edge('start_project', "analyse_description")
        workflow.add_edge("analyse_description", "query_user")
        workflow.add_conditional_edges(
            'query_user',
             nodes.has_answers,
             {
                "YES": 'analyse_description',
                "NO": END,
            })
        self.app = workflow.compile()
