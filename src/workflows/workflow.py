"""Planning workflow."""

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from workflows.states import AnalysisState
from workflows.nodes import PlanningNodes
from crews.crew import AnalysisCrew, ReportingCrew

load_dotenv()

class PlaningWorkflow():

    def __init__(self):
        nodes = PlanningNodes()
        workflow = StateGraph(AnalysisState)

        workflow.add_node("start_project", nodes.start_project)
        workflow.add_node("analyze_description", AnalysisCrew().kickoff)
        workflow.add_node("query_user", nodes.query_user)
        workflow.add_node("generate_report", ReportingCrew().kickoff)

        workflow.set_entry_point("start_project")
        workflow.add_edge('start_project', "analyze_description")
        workflow.add_edge("analyze_description", "query_user")
        workflow.add_conditional_edges(
            'query_user',
             nodes.has_answers,
             {
                "CONTINUE": 'analyze_description',
                "FINISH": 'generate_report',
            })
        workflow.add_edge("generate_report", END)

        self.app = workflow.compile()
