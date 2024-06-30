import os
from datetime import datetime
from typing import Literal, Optional, TypeVar

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import LanguageModelInput
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from utils import terminal
from utils.common import normalize_text, is_verbose

from personas import BasePersona, DefaultPersona
from responses import BaseResponse, ConfirmationResponse, TextResponse

from .base_node import BaseNode

InitialState = TypeVar("InitialState", bound=BaseModel)
AgentPersona = TypeVar("AgentPersona", bound=BasePersona)
AgentResponse = TypeVar("AgentResponse", bound=BaseResponse)
ResultState = TypeVar("ResultState", bound=BaseModel)

class AgentNode[InitialState, AgentPersona, AgentResponse, ResultState](BaseNode[InitialState, ResultState]): # pylint: disable=too-few-public-methods
    def __init__(self,
                 state: InitialState,
                 agent: Optional[AgentPersona] = None,
                 goal: Optional[str] = None,
                 preamble_type: Literal["None", "Default", "Custom"] = "Default",
                 preamble: Optional[str] = None) -> None:
        super().__init__(state)
        preamble: str = normalize_text("""\
            This is a complex task that requires careful analysis.
            Let's do it step-by-step to arrive the best answer.""")

        self.agent = agent or DefaultPersona()
        self.goal = goal or "Your goal is to help the user to achieve the best answer."
        match preamble_type:
            case "None":
                self.preamble = ""
            case "Custom" if not preamble:
                raise ValueError("Preamble text is required when preamble type is 'Custom'.")
            case "Custom":
                self.preamble = preamble

    def _execute(self) -> ResultState:
        messages = [SystemMessage(content=self._get_system_message())]
        self._ask_model_to_acknowledge(messages, self.state.describe())
        response = self._ask_model_for_text(messages, "PROCEED")
        return self._create_result(response)

    def _ask_model_for_text(self, messages: LanguageModelInput, content: str) -> str:
        response_format = TextResponse.definition()
        messages.append(HumanMessage(content=self._get_user_message(content, response_format)))
        return self._ask_model(messages)

    def _ask_model_to_confirm(self, messages: LanguageModelInput, content: str) -> bool:
        messages.append(HumanMessage(content=self._get_user_message(content, ConfirmationResponse.definition())))
        response_text = self._ask_model(messages)
        return response_text.upper() == "YES"

    def _ask_model(self, messages: LanguageModelInput) -> str:
        response = ""
        finish = False
        original_user_message = messages[-1].content
        while not finish:
            model_response = self.__get_model().invoke(input=messages)
            if is_verbose:
                stop_reason = model_response.response_metadata["stop_reason"]
                terminal.write_line(f"Stop Reason: {stop_reason}", "yellow")
                input_tokens = model_response.usage_metadata["input_tokens"]
                output_tokens = model_response.usage_metadata["output_tokens"]
                total_tokens = model_response.usage_metadata["total_tokens"]
                terminal.write_line(f"Tokens: Input={input_tokens}; Output={output_tokens}; Total={total_tokens}")
                terminal.write_line(f"Model response: {model_response.content}", "green")
            response_text = StrOutputParser().invoke(model_response)
            response += response_text
            finish = model_response.response_metadata["stop_reason"] != "max_tokens"
            if not finish:
                messages[-1].content += os.linesep + response_text
            else:
                messages[-1].content = original_user_message
                messages.append(AIMessage(content=response))
        return response

    def __get_model(self):
        model_provider = os.environ["MODEL_PROVIDER"].upper()
        model_name = os.environ[f"{model_provider}_MODEL"]
        match model_provider:
            case "OPENAI":
                return ChatOpenAI(model=model_name, temperature=0, max_tokens=4096)
            case "ANTHROPIC":
                return ChatAnthropic(model=model_name, temperature=0, max_tokens=4096)
            case _:
                raise ValueError(f"Invalid model provider: {model_provider}")

    def _create_result(self, response: AgentResponse) -> ResultState: # pylint: disable=unused-argument
        raise NotImplementedError()

    def _get_system_message(self) -> str:
        generics = normalize_text(f"""\
            Now is {datetime.now().strftime("%H:%M")} on {datetime.today().strftime("%a, %-d %b %Y")}.
            """)
        agent = normalize_text(str(self.agent))
        goal = "# Goal" + os.linesep + normalize_text(self.goal)
        instructions = "# Instructions" + os.linesep + normalize_text(self.preamble)
        return generics + agent + goal + instructions

    def _get_user_message(self, content: str, response_format: AgentResponse, examples: str | None = None) -> str:
        content = normalize_text(content)
        examples = ("# Examples" + os.linesep + normalize_text(examples)) if examples else ""
        return content + examples + str(response_format)
