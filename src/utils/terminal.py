import sys
import time
from typing import Callable, Iterable, Literal, Optional, TypeVar
import asyncio

from .common import is_linux, is_win32 # pylint: disable=relative-beyond-top-level
from .base_terminal import Style, ActionKeyMapping, Color

if is_linux:
    from .linux_terminal import Terminal, KeyMapping as Key # pylint: disable=relative-beyond-top-level, unused-import
elif is_win32:
    from .win32_terminal import Terminal, KeyMapping as Key # pylint: disable=relative-beyond-top-level, unused-import
else:
    raise OSError(f"{sys.platform} is not supported.")

__terminal: Terminal = Terminal()

def clear() -> str:
    """
    Clears the terminal screen.
    """
    return __terminal.clear()


def read_text(previous_content: Optional[str] = None) -> str:
    """
    Allows the user to enter a multiline string ending by pressing Shift+Enter.

    Returns:
        str: The text entered by the user.
    """
    return __terminal.read_text(previous_content)


def read_line(previous_content: Optional[str] = None) -> str:
    """
    Allows the user to enter a single string.

    Returns:
        str: The line entered by the user.
    """
    return __terminal.read_line(previous_content)


def read_key() -> str:
    """
    Allows the user to enter a single key.

    Returns:
        str: The key entered by the user.
    """
    return __terminal.read_key()

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
__CHECK = "\u2713"
__FAIL = "\u2717"

async def start_spinner(text: str, stop: asyncio.Event):
    state = "RUNNING"
    try:
        start = time.time()
        text = "Processing" if text is None else text
        frame_count = len(__SPINNER_FRAMES)
        current_frane = 0
        while not stop.is_set():
            __terminal.set_cursor_position(1)
            __terminal.write(f" {__SPINNER_FRAMES[current_frane]} {text} {(time.time() - start):0.1f}s  ")
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
    __terminal.write(ActionKeyMapping.MOVE_TO_COL_N.replace("#n", "1"))
    if state == "STOPPED":
        symbol = set_style(__CHECK, "green")
        __terminal.write(f" {symbol}  Done. Ellapsed time: {ellapsed:0.1f}s")
    elif state == "TIMEOUT":
        symbol = set_style(__FAIL, "red")
        __terminal.write(f" {symbol}  Timeout! Ellapsed time: {ellapsed:0.1f}s")
    else:
        symbol = set_style(__FAIL, "red")
        __terminal.write(f" {symbol}  Error! Ellapsed time: {ellapsed:0.1f}s")
    __terminal.write(ActionKeyMapping.CLEAR_TO_END_OF_LINE)
    __terminal.write_line()


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

R = TypeVar("R")

def do_until_confirmed(func: Callable[[], R], /, message: str | None = None, continue_on: Literal["y", "n"] = "y", allow_exit: bool = True) -> R:
    result = func()
    while __show_yes_or_no_question(message, default_answer=continue_on, allow_exit=allow_exit) != continue_on:
        result = func()
    return result

def request_confirmation(message: str | None = None, default_answer: Literal["y", "n"] = "y", allow_exit: bool = True) -> Literal["y"] | Literal["n"]:
    answer = __show_yes_or_no_question(message, default_answer, allow_exit)
    while not answer:
        answer = __show_yes_or_no_question(message, default_answer, allow_exit)
    return answer

def __show_yes_or_no_question(message: str | None, default_answer: Literal["y", "n"], allow_exit: bool) -> Literal["y"] | Literal["n"] | None:
    message = message if message else "Continue?"
    yes_option = "[Yes]" if default_answer == "y" else "Yes"
    no_option = "/[No]" if default_answer == "n" else "/No"
    exit_option = "/eXit" if allow_exit else ""
    write(f"""{message} ({yes_option}{no_option}{exit_option}) """)
    answer = read_line().lower().strip()
    match answer:
        case "" | None:
            return default_answer
        case "yes" | "y":
            return "y"
        case "no" | "n":
            return "n"
        case "exit" | "x" if allow_exit:
            sys.exit(0)
    __terminal.write_line("Error: Invalid answer. Please try again.", "red")
    return None

def wait_for_key(message: str | None = None, allow_exit: bool = True) -> None:
    message = message if message else "Press any key to continue."
    if allow_exit:
        message += " (or press 'x' to exit)"
    write(message)
    answer = read_key()
    if allow_exit and answer == "x":
        sys.exit(0)
