import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

from models.project_state import ProjectState
from utils.general import normalize_text

def create(state: ProjectState) -> ProjectState:
    model_provider = os.environ["MODEL_PROVIDER"]
    model_name = os.environ[f"{model_provider.upper()}_MODEL"]
    model = init_chat_model(model_name, model_provider=model_provider, temperature=0)

    parser = StrOutputParser()

    agent_description = normalize_text("""\
        You are a Senior System Analyst and an expert in system analysis.
        You are able to communicate effectively with both technical and non-technical stakeholders.
        This includes active listening, asking questions, and explaining technical concepts in simple terms.
        You are able to process and interpret the information from different sources to identify patterns, trends, and gaps in the information.
        You are able to assess the validity and reliability of the sources.
        You are attentive to details and able to identify inconsistencies in the information provided.
        You are always thorough in your analysis to find any and all the information required to properly define a software development project.
        You enjoy generating the most accurate and complete project descriptions possible.
        """)



    task_description = normalize_text("""\
        Your goal is to generate an updated description of the project.
        Your will analyze all the information provided about the project by the user.
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
        IMPORTANT! DO NOT make assumptions and DO NOT add information that was not provided yet.
        IMPORTANT! DO NOT add unanswered questions to the description.
        """)

    expected_result = normalize_text("""\
        Your final answer MUST be an updated description of the project.
        The text MUST be clear, concise, and easy to understand.
        You MUST present only the content of the description, without any preamble, conclusion or additional information that is not part of the description.
        The description MUST be organized in in paragraphs and bullet points to help any person to understand the project.
        The description MUST NOT contain unanswered questions, it MUST be an assertive and thoughtful overview of the project.
        IMPORTANT! You MUST NOT add any information that is not in the previous description or in the answers provided by the user.
        You MUST NOT make assumptions or add information that was not yet provided.
        """)

    system_message = normalize_text(
        f"""
        {agent_description}
        -----------------------------------------------------------

        Task Description
        -----------------------------------------------------------
        {task_description}
        -----------------------------------------------------------

        Expected Result
        -----------------------------------------------------------
        {expected_result}
        -----------------------------------------------------------
        """)

    # queries: str = ""
    # if state["queries"]:
    #     for i, query in enumerate(state["queries"]):
    #         queries += normalize_text(f"""\
    #         {i+1}.
    #         Question: {query["question"]}
    #         Answer: {query["answer"]}
    #
    #         """)

    user_message = normalize_text(f"""\
        Project Name: {state.name}
        Project Description:
        {state.description[-1]}
        """)

    result = model.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ])

    response = parser.invoke(result)

    state.description.append(response)
    return state
