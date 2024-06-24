from utils.common import static_init


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