"""
Represents a task to analyze the initial information about the project and ask the user for more details to refine the project description if necessary.
"""

from crewai import Task

from models.crew import CrewInput, CrewOutput
from utils import outdent

def create(agent, data: CrewInput) -> Task:
    """
    Task to analyze the initial information about the project and ask the user for more details to refine the project description if necessary.

    Parameters:
    - agent (str): The name of the agent responsible for the task.
    - state (CrewInput): The current state of the planning workflow.

    Returns:
    - Task: A Task object representing the initial analisys task.
    """
    queries_output: str = ''
    if data['queries'] is not None:
        queries_output = "\nQueries:\n"
        for i, query in enumerate(data['queries']):
            question: str = query['question']
            answer: str = query['answer']
            queries_output += f"{i+1}. {question}\n{answer}\n\n"

    analysis_description = outdent(f"""\
                                The objective is to analyze the all the information provided about the project, including the current description and the answers to the existing questions and generate an updated description of the project.
                                Use all your expertise in system analysis to identify patterns, trends, and gaps in the information provided.
                                Assess the validity and reliability of the information.
                                Be attentive to details and identify inconsistencies in the information provided.
                                Make sure to try to cover all the most important aspects of the project, including but not limited to:
                                 - Major components, like a console application, API, library, web application, mobile application, desktop application, or background service;
                                 - OS and Platform of the project, like Windows, Linux, macOS, Android, iOS, or web;
                                 - Programming Languages, Frameworks, and/or Tools;
                                 - Professional Resources Required, like developers, designers, testers, and project managers;
                                 - Goals and Objectives;
                                 - Major Features;
                                 - Constraints, Assumptions, and Risks;
                                 - Target Audience;
                                 - Security Requirements, like authentication, authorization, and data protection;
                                 - Data Management like data storage, or external data sources;
                                 - Externat Resources like services or APIs;
                                 - Design preferences, like colors, fonts, themes, layouts, navigation;
                                 - UI requiremtns, like pages, components, and navigation;
                                IMPORTANT! DO NOT ADD to the description any information not found in the previous description or answered questions.
                                IMPORTANT! DO NOT MAKE assumptions or add information that was not yet provided.
                                IMPORTANT! DO NOT ADD unanswered questions to the description.

                                Project Information
                                -----------------------------------------------------------
                                Project Name: {data['project_name']}

                                Project Description:
                                {data['project_description']}
                                {queries_output}
                                -----------------------------------------------------------

                                User Rquested to Finish Analysis: {data['finish']}
                                """)

    questions_description = outdent(f"""\
                                The objective is to identify the gaps in the information provided about the project and ask for more details if needed.
                                Analyze the current information about the project including the description and the answers provided by the user.
                                Use your expertise in system analysis to identify patterns, trends, and GAPS in the information provided.
                                Assess the validity and reliability of the information.
                                Be attentive to details and identify inconsistencies in the information provided.
                                IMPORTANT! Ask as many questions to refine the project information as necessary.
                                IMPORTANT! If all the required information is already provided, do not ask any more questions.
                                IMPORTANT! Do not repeat a question that was already asked and answered.
                                Keep asking until you have all the information you need to properly define the project charter or until the user asks you to finish.
                                IMPORTANT! When you ask a question add an explain what information you expect to get from that question, and how it will help you to refine the project description.
                                Make sure to cover all the most important aspects of the project, including but not limited to:
                                 - What is the Project Goal? The project goal establishes the objectives of the project.
                                 - Who is the Target Audience? The target audience is the group of people who will be impacted by the project.
                                 - What is the Project Scope? The project scope establishes the boundaries of the project. It identifies the limits and defines the deliverables.
                                 - What are the Major Features? Major Features are the key functionalities in a high-level view.
                                 - What ara the Major Components? Major Components are the different applications or services that make up the project.
                                 - What is the OS and/or Platform? Like Windows, Linux, mobile, web, etc. Different components can be running on different platforms.
                                 - What are the programming languages, frameworks, and tools used? Like Python, Java, C#, RUST, .NET, Flutter, Node.js, React, Angular, etc.
                                 - What are the Professional Resources? Professional Resources are the people, organizations, or services that are required to perform the project tasks.
                                 - What are the Assumptions? Assumptions are the facts that are assumed to be true.
                                 - What are the Constraints? Constraints are factors that limit the project team's options.
                                 - What are the Risk? Risks are potential events or conditions that can have a negative impact on the project.
                                 - What are the Authentication Requirements? Authentication Requirements define how the users will be authenticated.
                                 - What are the Authorization Requirements? Authorization Requirements define whatm roles and permissions will be assigned to users.
                                 - What are the Data Storage Requirements? Data Storage Requirements define how the data will be stored ans retrived
                                 - What are the External Connections? External Connections are the external sources, services, or APIs that are required to perform the project tasks.
                                 - What are the Design Preferences? Design Preferences are the colors, fonts, themes, and  layouts that will be used in the project.
                                 - What are the views or pages and how to navigate between them? Those are the interfaces that will be used in the project and how they are connected.
                                Do NOT limit yourself to these questions. Feel free to ask any question that you think will help you to refine the project description.

                                Project Information
                                -----------------------------------------------------------
                                Project Name: {data['project_name']}

                                Project Description:
                                {data['project_description']}
                                {queries_output}
                                -----------------------------------------------------------

                                Finish: {data['finish']}
                                """)
    analysis_output = outdent("""\
                                Your final answer MUST be a text containing the updated description of the project.
                                The description MUST be contain the original description enriched with the answers provided by analysts and the user.
                                The description MUST contain ALL the information relevant to the project in a clear, detailed, and concise way.
                                The description MUST be organized in in paragraphs and bullet points to help any person to understand the project.
                                The description MUST NOT contain unanswered questions, it MUST be an assertive and thoughtful overview of the project.
                                IMPORTANT! You MUST NOT add any information that is not in the previous description or in the answers provided by the user.
                                You MUST NOT make assumptions or add information that was not yet provided.
                                """)

    questions_output = outdent("""\
                                Your final answer MUST be a json containing:
                                 - a string parameter named "description" containing an UPDATED DESCRIPTION of the project based on the PROJECT DESCRIPTION and answers to the PENDING QUESTION.
                                 - an object array parameter named "questions" containing the ADDITIONAL QUESTIONS you want to ask the user to improva and refine the project description.
                                 - each object in the array MUST have:
                                 - a string parameter named "text" containing the question to ask the user; and
                                 - a optional string parameter named "proposed answer" containing the analyst proposed answer to that question. If no proposed answer is given send an empty string.
                                Here is an example of the expected output:
                                ```json
                                {
                                  "description": "The project is a simple calculator that performs basic arithmetic operations like addition, subtraction, multiplication, and division.",
                                  "questions": [
                                    {
                                      "text": "What is the Project Objective?\nDescribe the specific objectives of the project. What value does this project add to the organization? What results are expected?  What are the deliverables? What benefits will be realized? What problems will be resolved?",
                                      "proposed answer": "The project objective is to create a simple calculator that performs basic arithmetic operations like addition, subtraction, multiplication, and division."
                                    },
                                    {
                                      "text": "What are the Major Features?\nDescribe the key functionalities of the project. What are the main components of the project? What are the main use cases of the project?",
                                      "proposed answer": ""
                                    }
                                  }
                                }
                                IMPORTANT! If the user asks you to finish (Finish: True), you MUST return only the updated project description and an empty array of ADDITIONAL QUESTIONS.
                                IMPORTANT! If you DO NOT HAVE any ADDITIONAL QUESTIONS to ask, you MUST return only the updated project description and an empty array of questions.
                                """)
    return Task(
        description=questions_description,
        expected_output=questions_output,
        agent=agent,
        output_json=CrewOutput,
    )
