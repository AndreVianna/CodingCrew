"""
Represents utility functions used throughout the application.
"""

import os

def clear():
    """
    Clears the console screen.

    This function clears the console screen by executing the appropriate command
    based on the operating system. On Windows, it uses the 'cls' command, while
    on Mac and Linux, it uses the 'clear' command.

    Note:
        This function relies on the `os` module.

    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def multiline_input(prompt: str) -> list[str]:
    """
    Prompts the user to enter a multiline string.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The multiline string entered by the user.
    """
    print(prompt)
    multiline = list[str]()
    while True:
        try:
            line: str = input()
        except EOFError:
            break
        multiline.append(line)
    return multiline
