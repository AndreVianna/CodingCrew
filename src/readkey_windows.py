"""
Represents utility functions used throughout the application.
"""


import os
if os.name == "nt":
    import msvcrt
    import sys

    _name = {
        "\x01"  : "CTRL+A",
        "\x02"  : "CTRL+B",
        "\x03"  : "CTRL+C",
        "\x04"  : "CTRL+D",
        "\x05"  : "CTRL+E",
        "\x06"  : "CTRL+F",
        "\x07"  : "CTRL+G",
        "\b"    : "BACKSPACE",
        "\t"    : "TAB",
        "\n"    : "NEWLINE",
        "\x0b"  : "CTRL+K",
        "\x0c"  : "CTRL+L",
        "\r"    : "ENTER",
        "\x0e"  : "CTRL+N",
        "\x0f"  : "CTRL+O",
        "\x10"  : "CTRL+P",
        "\x11"  : "CTRL+Q",
        "\x12"  : "CTRL+R",
        "\x13"  : "CTRL+S",
        "\x14"  : "CTRL+T",
        "\x15"  : "CTRL+U",
        "\x17"  : "CTRL+W",
        "\x18"  : "CTRL+X",
        "\x19"  : "CTRL+Y",
        "\x1a"  : "CTRL+Z",
        "\x1c"  : "CTRL+*",
        "\x1d"  : "CTRL+$",
        "\x7f"  : "CTRL+BACKSPACE",
        "^[\x8d": "CTRL+UP",
        "^[\x91": "DCTRL+OWN" ,
        "^[s"   : "CTRL+LEFT",
        "^[t"   : "CTRL+RIGHT",
    }

    class _keyboard:
        TOP            = "^[H"
        DOWN           = "^[P"
        RIGHT          = "^[M"
        LEFT           = "^[K"
        DEL            = "^[S"
        END            = "^[O"
        BACKSPACE      = "\b"
        TAB            = "\t"
        ENTER          = "\r"
        CTRL_BACKSPACE = "\x7f"
        CTRL_TAB       = "???"
        CTRL_ENTER     = "???"
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
        CTRL_W         = "\x17"
        CTRL_X         = "\x18"
        CTRL_Y         = "\x19"
        CTRL_Z         = "\x1a"
        CTRL_AST       = "\x1c"
        CTRL_DOLLAR    = "\x1d"
        CTRL_UP        = "^[\x8d"
        CTRL_DOWN      = "^[\x91"
        CTRL_LEFT      = "^[s"
        CTRL_RIGHT     = "^[t"

        @staticmethod
        def namr(char) :
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
                >>> utils.namr("\x01")
                'CTRL+A'
                >>> utils.namr("\n")
                'NL'
                >>> utils.namr("A")
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
        ch = msvcrt.getwch()

        if ord(ch) == 224 :
            ch = "^[" + read_key()
        return ch if raw else _keyboard.name(ch)
