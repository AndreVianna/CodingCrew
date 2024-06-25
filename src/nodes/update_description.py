from pydantic import BaseModel

from nodes.base_analysis_task import BaseAnalysisTask

from models.project_state import ProjectState

from .common import JsonResponseFormat

class UpdateDescriptionResponse(BaseModel):
    description: str

class UpdateDescription(BaseAnalysisTask[ProjectState, UpdateDescriptionResponse]):
    def __init__(self) -> None:
        goal = """
            Your goal is to generate an updated description of the project.
            Your will analyze all the project definition provided by the USER, including the project description and the answers to the previous questions.
            """

        response_format = JsonResponseFormat(json_schema="""\
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
        super().__init__(goal, UpdateDescriptionResponse, response_format)

    def _update_state(self, response: UpdateDescriptionResponse, state: ProjectState) -> ProjectState:
        state.description.append(response.description)
        state.counter += 1
        for query in state.queries:
            query.done = True
        state_file = f"{state.folder}/state.json"
        with open(state_file, "w", encoding="utf-8") as state_file:
            state_file.write(state.to_json())
        return state
