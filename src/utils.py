"""
Represents utility functions used throughout the application.
"""

import re
import sys
import os
import curses
from typing import Iterable, Literal

if sys.platform.startswith("win32"):
    from windows.read import read_key as _read_key, read_line as _read_line, read_lines as _read_lines, read_text as _read_text, IndentationMode, KeyMapping
elif sys.platform.startswith("linux"):
    from linux.read import read_key as _read_key, read_line as _read_line, read_lines as _read_lines, read_text as _read_text, IndentationMode, KeyMapping
else:
    raise OSError(f"{sys.platform} is not supported.")

__is_linux = sys.platform.startswith("linux")

Style = Literal[
    "bold",
    "dim",
    "italic",
    "underline",
    "blink",
    "reverse",
    "conceal",
    "strikethrough",
]

Color = Literal[
    "black",
    "grey",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
    "white",
]

STYLES: dict[Style, int] = {
    "bold": 1,
    "dim": 2,
    "italic": 3,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "conceal": 8,
    "strikethrough": 9,
}

COLORS: dict[Color, int] = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "light_grey": 37,
    "dark_grey": 90,
    "light_red": 91,
    "light_green": 92,
    "light_yellow": 93,
    "light_blue": 94,
    "light_magenta": 95,
    "light_cyan": 96,
    "white": 97,
}

RESET = "\x1b[0m"

Key = KeyMapping

def clear():
    """
    Clears the terminal screen.

    This function clears the terminal screen by executing the appropriate operating system's command
    """
    if __is_linux:
        os.system("clear")
    else:
        os.system("cls")

def paint(text: object, foreground: Color | None = None, background: Color | None = None, styles: Iterable[Style] | None = None) -> str:
    """
    returns a formated text.

    Args:
        text (str): The text to be formatted.
        foreground (str): The color of the prompt. See available colors below.
        background (str): The background color of the prompt.
        style (Iterable[str]): The style of the prompt (values: bold, dark, underline, blink, reverse, concealed).

    Notes:
        Available colors:
            black, red, green, yellow, blue, magenta, cyan, white,
            light_grey, dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan.
        Available style:
            bold, dark, underline, blink, reverse, concealed.

        """
    code = "\x1b[%dm%s"
    fmt = ""
    if foreground is not None:
        fmt = code % (COLORS[foreground], fmt)
    if background is not None:
        fmt = code % (COLORS[background] + 10, fmt)
    if styles is not None:
        for style in styles:
            fmt = code % (STYLES[style], fmt)
    return str(text) if not fmt else RESET+fmt+str(text).replace(RESET+RESET,RESET+fmt)+RESET+RESET


def write(text: str, foreground: Color | None = None, background: Color | None = None, styles: Iterable[Style] | None = None) -> None:
    """
    Writes a formated text.

    Args:
        text (str): The prompt to display to the user.
        foreground (str): The color of the prompt. See available colors below.
        background (str): The background color of the prompt.
        style (Iterable[str]): The style of the prompt (values: bold, dark, underline, blink, reverse, concealed).

    Notes:
        Available colors:
            black, red, green, yellow, blue, magenta, cyan, white,
            light_grey, dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan.
        Available style:
            bold, dark, underline, blink, reverse, concealed.

        """
    if text:
        print(paint(text, foreground, background, styles), end = None)

def write_line(text: str | None = None, foreground: Color | None = None, background: Color | None = None, styles: Iterable[Style] | None = None) -> None:
    """
    Prints a formated text with the operating system's line separator character at the end.
    """
    if text:
        print(paint(text, foreground, background, styles))
    else:
        print()

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


def write_raw(text: str) -> None:
    """
    Prints a colored prompt.
    """
    if text:
        print(text, end = "", flush = True)

def get_cursor_position():
    """
    Returns the current cursor position and the text at the cursor position.
    """
    curses.filter()
    scr = curses.initscr()
    try:
        y, x = scr.getyx()
        char = chr(scr.inch(y, x))
    finally:
        curses.endwin()
    return (y, x, char)

def read_key() -> str:
    """
    Allows the user to enter a single string.

    Returns:
        str: The multiline string entered by the user.
    """
    return _read_key()

def read_line() -> str:
    """
    Allows the user to enter a single string.

    Returns:
        str: The multiline string entered by the user.
    """
    return _read_line(trim_line=True)

def read_text() -> str:
    """
    Allows the user to enter a multiline string ending by pressing Shift+Enter.

        Returns:
        str: The text entered by the user.
    """
    return _read_text(remove_empty_lines=True, trim_line_ends = True, indentation_mode=IndentationMode.NORMALIZE)

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
