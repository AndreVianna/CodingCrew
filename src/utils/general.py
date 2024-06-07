# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Represents utility functions used throughout the application.
"""

import os
import sys
import re
from enum import IntEnum

is_linux = sys.platform.startswith("linux")
is_win32 = sys.platform.startswith("win32")

def static_init(cls):
    """
    Initializes the static members of a class.
    """
    if getattr(cls, "__static_init__", None):
        cls.__static_init__()
    return cls


class IndentationMode(IntEnum):
    """
    Enumeration class representing different indentation modes.

    Attributes:
        Keep (int): Keep the original indentation.
        RemoveAll (int): Remove all indentation.
        Dedent (int): Dedent the code.
        Normalize (int): Normalize the indentation.
    """

    KEEP = 0
    REMOVE_ALL = 1
    DEDENT = 2
    NORMALIZE = 3


def outdent(text: object) -> str:
    """
    Removes the leading whitespace from the text.

    Args:
        text (str): The text to remove the leading whitespace.

    Returns:
        str: The text without the leading whitespace.
    """
    lines = str(text).split(os.linesep)
    if len(lines) == 0:
        return ""
    last_line = lines[-1]
    is_line_all_whitespace = not last_line.strip()
    if not is_line_all_whitespace:
        return os.linesep.join(lines)
    indent_size = len(last_line)
    lines = lines[:-1]
    new_lines = []
    for line in lines:
        if len(line) <= indent_size:
            if not line.strip():
                new_lines.append("")
            else:
                return os.linesep.join(lines)
        if not line.startswith(last_line):
            return os.linesep.join(lines)
        new_lines.append(line[indent_size:])
    return os.linesep.join(new_lines)


symbols = re.compile(r"\W")
alpha_before_digit = re.compile(r"([A-Za-z])([0-9])")
digit_before_alpha = re.compile(r"([0-9])([A-Za-z])")
char_before_upper = re.compile(r"(.)([A-Z][a-z]+)")
lower_before_upper = re.compile(r"([a-z])([A-Z])")


def to_snake_case(name):
    """
    Converts a given string to snake case.

    Args:
        name (str): The string to be converted.

    Returns:
        str: The converted string in snake case.
    """
    name = symbols.sub("_", name)
    name = alpha_before_digit.sub(r"\1_\2", name)
    name = digit_before_alpha.sub(r"\1_\2", name)
    name = char_before_upper.sub(r"\1_\2", name)
    name = lower_before_upper.sub(r"\1_\2", name)
    while "__" in name:
        name = name.replace("__", "_")
    name = name.strip("_")
    return name.lower()
