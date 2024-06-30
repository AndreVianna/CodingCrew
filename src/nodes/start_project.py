import os
from typing import ClassVar
from datetime import datetime
import re

from models import Project

from utils.common import delete_tree, normalize_text, static_init, snake_case, format_duration
from utils import terminal

from states import BaseState, AnalysisState

from .base_node import BaseNode

@static_init
class StartProject(BaseNode[BaseState, AnalysisState]): # pylint: disable=too-few-public-methods
    name: ClassVar[str] = "start_project"
    __project_name_regex: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9\s_-]*$")

    def _execute(self) -> AnalysisState:
        self.__show_introduction()
        self.__confirm_workspace()
        name = self.__request_project_name()
        result = self.__load_previous_or_create_new_project(name)
        if result.run.status != "NEW":
            return result
        result.project.description = self.__request_project_description()
        result.run.status = "STARTED"
        result.save()
        self.__show_conclusion()
        return result

    def __show_introduction(self):
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

    def __confirm_workspace(self) -> None:
        while True:
            formatted = terminal.set_style(self.state.base_folder, "cyan")
            terminal.write(f"Workspace folder ({formatted}): ")
            new_folder = terminal.read_line()
            if not new_folder:
                return
            if not os.path.isdir(new_folder):
                terminal.write_line("Error: The provided folder does not exist!", "red")
                continue
            terminal.write_line(f"""The select workspace folder is '{terminal.set_style(new_folder, "cyan")}'.""")
            self.state.base_folder = new_folder or self.state.base_folder

    def __request_project_name(self) -> str:
        return terminal.do_until_confirmed(self.___ask_for_project_name, "Is that correct?")

    def ___ask_for_project_name(self) -> str:
        name: str = ""
        while True:
            terminal.write("Please, enter the project name: ")
            name = terminal.read_line()
            if name and re.match(self.__project_name_regex, name):
                break
            terminal.write_line("Error: Invalid project name!", "red")
            terminal.write_line("The name must start with a letter and contain only letters, digits, spaces, underscores, and hyphens.")
        project_folder = os.path.join(self.state.base_folder, snake_case(name))
        formatted = terminal.set_style(project_folder, "cyan")
        terminal.write_line(f"Project location: '{formatted}'.")
        return name

    def __load_previous_or_create_new_project(self, name: str) -> AnalysisState:
        state_file = self.___find_previous_state_file()
        if not state_file:
            terminal.write_line("Starting new run...")
            return AnalysisState(self.state, Project(name))

        terminal.write_line("Loading previous run...")
        return AnalysisState.create_from_file(state_file)

    def ___find_previous_state_file(self) -> str | None:
        latest_run = self.____find_latest_run()
        if not latest_run:
            return None

        run_folder = os.path.join(self.state.folder, latest_run)
        last_step_file = self.____find_last_step(run_folder)
        if not last_step_file:
            delete_tree(latest_run)
            return None

        step_info = last_step_file.split(".")
        age = datetime.now() - datetime.strptime(latest_run, "%Y%m%dT%H%M%S")
        age = terminal.set_style(format_duration(age), "cyan")
        status = step_info[1].upper()
        if status == "FINISHED":
            return None
        status = terminal.set_style(status, "cyan")

        terminal.write_line(f"A previous run of this project created {age} ago with status '{status}' was found.")
        resume = terminal.request_confirmation("Do you want to resume that run?")
        return os.path.join(run_folder, last_step_file) if resume == "y" else None

    def ____find_latest_run(self) -> str | None:
        folder = self.state.folder
        if not os.path.isdir(folder):
            return None

        runs = next(os.walk(folder))[1]
        if not runs:
            return None
        return runs[-1]

    def ____find_last_step(self, folder: str) -> str | None:
        entries = os.walk(folder)
        entry = next(entries, None)
        steps = entry[2] if entry else None
        return steps[-1] if steps else None

    def __request_project_description(self) -> str:
        terminal.write_line("Please provide a detailed description of the project:")
        return terminal.read_text(self.state.description)
