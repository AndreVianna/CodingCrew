import os
from datetime import datetime
from typing import Generic, TypeVar

# pylint: disable=import-error
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models import LanguageModelInput
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
# pylint: enable=import-error

from utils import terminal
from utils.common import normalize_text, is_verbose

from models import BaseState
from responses import BaseAgentResponse, AcknowledgementResponse, MarkdownResponse

from .base_task import BaseTask

S = TypeVar("S", bound=BaseState)
R = TypeVar("R", bound=BaseAgentResponse)

class BaseAgentTask(BaseTask[S], Generic[S]): # pylint: disable=too-few-public-methods
    agent: str = ""
    goal: str = ""
    description: str = ""
    allow_markdown: bool = False

    def __init__(self, agent: str, goal: str, allow_markdown: bool = False) -> None:
        super().__init__()
        self.agent = agent
        self.goal = goal
        self.allow_markdown = allow_markdown
        self.description = normalize_text("""
            IMPORTANT! This taks is complex let's do it step-by step to arrive the best answer.
            """)

    def _execute(self, state: S) -> S:
        messages = [SystemMessage(content=self._get_system_message(self.agent, self.description, self.goal))]
        self._ask_model_to_acknowledge(messages, state.describe())
        response = self._ask_model_for_text(messages, "PROCEED")
        return self._update_state(state, response)

    def _ask_model_for_text(self, messages: LanguageModelInput, content: str) -> str:
        response_format = MarkdownResponse() if self.allow_markdown else BaseAgentResponse()
        messages.append(HumanMessage(content=self._get_user_message(content, response_format)))
        return self._ask_model(messages)

    def _ask_model_to_acknowledge(self, messages: LanguageModelInput, content: str) -> bool:
        messages.append(HumanMessage(content=self._get_user_message(content, AcknowledgementResponse())))
        response_text = self._ask_model(messages)
        return response_text == "ACKNOWLEDGE"

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

    def _update_state(self, state: S, response: R | str) -> S: # pylint: disable=unused-argument
        if not response:
            raise ValueError("Response must be provided.")
        return state

    def _get_system_message(self, agent: str, task: str, goal: str) -> str:
        if not agent:
            raise ValueError("Agent must be provided.")
        if not task:
            raise ValueError("Task must be provided.")
        generics = normalize_text(f"""\
            Now is {datetime.now().strftime("%H:%M")} on {datetime.today().strftime("%a, %-d %b %Y")}.
            """)
        task = "# Task Description" + os.linesep + normalize_text(task)
        goal = "# Goal" + os.linesep + normalize_text(goal)
        return generics + normalize_text(agent) + task + goal

    def _get_user_message(self, content: str, response_format: BaseAgentResponse, examples: str | None = None) -> str:
        content = normalize_text(content)
        examples = ("# Examples" + os.linesep + normalize_text(examples)) if examples else ""
        return content + examples + str(response_format)
