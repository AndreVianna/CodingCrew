from datetime import timedelta
import os
import sys
import re
from typing import Literal

is_linux: bool = sys.platform.startswith("linux")
is_win32: bool = sys.platform.startswith("win32")
is_verbose: bool = any(arg in sys.argv for arg in ["-v"])

default_indent_size: Literal[4] = 4
default_indent_char: Literal[" "] = " "

def static_init(cls):
    if getattr(cls, "__static_init__", None):
        cls.__static_init__()
    return cls

symbols = re.compile(r"\W")
alpha_before_digit = re.compile(r"([A-Za-z])([0-9])")
digit_before_alpha = re.compile(r"([0-9])([A-Za-z])")
char_before_upper = re.compile(r"(.)([A-Z][a-z]+)")
lower_before_upper = re.compile(r"([a-z])([A-Z])")

def to_snake_case(name):
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

def format_duration(delta: timedelta):
    days_text = f"{delta.days} days " if delta.days > 1 else "1 day " if delta.days else None
    hours = delta.seconds // 3600
    hours_text = f"{hours} hours " if hours > 1 else "1 hour " if hours else None
    minutes = (delta.seconds // 60) % 60
    minutes_text = f"{minutes} minutes" if minutes > 1 else "1 minute" if minutes else None
    parts = [filter(None, [days_text,hours_text,minutes_text])]
    part_count = len(parts)
    period = parts[0] if part_count == 1 else f"{parts[0]} and {parts[1]}" if part_count == 2 else f"{parts[0]}, {parts[1]}, and {parts[2]}"
    return period

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
        if not line:
            result.append(line)
            continue
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
