import os
import sys
import re
from typing import Literal
from functools import singledispatch

is_linux: bool = sys.platform.startswith("linux")
is_win32: bool = sys.platform.startswith("win32")
is_verbose: bool = any(arg in sys.argv for arg in ["-v"])

default_indent_size: Literal[4] = 4
default_indent_char: Literal[" "] = " "

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

def normalize_text(text: str | list[str], /, indent_level: int = 0, indent_size: int = default_indent_size, indent_char: str = default_indent_char) -> str:
    lines = text.split("\n") if isinstance(text, str) else text
    lines = __remove_top_empty_lines(lines)
    lines = __remove_bottom_empty_lines(lines)
    lines = __merge_empty_lines(lines)
    lines = __align_left(lines,  indent_level, indent_size, indent_char)
    return os.linesep.join(lines)+os.linesep

def __remove_top_empty_lines(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    return lines

def __remove_bottom_empty_lines(lines: list[str]) -> list[str]:
    while lines and not lines[-1].strip():
        lines.pop()
    return lines

def __merge_empty_lines(lines: list[str]) -> list[str]:
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

def __align_left(lines: list[str], indent_level: int = 0, indent_size: int = default_indent_size, indent_char: str = default_indent_char) -> list[str]:
    indent_level = max(0, indent_level)
    indent_size = max(1, indent_size)
    if not lines:
        return lines

    result = list[str]()
    first_offset = len(lines[0]) - len(lines[0].lstrip())
    for line in [line.rstrip() for line in lines]:
        striped_line = line.lstrip()
        line_level = 0
        line_offset = len(line) - len(striped_line)
        if line_offset < first_offset:
            raise ValueError("Inconsistent indentation in the input text.")
        line_offset = line_offset - first_offset
        if line_offset > 0:
            line_level = (line_offset // indent_size) + (1 if line_offset % indent_size > 1 else 0)
        indent = indent_char * (indent_size * (indent_level + line_level))
        result.append(indent + striped_line)
    return result
