from datetime import datetime
import os
from os.path import expanduser
import json

from models.project_state import ProjectState

from utils.common import to_snake_case, is_linux
from utils.terminal.terminal import clear, set_style, write, write_line, read_line, read_text, repeat_until_confirmed

def get_name_and_folder(state: ProjectState):
    user_folder = expanduser("~") if is_linux else os.environ.get("USERPROFILE")
    default_folder = os.path.join(user_folder, "projects")
    write("Please, enter the project name: ")
    state.name = read_line()
    write_line()

    formatted_default_folder = set_style(default_folder, "cyan")
    write_line(f"Please, enter the full path of the projects root folder (default: '{formatted_default_folder}'): ")
    base_folder = read_line()
    if not base_folder:
        base_folder = default_folder
    project_folder = os.path.join(base_folder, to_snake_case(state.name))

    choice = "n"
    runs = [entry for entry in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, entry)) and entry != state.project_id]
    runs.sort(key=lambda run: os.path.getmtime(os.path.join(project_folder, run)), reverse=True)
    last_run = runs[0] if runs else None
    if last_run:
        choice = "x"
        formatted_last_run = set_style(last_run, "cyan")
        delta = datetime.now() - datetime.fromtimestamp(os.path.getmtime(os.path.join(project_folder, last_run)))
        formatted_delta = set_style(f"{delta.days} days " if delta.days else "" + f"{':'.join(str(delta).split(':')[:2])}h", "cyan")
        write_line(F"There is a pre-existing project run in the folder '{formatted_last_run}', created {formatted_delta} ago.")
        while choice and choice.lower() not in ["resume", "r", "new", "n"]:
            write("Do you want to resume the previous run or start a new one? (Resume/[New]/eXit) ")
            choice = read_line()
            if choice.lower() in ["exit", "x"]:
                write_line("Exiting the application.")
                exit(0)
            if not choice or choice.lower() in ["resume", "r", "new", "n"]:
                choice = "n" if not choice else choice[0].lower()
                break
            write_line(set_style("Invalid choice!", "red"))
    if choice == "r":
        state_folder = os.path.join(project_folder, last_run)
        write_line(f"Resuming previous run located at: '{set_style(state_folder, 'cyan')}'.")
        state_file = os.path.join(state_folder, "state.json")
        with open(state_file, "r", encoding="utf-8") as state_file:
            content = json.load(state_file)
            state.__dict__.update(**content)
            write_line("State loaded from JSON file.")
    else:
        state.folder = os.path.join(project_folder, state.project_id)
        write_line(f"Starting new run located at: '{set_style(state.folder, 'cyan')}'.")

def get_description(state: ProjectState):
    write_line("Please provide a detailed description of the project:")
    previous_description = state.description[-1] if state.description else None
    description = read_text(previous_description)
    if state.description:
        state.description[-1] = description
    else:
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

    state.status = "STARTED"
    os.makedirs(state.folder, exist_ok=True)
    state_file = f"{state.folder}/state.json"
    with open(state_file, "w", encoding="utf-8") as state_file:
        json.dump(state.__dict__, state_file)

    write_line("Project state saved.")
    write_line("Let's proceed with the initial analysis.")
    return state
