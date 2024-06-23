# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Represents utility functions used throughout the application.
"""

import sys
import time
from typing import Callable, Iterable, Literal, TypeVar
import asyncio

from ..general import is_linux, is_win32 # pylint: disable=relative-beyond-top-level
from .common import Color, Style, Action as Action # pylint: disable=relative-beyond-top-level

if is_linux:
    from .linux import Terminal, KeyMapping as Key # pylint: disable=relative-beyond-top-level, unused-import
elif is_win32:
    from .win32 import Terminal, KeyMapping as Key # pylint: disable=relative-beyond-top-level, unused-import
else:
    raise OSError(f"{sys.platform} is not supported.")

__terminal: Terminal = Terminal()

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

_R = TypeVar("_R")

async def wait_for(func: Callable[[], _R],
             /,
             text: str | None = None,
             timeout: float = 5.0,
             raise_timeout_error: bool = True) -> _R | None:
    """
    Waits for the callback to return asynchronously and displays a spinner.

    Args:
        callback: The callback function to wait for.

    Returns:
        The result of the callback function.
    """
    if timeout <= 0:
        raise ValueError("Timeout must be greater than 0.")

    text = "Processing" if text is None else text

    stop_spinner = asyncio.Event()
    long_run: asyncio.Task[_R] = asyncio.create_task(asyncio.to_thread(func))
    spinner: asyncio.Task[None] = asyncio.create_task(start_spinner(text, stop_spinner))
    combined = asyncio.wait([long_run, spinner], timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
    try:
        await combined
        if long_run.done():
            stop_spinner.set()
        else:
            long_run.cancel()
            spinner.cancel()
            if raise_timeout_error:
                raise asyncio.TimeoutError("The operation timed out!")
        return long_run.result() if long_run.done() else None
    except asyncio.CancelledError:
        spinner.cancel()
        return None
    finally:
        await spinner
        combined.close()

__SPINNER_FRAMES: list[str] = [
    "\u2594\u2594",
    "\u2003\u231d",
    "\u2003\u23b9",
    "\u2003\u231f",
    "\u2581\u2581",
    "\u231e\u2003",
    "\u23b8\u2003",
    "\u231c\u2003",
]
__CHECK: Literal["\u2713"] = "\u2713"
__FAIL: Literal["\u2717"] = "\u2717"

async def start_spinner(text: str, stop: asyncio.Event):
    state = "RUNNING"
    try:
        start = time.time()
        text = "Processing" if text is None else text
        frame_count = len(__SPINNER_FRAMES)
        current_frane = 0
        while not stop.is_set():
            write(Action.MOVE_TO_COL_N.replace("#n", "1"))
            write(f" {__SPINNER_FRAMES[current_frane]} {text} {(time.time() - start):0.1f}s  ")
            current_frane = 0 if current_frane >= frame_count - 1 else current_frane + 1
            await asyncio.sleep(0.1)
        state = "STOPPED"
    except asyncio.CancelledError:
        state = "TIMEOUT"
    except Exception:
        state = "ERROR"
        raise
    finally:
        await end_spinner(state, time.time() - start)

async def end_spinner(state: Literal["STOPPED", "TIMEOUT", "ERROR"], ellapsed: float) -> None:
    write(Action.MOVE_TO_COL_N.replace("#n", "1"))
    if state == "STOPPED":
        symbol = set_style(__CHECK, "green")
        write(f" {symbol}  Done. Ellapsed time: {ellapsed:0.1f}s")
    elif state == "TIMEOUT":
        symbol = set_style(__FAIL, "red")
        write(f" {symbol}  Timeout! Ellapsed time: {ellapsed:0.1f}s")
    else:
        symbol = set_style(__FAIL, "red")
        write(f" {symbol}  Error! Ellapsed time: {ellapsed:0.1f}s")
    write(Action.CLEAR_TO_END_OF_LINE)
    write_line()


def set_style(
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

def repeat_until_confirmed(func, message: str | None = None, default: bool = True, allow_exit: bool = True):
    while True:
        func()
        if can_proceed(message, default=default, allow_exit=allow_exit):
            break

def can_proceed(message: str | None = None, default: bool = True, allow_exit: bool = True) -> bool:
    message = message if message else "Can we proceed?"
    write(f"""{message} ({"[Yes]" if default else "Yes"}/{"[No]" if not default else "No"}{"/eXit" if allow_exit else ""}): """)
    answer = read_line().lower()
    if allow_exit and answer in ["exit", "x"]:
        sys.exit(0)
    answer = "yes" if not answer else answer
    return answer in ["yes", "y"]
