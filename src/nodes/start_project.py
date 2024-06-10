"""
represents the first node of the analysis, where the user is prompted to enter the project name and description.

Args:
    state (AnalysisState): The current state of the analysis.

Returns:
    AnalysisState: The updated state after querying the user.
"""

import os
import sys
from os.path import expanduser

from models.workflow import AnalysisState

# pylint: disable=import-error
from utils.general import to_snake_case, is_linux
from utils.terminal import clear, read_text, format, write_line, write, Action

# pylint: enable=import-error


def create(state: AnalysisState) -> AnalysisState:
    """
    Prompts the user to enter the project name and description, and updates the state accordingly.

    Args:
        state (AnalysisState): The current state of the analysis.

    Returns:
        dict: The updated state with the project name and description added.
    """
    yes_no = ""
    while yes_no != "yes" and yes_no != "y":
        yes_no = ""
        clear()
        name = format("Project Builder", "yellow", styles=["bold"])
        write_line(f"Welcome to {name}.", styles=["bold"])
        write_line()
        write_line("Let's start by getting some basic information about the project.")
        user_folder = expanduser("~") if is_linux else os.environ.get("USERPROFILE")
        folder_separator = "/" if is_linux else "\\"
        default_folder = f"{user_folder}{folder_separator}projects"

        project_name = input("Please, enter the project name: ")
        write_line()

        default_folder_color = format(default_folder, "cyan")
        base_folder = input(
            f"Please, enter the full path of the project location (default: '{default_folder_color}'): "
        )
        if not base_folder:
            base_folder = default_folder
        project_root_folder = (
            f"{base_folder}{folder_separator}{to_snake_case(project_name)}"
        )
        write_line()

        project_root_folder_color = format(project_root_folder, "cyan")
        write_line(f"Your project will be located at: '{project_root_folder_color}'.")
        write_line("Is that OK? ([Yes]/No/eXit): ")
        yes_no = input().lower()
        if yes_no == "exit" or yes_no == "x":
            sys.exit(0)
        if not yes_no:
            yes_no = "yes"

    yes_no = ""
    lines = []
    while yes_no != "yes" and yes_no != "y":
        yes_no = ""
        write_line()
        write_line("Please provide a detailed description of the project:")
        lines += read_text()
        write_line()
        write_line("Can we proceed to the analysis of the project description? ([Yes]/no/eXit): ")
        yes_no = input().lower()
        if yes_no == "exit" or yes_no == "x":
            sys.exit(0)
        if not yes_no:
            yes_no = "yes"

    os.makedirs(project_root_folder, exist_ok=True)
    write_line("Project folder created.")
    write_line("Let's proceed with the initial analysis.")

    project_description = "\n".join(lines)
    return {
        **state,
        "project_name": project_name,
        "project_root_folder": project_root_folder,
        "project_description": project_description,
    }
