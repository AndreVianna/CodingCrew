"""Tasks for the email filter crew."""

from textwrap import dedent
from crewai import Task

class EmailFilterTasks:
    """
    A class that defines tasks related to email filtering and analysis.
    """

    def filter_emails_task(self, agent, emails):
        """
        Task to filter a batch of emails and remove non-essential ones.

        Parameters:
        - agent (str): The name of the agent responsible for filtering the emails.
        - emails (list): A list of email messages to be filtered.

        Returns:
        - Task: A Task object representing the filtering task.
        """
        return Task(
            description=dedent(f"""\
                Analyze a batch of emails and filter out
                non-essential ones such as newsletters, promotional content and notifications.

                Use your expertise in email content analysis to distinguish
                important emails from the rest, pay attention to the sender and avoind invalid emails.

                Make sure to filter for the messages actually directed at the user and avoid notifications.

                EMAILS
                -------
                {emails}

                Your final answer MUST be a the relevant thread_ids and the sender, use bullet points.
                """),
            agent=agent
        )

    def action_required_emails_task(self, agent):
        """
        Task to analyze and summarize action-required emails.

        Parameters:
        - agent (str): The name of the agent responsible for analyzing the emails.

        Returns:
        - Task: A Task object representing the analysis task.
        """
        return Task(
            description=dedent("""\
                For each email thread, pull and analyze the complete threads using only the actual Thread ID.
                understand the context, key points, and the overall sentiment
                of the conversation.

                Identify the main query or concerns that needs to be
                addressed in the response for each

                Your final answer MUST be a list for all emails with:
                - the thread_id
                - a summary of the email thread
                - a highlighting with the main points
                - identify the user and who he will be answering to
                - communication style in the thread
                - the sender's email address
                """),
            agent=agent
        )

    def draft_responses_task(self, agent):
        """
        Task to draft responses for action-required emails.

        Parameters:
        - agent (str): The name of the agent responsible for drafting the responses.

        Returns:
        - Task: A Task object representing the drafting task.
        """
        return Task(
            description=dedent("""\
                Based on the action-required emails identified, draft responses for each.
                Ensure that each response is tailored to address the specific needs
                and context outlined in the email.

                - Assume the persona of the user and mimic the communication style in the thread.
                - Feel free to do research on the topic to provide a more detailed response, IF NECESSARY.
                - IF a research is necessary do it BEFORE drafting the response.
                - If you need to pull the thread again do it using only the actual Thread ID.

                Use the tool provided to draft each of the responses.
                When using the tool pass the following input:
                - to (sender to be responded)
                - subject
                - message

                You MUST create all drafts before sending your final answer.
                Your final answer MUST be a confirmation that all responses have been drafted.
                """),
            agent=agent
        )
