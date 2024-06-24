import json
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from models.project_state import ProjectState
from utils.common import ask_model, normalize_text

class Response(BaseModel):
    description: str


def create(state: ProjectState) -> ProjectState:
    agent_description = """
        You are a Senior System Analyst and an expert in system analysis.
        You are able to communicate effectively with both technical and non-technical stakeholders.
        This includes active listening, asking questions, and explaining technical concepts in simple terms.
        You are able to process and interpret the information from different sources to identify patterns, trends, and gaps in the information.
        You are able to assess the validity and reliability of the sources.
        You are attentive to details and able to identify inconsistencies in the information provided.
        You are always thorough in your analysis to find any and all the information required to properly define a software development project.
        You enjoy generating the most accurate and complete project descriptions possible.
        """

    task_description = """
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
        """

    expected_result = """
        Your final answer MUST be in a JSON format.
        It MUST BE only the JSON.
        It MUST NOT contain any title, preamble, conclusion or additional information.
        Here is the JSON schema for the answer:
        ```json
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Response schema",
            "type": "object",
            "properties": {
                "description": {
                    "type": "string"
                }
            },
            "required": [
                "description"
            ]
        }
        ```
        IMPORTANT! All linebreaks with strings must be escaped with the character sequence '\\n'.
        The JSON must contain the updated description.
        The description MUST be clear, concise, and easy to understand.
        IMPORTANT! The description MUST contain all the information gathered so far. It MUST be a complete and accurate description of the project.
        IMPORTANT! The description MUST NOT contain unanswered questions or any information not provided by the user in the previous description or answered questions. You MUST NOT make assumptions.
        IMPORTANT! The text of the description MUST be organized in chapters and bullet points using markdown syntax to help any person to understand the project.
        IMPORTANT! The text of the description will be appended to a pre-existing document. So no need to add any title, preamble, or conclusion, just the content starting at LEVEL 3 of the markdown document.
        """

    system_message = normalize_text(f"""
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

    queries: str = ""
    if state.queries:
        queries = """\
        Queries:
        """
        for i, query in enumerate(state.queries):
            queries += f"""\
        {i+1}.
        Question: {query.question}
        Answer: {query.answer}

        """

    user_message = normalize_text(f"""\
        Project Name: {state.name}
        Project Description:
        {state.description[-1]}
        {queries}
        """)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ]
    model_response = ask_model(messages)
    response_json = json.loads(model_response)
    response = Response(**response_json)
    state.description.append(response.description)
    state.counter += 1
    for query in state.queries:
        query.done = True
    state_file = f"{state.folder}/state.json"
    with open(state_file, "w", encoding="utf-8") as state_file:
        state_file.write(state.to_json())
    return state
