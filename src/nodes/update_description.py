import json
from typing import ClassVar
from pydantic import BaseModel

from nodes.base_analysis_task import BaseAnalysisTask

from models.project_state import ProjectState
from utils.common import normalize_text

class UpdateDescriptionResponse(BaseModel):
    description: str
    json_schema: ClassVar[str] = normalize_text("""\
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
        """)

class UpdateDescription(BaseAnalysisTask[ProjectState, UpdateDescriptionResponse]):
    def __init__(self) -> None:
        goal = """
            Your goal is to generate an updated description of the project.
            You MUST analyze all the project definition provided by the USER, including the PROJECT DESCRIPTION and the ANSWERS to the previous questions.
            You MUST include in the NEW UPDATED DESCRIPTION all the existing information in the current descripiotn and the new information added through the answers.
            You MUST provide a clear and complete description of the project.
            The description MUST be composed of CHAPTERS, aggregating the main points of the analysis.
            Each CHAPTER MUST HAVE BULLET POINTS representing the main aspects of the application.
            Each BULLET POINT MUST HAVE a TITLE and a short description explaining that topic, how it is related to the project and the solution adopted.
            The description can be as long as necessary. DO NOT WORRY about the length of the chapters or bullet point text.
            """
        super().__init__(goal, UpdateDescriptionResponse, allow_markdown=True)

    def _update_state(self, response: UpdateDescriptionResponse, state: ProjectState) -> ProjectState:
        state.description.append(response.description)
        state.counter += 1
        for query in state.queries:
            query.done = True
        state_file = f"{state.folder}/state.json"
        with open(state_file, "w", encoding="utf-8") as state_file:
            json.dump(state, state_file)
        return state
