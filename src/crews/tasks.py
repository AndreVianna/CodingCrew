"""Tasks for the planning crew."""

from textwrap import dedent
from crewai import Task

from crews.models import CrewInput, CrewOutput

class PlanningTasks:
    """
    A class that defines tasks related to project planning and analysis.
    """

    def initial_analysis(self, agent, data: CrewInput) -> Task:
        """
        Task to analyze the initial information about the project and ask the user for more details to refine the project description if necessary.

        Parameters:
        - agent (str): The name of the agent responsible for the task.
        - state (CrewInput): The current state of the planning workflow.

        Returns:
        - Task: A Task object representing the initial analisys task.
        """
        queries_output = ''
        if data['queries'] is not None:
            queries_output = "\n\nQueries:\n"
            for i, query in enumerate(data['queries']):
                question = query['question']
                answer = query['answer']
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
                The ADDITIONAL QUESTIONS should be clear, concise, and relevant to the project.
                You can ask as many ADDITIONAL QUESTIONS as you need to properly define the project.
                When you ask a question, explain what information you expect to get from that question, and how it will help you to refine the project description. For example:
                 - What is the Project Objective?\nDescribe the specific objectives of the project. What value does this project add to the organization? What results are expected?  What are the deliverables?  What benefits will be realized?  What problems will be resolved? 
                 - What is the Project Scope?\nDescribe the scope of the project. The project scope establishes the boundaries of the project. It identifies the limits of the project and defines the deliverables.  
                 - What are the Major Features?\nDescribe the key functionalities of the project. What are the main components of the project? What are the main use cases of the project?
                 - What is the major components of the project?\nIs it a console application, API, library, web application, mobile application, desktop application, or background service? Are there multiple components? How are they connected?
                 - Does the project requires a frontend?\nDescribe if the project requires a frontend. That is, if the project requires a user interface that interacts with the user.
                 - What is the os and platform of the components?\nIs it Windows, Linux, macOS, Android, iOS, web, or a combination of these?
                 - What are the programming languages, frameworks, and tools used by the project's components?\nIs it Python, Java, C#, RUST, .NET, Flutter, Node.js, React, Angular, or some other technology?
                 - What are the Professional Resources?\nDescribe the professional resources required by the project. What roles are needed? What skills are required? Like developers, designers, testers, project managers, etc.
                 - What are the Assumptions?\nDescribe the assumptions that have been made in the project. Assumptions are factors that are considered to be true, real, or certain without proof or demonstration.
                 - What are the Constraints?\nDescribe the constraints that have been identified in the project. Constraints are factors that limit the project team's options.
                 - What are the Risk?\nDescribe the risks that have been identified in the project. Risks are potential events or conditions that can have a negative impact on the project.
                 - Who is the Target Audience?\nDescribe the target audience of the project. Who are the end users of the project? What are their needs, preferences, and expectations?
                 - What are the Authentication Requirements?\nDescribe the authentication requirements of the project. How will users be authenticated? What security measures are in place to protect user data?
                 - What are the Authorization Requirements?\nDescribe the authorization requirements of the project. What permissions and roles are assigned to users? What actions can users perform?
                 - What are the Data Storage Requirements?\nDescribe the data storage requirements of the project. What data needs to be stored? How will the data be stored? Where will the data be stored?
                 - What are the External Connections?\nDescribe the external connections required by the project. What external sources, services, or APIs are needed? How will the project interact with these external entities?
                If the project requires a frontend, you can ask additional questions about the design preferences and navigation. For example:
                 - what is the UI fremework used?\nDescribe the UI framework used by the project. Bootstrap, Materialize, Tailwind, or custom?
                 - What are the Design Preferences?\nDescribe the design preferences of the project. What theme, style, color palette, font, or layout are preferred? What design principles should be followed?
                 - What are the views or pages and how to navigate between them?\nDescribe the main views/pages of the project. How are they connected? How can users navigate between them?
                If the user introduces specifc components like a database, api, or external service, you can ask additional questions about each these components. For example:
                 - For the datanase "XYZ", how is the data stored and accessed?\nDescribe how the data is stored and accessed in the database XYZ. What tables, fields, and relationships are used? What queries are performed? What data is returned?
                 - For the API "XYZ", what are the endpoints and data formats?\nDescribe the endpoints and data formats used by the API XYZ. What data can be retrieved or sent? What methods are available? What data formats are used?
                 - For the service "XYZ", how is the service accessed and what data is returned?\nDescribe how the service XYZ is accessed. What data is returned? What methods are available? What data formats are used?
                If the user introduces specifc terms or concepts that you are not familiar with, do not hesitate to ask for clarification. For example:
                Do NOT limit yourself to these questions. Feel free to ask any question that you think will help you to refine the project description.
                IMPORTANT! For each question, if you have a proposed solution for the question, you should also add your proposal to it.
                Your proposal should be clear, concise, relevant to the project, and be a solution to the question.
                IMPORTANT! Do not add a proposal if the answer is to be left completly to the user to answer or you do not have a good proposal to it.
                IMPORTANT! Ask first the questions that do not require information previously provided by the user. To give a proper proposal about the required professional resources, you need to know the project's goals and objectives, and the project components. So do not ask about the professional resources before havind all the required information to make a proposal.
                For example:
                 - Question: What is the Project Objective?\nDescribe the specific objectives of the project. What value does this project add to the organization? What results are expected?  What are the deliverables?  What benefits will be realized?  What problems will be resolved?
                 - Proposal: None (The user should provide the answer to this question.)
                 - Question: Does the project requires a frontend?\nDescribe if the project requires a frontend. That is, if the project requires a user interface that interacts with the user.
                 - Proposal: The user responded previously that the project is a web application, because of that, the project requires a frontend. 
                 - Question: What are the Professional Resources?\nDescribe the professional resources required by the project. What roles are needed? What skills are required? Like developers, designers, testers, project managers, etc.
                 - Proposal: The project requires a team of developers, designers, testers, and a project managers. The developers should have experience with Python, Django, and React. The designers should have experience with UI/UX design. The testers should have experience with automated testing. The project managers should have experience with Agile methodologies.
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
                 - each object in the array must have:
                   - a string parameter named "text" containing the question to ask the user; and
                   - a optional string parameter named "proposal" containing the analyst proposal to that question. If no proposal is given send an empty string.
                Here is an example of the expected output:
                {
                    "description": "The project is a simple calculator that performs basic arithmetic operations like addition, subtraction, multiplication, and division.",
                    "questions": [
                        {
                            "text": "What is the Project Objective?",
                            "proposal": "The project objective is to create a simple calculator that performs basic arithmetic operations like addition, subtraction, multiplication, and division."
                        },
                        {
                            "text": "What are the Major Features?",
                            "proposal": ""
                        }
                    }
                }
                IMPORTANT! If the user asks you to finish, you should return only the updated project description and an empty array of ADDITIONAL QUESTIONS.
                IMPORTANT! If you DO NOT HAVE any ADDITIONAL QUESTIONS to ask, you should return only the updated project description and an empty array of questions.
                """)
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            output_json=CrewOutput,
        )

    def final_report(self, agent, data: CrewInput) -> Task:
        """
        Task to analyze the current information about the project and generate a Project Summary Report.

        Parameters:
        - agent (str): The name of the agent responsible for the task.
        - state (CrewInput): The current state of the planning workflow.

        Returns:
        - Task: A Task object representing the final analysis task.
        """
        queries_output = ''
        if data['queries'] is not None:
            queries_output = "\n\nQueries:\n"
            for i, query in enumerate(data['queries']):
                question = query['question']
                answer = query['answer']
                queries_output += f"{i+1}. {question}\n{answer}\n\n"

        description = dedent(f"""\
                The objective is analyze the current information about the project including the queries submited to the user to generate a Project Summary Report.
                The report in markdown format should contain all the information required to properly define the project.
                You will base your analysis on the following information:
                -----------------------
                Project Name: {data['project_name']}
                
                Project Description:
                {data['project_description']}
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
                """)
        expected_output = dedent("""\
                Your final answer MUST be a markdown document containing the Project Summary Report.
                """)
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
        )
