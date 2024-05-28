"""
Represents a task to analyze the initial information about the project and ask the user for more details to refine the project description if necessary.
"""

from textwrap import dedent
from crewai import Task

from models.crew import CrewInput, CrewOutput

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

    description = dedent(f"""\
            The objective is to gather all the information required to build a detailed project charter.
            Analyze the current information about the project including the description and the answers provided by the user.
            Use your expertise in system analysis to identify patterns, trends, and gaps in the information provided.
            Assess the validity and reliability of the information.
            Be attentive to details and identify inconsistencies in the information provided.
            IMPORTANT! Ask the user questions to refine the project description.
            Keep asking until you have all the information you need to properly define the project charter or until the user asks you to finish.
            Make sure to cover all the most important aspects of the project, including but not limited to:
                - the major components, like a console application, API, library, web application, mobile application, desktop application, or background service;
                - the os and platform of the project, like Windows, Linux, macOS, Android, iOS, or web;
                - the programming languages, frameworks, and tools;
                - the professional resources, like developers, designers, testers, and project managers;
                - the project's goals and objectives;
                - major features;
                - constraints, assumptions, and risks;
                - target audience;
                - security requirements, like authentication, authorization, and data protection;
                - data and services requirements, like data storage, external sources, services or APIs;
                - design preferences, like colors, fonts, themes, layouts, navigation;
            The ADDITIONAL QUESTIONS MUST be clear, concise, and relevant to the project.
            You can ask as many ADDITIONAL QUESTIONS as you need to properly define the project.
            IMPORTANT! When you ask a question add an explain what information you expect to get from that question, and how it will help you to refine the project description.
            Here are some examples of questions, their full text are between '[' and ']':
                -> [What is the Project Objective?
                    Describe the specific objectives of the project. What value does this project add to the organization? What results are expected?  What are the deliverables? What benefits will be realized? What problems will be resolved?]
                -> [What is the Project Scope?
                    Describe the scope of the project. The project scope establishes the boundaries of the project. It identifies the limits of the project and defines the deliverables.]
                -> [What are the Major Features?
                    Describe the key functionalities of the project. What are the main components of the project? What are the main use cases of the project?]
                ->  [What is the major components of the project?
                    Is it a console application, API, library, web application, mobile application, desktop application, or background service? Are there multiple components? How are they connected?]
                -> [Does the project requires a frontend?
                    Describe if the project requires a frontend. That is, if the project requires a user interface that interacts with the user.]
                -> [What is the os and platform of the components?
                    Is it Windows, Linux, macOS, Android, iOS, web, or a combination of these?]
                -> [What are the programming languages, frameworks, and tools used by the project's components?
                    Is it Python, Java, C#, RUST, .NET, Flutter, Node.js, React, Angular, or some other technology?]
                -> [What are the Professional Resources?
                    Describe the professional resources required by the project. What roles are needed? What skills are required? Like developers, designers, testers, project managers, etc.]
                -> [What are the Assumptions?
                    Describe the assumptions that have been made in the project. Assumptions are factors that are considered to be true, real, or certain without proof or demonstration.]
                -> [What are the Constraints?
                    Describe the constraints that have been identified in the project. Constraints are factors that limit the project team's options.]
                -> [What are the Risk?
                    Describe the risks that have been identified in the project. Risks are potential events or conditions that can have a negative impact on the project.]
                -> [Who is the Target Audience?
                    Describe the target audience of the project. Who are the end users of the project? What are their needs, preferences, and expectations?]
                -> [What are the Authentication Requirements?
                    Describe the authentication requirements of the project. How will users be authenticated? What security measures are in place to protect user data?]
                -> [What are the Authorization Requirements?
                    Describe the authorization requirements of the project. What permissions and roles are assigned to users? What actions can users perform?]
                -> [What are the Data Storage Requirements?
                    Describe the data storage requirements of the project. What data needs to be stored? How will the data be stored? Where will the data be stored?]
                -> [What are the External Connections?
                    Describe the external connections required by the project. What external sources, services, or APIs are needed? How will the project interact with these external entities?]
            If the project requires a frontend, you can ask additional questions about the design preferences and navigation. For example:
                -> [what is the UI fremework used?
                    Describe the UI framework used by the project. Bootstrap, Materialize, Tailwind, or custom?]
                -> [What are the Design Preferences?
                    Describe the design preferences of the project. What theme, style, color palette, font, or layout are preferred? What design principles should be followed?]
                -> [What are the views or pages and how to navigate between them?
                    Describe the main views/pages of the project. How are they connected? How can users navigate between them?]
            If the user introduces specifc components like a database, api, or external service, you can ask additional questions about each these components. For example:
                -> [For the datanase "XYZ", how is the data stored and accessed?
                    Describe how the data is stored and accessed in the database XYZ. What tables, fields, and relationships are used? What queries are performed? What data is returned?]
                -> [For the API "XYZ", what are the endpoints and data formats?
                    Describe the endpoints and data formats used by the API XYZ. What data can be retrieved or sent? What methods are available? What data formats are used?]
                -> [For the service "XYZ", how is the service accessed and what data is returned?
                    Describe how the service XYZ is accessed. What data is returned? What methods are available? What data formats are used?]
            Do NOT limit yourself to these questions. Feel free to ask any question that you think will help you to refine the project description.
            IMPORTANT! For each question, if you have a proposed solution for the question, you MUST also add your proposed answer to it.
            Your proposed answer MUST be clear, concise, relevant to the project, and be a solution to the question.
            Your proposed answer MUST NOT be a question it MUST be assertive.
            IMPORTANT! Do not add a proposed answer if the answer is to be left completly to the user to answer or you do not have a good proposed answer to it.
            IMPORTANT! Ask first the questions that do not require information previously provided by the user. To give a proper proposed answer about the required professional resources, you need to know the project's goals and objectives, and the project components. So do not ask about the professional resources before havind all the required information to make a proposed answer.
            For example:
                - For the question "Does the project requires a frontend?" you could add the following proposed answer:
                - "The user responded previously that the project is a web application, because of that, the project requires a frontend."
                - For the question "What are the Professional Resources?" you could add the following proposed answer:
                - "The project requires a team of developers, designers, testers, and a project managers. The developers MUST have experience with Python, Django, and React. The designers MUST have experience with UI/UX design. The testers MUST have experience with automated testing. The project managers MUST have experience with Agile methodologies."
                - For the question "What are the Authentication Requirements?" you could add the following proposed answer:
                - "The project requires user authentication using JWT tokens. The users will be authenticated using a username and password. The authentication process will be handled by a custom authentication service."
            Is it ok not having any more relevant additional questions.
            IMPORTANT! DO NET REPEAT A QUESTION. if an information was already answered by a previous question do not request again the same information.

            Project Information
            -------
            Project Name: {data['project_name']}

            Project Description:
            {data['project_description']}
            {queries_output}
            -------

            Finish: {data['finish']}
            """)
    expected_output = dedent("""\
            Your final answer MUST be a json containing:
                - a string parameter named "description" containing an UPDATED DESCRIPTION of the project based on the PROJECT DESCRIPTION and answers to the PENDING QUESTION.
                - an object array parameter named "questions" containing the ADDITIONAL QUESTIONS you want to ask the user to improva and refine the project description.
                - each object in the array MUST have:
                - a string parameter named "text" containing the question to ask the user; and
                - a optional string parameter named "proposed answer" containing the analyst proposed answer to that question. If no proposed answer is given send an empty string.
            Here is an example of the expected output:
            {
                "description": "The project is a simple calculator that performs basic arithmetic operations like addition, subtraction, multiplication, and division.",
                "questions": [
                    {
                        "text": "What is the Project Objective?",
                        "proposed answer": "The project objective is to create a simple calculator that performs basic arithmetic operations like addition, subtraction, multiplication, and division."
                    },
                    {
                        "text": "What are the Major Features?",
                        "proposed answer": ""
                    }
                }
            }
            IMPORTANT! If the user asks you to finish (Finish: True), you MUST return only the updated project description and an empty array of ADDITIONAL QUESTIONS.
            IMPORTANT! If you DO NOT HAVE any ADDITIONAL QUESTIONS to ask, you MUST return only the updated project description and an empty array of questions.
            """)
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        output_json=CrewOutput,
    )
