# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Represents utility functions used throughout the application.
"""

import sys
from typing import Iterable
from utils.general import is_linux, is_win32
from utils.terminal_common import Color, Style, TerminalAction

if is_linux:
    import utils.terminal_linux as linux_terminal

    Key = linux_terminal.KeyMapping
    __terminal: linux_terminal.Terminal = linux_terminal.Terminal()
elif is_win32:
    import utils.terminal_win32 as win32_terminal

    Key = win32_terminal.KeyMapping
    __terminal: win32_terminal.Terminal = win32_terminal.Terminal()
else:
    raise OSError(f"{sys.platform} is not supported.")

Action = TerminalAction

def clear() -> str:
    """
    Clears the terminal screen.
    """
    return __terminal.clear()


def read_text() -> str:
    """
    Allows the user to enter a multiline string ending by pressing Shift+Enter.

    Returns:
        str: The text entered by the user.
    """
    return __terminal.read_text()


def read_line() -> str:
    """
    Allows the user to enter a single string.

    Returns:
        str: The line entered by the user.
    """
    return __terminal.read_line()


def read_key() -> str:
    """
    Allows the user to enter a single key.

    Returns:
        str: The key entered by the user.
    """
    return __terminal.read_key()


def format(
    text: str,
    foreground: Color | None = None,
    background: Color | None = None,
    styles: Iterable[Style] | None = None,
) -> str:
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
    return __terminal.format(text, foreground, background, styles)


def write(
    text: str,
    foreground: Color | None = None,
    background: Color | None = None,
    styles: Iterable[Style] | None = None,
) -> str:
    """
    Writes a formatted text to the terminal.

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
    return __terminal.write(text, foreground, background, styles)


def write_line(
    text: str | None = None,
    foreground: Color | None = None,
    background: Color | None = None,
    styles: Iterable[Style] | None = None,
) -> str:
    """
    Writes a formatted text to the terminal and adds a new line.

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
    return __terminal.write_line(text, foreground, background, styles)
