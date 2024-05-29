"""
Represents utility functions used throughout the application.
"""

import os
from typing import Iterable, Literal

Style = Literal[
    "bold",
    "dark",
    "underline",
    "blink",
    "reverse",
    "concealed",
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
    "dark": 2,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "concealed": 8,
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


RESET = "\033[0m"

paint_stack: list[(Color | None, Color | None, Style | None)]

def __init__():
    paint_stack = list[(Color | None, Color | None, Style | None)]()

def clear():
    """
    Clears the terminal screen.

    This function clears the terminal screen by executing the appropriate operating system's command
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

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
    previous = paint.pop() if paint else (None, None, None)
    result = str(text)
    code = "\033[%dm%s"
    if foreground is not None:
        result = code % (COLORS[foreground], result)
    if background is not None:
        result = code % (COLORS[background] + 10, result)
    if styles is not None:
        for style in styles:
            result = code % (STYLES[style], result)
    return result


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
    if (len(lines) == 0):
        return ''
    last_line = lines[-1]
    is_line_all_whitespace = not last_line.strip()
    if not is_line_all_whitespace:
        return os.linesep.join(lines)
    indent_size = len(last_line)
    new_lines = []
    for line in lines:
        if len(line) < indent_size:
            if not line.strip():
                new_lines.append('')
            else:
                return os.linesep.join(lines)
        if not line.startswith(last_line):
            return os.linesep.join(lines)
        new_lines.append(line[indent_size:])
    return os.linesep.join(new_lines)


def write_raw(text: str | None = None, foreground: Color | None = None, background: Color | None = None, styles: Iterable[Style] | None = None) -> None:
    """
    Prints a colored prompt.
    """
    if text:
        write(outdent(text), foreground, background, styles)

def read() -> str:
    """
    Allows the user to enter a single string.

    Returns:
        str: The multiline string entered by the user.
    """
    return input()

def multiline_read() -> Iterable[str]:
    """
    Allows the user to enter a multiline string.

    Returns:
        Iterable[str]: The multiline string entered by the user.
    """
    multiline = list[str]()
    while True:
        try:
            line: str = input()
        except EOFError:
            break
        multiline.append(line)
    return multiline
