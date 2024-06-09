"""
Represents the task to generate a Project Summary Report.
"""

from crewai import Task

from models.crew import CrewInput

# pylint: disable=import-error
from utils.general import normalize_text

# pylint: enable=import-error


def create(agent, data: CrewInput) -> Task:
    """
    Task to analyze the current information about the project and generate a Project Summary Report.

    Parameters:
    - agent (str): The name of the agent responsible for the task.
    - state (CrewInput): The current state of the planning workflow.

    Returns:
    - Task: A Task object representing the final analysis task.
    """
    queries_output = ""
    if data["queries"] is not None:
        queries_output = """

            Queries:
            """
        total = len(data["queries"])
        for i, query in enumerate(data["queries"]):
            question: str = query["question"]
            answer: str = query["answer"]
            queries_output += normalize_text(
                f"""

                Question {i+1} of {total}:
                {question}
                Answer:
                {answer}
                """
            )

    description = normalize_text(
        f"""
                            The objective is analyze the current information about the project including the queries submited to the user to generate a Project Summary Report.
                            The report in markdown format should contain all the information required to properly define the project.
                            You will base your analysis on the following information:
                            -----------------------
                            Project Name: {data["project_name"]}

                            Project Description:
                            {data["project_description"]}
                            {queries_output}
                            -----------------------

                            The final report should be very detailed and use the following template:
                            -----------------------
                            # [[Add here the Project Name]]
                            #### Projecj Summary Report

                            ## Project Brief Summary
                            [[add here a brief summary of the project]]

                            ## Project Goals and Objectives
                            [[add here the project goals and objectives]]

                            ## Project Scope
                            [[add here the project scope]]

                            ## Major Features
                                - **[[feature name]]**: [[detailed feature description]]
                                - **[[feature name]]**: [[detailed feature description]]
                                [[add the other features here as a bullet list like above]]

                            ## Major Components
                                - **[[component name]]**: [[detailed component description including the programming languages, frameworks, and tools used]]
                                - **[[component name]]**: [[detailed component description including the programming languages, frameworks, and tools used]]
                                [[add the other components here as a bullet list like above]]

                            ## Professional Resources
                                - **[Professional Type]] ([[number of professionals]])**: [[decribe the required professional skils and type of activities they will execute in the project]]
                                - **[Professional Type]] ([[number of professionals]])**: [[decribe the required professional skils and type of activities they will execute in the project]]
                                [[add the other professional resources here as a bullet list like above]]

                            ## Assumptions, Constraints, and Risks
                            ### Assumptions
                                - **[[assumption name]]**: [[detailed assumption description]]
                                - **[[assumption name]]**: [[detailed assumption description]]
                                [[add the other assumptions here as a bullet list like above]]

                            ### Constraints
                                - **[[constraint name]]**: [[detailed constraint description]]
                                - **[[constraint name]]**: [[detailed constraint description]]
                                [[add the other constraints here as a bullet list like above]]

                            ### Risks
                                - **[[risk name]]**: [[detailed risk description]]
                                - **[[risk name]]**: [[detailed risk description]]
                                [[add the other risks here as a bullet list like above]]

                            ## Target Audience
                            [[add here the target audience of the project]]

                            ## Backend Requirements
                            ### Security
                            #### Authentication
                            [[add here the authentication requirements of the project]]

                            #### Authorization
                            [[add here the authorization requirements of the project]]

                            ### Data, External Connections (API, Services, etc)
                            #### Data Storage
                            [[add here the data storage requirements of the project]]

                            #### External Connections
                            [[add here the external connections required by the project]]

                            ## Frontend Requirements
                            ### UI Framework
                            [[add here the UI framework used by the project]]

                            ### Design Preferences
                            [[add here the design preferences of the project]]

                            ### Views/Pages and Navigation
                                - **[[view or page name]]**: [[detailed view or page description and how to navigate to and from it]]
                                - **[[view or page name]]**: [[detailed view or page description and how to navigate to and from it]]
                                [[add the other views or pages here as a bullet list like above]]

                            ## Additional Information
                            [[add here any additional or specific information that is relevant to the project]]
                            -----------------------
                            """
    )
    expected_output = normalize_text(
        """
                            Your final answer MUST be a markdown document containing the Project Summary Report.
                            """
    )
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )
