"""
Represents utility functions used throughout the application.
"""

import os
import re
from typing import Iterable, Literal

from readchar import readchar

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
    code = "\x1b[%dm%s"
    fmt = ''
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
        return ''
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

key_mapping = {
    (127,): 'backspace',
    (10,): 'return',
    (32,): 'space',
    (9,): 'tab',
    (27,): 'esc',
    (27, 91, 65): 'up',
    (27, 91, 66,): 'down',
    (27, 91, 67,): 'right',
    (27, 91, 68,): 'left',
    (27, 91, 72): 'home',
    (27, 91, 70): 'end',
    (27, 91, 50, 126): 'insert',
    (27, 91, 51, 126): 'delete',
    (27, 91, 53, 126): 'pageup',
    (27, 91, 54, 126): 'pagedown',
    (27, 79, 80): 'f1',
    (27, 79, 81): 'f2',
    (27, 79, 82): 'f3',
    (27, 79, 83): 'f4',
    (27, 91, 49, 53, 126): 'f5',
    (27, 91, 49, 55, 126): 'f6',
    (27, 91, 49, 56, 126): 'f7',
    (27, 91, 49, 57, 126): 'f8',
    (27, 91, 50, 48, 126): 'f9',
    (27, 91, 50, 49, 126): 'f10',
    # F11 is already used to toggle fullscreen.
    (27, 91, 50, 52, 126): 'f12',
}

def get_key() -> str:
    """
    Reads a single key press from the user.

    Returns:
        str: The key pressed by the user.
    """
    key = readchar()
    if key == '\x19':
        return 'ctrl+y'
    return key

def read_text() -> list[str]:
    """
    Allows the user to enter a multiline string ending by pressing Shift+Enter.

        Returns:
        list[str]: The multiline string entered by the user.
    """
    multiline = list[str]()
    key = get_key()
    while key != 'ctrl+enter':
        line = ''
        while key != 'enter':
            line += key
            print(key, end = '')
            key = get_key()
        multiline.append(line)
    return multiline

symbols = re.compile(r'\W')
alpha_before_digit = re.compile(r'([A-Za-z])([0-9])')
digit_before_alpha = re.compile(r'([0-9])([A-Za-z])')
char_before_upper = re.compile(r'(.)([A-Z][a-z]+)')
lower_before_upper = re.compile(r'([a-z])([A-Z])')

def to_snake_case(name):
    """
    Converts a given string to snake case.

    Args:
        name (str): The string to be converted.

    Returns:
        str: The converted string in snake case.
    """
    name = symbols.sub('_', name)
    name = alpha_before_digit.sub(r'\1_\2', name)
    name = digit_before_alpha.sub(r'\1_\2', name)
    name = char_before_upper.sub(r'\1_\2', name)
    name = lower_before_upper.sub(r'\1_\2', name)
    while '__' in name:
        name = name.replace('__', '_')
    name = name.strip('_')
    return name.lower()
