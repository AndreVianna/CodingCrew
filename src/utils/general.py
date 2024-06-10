# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Represents utility functions used throughout the application.
"""

import sys
import re

is_linux = sys.platform.startswith("linux")
is_win32 = sys.platform.startswith("win32")
is_verbose = any(arg in sys.argv for arg in ["--verbose", "-v"])

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
    lines = text.split("\n") if isinstance(text, str) else text
    lines = remove_top_empty_lines(lines)
    lines = remove_bottom_empty_lines(lines)
    lines = merge_empty_lines(lines)
    lines = align_left(lines)
    lines = normalize_tabs(lines)
    return "\n".join(lines)+"\n"

def remove_top_empty_lines(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    return lines

def remove_bottom_empty_lines(lines: list[str]) -> list[str]:
    while lines and not lines[-1].strip():
        lines.pop()
    return lines

def merge_empty_lines(lines: list[str]) -> list[str]:
    if not lines:
        return lines

    result = list[str]()
    previous_was_empty = False
    for line in lines:
        if line.strip():
            result.append(line)
            previous_was_empty = False
        elif not previous_was_empty:
            result.append(line)
            previous_was_empty = True
    return result

def align_left(lines: list[str]) -> list[str]:
    if not lines:
        return lines

    offset = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
    if not offset:
        return lines

    result = list[str]()
    for line in [line.rstrip() for line in lines]:
        result.append(line[offset:])
    return result

def normalize_tabs(lines: list[str]) -> list[str]:
    if not lines:
        return lines

    result = list[str]()
    for line in lines:
        indent = ""
        text = line.lstrip()
        if text:
            offset = len(line) - len(text)
            level = (offset // 4) + (1 if offset % 4 else 0)
            indent = " " * (4 * level)
        result.append(indent + text)
    return result
