# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Tools that helps reading the console input from the user in LINUX.
"""

import sys
import tty
import termios

from typing import Any

from utils.general import static_init
from utils.terminal_common import TerminalBase


@static_init
class KeyMapping:
    """
    Represents a collection of key constants used for keyboard input handling.
    Each key is represented as a string literal.
    """

    _name_of: dict[str, str] = dict[str, str]()

    @classmethod
    def __static_init__(cls):
        members = [
            attr
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("_")
        ]
        for member in members:
            name = (
                member.replace("CTRL_", "CTRL+")
                .replace("ALT_", "ALT+")
                .replace("SHIFT_", "SHIFT+")
                .replace("_", "")
            )
            value: str = getattr(cls, member)
            if value not in cls._name_of.keys():
                cls._name_of[value] = name
            else:
                cls._name_of[value] += f" | {name}"

    @classmethod
    def list(cls) -> list[(str, str)]:
        result: list[(str, str)] = list[(str, str)]()
        members = [
            attr
            for attr in dir(cls)
            if not callable(getattr(cls, attr)) and not attr.startswith("_")
        ]
        for member in members:
            value: str = getattr(cls, member)
            entry = (cls._name_of[value], cls.code_of(value))
            if entry not in result:
                result.append(entry)
        return result

    @classmethod
    def name_of(cls, char: str) -> str:
        return cls._name_of[char]

    @staticmethod
    def code_of(char: str) -> str:
        if char == "???":
            return char
        return "".join([f"\\x{ord(c):02x}" for c in char])

    CTRL_2 = "\x00"  # Need to find out the value
    CTRL_6 = "\x1e"

    CTRL_A = "\x01"
    CTRL_B = "\x02"
    CTRL_C = "\x03"
    CTRL_D = "\x04"
    CTRL_E = "\x05"
    CTRL_F = "\x06"
    CTRL_G = "\x07"
    CTRL_H = "\x08"
    CTRL_I = "\x09"
    CTRL_J = "\x0a"
    CTRL_K = "\x0b"
    CTRL_L = "\x0c"
    CTRL_M = "\x0d"
    CTRL_N = "\x0e"
    CTRL_O = "\x0f"
    CTRL_P = "\x10"
    CTRL_Q = "\x11"
    CTRL_R = "\x12"
    CTRL_S = "\x13"
    CTRL_T = "\x14"
    CTRL_U = "\x15"
    CTRL_V = "\x16"
    CTRL_W = "\x17"
    CTRL_X = "\x18"
    CTRL_Y = "\x19"
    CTRL_Z = "\x1a"

    CTRL_BACKSPACE = "\x08"
    TAB = "\x09"
    CTRL_ENTER = "\x0a"
    ENTER = "\x0d"

    ESC = "\x1b"
    CTRL_BKSLASH = "\x1c"
    CTRL_MINUS = "\x1d"
    CTRL_SLASH = "\x1f"

    BACKSPACE = "\x7f"

    UP = "\x1b[A"
    DOWN = "\x1b[B"
    RIGHT = "\x1b[C"
    LEFT = "\x1b[D"
    END = "\x1b[G"
    HOME = "\x1b[I"
    F1 = "\x1b[P"
    F2 = "\x1b[Q"
    F3 = "\x1b[R"
    F4 = "\x1b[S"

    SHIFT_TAB = "\x1b[Z"
    ALT_TAB = "\x1b[27;3~"
    ALT_SHIFT_TAB = "\x1b[27;4~"
    CTRL_TAB = "\x1b[27;5~"
    CTRL_SHIFT_TAB = "\x1b[27;6~"
    CTRL_ALT_TAB = "\x1b[27;7~"
    CTRL_ALT_SHIFT_TAB = "\x1b[27;8~"

    SHIFT_UP = "\x1b[1;2A"
    SHIFT_DOWN = "\x1b[1;2B"
    SHIFT_RIGHT = "\x1b[1;2C"
    SHIFT_LEFT = "\x1b[1;2D"
    SHIFT_BEGIN = "\x1b[1;2E"
    SHIFT_END = "\x1b[1;2F"
    SHIFT_HOME = "\x1b[1;2H"
    SHIFT_F1 = "\x1b[1;2P"
    SHIFT_F2 = "\x1b[1;2Q"
    SHIFT_F3 = "\x1b[1;2R"
    SHIFT_F4 = "\x1b[1;2S"
    ALT_UP = "\x1b[1;3A"
    ALT_DOWN = "\x1b[1;3B"
    ALT_RIGHT = "\x1b[1;3C"
    ALT_LEFT = "\x1b[1;3D"
    ALT_BEGIN = "\x1b[1;3E"
    ALT_END = "\x1b[1;3F"
    ALT_HOME = "\x1b[1;3H"
    ALT_F1 = "\x1b[1;3P"
    ALT_F2 = "\x1b[1;3Q"
    ALT_F3 = "\x1b[1;3R"
    ALT_F4 = "\x1b[1;3S"
    ALT_SHIFT_UP = "\x1b[1;4A"
    ALT_SHIFT_DOWN = "\x1b[1;4B"
    ALT_SHIFT_RIGHT = "\x1b[1;4C"
    ALT_SHIFT_LEFT = "\x1b[1;4D"
    ALT_SHIFT_BEGIN = "\x1b[1;4E"
    ALT_SHIFT_END = "\x1b[1;4F"
    ALT_SHIFT_HOME = "\x1b[1;4H"
    ALT_SHIFT_F1 = "\x1b[1;4P"
    ALT_SHIFT_F2 = "\x1b[1;4Q"
    ALT_SHIFT_F3 = "\x1b[1;4R"
    ALT_SHIFT_F4 = "\x1b[1;4S"
    CTRL_UP = "\x1b[1;5A"
    CTRL_DOWN = "\x1b[1;5B"
    CTRL_RIGHT = "\x1b[1;5C"
    CTRL_LEFT = "\x1b[1;5D"
    CTRL_BEGIN = "\x1b[1;5E"
    CTRL_END = "\x1b[1;5F"
    CTRL_HOME = "\x1b[1;5H"
    CTRL_F1 = "\x1b[1;5P"
    CTRL_F2 = "\x1b[1;5Q"
    CTRL_F3 = "\x1b[1;5R"
    CTRL_F4 = "\x1b[1;5S"
    CTRL_SHIFT_UP = "\x1b[1;6A"
    CTRL_SHIFT_DOWN = "\x1b[1;6B"
    CTRL_SHIFT_RIGHT = "\x1b[1;6C"
    CTRL_SHIFT_LEFT = "\x1b[1;6D"
    CTRL_SHIFT_BEGIN = "\x1b[1;6E"
    CTRL_SHIFT_END = "\x1b[1;6F"
    CTRL_SHIFT_HOME = "\x1b[1;6H"
    CTRL_SHIFT_F1 = "\x1b[1;6P"
    CTRL_SHIFT_F2 = "\x1b[1;6Q"
    CTRL_SHIFT_F3 = "\x1b[1;6R"
    CTRL_SHIFT_F4 = "\x1b[1;6S"
    CTRL_ALT_UP = "\x1b[1;7A"
    CTRL_ALT_DOWN = "\x1b[1;7B"
    CTRL_ALT_RIGHT = "\x1b[1;7C"
    CTRL_ALT_LEFT = "\x1b[1;7D"
    CTRL_ALT_BEGIN = "\x1b[1;7E"
    CTRL_ALT_END = "\x1b[1;7F"
    CTRL_ALT_HOME = "\x1b[1;7H"
    CTRL_ALT_F1 = "\x1b[1;7P"
    CTRL_ALT_F2 = "\x1b[1;7Q"
    CTRL_ALT_F3 = "\x1b[1;7R"
    CTRL_ALT_F4 = "\x1b[1;7S"
    CTRL_ALT_SHIFT_UP = "\x1b[1;8A"
    CTRL_ALT_SHIFT_DOWN = "\x1b[1;8B"
    CTRL_ALT_SHIFT_RIGHT = "\x1b[1;8C"
    CTRL_ALT_SHIFT_LEFT = "\x1b[1;8D"
    CTRL_ALT_SHIFT_BEGIN = "\x1b[1;8E"
    CTRL_ALT_SHIFT_END = "\x1b[1;8F"
    CTRL_ALT_SHIFT_HOME = "\x1b[1;8H"
    CTRL_ALT_SHIFT_F1 = "\x1b[1;8P"
    CTRL_ALT_SHIFT_F2 = "\x1b[1;8Q"
    CTRL_ALT_SHIFT_F3 = "\x1b[1;8R"
    CTRL_ALT_SHIFT_F4 = "\x1b[1;8S"
    INSERT = "\x1b[2~"
    SHIFT_INSERT = "\x1b[2;2~"
    ALT_INSERT = "\x1b[2;3~"
    ALT_SHIFT_INSERT = "\x1b[2;4~"
    CTRL_INSERT = "\x1b[2;5~"
    CTRL_SHIFT_INSERT = "\x1b[2;6~"
    CTRL_ALT_INSERT = "\x1b[2;7~"
    CTRL_ALT_SHIFT_INSERT = "\x1b[2;8~"
    DEL = "\x1b[3~"
    SHIFT_DEL = "\x1b[3;2~"
    ALT_DEL = "\x1b[3;3~"
    ALT_SHIFT_DEL = "\x1b[3;4~"
    CTRL_DEL = "\x1b[3;5~"
    CTRL_SHIFT_DEL = "\x1b[3;6~"
    CTRL_ALT_DEL = "\x1b[3;7~"
    CTRL_ALT_SHIFT_DEL = "\x1b[3;8~"

    ENTER_INSERT_MODE = "\x1b[4h"
    EXIT_INSERT_MODE = "\x1b[4l"
    ENTER_UNDERLINE_MODE = "\x1b[4m"
    EXIT_UNDERLINE_MODE = "\x1b[24m"

    PG_UP = "\x1b[5~"
    SHIFT_PAGE_UP = "\x1b[5;2~"
    ALT_PAGE_UP = "\x1b[5;3~"
    ALT_SHIFT_PAGE_UP = "\x1b[5;4~"
    CTRL_PAGE_UP = "\x1b[5;5~"
    CTRL_SHIFT_PAGE_UP = "\x1b[5;6~"
    CTRL_ALT_PAGE_UP = "\x1b[5;7~"
    CTRL_ALT_SHIFT_PAGE_UP = "\x1b[5;8~"
    PG_DOWN = "\x1b[6~"
    SHIFT_PAGE_DOWN = "\x1b[6;2~"
    ALT_PAGE_DOWN = "\x1b[6;3~"
    ALT_SHIFT_PAGE_DOWN = "\x1b[6;4~"
    CTRL_PAGE_DOWN = "\x1b[6;5~"
    CTRL_SHIFT_PAGE_DOWN = "\x1b[6;6~"
    CTRL_ALT_PAGE_DOWN = "\x1b[6;7~"
    CTRL_ALT_SHIFT_PAGE_DOWN = "\x1b[6;8~"
    F5 = "\x1b[15~"
    SHIFT_F5 = "\x1b[15;2~"
    ALT_F5 = "\x1b[15;3~"
    ALT_SHIFT_F5 = "\x1b[15;4~"
    CTRL_F5 = "\x1b[15;5~"
    CTRL_SHIFT_F5 = "\x1b[15;6~"
    CTRL_ALT_F5 = "\x1b[15;7~"
    CTRL_ALT_SHIFT_F5 = "\x1b[15;8~"
    SHIFT_F6 = "\x1b[17;2~"
    F6 = "\x1b[17~"
    ALT_F6 = "\x1b[17;3~"
    ALT_SHIFT_F6 = "\x1b[17;4~"
    CTRL_F6 = "\x1b[17;5~"
    CTRL_SHIFT_F6 = "\x1b[17;6~"
    CTRL_ALT_F6 = "\x1b[17;7~"
    CTRL_ALT_SHIFT_F6 = "\x1b[17;8~"
    F7 = "\x1b[18~"
    SHIFT_F7 = "\x1b[18;2~"
    ALT_F7 = "\x1b[18;3~"
    ALT_SHIFT_F7 = "\x1b[18;4~"
    CTRL_F7 = "\x1b[18;5~"
    CTRL_SHIFT_F7 = "\x1b[18;6~"
    CTRL_ALT_F7 = "\x1b[18;7~"
    CTRL_ALT_SHIFT_F7 = "\x1b[18;8~"
    F8 = "\x1b[19~"
    SHIFT_F8 = "\x1b[19;2~"
    ALT_F8 = "\x1b[19;3~"
    ALT_SHIFT_F8 = "\x1b[19;4~"
    CTRL_F8 = "\x1b[19;5~"
    CTRL_SHIFT_F8 = "\x1b[19;6~"
    CTRL_ALT_F8 = "\x1b[19;7~"
    CTRL_ALT_SHIFT_F8 = "\x1b[19;8~"
    F9 = "\x1b[20~"
    SHIFT_F9 = "\x1b[20;2~"
    ALT_F9 = "\x1b[20;3~"
    ALT_SHIFT_F9 = "\x1b[20;4~"
    CTRL_F9 = "\x1b[20;5~"
    CTRL_SHIFT_F9 = "\x1b[20;6~"
    CTRL_ALT_F9 = "\x1b[20;7~"
    CTRL_ALT_SHIFT_F9 = "\x1b[20;8~"
    F10 = "\x1b[21~"
    SHIFT_F10 = "\x1b[21;2~"
    ALT_F10 = "\x1b[21;3~"
    ALT_SHIFT_F10 = "\x1b[21;4~"
    CTRL_F10 = "\x1b[21;5~"
    CTRL_SHIFT_F10 = "\x1b[21;6~"
    CTRL_ALT_F10 = "\x1b[21;7~"
    CTRL_ALT_SHIFT_F10 = "\x1b[21;8~"
    F11 = "\x1b[23~"
    SHIFT_F11 = "\x1b[23;2~"
    ALT_F11 = "\x1b[23;3~"
    ALT_SHIFT_F11 = "\x1b[23;4~"
    CTRL_F11 = "\x1b[23;5~"
    CTRL_SHIFT_F11 = "\x1b[23;6~"
    CTRL_ALT_F11 = "\x1b[23;7~"
    CTRL_ALT_SHIFT_F11 = "\x1b[23;8~"
    F12 = "\x1b[24~"
    SHIFT_F12 = "\x1b[24;2~"
    ALT_F12 = "\x1b[24;3~"
    ALT_SHIFT_F12 = "\x1b[24;4~"
    CTRL_F12 = "\x1b[24;5~"
    CTRL_SHIFT_F12 = "\x1b[24;6~"
    CTRL_ALT_F12 = "\x1b[24;7~"
    CTRL_ALT_SHIFT_F12 = "\x1b[24;8~"


class Terminal(TerminalBase):
    __exit_keys: list[str] = [KeyMapping.CTRL_ENTER]
    __linebreak_keys: list[KeyMapping] = [KeyMapping.ENTER, KeyMapping.CTRL_ENTER]
    __backspace_keys: list[KeyMapping] = [KeyMapping.BACKSPACE]
    __arrow_keys: list[KeyMapping] = [KeyMapping.UP, KeyMapping.DOWN, KeyMapping.RIGHT, KeyMapping.LEFT]

    def read_lines(self) -> list[str]:
        """
        Reads a multipe lines from the user's input.
        If one of the linebreak keys is pressed it ends a line (default: [ ENTER ]).
        If one of the exit keys is pressed it ends a line AND finishes the input (default: [ CTRL+ENTER, CTRL+D ]).

        Returns:
            list[str]: The lines entered by the user.
        """
        max_line_size = self._get_line_size()
        buffer = list[str]([""])

        print(f"Line size: {max_line_size}")

        fd, old_settings = self.__start_read()
        try:
            while True:
                key = self.__read_key()
                if key.isprintable():
                    self._handle_printable(buffer, key, max_line_size)
                elif key in self.__backspace_keys:
                    self._handle_backspace(buffer)
                elif key in self.__arrow_keys:
                    self._handle_cursor_movement(buffer, key)
                elif key in self.__linebreak_keys:
                    self._handle_linebreak(buffer)
                if key in self.__exit_keys:
                    break
        finally:
            self.__end_read(fd, old_settings)

        lines = list[str]()
        line = ""
        for entry in buffer:
            line += entry
            if line.endswith("\n"):
                line = line.rstrip("\n")
                lines.append(line)
                line = ""
        return lines

    def read_line(self) -> str:
        """
        Reads a line from the from the user's input.
        If one of the exit keys is pressed it finishes the input (default: [ ENTER, CTRL+ENTER, CTRL+D ]).

        Args:
            interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
            exit_keys (Iterable[str]): The keys that will finish the input.

        Returns:
            str: The line entered by the user.
        """
        max_line_size = self._get_line_size()
        buffer = list[str]([""])
        fd, old_settings = self.__start_read()
        try:
            while True:
                key = self.__read_key()
                if key.isprintable():
                    self._handle_printable(buffer, key, max_line_size)
                elif key in self.__backspace_keys:
                    self._handle_backspace(buffer)
                elif key in self.__linebreak_keys:
                    self._handle_linebreak(buffer)
                    break
        finally:
            self.__end_read(fd, old_settings)

        line = ""
        for entry in buffer:
            line += entry
            if line.endswith("\n"):
                line = line.rstrip("\n")
                break
        return line

    def read_key(self) -> str:
        """
        Reads a single key press from the user.

        Args:
            interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).

        Returns:
            str: The key pressed by the user.
        """
        fd, old_settings = self.__start_read()
        try:
            return self.__read_key()
        finally:
            self.__end_read(fd, old_settings)

    def __start_read(self) -> tuple[int, list[Any]]:
        sys.stdout.flush()
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        return fd, old_settings

    def __end_read(self, fd: int, old_settings: list[Any]) -> None:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def __read_key(self) -> str:
        ch = sys.stdin.read(1)
        if ord(ch) == 27:
            ch = "\x1b"
            ch += sys.stdin.read(1)
            code = sys.stdin.read(1)
            ch += code
            while code.isnumeric() or code == ";":
                code = sys.stdin.read(1)
                ch += code
        if ch in KeyMapping.CTRL_C:
            raise KeyboardInterrupt
        return ch
