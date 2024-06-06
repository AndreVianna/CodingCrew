"""
Tools that helps reading the console input from the user in Windows.
"""

import msvcrt
from enum import IntEnum
from typing import Iterable
from windows.mappings import KeyMapping

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
    If one of the exit keys is pressed it ends a line AND finishes the input (default: [ CTRL+ENTER ]).

    Args:
        interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
        linebreak_keys (Iterable[str]): The keys that will end a line.
        exit_keys (Iterable[str]): The keys that will finish the input.

    Returns:
        list[str]: The lines entered by the user.
    """
    linebreak_keys = linebreak_keys if linebreak_keys else [KeyMapping.ENTER]
    exit_keys = exit_keys if exit_keys else [KeyMapping.CTRL_ENTER]
    multiline = list[str]()
    line = ""
    key = read_key(interrupt)
    while key not in exit_keys:
        # TODO: Handle special keys
        if key in linebreak_keys:
            multiline.append(line)
            line = ""
        else:
            line += key
        print(key, end="", flush=True)
        key = read_key(interrupt)
    multiline.append(line)
    print(flush=True)

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
    If one of the exit keys is pressed it finishes the input (default: [ ENTER, CTRL+ENTER ]).

    Args:
        interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
        exit_keys (Iterable[str]): The keys that will finish the input.

    Returns:
        str: The line entered by the user.
    """
    exit_keys = exit_keys if exit_keys else [KeyMapping.ENTER, KeyMapping.CTRL_ENTER]
    line = ""
    key = read_key(interrupt)
    while key not in exit_keys:
        # TODO: Handle speacil keys (left and right only)
        line += key
        print(key, end="", flush=True)
        key = read_key(interrupt)

    return line.strip() if trim_line else line

def read_key(interrupt: bool = True) -> str:
    """
    Reads a single key press from the user.

    Args:
        interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).

    Returns:
        str: The key pressed by the user.
    """
    ch = msvcrt.getwch()
    if ord(ch) in (0, 224) :
        ch += msvcrt.getwch()
    if interrupt and ch == KeyMapping.CTRL_C:
        raise KeyboardInterrupt
    return ch
