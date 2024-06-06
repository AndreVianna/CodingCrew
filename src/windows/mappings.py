# pylint: disable=missing-docstring,no-member
"""
Tools that helps reading the console input from the user for WINDOWS.
"""

def init_key_mapping(cls):
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls

@init_key_mapping
class KeyMapping:
    """
    Represents a collection of key constants used for keyboard input handling.
    Each key is represented as a string literal.
    """
    _name_of: dict[str, str] = dict[str, str]()

    @classmethod
    def static_init(cls):
        members = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("_")]
        for member in members:
            name = member.replace("CTRL_", "CTRL+").replace("ALT_", "ALT+").replace("SHIFT_", "SHIFT+").replace("_", " ").replace("_", " ")
            value :str = getattr(cls, member)
            if value not in cls._name_of.keys():
                cls._name_of[value] = name
            else:
                cls._name_of[value] += f" | {name}"

    @classmethod
    def list(cls) -> list[(str, str)]:
        result: list[(str, str)] = list[(str, str)]()
        members = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("_")]
        for member in members:
            value :str = getattr(cls, member)
            result.append((cls._name_of[value], cls.code_of(value)))
        return result

    @classmethod
    def name_of(cls, char: str) -> str:
        return cls._name_of[char]

    @staticmethod
    def code_of(char: str) -> str:
        if char == "???":
            return char
        return ''.join([f"\\x{ord(c):02x}" for c in char])


    CTRL_A = "\x01"
    CTRL_B = "\x02"
    CTRL_C = "\x03"
    CTRL_D = "\x04"
    CTRL_E = "\x05"
    CTRL_F = "\x06"
    CTRL_G = "\x07"
    CTRL_H = "\x08"
    BACKSPACE = "\x08"
    CTRL_I = "\x09"
    TAB = "\x09"
    CTRL_J = "\x0a"
    CTRL_ENTER = "\x0a"
    CTRL_K = "\x0b"
    CTRL_L = "\x0c"
    CTRL_M = "\x0d"
    ENTER = "\x0d"
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
    ESC = "\x1b"

    CTRL_0 = "Undefined"
    CTRL_1 = "Undefined"
    CTRL_2 = "^\x03"
    CTRL_3 = "Undefined"
    CTRL_4 = "Undefined"
    CTRL_5 = "Undefined"
    CTRL_6 = "Undefined"
    CTRL_7 = "Undefined"
    CTRL_8 = "Undefined"
    CTRL_9 = "Undefined"

    CTRL_BACKSPACE = "\x7f"

    PRNT_SCR = "^\x37"
    F1 = "^\x3b"
    F2 = "^\x3c"
    F3 = "^\x3d"
    F4 = "^\x3e"
    F5 = "^\x3f"
    F6 = "^\x40"
    F7 = "^\x41"
    F8 = "^\x42"
    F9 = "^\x43"
    F10 = "^\x44"
    HOME = "^\x47"
    UP = "^\x48"
    PAGE_UP = "^\x49"
    LEFT = "^\x4b"
    NUM_PAD_5 = "^\x4c"
    RIGHT = "^\x4d"
    END = "^\x4f"
    DOWN = "^\x50"
    PAGE_DOWN = "^\x51"
    INS = "^\x52"
    DEL = "^\x53"
    SHIFT_F1 = "^\x54"
    SHIFT_F2 = "^\x55"
    SHIFT_F3 = "^\x56"
    SHIFT_F4 = "^\x57"
    SHIFT_F5 = "^\x58"
    SHIFT_F6 = "^\x59"
    SHIFT_F7 = "^\x5a"
    SHIFT_F8 = "^\x5b"
    SHIFT_F9 = "^\x5c"
    SHIFT_F10 = "^\x5d"
    CTRL_F1 = "^\x5e"
    CTRL_F2 = "^\x5f"
    CTRL_F3 = "^\x60"
    CTRL_F4 = "^\x61"
    CTRL_F5 = "^\x62"
    CTRL_F6 = "^\x63"
    CTRL_F7 = "^\x64"
    CTRL_F8 = "^\x65"
    CTRL_F9 = "^\x66"
    CTRL_F10 = "^\x67"
    ALT_F1 = "^\x68"
    ALT_F2 = "^\x69"
    ALT_F3 = "^\x6a"
    ALT_F4 = "^\x6b"
    ALT_F5 = "^\x6c"
    ALT_F6 = "^\x6d"
    ALT_F7 = "^\x6e"
    ALT_F8 = "^\x6f"
    ALT_F9 = "^\x70"
    ALT_F10 = "^\x71"
    CTRL_PRNT_SCR = "^\x72"
    CTRL_LEFT = "^\x73"
    CTRL_RIGHT = "^\x74"
    CTRL_END = "^\x75"
    CTRL_PAGE_DOWN = "^\x76"
    CTRL_HOME = "^\x77"

    ALT_1 = "^\x78"
    ALT_2 = "^\x79"
    ALT_3 = "^\x7a"
    ALT_4 = "^\x7b"
    ALT_5 = "^\x7c"
    ALT_6 = "^\x7d"
    ALT_7 = "^\x7e"
    ALT_8 = "^\x7f"
    ALT_9 = "^\x80"
    ALT_0 = "^\x81"
    ALT_MINUS = "^\x82"
    ALT_EQUALS = "^\x83"

    CTRL_PAGE_UP = "^\x84"
    F11 = "^\x85"
    F12 = "^\x86"
    SHIFT_F11 = "^\x87"
    SHIFT_F12 = "^\x88"
    CTRL_F11 = "^\x89"
    CTRL_F12 = "^\x8a"
    ALT_F11 = "^\x8b"
    ALT_F12 = "^\x8c"
    CTRL_UP = "^\x8d"
    CTRL_MINUS = "^\x8e"
    CTRL_5 = "^\x8f"
    CTRL_PLUS = "^\x90"
    CTRL_DOWN = "^\x91"
    CTRL_INS = "^\x92"
    CTRL_DEL = "^\x93"
    CTRL_TAB = "^\x94"
    CTRL_SLASH = "^\x95"
    CTRL_START = "^\x96"
    ALT_HOME = "^\x97"
    ALT_UP = "^\x98"
    ALT_PAGE_UP = "^\x99"
    ALT_LEFT = "^\x9b"
    ALT_RIGHT = "^\x9d"
    ALT_END = "^\x9f"
    ALT_DOWN = "^\xa0"
    ALT_PAGE_DOWN = "^\xa1"
    ALT_INS = "^\xa2"
    ALT_DEL = "^\xa3"
    ALT_SLASH = "^\xa4"
    ALT_TAB = "^\xa5"
    ALT_ENTER = "^\xa6"
