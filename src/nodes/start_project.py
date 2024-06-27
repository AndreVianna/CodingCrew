import os
from typing import ClassVar
import re
from datetime import datetime

from models import BaseState, Project

from utils.common import normalize_text, static_init, to_snake_case, format_duration
from utils import terminal

from .base_task import BaseTask

@static_init
class StartProject(BaseTask[BaseState]):
    name: ClassVar[str] = "start_project"
    __project_name_regex: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Za-z][A-Za-z0-9\s_-]*$")

    def __init__(self, state: BaseState) -> None:
        super().__init__(state)
        self.state = state

    def _execute(self) -> Project:
        self.__show_introduction()
        self.__confirm_workspace()
        name = self.__request_project_name()
        self.__load_previous_or_create_new_project(name)
        if self.state.status != "NEW":
            return self.state
        self.__request_project_description()
        self.state.status = "STARTED"
        self.state.save()
        self.__show_conclusion()
        return self.state

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
            formatted = terminal.set_style(self.state.workspace, "cyan")
            terminal.write(f"Workspace folder ({formatted}): ")
            new_folder = terminal.read_line()
            if not new_folder:
                return
            if not os.path.isdir(new_folder):
                terminal.write_line("Error: The provided folder does not exist!", "red")
                continue
            terminal.write_line(f"The select workspace folder is '{terminal.set_style(new_folder, 'cyan')}'.")
            self.state.workspace = new_folder or self.state.workspace

    def __request_project_name(self) -> str:
        return terminal.do_until_confirmed(self.__ask_for_project_name, "Is that correct?")

    def __ask_for_project_name(self) -> str:
        project_name: str = ""
        while True:
            terminal.write("Please, enter the project name: ")
            project_name = terminal.read_line()
            if project_name and re.match(self.__project_name_regex, project_name):
                break
            terminal.write_line("Error: Invalid project name!", "red")
            terminal.write_line("The name must start with a letter and contain only letters, digits, spaces, underscores, and hyphens.")
        return project_name

    def __load_previous_or_create_new_project(self, name: str) -> None:
        project_folder = os.path.join(self.state.workspace, to_snake_case(name))
        self.state.folder = os.path.join(project_folder, self.state.run)
        previous_run = self.__find_latest_run(self.state, project_folder)
        if not previous_run:
            terminal.write_line(f"Starting new run located at: '{terminal.set_style(self.state.folder, 'cyan')}'.")
            return

        run_folder = os.path.join(project_folder, previous_run)
        last_step_file = self.__find_last_step(run_folder)
        if not last_step_file:
            os.rmdir(run_folder)
            terminal.write_line(f"Starting new run located at: '{terminal.set_style(self.state.folder, 'cyan')}'.")
            return

        last_step = int(last_step_file.split(".")[0])
        terminal.write_line(f"Loading step {last_step} from previous run located at '{terminal.set_style(run_folder, 'cyan')}'...")
        state_file = os.path.join(run_folder, last_step_file)
        self.state = Project.load_from(state_file)

    def __find_latest_run(self, state: BaseState, project_folder: str) -> str | None:
        if not os.path.isdir(project_folder):
            return None

        runs = [entry for entry in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder, entry)) and entry != state.run]
        if not runs:
            return None

        runs.sort(key=lambda run: os.path.getmtime(os.path.join(project_folder, run)))
        last_run = runs[-1]

        formatted_last_run = terminal.set_style(os.path.join(project_folder, last_run), "cyan")
        delta = datetime.now() - datetime.fromtimestamp(os.path.getmtime(os.path.join(project_folder, last_run)))
        duration = terminal.set_style(format_duration(delta), "cyan")
        terminal.write_line(f"There is a pre-existing project run in the folder '{formatted_last_run}', created {duration} ago.")

        resume = terminal.request_confirmation("Do you want to resume this run?")
        return last_run if resume == "y" else None

    def __find_last_step(self, run_folder: str) -> int | None:
        steps = [entry for entry in os.listdir(run_folder) if os.path.isfile(os.path.join(run_folder, entry))]
        return steps[-1] if steps else None

    def __request_project_description(self) -> None:
        terminal.write_line("Please provide a detailed description of the project:")
        self.state.description = terminal.read_text(self.state.description)
