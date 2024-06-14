from crewai import Task
from pydantic import BaseModel

from tasks.models import ProjectState, Query
from utils.general import normalize_text

class UpdateDescriptionInput(BaseModel):
    project_name: str
    project_description: str
    queries: list[Query]

def create(agent, data: ProjectState) -> Task:
    input_queries: str = ""
    if data["queries"] is not None:
        input_queries = "\nQueries:\n"
        for i, query in enumerate(data["queries"]):
            question: str = query["question"]
            answer: str = query["answer"]
            input_queries += f"{i+1}. {question}\n{answer}\n\n"
    input_queries = "No queries yet." if not input_queries else input_queries

    task_description = normalize_text(
      f"""
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
        IMPORTANT! DO NOT make assumptions and DO NOT add information that was not provided yet.
        IMPORTANT! DO NOT add unanswered questions to the description.

        Project Information
        -----------------------------------------------------------
        Project Name: {data["project_name"]}

        Project Description:
        {data["project_description"]}
        {input_queries}
        -----------------------------------------------------------
        """)

    task_output = normalize_text(
      """
      Your final answer MUST be a text containing the updated description of the project.
      The description MUST contain ALL the information relevant to the project in a clear, detailed, and concise way.
      The description MUST be organized in in paragraphs and bullet points to help any person to understand the project.
      The description MUST NOT contain unanswered questions, it MUST be an assertive and thoughtful overview of the project.
      IMPORTANT! You MUST NOT add any information that is not in the previous description or in the answers provided by the user.
      You MUST NOT make assumptions or add information that was not yet provided.
      """
    )

    return Task(
        description=task_description,
        expected_output=task_output,
        agent=agent,
    )
