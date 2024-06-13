import ast
from crewai import Task
from pydantic import BaseModel

from models.common import Query, Question
from utils.general import normalize_text


class GenerateQuestionsInput(BaseModel):
    project_name: str
    project_description: str
    queries: list[Query]
    finish: bool

class GenerateQuestionsOutput(BaseModel):
    questions: list[Question]

    @classmethod
    def from_json(cls, json_data: dict | str) -> "GenerateQuestionsOutput":
        if isinstance(json_data, str):
            json_data = ast.literal_eval(json_data.strip(" `\n"))
        return cls(**json_data)


def create(agent, data: GenerateQuestionsInput) -> Task:
    queries_output: str = ""
    if data["queries"] is not None:
        queries_output = "\nQueries:\n"
        for i, query in enumerate(data["queries"]):
            question: str = query["question"]
            answer: str = query["answer"]
            queries_output += f"{i+1}. {question}\n{answer}\n\n"

    task_description = normalize_text(
      f"""
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
      Here is a list of questions you can ask to refine the project description:
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
      Project Name: {data["project_name"]}

      Project Description:
      {data["project_description"]}
      {queries_output}
      -----------------------------------------------------------

      Finish: {data["finish"]}
      """
    )

    task_output = normalize_text(
        """
        Your final answer MUST be a json containing:
          - a string parameter named "description" containing an UPDATED DESCRIPTION of the project based on the PROJECT DESCRIPTION and answers to the PENDING QUESTION.
          - an object array parameter named "questions" containing the ADDITIONAL QUESTIONS you want to ask the user to improva and refine the project description.
          - each object in the array MUST have:
          - a string parameter named "text" containing the question to ask the user; and
          - a optional string parameter named "proposed answer" containing the analyst proposed answer to that question. If no proposed answer is given send an empty string.
        Here is the json schema for the answer:
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "type": "object",
          "title": "GenerateQuestionsOutput",
          "description": "Response for the task to generate questions to refine the project description.",
          "properties": {
            "questions": {
              "type": "array",
              "description": "The list of questions to ask the user to refine the project description.",
              "items": [
                {
                  "type": "object",
                  "description": "A question to ask the user to refine the project description.",
                  "properties": {
                    "text": {
                      "type": "string",
                      "description": "The question to ask the user."
                    },
                    "proposed_answer": {
                      "type": "string",
                      "description": "Add here your proposed answer to the question."
                    }
                  },
                  "required": [
                    "text",
                    "proposed_answer"
                  ]
                }
              ]
            }
          },
          "required": [
            "description",
            "questions"
          ]
        }
        IMPORTANT! If the user asks you to finish (Finish: True), you MUST return only the updated project description and an empty array of ADDITIONAL QUESTIONS.
        IMPORTANT! If you DO NOT HAVE any ADDITIONAL QUESTIONS to ask, you MUST return only the updated project description and an empty array of questions.
        """
    )
    return Task(
        description=task_description,
        expected_output=task_output,
        agent=agent,
        output_json=GenerateQuestionsOutput,
    )
