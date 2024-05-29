"""
represents the first node of the analysis, where the user is prompted to enter the project name and description.

Args:
    state (AnalysisState): The current state of the analysis.

Returns:
    AnalysisState: The updated state after querying the user.
"""

import os
import sys
from models.workflow import AnalysisState
from utils import clear, multiline_read, paint, write_line

def create(state: AnalysisState) -> AnalysisState:
    """
    Prompts the user to enter the project name and description, and updates the state accordingly.

    Args:
        state (AnalysisState): The current state of the analysis.

    Returns:
        dict: The updated state with the project name and description added.
    """

    app_name = paint("Project Builder", styles=['bold'])

    yes_no = ""
    while yes_no != "yes" and yes_no != "y":
        yes_no = ""
        clear()
        write_line(f"Welcome to {app_name}.")
        write_line()
        write_line("Let's start by getting some basic infomation about the project.")
        default_folder = "~/projects" if os.name != 'nt' else "%USERPROFILE%\\Projects"
        folder_separator = "/" if os.name != 'nt' else "\\"

        project_name = input("Please, enter the project name: ")
        write_line()

        base_folder = input(f"Please, enter the full path of the project localtion (default: '{paint(default_folder, 'cyan')}'): ")
        if not base_folder:
            base_folder = default_folder
        project_root_folder = f"{base_folder}{folder_separator}{project_name.lower().replace(' ', '_')}"
        write_line()

        write_line(f"Your project will be located at: '{paint(project_root_folder, 'cyan')}'.")
        write_line("Is that OK? ([Yes]/No/eXit): ")
        yes_no = input().lower()
        if yes_no == "exit" or yes_no == "x":
            sys.exit(0)
        if not yes_no:
            yes_no = 'yes'

    write_line()
    write_line("Please provide a detailed description of the project.")
    yes_no = ""
    submit_key = paint("Ctrl-D" if os.name != 'nt' else "Ctrl-Z", styles=['bold'])
    lines = []
    while yes_no != "yes" and yes_no != "y":
        yes_no = ""

        write_line(f"You can add multiple lines. Press '{submit_key}' to submit.", styles=['dark'])
        lines += multiline_read()

        write_line()
        write_line("Can we proceed to the analysis of the project description? ([Yes]/no/eXit): ")
        yes_no = input().lower()
        if yes_no == "exit" or yes_no == "x":
            sys.exit(0)
        if not yes_no:
            yes_no = 'yes'

    project_description = '\n'.join(lines)
    return {
        **state,
        'project_name': project_name,
        'project_root_folder': project_root_folder,
        'project_description': project_description,
    }
