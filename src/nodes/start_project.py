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
from utils import clear, read_lines, paint, write_line, to_snake_case

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
        name = paint("Project Builder", "yellow", styles=["bold"])
        write_line(f"Welcome to {name}.", styles=["bold"])
        write_line()
        write_line("Let's start by getting some basic information about the project.")
        user_folder =expanduser("~")
        default_folder = f"{user_folder}/projects" if os.name != "nt" else "%USERPROFILE%\\Projects"
        folder_separator = "/" if os.name != "nt" else "\\"

        project_name = input("Please, enter the project name: ")
        write_line()

        default_folder_color = paint(default_folder, "cyan")
        base_folder = input(f"Please, enter the full path of the project location (default: '{default_folder_color}'): ")
        if not base_folder:
            base_folder = default_folder
        project_root_folder = f"{base_folder}{folder_separator}{to_snake_case(project_name)}"
        write_line()

        project_root_folder_color = paint(project_root_folder, "cyan")
        write_line(f"Your project will be located at: '{project_root_folder_color}'.")
        write_line("Is that OK? ([Yes]/No/eXit): ")
        yes_no = input().lower()
        if yes_no == "exit" or yes_no == "x":
            sys.exit(0)
        if not yes_no:
            yes_no = "yes"

    write_line()
    write_line("Please provide a detailed description of the project.")
    yes_no = ""
    submit_key = paint("Ctrl+Enter", "yellow", styles=["bold", "dim"])
    lines = []
    while yes_no != "yes" and yes_no != "y":
        yes_no = ""

        write_line(f"You can add multiple lines. Press '{submit_key}' to submit.", styles=["dim"])
        lines += read_lines()

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
