import os
from datetime import datetime
from pydantic import BaseModel

from utils.common import normalize_text

class JsonResponseFormat(BaseModel):
    json_schema: str | None = None

    def __init__(self, json_schema: str | None = None) -> None:
        super().__init__()
        self.json_schema = json_schema

    def to_string(self) -> str:
        text: str = normalize_text("""\
            # Expected Response Format
            Your final answer MUST be in a JSON format.
            IMPORTANT! It MUST contain only the JSON object, no title, preamble, conclusion or additional information.
            IMPORTANT! All linebreaks within strings must be escaped with the character sequence '\\n'.
            IMPORTANT! All double quotes within strings must be escaped with the character sequence '\\\\"'.
            IMPORTANT! All strings should use UTF-8 encoding.""")
        if self.json_schema:
            text += normalize_text("""\
                Here is the JSON schema for the answer:
                ```json""") + \
                normalize_text(self.json_schema) + \
                "```" + os.linesep
        if text:
            text = "# Expected Response Format"  + os.linesep + text
        return text


def get_system_message(agent: str, task: str, goal: str, response_format: JsonResponseFormat, examples: str | None = None) -> str:
    if not agent:
        raise ValueError("Agent must be provided.")
    if not task:
        raise ValueError("Task must be provided.")
    generics = normalize_text(f"""\
        Today is {datetime.today().strftime("%a, %-d %b, %Y")}. The time is {datetime.now().strftime("%H:%M %Z")}.
        """)
    task = "# Task Description" + os.linesep + normalize_text(task)
    goal = "# Goal" + os.linesep + normalize_text(goal)
    examples = ("# Examples" + os.linesep + examples) if examples else ""
    return generics + normalize_text(agent) + task + goal + examples + response_format.to_string()
