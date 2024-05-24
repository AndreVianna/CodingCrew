"""Main workflow."""

from dotenv import load_dotenv
from langgraph.graph import StateGraph
from .email_responder_crew import EmailFilterCrew

from .workflows.states import EmailsState
from .workflows.nodes import Nodes

load_dotenv()

class WorkFlow():
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(EmailsState)

        workflow.add_node("check_new_emails", nodes.check_email)
        workflow.add_node("wait_next_run", nodes.wait_next_run)
        workflow.add_node("draft_responses", EmailFilterCrew().kickoff)

        workflow.set_entry_point("check_new_emails")
        workflow.add_conditional_edges(
                "check_new_emails",
                nodes.new_emails,
                {
                    "you_have_mail": 'draft_responses',
                    "sleep": 'wait_next_run',
                }
        )
        workflow.add_edge('draft_responses', 'wait_next_run')
        workflow.add_conditional_edges(
                "wait_next_run",
                nodes.terminate,
                {
                    "continue": 'check_new_emails',
                    "end": '__end__'
                }
        )
        self.app = workflow.compile()
