"""Agents for the email filter crew."""

from textwrap import dedent

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.get_thread import GmailGetThread
from langchain_community.tools.tavily_search import TavilySearchResults

from crewai import Agent
from crews.email_filter.tools import EmailFilterTools    

class EmailFilterAgents():
    """
    A class that represents different types of email filter agents.

    This class provides methods to create instances of different email filter agents, such as Senior Email Analyst,
    Email Action Specialist, and Email Response Writer. Each agent has specific attributes, such as role, goal, backstory,
    tools, verbosity, and delegation settings.

    Attributes:
        gmail (GmailToolkit): An instance of the GmailToolkit class.

    Methods:
        email_filter_agent: Creates an Agent object representing a Senior Email Analyst.
        email_action_agent: Creates an Agent object for the Email Action Specialist role.
        email_response_writer: Creates an instance of the Agent class for an Email Response Writer.
    """

    def __init__(self):
        self.gmail = GmailToolkit()

    def email_filter_agent(self):
        """
        Creates an Agent object representing a Senior Email Analyst.

        Returns:
            Agent: An Agent object with the following attributes:
                - role: The role of the agent, set to 'Senior Email Analyst'.
                - goal: The goal of the agent, set to 'Filter out non-essential emails like newsletters and promotional content'.
                - backstory: The backstory of the agent, providing information about their experience and expertise in email content analysis.
                - verbose: A boolean indicating whether the agent should provide verbose output.
                - allow_delegation: A boolean indicating whether the agent is allowed to delegate tasks.

        """
        return Agent(
            role='Senior Email Analyst',
            goal='Filter out non-essential emails like newsletters and promotional content',
            backstory=dedent("""\
                As a Senior Email Analyst, you have extensive experience in email content analysis.
                You are adept at distinguishing important emails from spam, newsletters, and other
                irrelevant content. Your expertise lies in identifying key patterns and markers that
                signify the importance of an email."""),
            verbose=True,
            allow_delegation=False
        )

    def email_action_agent(self):
        """
        Creates an agent object for the Email Action Specialist role.

        Returns:
            Agent: An agent object with the specified role, goal, backstory, tools, verbosity, and delegation settings.
        """
        return Agent(
            role='Email Action Specialist',
            goal='Identify action-required emails and compile a list of their IDs',
            backstory=dedent("""\
                With a keen eye for detail and a knack for understanding context, you specialize
                in identifying emails that require immediate action. Your skill set includes interpreting
                the urgency and importance of an email based on its content and context."""),
            tools=[
                GmailGetThread(api_resource=self.gmail.api_resource),
                TavilySearchResults()
            ],
            verbose=True,
            allow_delegation=False,
        )

    def email_response_writer(self):
        """
        Creates an instance of the Agent class for an Email Response Writer.

        Returns:
            Agent: An instance of the Agent class with the specified role, goal, backstory, tools, verbose, and allow_delegation attributes.
        """
        return Agent(
            role='Email Response Writer',
            goal='Draft responses to action-required emails',
            backstory=dedent("""\
                You are a skilled writer, adept at crafting clear, concise, and effective email responses.
                Your strength lies in your ability to communicate effectively, ensuring that each response is
                tailored to address the specific needs and context of the email."""),
            tools=[
                TavilySearchResults(),
                GmailGetThread(api_resource=self.gmail.api_resource),
                EmailFilterTools.create_draft
            ],
            verbose=True,
            allow_delegation=False,
        )
