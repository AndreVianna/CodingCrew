# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Represents utility functions used throughout the application.
"""

import sys
import re

is_linux = sys.platform.startswith("linux")
is_win32 = sys.platform.startswith("win32")

def static_init(cls):
    """
    Initializes the static members of a class.
    """
    if getattr(cls, "__static_init__", None):
        cls.__static_init__()
    return cls


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

def normalize_text(text: str | list[str]) -> str:
    lines = text if isinstance(list[str]) else text.split("\n")
    lines = normalize_lines(lines)
    return "\n".join(lines)+"\n"

def normalize_lines(lines: list[str]) -> list[str]:
    if not lines:
        return lines
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return lines
    while lines and not lines[-1].strip():
        lines.pop(-1)
    if not lines:
        return lines
    min_offset = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    if not min_offset:
        return lines

    result = list[str]()
    previous_was_empty = False
    for line in [line.rstrip() for line in lines]:
        if not line:
            if not previous_was_empty:
                result.append(line)
            previous_was_empty = True
            continue
        previous_was_empty = False
        line = line[min_offset:]
        trimmed = line.lstrip()
        if trimmed == line:
            result.append(trimmed)
            continue
        offset = len(line) - len(trimmed)
        indent_level = (offset // 4) + (offset % 4 >= 2)
        indent = " " * (4 * indent_level)
        result.append(indent + trimmed)
    return result
