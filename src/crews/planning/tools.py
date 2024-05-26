"""Tools for the crew agents."""

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain.tools import tool

class PlanningTools():
    """
    This class represents a tool for creating email drafts.
    It uses the GmailToolkit and GmailCreateDraft from the langchain_community package.
    """

    @tool("Create Draft")
    def create_draft(self, data: str):
        """
        This method creates an email draft.

        The input to this tool should be a pipe (|) separated text
        of length 3 (three), representing who to send the email to,
        the subject of the email and the actual message.
        For example, `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`.

        Args:
            data (str): Pipe-separated string containing email, subject, and message.

        Returns:
            str: A string indicating the result of the draft creation.
        """
        email, subject, message = data.split('|')
        gmail = GmailToolkit()
        draft = GmailCreateDraft(api_resource=gmail.api_resource)
        resutl = draft({
                                'to': [email],
                                'subject': subject,
                                'message': message
                })
        return f"\nDraft created: {resutl}\n"
