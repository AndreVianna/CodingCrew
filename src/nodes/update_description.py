import json
from typing import ClassVar

from models import Project, UpdateDescriptionModel
from responses import UpdatedDescription
from utils.common import normalize_text

from .simple_analysis_node import SimpleAnalysisNode

class UpdateDescription(SimpleAnalysisNode[UpdateDescriptionModel, UpdatedDescription]): # pylint: disable=too-few-public-methods
    name: ClassVar[str] = "update_description"
    def __init__(self, state: Project) -> None:
        super().__init__(state, goal = normalize_text("""\
            Your goal is to generate an updated description of the project.
            You MUST analyze all the project definition provided by the USER, including the PROJECT DESCRIPTION and the ANSWERS to the previous questions.
            You MUST include in the NEW UPDATED DESCRIPTION all the existing information in the current descripiotn and the new information added through the answers.
            You MUST provide a clear and complete description of the project.
            The description MUST be composed of CHAPTERS, aggregating the main points of the analysis.
            Each CHAPTER MUST HAVE BULLET POINTS representing the main aspects of the application.
            Each BULLET POINT MUST HAVE a TITLE and a short description explaining that topic, how it is related to the project and the solution adopted.
            The description can be as long as necessary. DO NOT WORRY about the length of the chapters or bullet point text.
            """))

    def _create_final_state(self, response: UpdatedDescription) -> UpdateDescriptionModel:
        self.state.description = response.description
        self.state.counter += 1
        for query in self.state.queries:
            query.done = True
        state_file = f"{self.state.folder}/state.json"
        with open(state_file, "w", encoding="utf-8") as state_file:
            json.dump(self.state, state_file)
        return self.state
