import os
from os.path import expanduser
import uuid

from models.query import Query
from models.project_state import ProjectState

from utils.general import to_snake_case, is_linux
from utils.terminal.terminal import clear, set_style, write, write_line, read_line, read_text, repeat_until_confirmed

def get_name_and_folder(state: ProjectState):
    user_folder = expanduser("~") if is_linux else os.environ.get("USERPROFILE")
    folder_separator = "/" if is_linux else "\\"
    default_folder = f"{user_folder}{folder_separator}projects"
    state.project_id = uuid.uuid4()
    write("Please, enter the project name: ")
    state.name = read_line()
    write_line()

    formatted_default_folder = set_style(default_folder, "cyan")
    write_line(f"Please, enter the full path of the projects root folder (default: '{formatted_default_folder}'): ")
    base_folder = read_line()
    if not base_folder:
        base_folder = default_folder
    project_folder = f"{base_folder}{folder_separator}{to_snake_case(state.name)}"
    state.folder = f"{project_folder}{folder_separator}{state.project_id}"
    write_line(f"""Your project will be located at: '{set_style(state.folder, 'cyan')}'.""")

def get_description(state: ProjectState):
    write_line("Please provide a detailed description of the project:")
    description = read_text()
    state.description.append(description)
    write_line("Next we will proceed to the analysis of the project description.")


def create(state: ProjectState) -> ProjectState:
    clear()
    name = set_style("Project Builder", "yellow", styles=["bold"])
    write_line(f"Welcome to {name}.", styles=["bold"])
    write_line()
    write_line("Let's start by getting some basic information about the project.")

    repeat_until_confirmed(lambda: get_name_and_folder(state))
    write_line()

    repeat_until_confirmed(lambda: get_description(state))
    write_line()

    os.makedirs(state.folder, exist_ok=True)
    write_line("Project folder created.")
    write_line("Let's proceed with the initial analysis.")

    state.queries = list[Query]()
    state.status = "STARTED"
    return state
