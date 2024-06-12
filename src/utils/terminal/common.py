# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Represents utility functions used throughout the application.
"""

import sys
import curses
from typing import Iterable, Literal

from attr import dataclass

from ..general import static_init, normalize_text        # pylint: disable=relative-beyond-top-level

is_linux = sys.platform.startswith("linux")
is_win32 = sys.platform.startswith("win32")

@static_init
class Action:
    """
    Represents a collection of ansi escape codes used for manipulate the terminal.
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

    GET_CURSOR_POS = "\x1b[6n"  # reports as \x1b[#l;#cR

    ADD_NEW_LINE = "\r\n"

    MOVE_UP = "\x1b[A"
    MOVE_UP_N = "\x1b[#nA"
    MOVE_DOWN = "\x1b[B"
    MOVE_DOWN_N = "\x1b[#nB"
    MOVE_RIGHT = "\x1b[C"
    MOVE_RIGHT_N = "\x1b[#nC"
    MOVE_LEFT = "\x1b[D"
    MOVE_LEFT_N = "\x1b[#nD"
    # MOVE_DOWN_N_BOL     = "\x1b[#nE"
    # MOVE_UP_N_BOL       = "\x1b[#nF"
    # MOVE_TOP            = "\x1b[I"
    # MOVE_TO_LINE_N      = "\x1b[#nI"
    MOVE_TO_BEGIN_OF_LINE = "\x1b[E"
    MOVE_TO_COL_N = "\x1b[#nG"
    MOVE_TO_0_0 = "\x1b[H"
    MOVE_TO_L_C = "\x1b[#l;#cH"

    CLEAR_TO_END_OF_SCREEN = "\x1b[J"
    CLEAR_FROM_BEBIN_OF_SCREEN = "\x1b[1J"
    CLEAR_SCREEN = "\x1b[2J"
    CLEAR_TO_END_OF_LINE = "\x1b[K"
    CLEAR_FROM_BEGIN_OF_LINE = "\x1b[1K"
    CLEAR_LINE = "\x1b[2K"


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

@dataclass
class Position:
    line: int
    column: int

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class TerminalBase:
    def read_text(self) -> str:
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
        lines = self.read_lines()
        return normalize_text(lines)

    def read_lines(self) -> list[str]:
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
        return list[str]()

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
        return ""

    def read_key(self) -> str:
        """
        Reads a single key press from the user.

        Args:
            interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).

        Returns:
            str: The key pressed by the user.
        """
        return ""

    def clear(self):
        """
        Clears the terminal screen.

        This function clears the terminal screen by executing the appropriate operating system's command
        """
        self._write(Action.CLEAR_SCREEN)
        self._write(Action.MOVE_TO_0_0)

    def format(
        self,
        text: object,
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
        code = "\x1b[%dm%s"
        fmt = ""
        if foreground is not None:
            fmt = code % (COLORS[foreground], fmt)
        if background is not None:
            fmt = code % (COLORS[background] + 10, fmt)
        if styles is not None:
            for style in styles:
                fmt = code % (STYLES[style], fmt)
        return (
            str(text)
            if not fmt
            else RESET
            + fmt
            + str(text).replace(RESET + RESET, RESET + fmt)
            + RESET
            + RESET
        )

    def write(
        self,
        text: str,
        foreground: Color | None = None,
        background: Color | None = None,
        styles: Iterable[Style] | None = None,
    ) -> None:
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
            colored_text = self.format(text, foreground, background, styles)
            self._write(colored_text)

    def write_line(
        self,
        text: str | None = None,
        foreground: Color | None = None,
        background: Color | None = None,
        styles: Iterable[Style] | None = None,
    ) -> None:
        """
        writes a formated text with the operating system's line separator character at the end.
        """
        self.write(text, foreground, background, styles)
        self._write(Action.ADD_NEW_LINE)

    def _write(self, char: str) -> None:
        sys.stdout.write(char)
        sys.stdout.flush()

    def _get_cursor_position(self) -> Position:
        """
        Returns the current cursor position and the text at the cursor position.
        """
        return Position(0, 0)

    def _set_cursor_position(self, position: Position) -> None:
        """
        Sets the cursor position.
        """
        self._write(Action.MOVE_TO_L_C.replace("#l", str(position.line)).replace("#c", str(position.column)))

    def _get_line_size(self):
        """
        Returns the size of the terminal line.
        """
        curses.filter()
        scr = curses.initscr()
        try:
            _, x = scr.getmaxyx()
        finally:
            curses.endwin()
        return x

    def _write_footer(self, exit_options: list[str]) -> None:
        pos = self._get_cursor_position()
        self._write(Action.CLEAR_TO_END_OF_SCREEN)
        self._write(Action.ADD_NEW_LINE)
        self._write(Action.ADD_NEW_LINE)
        exit_options = " or ".join(
            [" or ".join(
                [(
                    "'" + self.format(item, "yellow", styles=["bold"]) + "'"
                ) for item in option.split("|")]
            ) for option in exit_options]
        )
        self.write(
            f"You can add multiple lines. Press {exit_options} to submit.",
            styles=["dim"],
        )
        self._write(Action.MOVE_UP_N.replace("#n", "2"))
        self._write(Action.MOVE_TO_COL_N.replace("#n", f"{pos.column}"))

    def _handle_printable(self, buffer: list[str], key: str, max_line_size: int) -> None:
        buffer[-1] += key
        self._write(key)
        if len(buffer[-1]) % max_line_size == 0:
            self.__add_new_line(buffer)

    def _handle_linebreak(self, buffer: list[str]) -> None:
        buffer[-1] += "\n"
        self.__add_new_line(buffer)


    def _handle_backspace(self, buffer: list[str]) -> None:
        if buffer[-1]:
            buffer[-1] = buffer[-1][:-1]
            self._write(Action.MOVE_LEFT)
        elif not buffer[-1] and len(buffer) > 1:
            buffer.pop()
            self._write(Action.MOVE_UP)
            if buffer[-1].endswith("\n"):
                buffer[-1] = buffer[-1].rstrip("\n")
            if buffer[-1]:
                self._write(Action.MOVE_TO_COL_N.replace("#n", str(len(buffer[-1]))))
                buffer[-1] = buffer[-1][:-1]
        self._write(Action.CLEAR_TO_END_OF_LINE)

    def __add_new_line(self, buffer: list[str]) -> None:
        buffer.append("")
        self._write(Action.ADD_NEW_LINE)
