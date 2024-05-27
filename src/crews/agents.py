"""Agents for the email filter crew."""

from textwrap import dedent

from crewai import Agent

class PlanningAgents():
    """
    A class representing planning agents for software development projects.

    Attributes:
        None

    Methods:
        system_analyst: Represents a system analyst planning agent.

    """

    def system_analyst(self):
        """
        Represents a system analyst planning agent.

        Returns:
            Agent: An instance of the Agent class representing a system analyst.

        """
        return Agent(
            role='Senior System Analyst',
            goal='Expand the project description by getting more information from the user.',
            backstory=dedent("""\
                             You are an expert in system analysis.
                             You are able to communicate effectively with both technical and non-technical stakeholders.
                             This includes active listening, asking questions, and explaining technical concepts in simple terms.
                             You are able to process and interpret the information from stakeholders to identify patterns, trends, and gaps in the information.
                             You are able to assess the validity and reliability of the sources.
                             You are attentive to details and able to identify inconsistencies in the information provided.
                             You are always thorough in your analysis to find any and all the information required to properly define a software development project.
                             You enjoy generating the most accurate and complete project descriptions possible.
                             You will cover all the most important aspects of the project, including but not limited to:
                                - the project's goals and objectives;
                                - major features;
                                - constraints, assumptions, and risks;
                                - target audience;
                                - security requirements, line authentication, authorization, and data protection;
                                - data requirements, like data sources, data formats, data storage, data access;
                                - design preferences, like colors, fonts, themes, layouts, navigation;
                                - development requirements, like programming languages, frameworks, and tools;
                             You will analyze the current information about the project and ask the user for more details to refine the project description.
                             You will keep asking until you have all the information you need to properly define the project or until the user asks you to proceed.
                             """),
            memory=True,
            verbose=True,
            allow_delegation=False
        )
