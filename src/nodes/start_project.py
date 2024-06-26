import re
import os
import json
from datetime import datetime
from typing import ClassVar
from unittest.mock import Base

from models import BaseState, Project

from models.update_description_state import UpdateDescriptionState
from utils.common import normalize_text, static_init, to_snake_case, is_win32
from utils import terminal

from .base_task import BaseTask

@static_init
class StartProject(BaseTask[BaseState]):
    name: ClassVar[str] = "start_project"
    __project_name_regex: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9\s_-]*$")

    def _execute(self, state: BaseState) -> UpdateDescriptionState:
        self.__show_intruduction()
        self.__confirm_workspace(state)
        name = self.__get_project_name()
        state = Project(state.run, state.step, "CREATED", name)
        self.__create_or_load_project(workspace_folder, state)
        self.__get_project_description(state)
        self.__create_or_update_project(state)
        self.__show_conclusion()
        return UpdateDescriptionState(state.run, state.step, "STARTED", state.name, state.description)

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

    def __confirm_workspace(self, state: BaseState) -> None:
        while True:
            formatted = terminal.set_style(state.workspace, "cyan")
            terminal.write(f"Workspace folder ({formatted}): ")
            new_folder = terminal.read_line()
            if not new_folder:
                return
            if not os.path.isdir(new_folder):
                terminal.write_line("Error: The provided folder does not exist!", "red")
                continue
            terminal.write_line(f"The select workspace folder is '{terminal.set_style(new_folder, 'cyan')}'.")
            state.workspace = new_folder or state.workspace

    def __get_project_name(self) -> str:
        return terminal.do_until_confirmed(self.__ask_for_project_name, "Is that correct?")

    def __ask_for_project_name(self) -> str:
        project_name: str = ""
        while True:
            terminal.write("Please, enter the project name: ")
            project_name = terminal.read_line()
            if not project_name or not re.match(self.__project_name_regex, project_name):
                terminal.write_line("Error: Invalid project name!", "red")
                terminal.write_line("The name must start with a letter and contain only letters, digits, spaces, underscores, and hyphens.")
                continue
            break
        return project_name

    def __create_or_load_project(self, state: BaseState, name: str) -> Project:
        project_folder_name = to_snake_case(name)
        project_folder = os.path.join(state.workspace, project_folder_name)
        state.folder = os.path.join(project_folder, state.run)
        return self.__try_load_from_previous_run(state, project_folder)

    def __try_load_from_previous_run(self, state: BaseState, project_folder) -> Project:
        previous_run = self.__get_previous_run(state, project_folder)
        if not previous_run:
            terminal.write_line(f"Starting new run located at: '{terminal.set_style(state.folder, 'cyan')}'.")
            return Project(

        run_folder = os.path.join(project_folder, previous_run)
        terminal.write_line(f"Loading previous run located at: '{terminal.set_style(run_folder, 'cyan')}'...")
        state_file = os.path.join(run_folder, "state.json")
        with open(state_file, "r", encoding="utf-8") as state_file:
            content = json.load(state_file)
            state.__dict__.update(**content)
        terminal.write_line("Previous state loaded.")
        return state


    def __get_previous_run(self, state: Project, project_folder: str) -> str | None:
        if not os.path.isdir(project_folder):
            return None
        runs = [entry for entry in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, entry)) and entry != state.project_id]
        if not runs:
            return None
        runs.sort(key=lambda run: os.path.getmtime(os.path.join(project_folder, run)), reverse=True)
        last_run = runs[0]
        formatted_last_run = terminal.set_style(last_run, "cyan")
        delta = datetime.now() - datetime.fromtimestamp(os.path.getmtime(os.path.join(project_folder, last_run)))
        formatted_delta = terminal.set_style(f"{delta.days} days " if delta.days else "" + f"{':'.join(str(delta).split(':')[:2])}h", "cyan")
        terminal.write_line(F"There is a pre-existing project run in the folder '{formatted_last_run}', created {formatted_delta} ago.")
        resume = terminal.request_confirmation("Do you want to resume the previous run?")
        return last_run if resume == "y" else None

    def __get_project_description(self, state: Project):
        terminal.write_line("Please provide a detailed description of the project:")
        previous_description = state.description[-1] if state.description else None
        description = terminal.read_text(previous_description)
        if state.description:
            state.description[-1] = description
        else:
            state.description.append(description)

    def __create_or_update_project(self, state):
        state.status = "STARTED"
        os.makedirs(state.folder, exist_ok=True)
        path = f"{state.folder}/state.json"
        with open(path, "w", encoding="utf-8") as state_file:
            json.dump(state, state_file, default=str)
