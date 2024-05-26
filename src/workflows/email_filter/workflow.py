"""Main workflow."""

from dotenv import load_dotenv
from langgraph.graph import StateGraph
from workflows.email_filter.states import EmailFilterState
from workflows.email_filter.nodes import EmailFilterNodes
from crews.email_filter.crew import EmailFilterCrew

load_dotenv()

class EmailFilterWorkflow():
    """
    Represents a workflow for responding to emails.

    This class sets up the workflow for responding to emails. It creates a StateGraph object and adds nodes and edges
    to define the flow of the workflow. The entry point of the workflow is set to the "check_new_emails" node.

    Nodes:
    - "check_new_emails": Checks for new emails.
    - "wait_next_run": Waits for the next run of the workflow.
    - "draft_responses": Kicks off the email filtering process.

    Edges:
    - From "check_new_emails":
        - If there are new emails: Goes to "draft_responses".
        - If there are no new emails: Goes to "wait_next_run".
    - From "draft_responses":
        - Goes to "wait_next_run".
    - From "wait_next_run":
        - If the workflow should continue: Goes to "check_new_emails".
        - If the workflow should end: Goes to "__end__".

    The compiled workflow is stored in the `app` attribute of the EmailResponderWorkflow instance.
    """

    def __init__(self):
        nodes = EmailFilterNodes()
        workflow = StateGraph(EmailFilterState)

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
