# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
"""
Tools that helps reading the console input from the user in Windows.
"""

# pylint: disable=import-error
# shows an error in the IDE when in Linux environment but works fine
import msvcrt
# pylint: enable=import-error

from ..common import static_init      # pylint: disable=relative-beyond-top-level
from .terminal_base import BaseKeyMapping, BaseTerminal       # pylint: disable=relative-beyond-top-level

@static_init
class KeyMapping(BaseKeyMapping):
    """
    Represents a collection of key constants used for keyboard input handling.
    Each key is represented as a string literal.
    """
    SHIFT_TAB = "\x00\x0f"

    ALT_A = "\x00\x1e"
    ALT_B = "\x00\x30"
    ALT_C = "\x00\x2e"
    ALT_D = "\x00\x20"
    ALT_E = "\x00\x12"
    ALT_F = "\x00\x21"
    ALT_G = "\x00\x22"
    ALT_H = "\x00\x23"
    ALT_I = "\x00\x17"
    ALT_J = "\x00\x24"
    ALT_K = "\x00\x25"
    ALT_L = "\x00\x26"
    ALT_M = "\x00\x32"
    ALT_N = "\x00\x31"
    ALT_O = "\x00\x18"
    ALT_P = "\x00\x19"
    ALT_Q = "\x00\x10"
    ALT_R = "\x00\x13"
    ALT_S = "\x00\x1f"
    ALT_T = "\x00\x14"
    ALT_U = "\x00\x16"
    ALT_V = "\x00\x2f"
    ALT_W = "\x00\x11"
    ALT_X = "\x00\x2d"
    ALT_Y = "\x00\x15"
    ALT_Z = "\x00\x2c"

    BACKSPACE = "\x08"
    TAB = "\x09"
    CTRL_ENTER = "\x0a"
    ENTER = "\x0d"
    ESC = "\x1b"

    CTRL_BREAK = "\x00\x00"
    NULL = "\x00\x03"

    CTRL_2 = "\x00\x03"
    CTRL_6 = "\x1e"
    ALT_1 = "\x00\x78"
    ALT_2 = "\x00\x79"
    ALT_3 = "\x00\x7a"
    ALT_4 = "\x00\x7b"
    ALT_5 = "\x00\x7c"
    ALT_6 = "\x00\x7d"
    ALT_7 = "\x00\x7e"
    ALT_8 = "\x00\x7e"
    ALT_9 = "\x00\x7f"
    ALT_0 = "\x00\x81"

    CTRL_MINUS = "\x1f"
    ALT_MINUS = "\x00\x82"

    CTRL_BACKSPACE = "\x7f"

    HOME = "\xe0\x47"
    UP = "\xe0\x48"
    PAGEUP = "\xe0\x49"
    LEFT = "\xe0\x4b"
    RIGHT = "\xe0\x4d"
    END = "\xe0\x4f"
    DOWN = "\xe0\x50"
    PAGEDOWN = "\xe0\x51"
    INS = "\xe0\x52"
    DEL = "\xe0\x53"

    PRINT_SCREEN = "\x00\x37"
    F1 = "\x00\x3b"
    F2 = "\x00\x3c"
    F3 = "\x00\x3d"
    F4 = "\x00\x3e"
    F5 = "\x00\x3f"
    F6 = "\x00\x40"
    F7 = "\x00\x41"
    F8 = "\x00\x42"
    F9 = "\x00\x43"
    F10 = "\x00\x44"
    KEYPAD_HOME = "\x00\x47"
    KEYPAD_UP = "\x00\x48"
    KEYPAD_PAGEUP = "\x00\x49"
    KEYPAD_LEFT = "\x00\x4b"
    KEYPAD_CENTER = "\x00\x4c"
    KEYPAD_RIGHT = "\x00\x4d"
    KEYPAD_END = "\x00\x4f"
    KEYPAD_DOWN = "\x00\x50"
    KEYPAD_PAGEDOWN = "\x00\x51"
    KEYPAD_INS = "\x00\x52"
    KEYPAD_DEL = "\x00\x53"

    SHIFT_F1 = "\x00\x54"
    SHIFT_F2 = "\x00\x55"
    SHIFT_F3 = "\x00\x56"
    SHIFT_F4 = "\x00\x57"
    SHIFT_F5 = "\x00\x58"
    SHIFT_F6 = "\x00\x59"
    SHIFT_F7 = "\x00\x5a"
    SHIFT_F8 = "\x00\x5b"
    SHIFT_F9 = "\x00\x5c"
    SHIFT_F10 = "\x00\x5d"
    CTRL_F1 = "\x00\x5e"
    CTRL_F2 = "\x00\x5f"
    CTRL_F3 = "\x00\x60"
    CTRL_F4 = "\x00\x61"
    CTRL_F5 = "\x00\x62"
    CTRL_F6 = "\x00\x63"
    CTRL_F7 = "\x00\x64"
    CTRL_F8 = "\x00\x65"
    CTRL_F9 = "\x00\x66"
    CTRL_F10 = "\x00\x67"
    ALT_F1 = "\x00\x68"
    ALT_F2 = "\x00\x69"
    ALT_F3 = "\x00\x6a"
    ALT_F4 = "\x00\x6b"
    ALT_F5 = "\x00\x6c"
    ALT_F6 = "\x00\x6d"
    ALT_F7 = "\x00\x6e"
    ALT_F8 = "\x00\x6f"
    ALT_F9 = "\x00\x70"
    ALT_F10 = "\x00\x71"

    CTRL_PRINT_SCREEN = "\xe0\x72"
    CTRL_LEFT = "\xe0\x73"
    CTRL_RIGHT = "\xe0\x74"
    CTRL_END = "\xe0\x75"
    CTRL_PAGEDOWN = "\xe0\x76"
    CTRL_HOME = "\xe0\x77"

    ALT_1 = "\x00\x78"
    ALT_2 = "\x00\x79"
    ALT_3 = "\x00\x7a"
    ALT_4 = "\x00\x7b"
    ALT_5 = "\x00\x7c"
    ALT_6 = "\x00\x7d"
    ALT_7 = "\x00\x7e"
    ALT_8 = "\x00\x7f"
    ALT_9 = "\x00\x80"
    ALT_0 = "\x00\x81"
    ALT_MINUS = "\x00\x82"
    ALT_EQUALS = "\x00\x83"

    CTRL_PAGEUP = "\x00\x84"
    F11 = "\x00\x85"
    F12 = "\x00\x86"
    SHIFT_F11 = "\x00\x87"
    SHIFT_F12 = "\x00\x88"
    CTRL_F11 = "\x00\x89"
    CTRL_F12 = "\x00\x8a"
    ALT_F11 = "\x00\x8b"
    ALT_F12 = "\x00\x8c"
    CTRL_UP = "\x00\x8d"
    CTRL_MINUS = "\x00\x8e"
    CTRL_5 = "\x00\x8f"
    CTRL_PLUS = "\x00\x90"
    CTRL_DOWN = "\x00\x91"
    CTRL_INS = "\x00\x92"
    CTRL_DEL = "\x00\x93"
    CTRL_TAB = "\x00\x94"
    CTRL_SLASH = "\x00\x95"
    CTRL_START = "\x00\x96"
    ALT_HOME = "\x00\x97"
    ALT_UP = "\x00\x98"
    ALT_PAGEUP = "\x00\x99"
    ALT_LEFT = "\x00\x9b"
    ALT_RIGHT = "\x00\x9d"
    ALT_END = "\x00\x9f"
    ALT_DOWN = "\x00\xa0"
    ALT_PAGEDOWN = "\x00\xa1"
    ALT_INS = "\x00\xa2"
    ALT_DEL = "\x00\xa3"
    ALT_SLASH = "\x00\xa4"
    ALT_TAB = "\x00\xa5"
    ALT_ENTER = "\x00\xa6"


class Terminal(BaseTerminal):
    def __init__(self):
        self._exit_keys: list[str] = [KeyMapping.CTRL_ENTER]
        self._linebreak_keys: list[KeyMapping] = [KeyMapping.ENTER]
        self._backspace_keys: list[KeyMapping] = [KeyMapping.BACKSPACE]
        self._arrow_keys = [KeyMapping.UP, KeyMapping.DOWN, KeyMapping.RIGHT, KeyMapping.LEFT]

    def _read_char(self) -> str:
        ch: str = msvcrt.getwch()
        if ord(ch) in (0, 224):
            ch += msvcrt.getwch()
        if ch == KeyMapping.CTRL_C:
            raise KeyboardInterrupt
        return ch
