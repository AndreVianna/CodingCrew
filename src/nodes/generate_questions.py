import json
from typing import ClassVar

from models import UpdateDescriptionState
from responses import GenerateQuestionsResponse

from .base_analysis_task import BaseAnalysisTask

class GenerateQuestions(BaseAnalysisTask[UpdateDescriptionState, GenerateQuestionsResponse]): # pylint: disable=too-few-public-methods
    name: ClassVar[str] = "generate_questions"
    def __init__(self) -> None:
        goal = """
            The objective is to understand the current project definition provided by the USER.
            The project definition is composed by the project description and the answers to the previous questions.
            After the analysis you should, IF NECESSARY, ask additional questions to refine, complete and correct the project definition.
            IMPORTANT! You DO NOT ASK a question that is NOT RELATED nor RELEVANT to the PROJECT.
            IMPORTANT! You DO NOT ASK a question that is already ANSWERED BY the CURRENT DESCRIPTION or the EXISTING ANSWERS.
            IMPORTANT! When asking a question, explain why you are asking it and what information you expect to get from that question.
            IMPORTANT! For all the questions you ask you must provide the answer that you consider the most appropriated to that question.
            IMPORTANT! If the project definition does not provide enough information for you to answer the question properly you most respond with: "According to the current definition, the project does not support that functionality." .
            """
        super().__init__(goal, GenerateQuestionsResponse)

    def _update_state(self, state: UpdateDescriptionState, response: GenerateQuestionsResponse) -> UpdateDescriptionState:
        state.queries.extend(response.queries)
        state_file = f"{state.folder}/state.json"
        with open(state_file, "w", encoding="utf-8") as state_file:
            json.dump(state, state_file)
        return state

    # def to_query(entry: dict[str, str]) -> Query:
    #     result = Query()
    #     result.__dict__ = entry
    #     return result
