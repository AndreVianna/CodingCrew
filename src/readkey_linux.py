"""
Represents utility functions used throughout the application.
"""

import os

if os.name != "nt":
    import sys
    import tty
    import termios

    _name = {
        "^[[A": "UP",
        "^[[1;2A": "SHIFT_UP",
        "^[[1;3A": "ALT_UP",
        "^[[1;4A": "ALT_SHIFT_UP",
        "^[[1;5A": "CTRL_UP",
        "^[[1;6A": "CTRL_SHIFT_UP",
        "^[[1;7A": "CTRL_ALT_UP",
        "^[[1;8A": "CTRL_ALT_SHIFT_UP",
        "^[[B": "DOWN",
        "^[[1;2B": "SHIFT_DOWN",
        "^[[1;3B": "ALT_DOWN",
        "^[[1;4B": "ALT_SHIFT_DOWN",
        "^[[1;5B": "CTRL_DOWN",
        "^[[1;6B": "CTRL_SHIFT_DOWN",
        "^[[1;7B": "CTRL_ALT_DOWN",
        "^[[1;8B": "CTRL_ALT_SHIFT_DOWN",
        "^[[C": "RIGHT",
        "^[[1;2C": "SHIFT_RIGHT",
        "^[[1;3C": "ALT_RIGHT",
        "^[[1;4C": "ALT_SHIFT_RIGHT",
        "^[[1;5C": "CTRL_RIGHT",
        "^[[1;6C": "CTRL_SHIFT_RIGHT",
        "^[[1;7C": "CTRL_ALT_RIGHT",
        "^[[1;8C": "CTRL_ALT_SHIFT_RIGHT",
        "^[[D": "LEFT",
        "^[[1;2D": "SHIFT_LEFT",
        "^[[1;3D": "ALT_LEFT",
        "^[[1;4D": "ALT_SHIFT_LEFT",
        "^[[1;5D": "CTRL_LEFT",
        "^[[1;6D": "CTRL_SHIFT_LEFT",
        "^[[1;7D": "CTRL_ALT_LEFT",
        "^[[1;8D": "CTRL_ALT_SHIFT_LEFT",
        "^[[F": "END",
        "^[[1;2F": "SHIFT_END",
        "^[[1;3F": "ALT_END",
        "^[[1;4F": "ALT_SHIFT_END",
        "^[[1;5F": "CTRL_END",
        "^[[1;6F": "CTRL_SHIFT_END",
        "^[[1;7F": "CTRL_ALT_END",
        "^[[1;8F": "CTRL_ALT_SHIFT_END",
        "^[[H": "HOME",
        "^[[1;2H": "SHIFT_HOME",
        "^[[1;3H": "ALT_HOME",
        "^[[1;4H": "ALT_SHIFT_HOME",
        "^[[1;5H": "CTRL_HOME",
        "^[[1;6H": "CTRL_SHIFT_HOME",
        "^[[1;7H": "CTRL_ALT_HOME",
        "^[[1;8H": "CTRL_ALT_SHIFT_HOME",
        "^[[2~": "INSERT",
        "^[[2;2~": "SHIFT_INSERT",
        "^[[2;3~": "ALT_INSERT",
        "^[[2;4~": "ALT_SHIFT_INSERT",
        "^[[2;5~": "CTRL_INSERT",
        "^[[2;6~": "CTRL_SHIFT_INSERT",
        "^[[2;7~": "CTRL_ALT_INSERT",
        "^[[2;8~": "CTRL_ALT_SHIFT_INSERT",
        "^[[3~": "DEL",
        "^[[3;2~": "SHIFT_DEL",
        "^[[3;3~": "ALT_DEL",
        "^[[3;4~": "ALT_SHIFT_DEL",
        "^[[3;5~": "CTRL_DEL",
        "^[[3;6~": "CTRL_SHIFT_DEL",
        "^[[3;7~": "CTRL_ALT_DEL",
        "^[[3;8~": "CTRL_ALT_SHIFT_DEL",
        "^[[5~": "PG_UP",
        "^[[5;2~": "SHIFT_UP",
        "^[[5;3~": "ALT_UP",
        "^[[5;4~": "ALT_SHIFT_UP",
        "^[[5;5~": "CTRL_PG_UP",
        "^[[5;6~": "CTRL_SHIFT_UP",
        "^[[5;7~": "CTRL_ALT_UP",
        "^[[5;8~": "CTRL_ALT_SHIFT_UP",
        "^[[6~": "PG_DOWN",
        "^[[6;2~": "SHIFT_DOWN",
        "^[[6;3~": "ALT_DOWN",
        "^[[6;4~": "ALT_SHIFT_DOWN",
        "^[[6;5~": "CTRL_PG_DOWN",
        "^[[6;6~": "CTRL_SHIFT_DOWN",
        "^[[6;7~": "CTRL_ALT_DOWN",
        "^[[6;8~": "CTRL_ALT_SHIFT_DOWN",
        "^[OP": "F1",
        "^[[1;2P": "SHIFT_F1",
        "^[[1;3P": "ALT_F1",
        "^[[1;4P": "ALT_SHIFT_F1",
        "^[[1;5P": "CTRL_F1",
        "^[[1;6P": "CTRL_SHIFT_F1",
        "^[[1;7P": "CTRL_ALT_F1",
        "^[[1;8P": "CTRL_ALT_SHIFT_F1",
        "^[OQ": "F2",
        "^[[1;2Q": "SHIFT_F2",
        "^[[1;3Q": "ALT_F2",
        "^[[1;4Q": "ALT_SHIFT_F2",
        "^[[1;5Q": "CTRL_F2",
        "^[[1;6Q": "CTRL_SHIFT_F2",
        "^[[1;7Q": "CTRL_ALT_F2",
        "^[[1;8Q": "CTRL_ALT_SHIFT_F2",
        "^[OR": "F3",
        "^[[1;2R": "SHIFT_F3",
        "^[[1;3R": "ALT_F3",
        "^[[1;4R": "ALT_SHIFT_F3",
        "^[[1;5R": "CTRL_F3",
        "^[[1;6R": "CTRL_SHIFT_F3",
        "^[[1;7R": "CTRL_ALT_F3",
        "^[[1;8R": "CTRL_ALT_SHIFT_F3",
        "^[OS": "F4",
        "^[[1;2S": "SHIFT_F4",
        "^[[1;3S": "ALT_F4",
        "^[[1;4S": "ALT_SHIFT_F4",
        "^[[1;5S": "CTRL_F4",
        "^[[1;6S": "CTRL_SHIFT_F4",
        "^[[1;7S": "CTRL_ALT_F4",
        "^[[1;8S": "CTRL_ALT_SHIFT_F4",
        "^[[15~": "F5",
        "^[[15;2~": "SHIFT_F5",
        "^[[15;3~": "ALT_F5",
        "^[[15;4~": "ALT_SHIFT_F5",
        "^[[15;5~": "CTRL_F5",
        "^[[15;6~": "CTRL_SHIFT_F5",
        "^[[15;7~": "CTRL_ALT_F5",
        "^[[15;8~": "CTRL_ALT_SHIFT_F5",
        "^[[17~": "F6",
        "^[[17;2~": "SHIFT_F6",
        "^[[17;3~": "ALT_F6",
        "^[[17;4~": "ALT_SHIFT_F6",
        "^[[17;5~": "CTRL_F6",
        "^[[17;6~": "CTRL_SHIFT_F6",
        "^[[17;7~": "CTRL_ALT_F6",
        "^[[17;8~": "CTRL_ALT_SHIFT_F6",
        "^[[18~": "F7",
        "^[[18;2~": "SHIFT_F7",
        "^[[18;3~": "ALT_F7",
        "^[[18;4~": "ALT_SHIFT_F7",
        "^[[18;5~": "CTRL_F7",
        "^[[18;6~": "CTRL_SHIFT_F7",
        "^[[18;7~": "CTRL_ALT_F7",
        "^[[18;8~": "CTRL_ALT_SHIFT_F7",
        "^[[19~": "F8",
        "^[[19;2~": "SHIFT_F8",
        "^[[19;3~": "ALT_F8",
        "^[[19;4~": "ALT_SHIFT_F8",
        "^[[19;5~": "CTRL_F8",
        "^[[19;6~": "CTRL_SHIFT_F8",
        "^[[19;7~": "CTRL_ALT_F8",
        "^[[19;8~": "CTRL_ALT_SHIFT_F8",
        "^[[20~": "F9",
        "^[[20;2~": "SHIFT_F9",
        "^[[20;3~": "ALT_F9",
        "^[[20;4~": "ALT_SHIFT_F9",
        "^[[20;5~": "CTRL_F9",
        "^[[20;6~": "CTRL_SHIFT_F9",
        "^[[20;7~": "CTRL_ALT_F9",
        "^[[20;8~": "CTRL_ALT_SHIFT_F9",
        "^[[21~": "F10",
        "^[[21;2~": "SHIFT_F10",
        "^[[21;3~": "ALT_F10",
        "^[[21;4~": "ALT_SHIFT_F10",
        "^[[21;5~": "CTRL_F10",
        "^[[21;6~": "CTRL_SHIFT_F10",
        "^[[21;7~": "CTRL_ALT_F10",
        "^[[21;8~": "CTRL_ALT_SHIFT_F10",
        "^[[23~": "F11",
        "^[[23;2~": "SHIFT_F11",
        "^[[23;3~": "ALT_F11",
        "^[[23;4~": "ALT_SHIFT_F11",
        "^[[23;5~": "CTRL_F11",
        "^[[23;6~": "CTRL_SHIFT_F11",
        "^[[23;7~": "CTRL_ALT_F11",
        "^[[23;8~": "CTRL_ALT_SHIFT_F11",
        "^[[24~": "F12",
        "^[[24;2~": "SHIFT_F12",
        "^[[24;3~": "ALT_F12",
        "^[[24;4~": "ALT_SHIFT_F12",
        "^[[24;5~": "CTRL_F12",
        "^[[24;6~": "CTRL_SHIFT_F12",
        "^[[24;7~": "CTRL_ALT_F12",
        "^[[24;8~": "CTRL_ALT_SHIFT_F12",

        "\x7f": "BACKSPACE",
        "\t": "TAB",
        "\r": "ENTER",
        "\b": "CTRL_BACKSPACE",
        "\n": "CTRL_ENTER",

        "\x01": "CTRL_A",
        "\x02": "CTRL_B",
        "\x03": "CTRL_C",
        "\x04": "CTRL_D",
        "\x05": "CTRL_E",
        "\x06": "CTRL_F",
        "\x07": "CTRL_G",
        "\x0b": "CTRL_K",
        "\x0c": "CTRL_L",
        "\x0e": "CTRL_N",
        "\x0f": "CTRL_O",
        "\x10": "CTRL_P",
        "\x11": "CTRL_Q",
        "\x12": "CTRL_R",
        "\x13": "CTRL_S",
        "\x14": "CTRL_T",
        "\x15": "CTRL_U",
        "\x18": "CTRL_X",
        "\x19": "CTRL_Y",
        "\x1a": "CTRL_Z",
    }

    class _keyboard:
        BACKSPACE      = "\x7f"
        TAB            = "\t"
        ENTER          = "\r"
        CTRL_BACKSPACE = "\b"
        # CTRL_TAB     = "???"
        CTRL_ENTER     = "\n"

        UP                 = "^[[A"
        SHIFT_UP           = "^[[1;2A"
        ALT_UP             = "^[[1;3A"
        ALT_SHIFT_UP       = "^[[1;4A"
        CTRL_UP            = "^[[1;5A"
        CTRL_SHIFT_UP      = "^[[1;6A"
        CTRL_ALT_UP        = "^[[1;7A"
        CTRL_ALT_SHIFT_UP  = "^[[1;8A"

        DOWN                 = "^[[B"
        SHIFT_DOWN           = "^[[1;2B"
        ALT_DOWN             = "^[[1;3B"
        ALT_SHIFT_DOWN       = "^[[1;4B"
        CTRL_DOWN            = "^[[1;5B"
        CTRL_SHIFT_DOWN      = "^[[1;6B"
        CTRL_ALT_DOWN        = "^[[1;7B"
        CTRL_ALT_SHIFT_DOWN  = "^[[1;8B"

        RIGHT                 = "^[[C"
        SHIFT_RIGHT           = "^[[1;2C"
        ALT_RIGHT             = "^[[1;3C"
        ALT_SHIFT_RIGHT       = "^[[1;4C"
        CTRL_RIGHT            = "^[[1;5C"
        CTRL_SHIFT_RIGHT      = "^[[1;6C"
        CTRL_ALT_RIGHT        = "^[[1;7C"
        CTRL_ALT_SHIFT_RIGHT  = "^[[1;8C"

        LEFT                 = "^[[D"
        SHIFT_LEFT           = "^[[1;2D"
        ALT_LEFT             = "^[[1;3D"
        ALT_SHIFT_LEFT       = "^[[1;4D"
        CTRL_LEFT            = "^[[1;5D"
        CTRL_SHIFT_LEFT      = "^[[1;6D"
        CTRL_ALT_LEFT        = "^[[1;7D"
        CTRL_ALT_SHIFT_LEFT  = "^[[1;8D"

        END                 = "^[[F"
        SHIFT_END           = "^[[1;2F"
        ALT_END             = "^[[1;3F"
        ALT_SHIFT_END       = "^[[1;4F"
        CTRL_END            = "^[[1;5F"
        CTRL_SHIFT_END      = "^[[1;6F"
        CTRL_ALT_END        = "^[[1;7F"
        CTRL_ALT_SHIFT_END  = "^[[1;8F"

        HOME                 = "^[[H"
        SHIFT_HOME           = "^[[1;2H"
        ALT_HOME             = "^[[1;3H"
        ALT_SHIFT_HOME       = "^[[1;4H"
        CTRL_HOME            = "^[[1;5H"
        CTRL_SHIFT_HOME      = "^[[1;6H"
        CTRL_ALT_HOME        = "^[[1;7H"
        CTRL_ALT_SHIFT_HOME  = "^[[1;8H"

        INSERT                 = "^[[2~"
        SHIFT_INSERT           = "^[[2;2~"
        ALT_INSERT             = "^[[2;3~"
        ALT_SHIFT_INSERT       = "^[[2;4~"
        CTRL_INSERT            = "^[[2;5~"
        CTRL_SHIFT_INSERT      = "^[[2;6~"
        CTRL_ALT_INSERT        = "^[[2;7~"
        CTRL_ALT_SHIFT_INSERT  = "^[[2;8~"

        DEL                 = "^[[3~"
        SHIFT_DEL           = "^[[3;2~"
        ALT_DEL             = "^[[3;3~"
        ALT_SHIFT_DEL       = "^[[3;4~"
        CTRL_DEL            = "^[[3;5~"
        CTRL_SHIFT_DEL      = "^[[3;6~"
        CTRL_ALT_DEL        = "^[[3;7~"
        CTRL_ALT_SHIFT_DEL  = "^[[3;8~"

        PG_UP              = "^[[5~"
        SHIFT_UP           = "^[[5;2~"
        ALT_UP             = "^[[5;3~"
        ALT_SHIFT_UP       = "^[[5;4~"
        CTRL_PG_UP         = "^[[5;5~"
        CTRL_SHIFT_UP      = "^[[5;6~"
        CTRL_ALT_UP        = "^[[5;7~"
        CTRL_ALT_SHIFT_UP  = "^[[5;8~"

        PG_DOWN              = "^[[6~"
        SHIFT_DOWN           = "^[[6;2~"
        ALT_DOWN             = "^[[6;3~"
        ALT_SHIFT_DOWN       = "^[[6;4~"
        CTRL_PG_DOWN         = "^[[6;5~"
        CTRL_SHIFT_DOWN      = "^[[6;6~"
        CTRL_ALT_DOWN        = "^[[6;7~"
        CTRL_ALT_SHIFT_DOWN  = "^[[6;8~"

        F1                 = "^[OP"
        SHIFT_F1           = "^[[1;2P"
        ALT_F1             = "^[[1;3P"
        ALT_SHIFT_F1       = "^[[1;4P"
        CTRL_F1            = "^[[1;5P"
        CTRL_SHIFT_F1      = "^[[1;6P"
        CTRL_ALT_F1        = "^[[1;7P"
        CTRL_ALT_SHIFT_F1  = "^[[1;8P"

        F2                 = "^[OQ"
        SHIFT_F2           = "^[[1;2Q"
        ALT_F2             = "^[[1;3Q"
        ALT_SHIFT_F2       = "^[[1;4Q"
        CTRL_F2            = "^[[1;5Q"
        CTRL_SHIFT_F2      = "^[[1;6Q"
        CTRL_ALT_F2        = "^[[1;7Q"
        CTRL_ALT_SHIFT_F2  = "^[[1;8Q"

        F3                 = "^[OR"
        SHIFT_F3           = "^[[1;2R"
        ALT_F3             = "^[[1;3R"
        ALT_SHIFT_F3       = "^[[1;4R"
        CTRL_F3            = "^[[1;5R"
        CTRL_SHIFT_F3      = "^[[1;6R"
        CTRL_ALT_F3        = "^[[1;7R"
        CTRL_ALT_SHIFT_F3  = "^[[1;8R"

        F4                 = "^[OS"
        SHIFT_F4           = "^[[1;2S"
        ALT_F4             = "^[[1;3S"
        ALT_SHIFT_F4       = "^[[1;4S"
        CTRL_F4            = "^[[1;5S"
        CTRL_SHIFT_F4      = "^[[1;6S"
        CTRL_ALT_F4        = "^[[1;7S"
        CTRL_ALT_SHIFT_F4  = "^[[1;8S"

        F5                 = "^[[15~"
        SHIFT_F5           = "^[[15;2~"
        ALT_F5             = "^[[15;3~"
        ALT_SHIFT_F5       = "^[[15;4~"
        CTRL_F5            = "^[[15;5~"
        CTRL_SHIFT_F5      = "^[[15;6~"
        CTRL_ALT_F5        = "^[[15;7~"
        CTRL_ALT_SHIFT_F5  = "^[[15;8~"

        F6                 = "^[[17~"
        SHIFT_F6           = "^[[17;2~"
        ALT_F6             = "^[[17;3~"
        ALT_SHIFT_F6       = "^[[17;4~"
        CTRL_F6            = "^[[17;5~"
        CTRL_SHIFT_F6      = "^[[17;6~"
        CTRL_ALT_F6        = "^[[17;7~"
        CTRL_ALT_SHIFT_F6  = "^[[17;8~"

        F7                 = "^[[18~"
        SHIFT_F7           = "^[[18;2~"
        ALT_F7             = "^[[18;3~"
        ALT_SHIFT_F7       = "^[[18;4~"
        CTRL_F7            = "^[[18;5~"
        CTRL_SHIFT_F7      = "^[[18;6~"
        CTRL_ALT_F7        = "^[[18;7~"
        CTRL_ALT_SHIFT_F7  = "^[[18;8~"

        F8                 = "^[[19~"
        SHIFT_F8           = "^[[19;2~"
        ALT_F8             = "^[[19;3~"
        ALT_SHIFT_F8       = "^[[19;4~"
        CTRL_F8            = "^[[19;5~"
        CTRL_SHIFT_F8      = "^[[19;6~"
        CTRL_ALT_F8        = "^[[19;7~"
        CTRL_ALT_SHIFT_F8  = "^[[19;8~"

        F9                 = "^[[20~"
        SHIFT_F9           = "^[[20;2~"
        ALT_F9             = "^[[20;3~"
        ALT_SHIFT_F9       = "^[[20;4~"
        CTRL_F9            = "^[[20;5~"
        CTRL_SHIFT_F9      = "^[[20;6~"
        CTRL_ALT_F9        = "^[[20;7~"
        CTRL_ALT_SHIFT_F9  = "^[[20;8~"

        F10                = "^[[21~"
        SHIFT_F10          = "^[[21;2~"
        ALT_F10            = "^[[21;3~"
        ALT_SHIFT_F10      = "^[[21;4~"
        CTRL_F10           = "^[[21;5~"
        CTRL_SHIFT_F10     = "^[[21;6~"
        CTRL_ALT_F10       = "^[[21;7~"
        CTRL_ALT_SHIFT_F10 = "^[[21;8~"

        F11                = "^[[23~"
        SHIFT_F11          = "^[[23;2~"
        ALT_F11            = "^[[23;3~"
        ALT_SHIFT_F11      = "^[[23;4~"
        CTRL_F11           = "^[[23;5~"
        CTRL_SHIFT_F11     = "^[[23;6~"
        CTRL_ALT_F11       = "^[[23;7~"
        CTRL_ALT_SHIFT_F11 = "^[[23;8~"

        F12                = "^[[24~"
        SHIFT_F12          = "^[[24;2~"
        ALT_F12            = "^[[24;3~"
        ALT_SHIFT_F12      = "^[[24;4~"
        CTRL_F12           = "^[[24;5~"
        CTRL_SHIFT_F12     = "^[[24;6~"
        CTRL_ALT_F12       = "^[[24;7~"
        CTRL_ALT_SHIFT_F12 = "^[[24;8~"

        CTRL_A         = "\x01"
        CTRL_B         = "\x02"
        CTRL_C         = "\x03"
        CTRL_D         = "\x04"
        CTRL_E         = "\x05"
        CTRL_F         = "\x06"
        CTRL_G         = "\x07"
        CTRL_H         = "\b"
        CTRL_I         = "\t"
        CTRL_J         = "\n"
        CTRL_K         = "\x0b"
        CTRL_L         = "\x0c"
        CTRL_M         = "\r"
        CTRL_N         = "\x0e"
        CTRL_O         = "\x0f"
        CTRL_P         = "\x10"
        CTRL_Q         = "\x11"
        CTRL_R         = "\x12"
        CTRL_S         = "\x13"
        CTRL_T         = "\x14"
        CTRL_U         = "\x15"
        CTRL_X         = "\x18"
        CTRL_Y         = "\x19"
        CTRL_Z         = "\x1a"

        @staticmethod
        def name(char: str) -> str:
            """
            Converts a control character or special character to its corresponding representation.

            Args:
                char (str): The character to be converted.

            Returns:
                str: The converted character or its representation.

            Raises:
                AssertionError: If the input `char` is not a string.

            Examples:
                >>> utils = Utils()
                >>> utils.name("\x01")
                'CTRL+A'
                >>> utils.name"\n")
                'NL'
                >>> utils.name("A")
                'A'
            """
            key = _name.get(char)
            result = key if key else char
            return result

    def read_key(raw: bool = False) -> str:
        """
        Reads a single key press from the user.

        Returns:
            str: The key pressed by the user.
        """
        sys.stdout.flush()
        ch = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try :
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally :
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ord(ch) == 27 :
            _ch = read_key()
            _ch += read_key()

            while _ch[-1].isnumeric() or _ch[-1] == ";" :
                _ch += read_key()

            ch = "^[" + _ch
        return ch if raw else _keyboard.name(ch)
