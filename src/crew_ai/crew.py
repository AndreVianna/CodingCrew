"""Email filter crew."""

from crewai import Crew

from crew_ai.agents import EmailFilterAgents
from crew_ai.tasks import EmailFilterTasks

class EmailFilterCrew():
    """
    Represents a crew responsible for filtering and processing emails.

    Attributes:
        filter_agent (EmailFilterAgent): The agent responsible for filtering emails.
        action_agent (EmailActionAgent): The agent responsible for taking action on emails.
        writer_agent (EmailResponseWriter): The agent responsible for writing email responses.
    """

    def __init__(self):
        agents = EmailFilterAgents()
        self.filter_agent = agents.email_filter_agent()
        self.action_agent = agents.email_action_agent()
        self.writer_agent = agents.email_response_writer()

    def kickoff(self, state):
        """
        Filters and processes emails based on the given state.

        Args:
            state (dict): The state containing the emails to be filtered and processed.

        Returns:
            dict: The updated state with the action required emails.

        """
        print("### Filtering emails")
        tasks = EmailFilterTasks()
        crew = Crew(
            agents=[self.filter_agent, self.action_agent, self.writer_agent],
            tasks=[
                tasks.filter_emails_task(self.filter_agent, self._format_emails(state['emails'])),
                tasks.action_required_emails_task(self.action_agent),
                tasks.draft_responses_task(self.writer_agent)
            ],
            verbose=True
        )
        result = crew.kickoff()
        return {**state, "action_required_emails": result}

    def _format_emails(self, emails):
        """
        Formats the given emails into a string representation.

        Args:
            emails (list): The list of emails to be formatted.

        Returns:
            str: The formatted string representation of the emails.

        """
        emails_string = []
        for email in emails:
            print(email)
            arr = [
                f"ID: {email['id']}",
                f"- Thread ID: {email['threadId']}",
                f"- Snippet: {email['snippet']}",
                f"- From: {email['sender']}",
                "--------"
            ]
            emails_string.append("\n".join(arr))
        return "\n".join(emails_string)
