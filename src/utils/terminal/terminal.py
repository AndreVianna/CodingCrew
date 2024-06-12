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

    stop = False
    def stop_spinner()-> bool:
        nonlocal stop
        return stop

    has_timed_out = False
    spinner_has_finished = False
    def on_finish(has_finished: bool, ellapsed: float) -> None:
        nonlocal has_timed_out
        # nonlocal task2
        nonlocal spinner_has_finished
        try:
            has_timed_out = not has_finished
            # if has_timed_out:
            #     task2.cancel()
            end_spinner(has_timed_out, ellapsed)
        finally:
            spinner_has_finished = True

    async_callback = asyncio.to_thread(callback)
    spinner = get_spinner_task(text, stop_spinner)
    done, pending = await asyncio.wait([async_callback, spinner],
                       timeout=timeout,
                       return_when=asyncio.FIRST_COMPLETED)
    
    if (not done or async_callback in done) and not spinner.cancelled():
        stop = True
        await spinner

    # loop = asyncio.get_event_loop()

    # stop = False
    # def stop_spinner()-> bool:
    #     nonlocal stop
    #     return stop

    # has_timed_out = False
    # spinner_has_finished = False
    # def on_finish(has_finished: bool, ellapsed: float) -> None:
    #     nonlocal has_timed_out
    #     nonlocal task2
    #     nonlocal spinner_has_finished
    #     try:
    #         has_timed_out = not has_finished
    #         if has_timed_out:
    #             task2.cancel()
    #         end_spinner(has_timed_out, ellapsed)
    #     finally:
    #         spinner_has_finished = True

    # loop.run_in_executor(None, start_spinner, stop_spinner, text, timeout, on_finish)
    # task2 = loop.run_in_executor(None, callback)
    # while not task2.done() and not task2.cancelled():
    #     pass
    # stop = True
    # while not spinner_has_finished:
    #     pass
    # if has_timed_out and raise_error:
    #     raise TimeoutError("The operation has timed out.")
    # return None if not task2.done() or task2.cancelled() else task2.result()


__SPINNER_FRAMES: list[str] = [
    "\u2594\u2594",
    " \u231d",
    " \u23b9",
    " \u231f",
    "\u2581\u2581",
    "\u231e ",
    "\u23b8 ",
]
__CHECK: Literal["\u2713"] = "\u2713"
__FAIL: Literal["\u2717"] = "\u2717"

def get_spinner_task(text: str, stop: Callable[[], bool]) -> asyncio.Task:

    async def start_spinner(text: str, stop: Callable[[], bool]) -> asyncio.Task:
        try:
            start = time.time()
            text = "Processing" if text is None else text
            stop_requested = False
            while not stop_requested:
                stop_requested = stop()
                for frame in __SPINNER_FRAMES:
                    if stop_requested:
                        break
                    write(Action.MOVE_TO_COL_N.replace("#n", "1"))
                    write(f" {frame} {text}... {(time.time() - start):0.1f}s  ")
                    time.sleep(0.1)
        except asyncio.CancelledError:
            pass
        finally:
            end_spinner(stop_requested, time.time() - start)

    return asyncio.create_task(start_spinner(text, stop))

def end_spinner(stop_requested: bool, ellapsed: float) -> None:
    write(Action.MOVE_TO_COL_N.replace("#n", "1"))
    if stop_requested:
        symbol = format(__CHECK, "green")
        write(f" {symbol} Done. Ellapsed time: {ellapsed:0.1f}s")
    else:
        symbol = format(__FAIL, "red")
        write(f" {symbol} Timed out! Ellapsed time: {ellapsed:0.1f}s")
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
