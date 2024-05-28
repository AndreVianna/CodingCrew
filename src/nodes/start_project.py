"""
represents the first node of the analysis, where the user is prompted to enter the project name and description.

Args:
    state (AnalysisState): The current state of the analysis.

Returns:
    AnalysisState: The updated state after querying the user.
"""


import os
import sys
import utils
from models.workflow import AnalysisState

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
        utils.clear()
        print("Welcome to the project helper. Let's start by creating a new project.\n\n")
        print("Let's start by getting some basic infomation about the project.")
        default_folder = "~/projects" if os.name != 'nt' else "%USERPROFILE%\\Projects"
        folder_separator = "/" if os.name != 'nt' else "\\"
        project_name = input("\nPlease, enter the project name: ")
        base_folder = input(f"\nPlease, enter the full path of the project localtion (default: '{default_folder}'): ")
        if not base_folder:
            base_folder = default_folder
        project_root_folder = f"{base_folder}{folder_separator}{project_name.lower().replace(' ', '_')}"
        print(f"\nYour project will be located at '{project_root_folder}'.\n")
        yes_no = input("Is that OK? ([Yes]/No/eXit): ").lower()
        if yes_no == "exit" or yes_no == "x":
            sys.exit(0)
        if not yes_no:
            yes_no = 'yes'

    yes_no = ""
    while yes_no != "yes" and yes_no != "y":
        yes_no = ""
        lines = utils.multiline_input("\n\nPlease provide a detailed description of the project.\nYou can enter multiple lines. Press Ctrl-D (or Ctrl-Z on Windows) to submit.\n")
        yes_no = input("\nAre you ok with this description? Can we proceed with the analysis phase? ([Yes]/no/eXit): ").lower()
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
