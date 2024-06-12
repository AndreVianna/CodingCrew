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


# def fire_and_forget(f):
#     def wrapped(*args, **kwargs):
#         loop = asyncio.get_event_loop()
#         return loop.run_in_executor(None, f, *args, *kwargs)

#     return wrapped

T = TypeVar("T")

async def wait_for(callback: Callable[[], T],
             /,
             text: str | None = None,
             timeout: float = 5.0,
             raise_error: bool = False) -> T:
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
    loop = asyncio.get_event_loop()

    is_timeout = False
    cancel = False
    def stop()-> bool:
        nonlocal cancel
        return cancel

    has_finished = False
    def on_finish(timeout) -> None:
        try:
            nonlocal is_timeout
            nonlocal task2
            nonlocal has_finished
            nonlocal loop
            task2.cancel()
            end_spinner(timeout)
        finally:
            is_timeout = timeout
            has_finished = True

    loop.run_in_executor(None, start_spinner, stop, text, timeout, on_finish)
    task2 = loop.run_in_executor(None, callback)
    while not task2.done() and not task2.cancelled():
        print("Waiting...")
        pass
    print("Ended")
    cancel = True
    while not has_finished:
        print("finishing")
        pass
    if is_timeout and raise_error:
        raise TimeoutError("The operation has timed out.")
    print("finished")
    return None if not task2.done() or task2.cancelled() else task2.result()


__SPINNER_FRAMES: list[str] = [
    "\u2308",
    "\u2309",
    "\u230b",
    "\u230a",
]
__CHECK: Literal["\u2714"] = "\u2714"
__FAIL: Literal["\u2714"] = "\u2718"

# @fire_and_forget
def start_spinner(stop: Callable[[], bool], text: str, timeout: float, on_finish: Callable[[bool], None]) -> None:
    start = time.time()
    text = "Processing" if text is None else text
    end = start + timeout
    while not stop():
        now = time.time()
        if  now > end:
            on_finish(True)
            return
        for frame in __SPINNER_FRAMES:
            write(Action.MOVE_TO_COL_N.replace("#n", "1"))
            write(f"{frame} {text}... {(now - start):0.1f}s  ")
            time.sleep(0.1)
    on_finish(False)


def end_spinner(is_timeout: bool) -> None:
    write(Action.MOVE_TO_COL_N.replace("#n", "1"))
    if is_timeout:
        write(f"Timed out! {__FAIL}")
    else:
        write(f"Done. {__CHECK}")
    write(Action.CLEAR_TO_END_OF_LINE)
    write_line()


# pylint: disable-next=redefined-builtin
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
