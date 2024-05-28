"""
represents the first node of the analysis, where the user is prompted to enter the project name and description.

Args:
    state (AnalysisState): The current state of the analysis.

Returns:
    AnalysisState: The updated state after querying the user.
"""


from textwrap import dedent
from models.workflow import AnalysisState

def create(state: AnalysisState) -> AnalysisState:
    """
    Prompts the user to enter the project name and description, and updates the state accordingly.

    Args:
        state (AnalysisState): The current state of the analysis.

    Returns:
        dict: The updated state with the project name and description added.
    """
    project_name = input("Enter the project name: ")
    print(dedent("""
          Enter the project description: (submit by pressing Ctrl-D or Ctrl-Z on windows)"""))
    project_description = ''
    while True:
        try:
            line = input()
        except EOFError:
            break
        project_description += f"{line}\n"
    return {
        **state,
        'project_name': project_name,
        'project_description': project_description,
    }
