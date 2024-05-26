"""Tasks for the planning crew."""

from textwrap import dedent
from crewai import Task

from workflows.planning.states import PlanningState, InitialAnalysisResult

class PlanningTasks:
    """
    A class that defines tasks related to project planning and analysis.
    """

    def initial_analysis(self, agent, state: PlanningState) -> Task:
        """
        Task to analyze the initial information about the project and ask the user for more details to refine the project description if necessary.

        Parameters:
        - agent (str): The name of the agent responsible for the task.
        - state (PlanningState): The current state of the planning workflow.

        Returns:
        - Task: A Task object representing the initial analisys task.
        """
        queries_output = ''
        context = state['context']
        if (context is not None):
            queries_output = "Pending Questions:\n"
            previous_queries = context['queries']
            if previous_queries is not None:
                for i, query in enumerate(previous_queries):
                    question = query['question']
                    answer = query['answer']
                    queries_output += f"{i+1}. {question}\n{answer}\n\n"
            queries_output += F"Proceed: {context['proceed']}"

        description = dedent(f"""\
                Analyze the current information about the project.
                Use your expertise in system analysis to identify patterns, trends, and gaps in the information provided.
                Assess the validity and reliability of the sources.
                Be attentive to details and identify inconsistencies in the information provided.
                IMPORTANT! if necessary, ask the user questions to refine the project description.
                Keep asking until you have all the information you need to properly define the project or until the user asks you to proceed.
                Make sure to cover all the most important aspects of the project, including but not limited to:
                - the project type, like a console application, API, library, web application, mobile application, desktop application, or background service;
                - the os and platform of the project, like Windows, Linux, macOS, Android, iOS, or web;
                - the programming languages, frameworks, and tools;
                - the project's goals and objectives;
                - major features;
                - constraints, assumptions, and risks;
                - target audience;
                - security requirements, like authentication, authorization, and data protection;
                - data requirements, like data sources, data formats, data storage, data access;
                - design preferences, like colors, fonts, themes, layouts, navigation;

                Project Information:
                -------
                Project Name: {state['project_name']}
                Project Description:
                {state['project_description']}
                {queries_output}
                -------
                """)
        expected_output = dedent("""\
                Your final answer MUST be a json containing:
                 - a string parameter named "updated_description" containing an UPDATED DESCRIPTION of the project based on the PROJECT DESCRIPTION and answers to the PENDING QUESTION.
                 - a string array parameter named "additional_questions" containing the ADDITIONAL QUESTIONS you want to ask the user to improva and refine the project description.
                The ADDITIONAL QUESTIONS should be clear, concise, and relevant to the project.
                You can ask as many ADDITIONAL QUESTIONS as you need to properly define the project.
                IMPORTANT! If the user asks you to PROCEED, you should return only the updated project description and an empty array of ADDITIONAL QUESTIONS.
                IMPORTANT! If you DO NOT HAVE any ADDITIONAL QUESTIONS to ask, you should return only the updated project description and an empty array of questions.
                """)
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            output_json=InitialAnalysisResult,
        )
