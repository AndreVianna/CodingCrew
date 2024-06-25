import re
import sys
import os
import json
from datetime import datetime

from models.project_state import ProjectState

from utils.common import normalize_text, static_init, to_snake_case, is_win32
from utils import terminal

from .base_task import BaseTask

@static_init
class StartProject(BaseTask[ProjectState]):
    __project_name_regex: re.Pattern[str]

    @classmethod
    def __static_init__(cls):
        __project_name_regex = re.compile(r"^[A-Za-z][A-Za-z0-9\s_-]*$")

    def execute(self, state: ProjectState) -> ProjectState:
        self.__show_intruduction()
        work_spacefolder = self.__confirm_workspace()
        self.__identify_project(state)
        self.__describe_project(state)
        self.__create_or_update_project(state)
        self.__show_conclusion()
        return state

    def __show_intruduction(self):
        terminal.clear()
        app_name = terminal.set_style("Project Builder", "yellow", styles=["bold"])
        terminal.write(normalize_text(f"""\
            Welcome to {app_name}.

            Let's start by getting some basic information about the project.
            """))

    def __show_conclusion(self):
        terminal.write(normalize_text("""
            Project state saved.
            Let's proceed with the initial analysis.
            """))

    def __create_or_update_project(self, state):
        state.status = "STARTED"
        os.makedirs(state.folder, exist_ok=True)
        state_file = f"{state.folder}/state.json"
        with open(state_file, "w", encoding="utf-8") as state_file:
            json.dump(state.__dict__, state_file)

    def __describe_project(self, state):
        terminal.do_until_confirmed(lambda: self.__get_description(state))
        terminal.write_line()

    def __confirm_workspace(self) -> str:
        workspace_folder: str = os.path.expanduser( os.environ["WORKSPACE_FOLDER"].replace("~", "$HOMEPATH").replace("/", "\\")) if is_win32 else \
                                os.path.expanduser( os.environ["WORKSPACE_FOLDER"].replace("$HOMEPATH", "~").replace("\\", "/"))
        formatted = terminal.set_style(workspace_folder, "cyan")
        terminal.write_line(f"The current workpace is located at '{formatted}'.")
        return terminal.do_until_confirmed(lambda: self.__ask_for_wokspace_folder(workspace_folder), "Is that OK? ([Yes]/No/eXit)")

    def __ask_for_wokspace_folder(self, workspace_folder: str) -> str:
        while True:
            terminal.write_line("To store the project in a different folder, please provide the new path or leave empty to proceed.")
            new_folder = terminal.read_line()
            if not new_folder:
                return workspace_folder
            if not os.path.isdir(new_folder):
                terminal.write_line("Error: The provided folder does not exist!", "red")
                continue
            terminal.write_line(f"The project will be stored in '{terminal.set_style(new_folder, 'cyan')}'.")
            return new_folder

    def __identify_project(self, state):
        terminal.do_until_confirmed(lambda: self.__ask_for_project_name(state))
        terminal.write_line()

    def __ask_for_project_name(self, state: ProjectState):
        project_name: str = ""
        while True:
            terminal.write("Please, enter a valid the project name: ")
            project_name = terminal.read_line()
            if not re.match(self.__project_name_regex, project_name):
                terminal.write_line("Error: Invalid project name!", "red")
                terminal.write_line("The name must start with a letter and contain only letters, digits, spaces, underscores, and hyphens.")
                continue
            terminal.write_line(f"The project name will be '{terminal.set_style(project_name, 'cyan')}'.")
            terminal.request_confirmation(message="Is that OK? ([Yes]/No/eXit)")
            terminal.write_line()
            break

        project_folder = os.path.join(workspace_folder, to_snake_case(state.name))

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
