from typing import ClassVar

from models import Project
from responses import GeneratedQueries
from states import AnalysisState

from utils.common import normalize_text

from .simple_analyst_agent_node import SimpleAnalystAgentNode

class GenerateQueries(SimpleAnalystAgentNode[AnalysisState, GeneratedQueries]): # pylint: disable=too-few-public-methods
    name: ClassVar[str] = "generate_questions"
    def __init__(self, state: Project) -> None:
        super().__init__(state, goal = normalize_text("""\
            Your goal is to understand the current project definition provided by the USER.
            The project definition is composed by the project description and the answers to the previous questions.
            After the analysis you should, IF NECESSARY, ask additional questions to refine, complete and correct the project definition.
            IMPORTANT! You DO NOT ASK a question that is NOT RELATED nor RELEVANT to the PROJECT.
            IMPORTANT! You DO NOT ASK a question that is already ANSWERED BY the CURRENT DESCRIPTION or the EXISTING ANSWERS.
            IMPORTANT! When asking a question, explain why you are asking it and what information you expect to get from that question.
            IMPORTANT! For all the questions you ask you must provide the answer that you consider the most appropriated to that question.
            IMPORTANT! If the project definition does not provide enough information for you to answer the question properly you most respond with: "According to the current definition, the project does not support that functionality." .
            """))

    def _create_result(self, response: GeneratedQueries) -> AnalysisState:
        result = AnalysisState(**self.state)
        result.queries.extend(response.value.items)
        result.save()
        return result
