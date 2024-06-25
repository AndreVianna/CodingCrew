import sys
import os
import json
from datetime import datetime

from models.project_state import ProjectState

from utils.common import to_snake_case, is_linux
from utils.terminal import terminal

from .base_task import BaseTask

class StartProjectTask(BaseTask[ProjectState]):
    def execute(self, state: ProjectState) -> ProjectState:
        terminal.clear()
        name = terminal.set_style("Project Builder", "yellow", styles=["bold"])
        terminal.write_line(f"Welcome to {name}.", styles=["bold"])
        terminal.write_line()
        terminal.write_line("Let's start by getting some basic information about the project.")

        terminal.repeat_until_confirmed(lambda: self.__get_name_and_folder(state))
        terminal.write_line()

        terminal.repeat_until_confirmed(lambda: self.__get_description(state))
        terminal.write_line()

        state.status = "STARTED"
        os.makedirs(state.folder, exist_ok=True)
        state_file = f"{state.folder}/state.json"
        with open(state_file, "w", encoding="utf-8") as state_file:
            json.dump(state.__dict__, state_file)

        terminal.write_line("Project state saved.")
        terminal.write_line("Let's proceed with the initial analysis.")
        return state

    def __get_name_and_folder(self, state: ProjectState):
        user_folder = os.path.expanduser("~") if is_linux else os.environ.get("USERPROFILE")
        default_folder = os.path.join(user_folder, "projects")
        terminal.write("Please, enter the project name: ")
        state.name = terminal.read_line()
        terminal.write_line()

        formatted_default_folder = terminal.set_style(default_folder, "cyan")
        terminal.write_line(f"Please, enter the full path of the projects root folder (default: '{formatted_default_folder}'): ")
        base_folder = terminal.read_line()
        if not base_folder:
            base_folder = default_folder
        project_folder = os.path.join(base_folder, to_snake_case(state.name))

        previous_run: str = ""
        if os.path.exists(project_folder):
            previous_run = self.__select_previous_run(state, project_folder)
        if previous_run:
            state_folder = os.path.join(project_folder, previous_run)
            terminal.write_line(f"Resuming previous run located at: '{terminal.set_style(state_folder, 'cyan')}'.")
            state_file = os.path.join(state_folder, "state.json")
            with open(state_file, "r", encoding="utf-8") as state_file:
                content = json.load(state_file)
                state.__dict__.update(**content)
                terminal.write_line("State loaded from JSON file.")
        else:
            state.folder = os.path.join(project_folder, state.project_id)
            terminal.write_line(f"Starting new run located at: '{terminal.set_style(state.folder, 'cyan')}'.")

    def __select_previous_run(self, state: ProjectState, project_folder: str) -> str:
        runs = [entry for entry in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, entry)) and entry != state.project_id]
        if not runs:
            return ""
        runs.sort(key=lambda run: os.path.getmtime(os.path.join(project_folder, run)), reverse=True)
        last_run = runs[0]
        choice = "x"
        formatted_last_run = terminal.set_style(last_run, "cyan")
        delta = datetime.now() - datetime.fromtimestamp(os.path.getmtime(os.path.join(project_folder, last_run)))
        formatted_delta = terminal.set_style(f"{delta.days} days " if delta.days else "" + f"{':'.join(str(delta).split(':')[:2])}h", "cyan")
        terminal.write_line(F"There is a pre-existing project run in the folder '{formatted_last_run}', created {formatted_delta} ago.")
        while choice and choice.lower() not in ["resume", "r", "new", "n"]:
            terminal.write("Do you want to resume the previous run or start a new one? (Resume/[New]/eXit) ")
            choice = terminal.read_line()
            if not choice or choice.lower() in ["new", "n"]:
                last_run = ""
                break
            if choice.lower() in ["resume", "r"]:
                break
            if choice.lower() in ["exit", "x"]:
                terminal.write_line("Exiting the application.")
                sys.exit(0)
            terminal.write_line(terminal.set_style("Invalid choice!", "red"))
        return last_run

    def __get_description(self, state: ProjectState):
        terminal.write_line("Please provide a detailed description of the project:")
        previous_description = state.description[-1] if state.description else None
        description = terminal.read_text(previous_description)
        if state.description:
            state.description[-1] = description
        else:
            state.description.append(description)
        terminal.write_line("Next we will proceed to the analysis of the project description.")
