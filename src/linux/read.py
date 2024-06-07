"""
Tools that helps reading the console input from the user in LINUX.
"""

import sys
import tty
import termios
import curses

from enum import IntEnum
from typing import Any, Iterable
from linux.mappings import KeyMapping as Key
from linux.actions import TerminalActions as Action

class IndentationMode(IntEnum):
    """
    Enumeration class representing different indentation modes.

    Attributes:
        Keep (int): Keep the original indentation.
        RemoveAll (int): Remove all indentation.
        Dedent (int): Dedent the code.
        Normalize (int): Normalize the indentation.
    """
    KEEP = 0
    REMOVE_ALL = 1
    DEDENT = 2
    NORMALIZE = 3

def read_text(interrupt: bool = True,
                linebreak_keys: Iterable[str] = None,
                exit_keys: Iterable[str] = None,
                remove_empty_lines: bool = False,
                trim_line_ends: bool = False,
                indentation_mode: IndentationMode = IndentationMode.KEEP,
                indent_size: int = 4,
                indent_str: str = " ") -> str:
    """
    Reads a text from the user's input.
    If one of the linebreak keys is pressed it ends a line (default: [ ENTER ]).
    If one of the exit keys is pressed it finishes the input (default: [ CTRL+ENTER ]).

    Args:
        interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
        linebreak_keys (Iterable[str]): The keys that will end a line.
        exit_keys (Iterable[str]): The keys that will finish the input.

    Returns:
        str: The text entered by the user.
    """
    return "\n".join(read_lines(interrupt, linebreak_keys, exit_keys, remove_empty_lines, trim_line_ends, indentation_mode, indent_size, indent_str))+"\n"

def __get_screen_size():
    """
    Returns the size of the terminal screen.
    """
    curses.filter()
    scr = curses.initscr()
    try:
        y, x = scr.getmaxyx()
    finally:
        curses.endwin()
    return y, x

def read_lines(interrupt: bool = True,
                linebreak_keys: Iterable[str] = None,
                exit_keys: Iterable[str] = None,
                remove_empty_lines: bool = False,
                trim_line_ends: bool = False,
                indentation_mode: IndentationMode = IndentationMode.KEEP,
                indent_size: int = 4,
                indent_str: str = " ") -> list[str]:
    """
    Reads a multipe lines from the user's input.
    If one of the linebreak keys is pressed it ends a line (default: [ ENTER ]).
    If one of the exit keys is pressed it ends a line AND finishes the input (default: [ CTRL+ENTER, CTRL+D ]).

    Args:
        interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
        linebreak_keys (Iterable[str]): The keys that will end a line.
        exit_keys (Iterable[str]): The keys that will finish the input.

    Returns:
        list[str]: The lines entered by the user.
    """
    indentation_mode = IndentationMode(indentation_mode)
    linebreak_keys = linebreak_keys if linebreak_keys else [Key.ENTER]
    exit_keys = exit_keys if exit_keys else [Key.CTRL_ENTER, Key.CTRL_D]
    max_y, max_x = __get_screen_size()
    multiline = list[str]()
    line = ""

    print(f"Width: {max_x}; Height: {max_y}")

    fd, old_settings = __start_read()
    try:
        key = __read_key(interrupt)
        while key not in exit_keys:
            # TODO: Handle special keys
            if key == Key.BACKSPACE:
                if not line and multiline:
                    line = multiline.pop()
                    __write(Action.MOVE_UP)
                if line:
                    offset = len(line) % max_x
                    line = line[:-1]
                    line_count = len(line) // max_x
                    if offset < max_x:
                        __write("\b")
                    __write(Action.CLEAR_TO_END_OF_LINE)
                    if line_count:
                        __write(Action.MOVE_UP_N.replace("#n", str(line_count)))
                    __write(Action.MOVE_TO_BEGIN_OF_LINE + line)
            elif key in linebreak_keys or key in exit_keys:
                multiline.append(line)
                line = ""
                __write("\n")
            else:
                line += key
            __write(key)
            key = __read_key(interrupt)
    finally:
        __end_read(fd, old_settings)

    multiline.append(line)
    __write("\n")
    if indentation_mode == IndentationMode.REMOVE_ALL:
        multiline = [line.lstrip() for line in multiline]
    elif indentation_mode in (IndentationMode.DEDENT, IndentationMode.NORMALIZE) and len(multiline) > 0:
        offset = min([len(line) - len(line.lstrip()) for line in multiline])
        result = list[str]()
        for line in multiline:
            offset_line = line[offset:]
            if indentation_mode == IndentationMode.NORMALIZE:
                extra_spaces = len(offset_line) - len(offset_line.lstrip())
                indent_level = (extra_spaces // indent_size) + (extra_spaces % indent_size >= indent_size // 2)
                indent = indent_str * (indent_size * indent_level)
                offset_line = indent + offset_line.lstrip()
            result.append(offset_line)
        multiline = result
    if trim_line_ends:
        multiline = [line.rstrip() for line in multiline]
    if remove_empty_lines:
        multiline = [line for line in multiline if line.strip()]
    return multiline

def read_line(interrupt: bool = True,
                exit_keys: Iterable[str] = None,
                trim_line: bool = False) -> str:
    """
    Reads a line from the from the user's input.
    If one of the exit keys is pressed it finishes the input (default: [ ENTER, CTRL+ENTER, CTRL+D ]).

    Args:
        interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
        exit_keys (Iterable[str]): The keys that will finish the input.

    Returns:
        str: The line entered by the user.
    """
    exit_keys = exit_keys if exit_keys else [Key.ENTER, Key.CTRL_ENTER, Key.CTRL_D]
    line = ""

    fd, old_settings = __start_read()
    try:
        key = __read_key(interrupt)
        while key not in exit_keys:
            # TODO: Handle arrow keys (left and right only)
            if key == Key.BACKSPACE:
                if line:
                    line = line[:-1]
                    __write("\b \b")
            else:
                line += key
                __write(key)
            key = __read_key(interrupt)
    finally:
        __end_read(fd, old_settings)

    return line.strip() if trim_line else line

def read_key(interrupt: bool = True) -> str:
    """
    Reads a single key press from the user.

    Args:
        interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).

    Returns:
        str: The key pressed by the user.
    """
    fd, old_settings = __start_read()
    try :
        return __read_key(interrupt)
    finally :
        __end_read(fd, old_settings)

def __start_read() -> tuple[int, list[Any]]:
    sys.stdout.flush()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)
    return fd, old_settings

def __end_read(fd: int, old_settings: list[Any]) -> None:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def __write(char: str) -> None:
    sys.stdout.write(char)
    sys.stdout.flush()

def __read_key(interrupt: bool) -> str:
    ch = sys.stdin.read(1)
    if ord(ch) == 27:
        ch = "\x1b"
        ch += sys.stdin.read(1)
        code = sys.stdin.read(1)
        ch += code
        while code.isnumeric() or code == ";":
            code = sys.stdin.read(1)
            ch += code
    if ch in Key.CTRL_C and interrupt:
        raise KeyboardInterrupt
    return ch
