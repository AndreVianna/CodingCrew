import json
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from models.project_state import ProjectState
from models.query import Query
from utils.common import ask_model, normalize_text

class Response(BaseModel):
    queries: list[Query]

def create(state: ProjectState) -> ProjectState:
    agent_description = """
        You are a Senior System Analyst and an expert in system analysis.
        You are able to communicate effectively with both technical and non-technical stakeholders.
        This includes active listening, asking questions, and explaining technical concepts in simple terms.
        You are able to process and interpret the information from different sources to identify patterns, trends, and gaps in the information.
        You are able to assess the validity, reliability and completude of the information provided.
        You are attentive to details and thorough in your analysis.
        You enjoy asking questions about the project to make sure it is well defined.
        """

    task_description = """
        The objective is to understand the description of the project and and the answers to the listed questions.
        Assess the validity and reliability of the information.
        Use your expertise in system analysis assess the validity, reliability and completude of the information.
        Be attentive to details and identify inconsistencies in the information provided.
        In the end, if necessary, you should ask additional questions to refine, complete and correct the project description.
        Ask as many questions as necessary.
        Make sure to consider all the important aspects of a software project, including but not limited to:
            - Major components, like a console application, API, library, web application, mobile application, desktop application, or background service;
            - OS and Platform of the project, like Windows, Linux, macOS, Android, iOS, or web;
            - Programming Languages, Frameworks, and/or Tools;
            - Professional Resources Required, like developers, designers, testers, and project managers;
            - Goals and Objectives;
            - Major Features;
            - Constraints, Assumptions, and Risks;
            - Target Audience;
            - System architecture, like layers, components, services, and data flows;
            - Security Requirements, like authentication, authorization, and data protection;
            - Data Management like data storage, or external data sources;
            - Externat Resources like services or APIs;
            - Design preferences, like colors, fonts, themes, layouts, navigation;
            - UI requiremtns, like pages, components, and navigation;
            - and more.
        IMPORTANT! When asking a question, explain why you are asking it and what information you expect to get from that question.
        IMPORTANT! For all the questions you ask you must provide the answer that you consider the most appropriated to that question.
        IMPORTANT! You MUST NOT ASK a question that is already ANSWERED BY the CURRENT DESCRIPTION or the EXISTING ANSWERS.
        IMPORTANT! You MUST NOT ASK a question that is NOT RELATED or RELEVANT to the PROJECT.
        """

    expected_result = """
        Your final answer MUST be in a JSON format.
        It MUST BE only the JSON.
        It MUST NOT contain any title, preamble, conclusion or additional information.
        Here is the JSON schema for the answer:
        ```json
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Generated schema for Root",
            "type": "object",
            "properties": {
                "queries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string"
                            },
                            "answer": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "question",
                            "answer"
                        ]
                    }
                }
            },
            "required": [
                "queries"
            ]
        }
        ```
        IMPORTANT! All linebreaks with strings must be escaped with the character sequence '\\n'.
        IMPORTANT! If you DO NOT HAVE any QUESTIONS to ask, you MUST return the json with an EMPTY ARRAY of queries.
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
        {state.description[-1]}"
        {queries}
        """)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ]

    model_response = ask_model(messages)
    response_json = json.loads(model_response)
    response = Response(**response_json)
    state.queries.extend(response.queries)
    state_file = f"{state.folder}/state.json"
    with open(state_file, "w", encoding="utf-8") as state_file:
        state_file.write(state.to_json())
    return state

def to_query(entry: dict[str, str]) -> Query:
    result = Query()
    result.__dict__ = entry
    return result
