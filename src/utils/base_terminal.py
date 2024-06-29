import sys
import curses
from typing import Iterable, Literal, Optional
from dataclasses import dataclass

from .common import static_init, normalize_text

RESET = "\x1b[0m"

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

@dataclass
class Position:
    line: int
    column: int

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def __iter__(self):
        return iter((self.line, self.column))

@static_init
class BaseMapping:
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
                .replace("_", " ")
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

class CommonKeyMapping(BaseMapping):
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

class ActionKeyMapping(BaseMapping):
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

class BaseTerminal:
    _linebreak_keys: list[str] = []
    _backspace_keys: list[str] = []
    _exit_keys: list[str] = []
    _arrow_keys: list[str] = []

    def read_text(self, previous_content: Optional[str] = None) -> str:
        """
        Reads a text from the user's input.
        If one of the line-break keys is pressed it ends a line (default: [ ENTER ]).
        If one of the exit keys is pressed it finishes the input (default: [ CTRL+ENTER ]).

        Args:
            interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
            linebreak_keys (Iterable[str]): The keys that will end a line.
            exit_keys (Iterable[str]): The keys that will finish the input.

        Returns:
            str: The text entered by the user.
        """
        previous_lines = previous_content.split("\n") if previous_content else None
        lines = self.read_lines(previous_lines)
        return normalize_text(lines)

    def read_lines(self, previous_content: Optional[list[str]] = None) -> list[str]:
        max_line_size = self.get_line_size()
        buffer = list[str]()
        if previous_content:
            for line in previous_content:
                line += "\n"
                buffer_lines = [line[i:i+max_line_size] for i in range(0, len(line), max_line_size)]
                buffer.extend(buffer_lines)
            buffer[-1] = buffer[-1].rstrip("\n")
            for line in previous_content[:-1]:
                self.write_line(line)
            self.write(previous_content[-1])
        else:
            buffer.append("")

        # exit_options = [KeyMapping.name_of(key) for key in self._exit_keys]
        # self._write_footer(exit_options)
        self.__handle_user_multiline_input(buffer, max_line_size)

        lines = list[str]()
        line = ""
        for entry in buffer:
            line += entry
            if line.endswith("\n"):
                line = line.rstrip("\n")
                lines.append(line)
                line = ""
        return lines

    def read_line(self, previous_content: Optional[str] = None) -> str:
        max_line_size = self.get_line_size()
        buffer = list[str]()
        if previous_content:
            for line in previous_content:
                line += "\n"
                buffer_lines = [line[i:i+max_line_size] for i in range(0, len(line), max_line_size)]
                buffer.extend(buffer_lines)
            buffer[-1] = buffer[-1].rstrip("\n")
            for line in previous_content[:-1]:
                self.write_line(line)
            self.write(previous_content[-1])
        else:
            buffer.append("")

        self.__handle_user_singleline_input(buffer, max_line_size)

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
        return self._read_char()

    def clear(self):
        """
        Clears the terminal screen.

        This function clears the terminal screen by executing the appropriate operating system's command
        """
        self._write(ActionKeyMapping.CLEAR_SCREEN)
        self._write(ActionKeyMapping.MOVE_TO_0_0)

    def format(
        self,
        text: object,
        foreground: Color | None = None,
        background: Color | None = None,
        styles: Iterable[Style] | None = None,
    ) -> str:
        """
        returns a formatted text.

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
        Writes a formatted text.

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
        writes a formatted text with the operating system's line separator character at the end.
        """
        self.write(text, foreground, background, styles)
        self._write(ActionKeyMapping.ADD_NEW_LINE)

    def get_cursor_position(self) -> Position:
        """
        Returns the current cursor position.
        """
        self.__write(ActionKeyMapping.GET_CURSOR_POS)
        if ord(self.__read_char()) != 27:
            raise ValueError("Invalid cursor position response.")
        self.__read_char() # skip next
        line = ""
        ch = self.__read_char()
        while ch.isnumeric():
            line += ch
            ch = self.__read_char()
        if ch != ";":
            raise ValueError("Invalid cursor position response.")
        if not line:
            raise ValueError("Invalid cursor position response.")
        col = ""
        ch = self.__read_char()
        while ch.isnumeric():
            col += ch
            ch = self.__read_char()
        if not col:
            raise ValueError("Invalid cursor position response.")
        return Position(int(line), int(col))

    def set_cursor_position(self, position: Position | int) -> None:
        """
        Sets the cursor position.
        """
        if isinstance(position, Position):
            code = ActionKeyMapping.MOVE_TO_L_C.replace("#l", str(position.line)).replace("#c", str(position.column))
        else:
            position = min(max(position, 1), self.get_line_size()) if position else 1
            code = ActionKeyMapping.MOVE_TO_COL_N.replace("#n", str(position))
        sys.stdout.write(code)

    def get_line_size(self):
        """
        Returns the size of the terminal line.
        """
        curses.setupterm()
        return curses.tigetnum("cols")


    def _write(self, char: str) -> None:
        self.__write(char)

    def _read_char(self) -> str:
        return self.__read_char()

    def __write(self, char: str) -> None:
        sys.stdout.write(char)
        sys.stdout.flush()

    def __read_char(self) -> str:
        return sys.stdin.read(1)

    def _write_footer(self, exit_options: list[str]) -> None:
        pos = self.get_cursor_position()
        self._write(ActionKeyMapping.CLEAR_TO_END_OF_SCREEN)
        self._write(ActionKeyMapping.ADD_NEW_LINE)
        self._write(ActionKeyMapping.ADD_NEW_LINE)
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
        self._write(ActionKeyMapping.MOVE_UP_N.replace("#n", "2"))
        self._write(ActionKeyMapping.MOVE_TO_COL_N.replace("#n", f"{pos.column}"))

    def __handle_user_multiline_input(self, buffer: list[str], max_line_size: int) -> None:
        while True:
            key = self.read_key()
            if key.isprintable():
                self.__handle_printable(buffer, key, max_line_size)
            elif key in self._backspace_keys:
                self.__handle_backspace(buffer)
            elif key in self._linebreak_keys:
                self.__handle_linebreak(buffer)
            if key in self._exit_keys:
                break

    def __handle_user_singleline_input(self, buffer: list[str], max_line_size: int) -> None:
        while True:
            key = self.read_key()
            if key.isprintable():
                self.__handle_printable(buffer, key, max_line_size)
            elif key in self._backspace_keys:
                self.__handle_backspace(buffer)
            elif key in self._linebreak_keys:
                self.__handle_linebreak(buffer)
                break

    def __handle_printable(self, buffer: list[str], key: str, max_line_size: int) -> None:
        buffer[-1] += key
        self._write(key)
        if len(buffer[-1]) % max_line_size == 0:
            self.__add_new_line(buffer)

    def __handle_linebreak(self, buffer: list[str]) -> None:
        buffer[-1] += "\n"
        self.__add_new_line(buffer)


    def __handle_backspace(self, buffer: list[str]) -> None:
        if buffer[-1]:
            buffer[-1] = buffer[-1][:-1]
            self._write(ActionKeyMapping.MOVE_LEFT)
        elif not buffer[-1] and len(buffer) > 1:
            buffer.pop()
            self._write(ActionKeyMapping.MOVE_UP)
            if buffer[-1].endswith("\n"):
                buffer[-1] = buffer[-1].rstrip("\n")
            if buffer[-1]:
                self._write(ActionKeyMapping.MOVE_TO_COL_N.replace("#n", str(len(buffer[-1]))))
                buffer[-1] = buffer[-1][:-1]
        self._write(ActionKeyMapping.CLEAR_TO_END_OF_LINE)

    def __add_new_line(self, buffer: list[str]) -> None:
        buffer.append("")
        self._write(ActionKeyMapping.ADD_NEW_LINE)
