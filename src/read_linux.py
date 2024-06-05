"""
Represents utility functions used throughout the application.
"""

import os
if os.name != "nt":
    import sys
    import tty
    import termios
    from typing import Any, Literal

    class Key:
        """
        Represents a collection of key constants used for keyboard input handling.
        Each key is represented as a string literal.
        """

        CTRL_A:                   Literal["\x01"] = "\x01"
        CTRL_B:                   Literal["\x02"] = "\x02"
        CTRL_C:                   Literal["\x03"] = "\x03"
        CTRL_D:                   Literal["\x04"] = "\x04"
        CTRL_E:                   Literal["\x05"] = "\x05"
        CTRL_F:                   Literal["\x06"] = "\x06"
        CTRL_G:                   Literal["\x07"] = "\x07"
        CTRL_BACKSPACE:           Literal["\x08"] = "\x08"
        CTRL_H:                   Literal["\x08"] = "\x08"
        TAB:                      Literal["\x09"] = "\x09"
        CTRL_I:                   Literal["\x09"] = "\x09"
        CTRL_ENTER:               Literal["\x0a"] = "\x0a"
        CTRL_J:                   Literal["\x0a"] = "\x0a"
        CTRL_K:                   Literal["\x0b"] = "\x0b"
        CTRL_L:                   Literal["\x0c"] = "\x0c"
        ENTER:                    Literal["\x0d"] = "\x0d"
        CTRL_M:                   Literal["\x0d"] = "\x0d"
        CTRL_N:                   Literal["\x0e"] = "\x0e"
        CTRL_O:                   Literal["\x0f"] = "\x0f"
        CTRL_P:                   Literal["\x10"] = "\x10"
        CTRL_Q:                   Literal["\x11"] = "\x11"
        CTRL_R:                   Literal["\x12"] = "\x12"
        CTRL_S:                   Literal["\x13"] = "\x13"
        CTRL_T:                   Literal["\x14"] = "\x14"
        CTRL_U:                   Literal["\x15"] = "\x15"
        CTRL_V:                   Literal["\x16"] = "\x16"
        CTRL_W:                   Literal["\x17"] = "\x17"
        CTRL_X:                   Literal["\x18"] = "\x18"
        CTRL_Y:                   Literal["\x19"] = "\x19"
        CTRL_Z:                   Literal["\x1a"] = "\x1a"
        ESC:                      Literal["\x1b"] = "\x1b"
        CTRL_BKSLASH:             Literal["\x1c"] = "\x1c"
        CTRL_SLASH:               Literal["\x1f"] = "\x1f"
        BACKSPACE:                Literal["\x7f"] = "\x7f"

        UP:                       Literal["^A"] = "^A"
        DOWN:                     Literal["^B"] = "^B"
        RIGHT:                    Literal["^C"] = "^C"
        LEFT:                     Literal["^D"] = "^D"
        NUM_PAD_5:                Literal["^E"] = "^E"
        END:                      Literal["^F"] = "^F"
        HOME:                     Literal["^H"] = "^H"
        SHIFT_TAB:                Literal["^Z"] = "^Z"
        CTRL_TAB:                 Literal["Undefined"] = "Undefined"
        F1:                       Literal["^OP"] = "^OP"
        F2:                       Literal["^OQ"] = "^OQ"
        F3:                       Literal["^OR"] = "^OR"
        F4:                       Literal["^OS"] = "^OS"
        SHIFT_UP:                 Literal["^1;2A"] = "^1;2A"
        SHIFT_DOWN:               Literal["^1;2B"] = "^1;2B"
        SHIFT_RIGHT:              Literal["^1;2C"] = "^1;2C"
        SHIFT_LEFT:               Literal["^1;2D"] = "^1;2D"
        SHIFT_NUM_PAD_5:          Literal["^1;2E"] = "^1;2E"
        SHIFT_END:                Literal["^1;2F"] = "^1;2F"
        SHIFT_HOME:               Literal["^1;2H"] = "^1;2H"
        SHIFT_F1:                 Literal["^1;2P"] = "^1;2P"
        SHIFT_F2:                 Literal["^1;2Q"] = "^1;2Q"
        SHIFT_F3:                 Literal["^1;2R"] = "^1;2R"
        SHIFT_F4:                 Literal["^1;2S"] = "^1;2S"
        ALT_UP:                   Literal["^1;3A"] = "^1;3A"
        ALT_DOWN:                 Literal["^1;3B"] = "^1;3B"
        ALT_RIGHT:                Literal["^1;3C"] = "^1;3C"
        ALT_LEFT:                 Literal["^1;3D"] = "^1;3D"
        ALT_NUM_PAD_5:            Literal["^1;3E"] = "^1;3E"
        ALT_END:                  Literal["^1;3F"] = "^1;3F"
        ALT_HOME:                 Literal["^1;3H"] = "^1;3H"
        ALT_F1:                   Literal["^1;3P"] = "^1;3P"
        ALT_F2:                   Literal["^1;3Q"] = "^1;3Q"
        ALT_F3:                   Literal["^1;3R"] = "^1;3R"
        ALT_F4:                   Literal["^1;3S"] = "^1;3S"
        ALT_SHIFT_UP:             Literal["^1;4A"] = "^1;4A"
        ALT_SHIFT_DOWN:           Literal["^1;4B"] = "^1;4B"
        ALT_SHIFT_RIGHT:          Literal["^1;4C"] = "^1;4C"
        ALT_SHIFT_LEFT:           Literal["^1;4D"] = "^1;4D"
        ALT_SHIFT_NUM_PAD_5:      Literal["^1;4E"] = "^1;4E"
        ALT_SHIFT_END:            Literal["^1;4F"] = "^1;4F"
        ALT_SHIFT_HOME:           Literal["^1;4H"] = "^1;4H"
        ALT_SHIFT_F1:             Literal["^1;4P"] = "^1;4P"
        ALT_SHIFT_F2:             Literal["^1;4Q"] = "^1;4Q"
        ALT_SHIFT_F3:             Literal["^1;4R"] = "^1;4R"
        ALT_SHIFT_F4:             Literal["^1;4S"] = "^1;4S"
        CTRL_UP:                  Literal["^1;5A"] = "^1;5A"
        CTRL_DOWN:                Literal["^1;5B"] = "^1;5B"
        CTRL_RIGHT:               Literal["^1;5C"] = "^1;5C"
        CTRL_LEFT:                Literal["^1;5D"] = "^1;5D"
        CTRL_NUM_PAD_5:           Literal["^1;5E"] = "^1;5E"
        CTRL_END:                 Literal["^1;5F"] = "^1;5F"
        CTRL_HOME:                Literal["^1;5H"] = "^1;5H"
        CTRL_F1:                  Literal["^1;5P"] = "^1;5P"
        CTRL_F2:                  Literal["^1;5Q"] = "^1;5Q"
        CTRL_F3:                  Literal["^1;5R"] = "^1;5R"
        CTRL_F4:                  Literal["^1;5S"] = "^1;5S"
        CTRL_SHIFT_UP:            Literal["^1;6A"] = "^1;6A"
        CTRL_SHIFT_DOWN:          Literal["^1;6B"] = "^1;6B"
        CTRL_SHIFT_RIGHT:         Literal["^1;6C"] = "^1;6C"
        CTRL_SHIFT_LEFT:          Literal["^1;6D"] = "^1;6D"
        CTRL_SHIFT_NUM_PAD_5:     Literal["^1;6E"] = "^1;6E"
        CTRL_SHIFT_END:           Literal["^1;6F"] = "^1;6F"
        CTRL_SHIFT_HOME:          Literal["^1;6H"] = "^1;6H"
        CTRL_SHIFT_F1:            Literal["^1;6P"] = "^1;6P"
        CTRL_SHIFT_F2:            Literal["^1;6Q"] = "^1;6Q"
        CTRL_SHIFT_F3:            Literal["^1;6R"] = "^1;6R"
        CTRL_SHIFT_F4:            Literal["^1;6S"] = "^1;6S"
        CTRL_ALT_UP:              Literal["^1;7A"] = "^1;7A"
        CTRL_ALT_DOWN:            Literal["^1;7B"] = "^1;7B"
        CTRL_ALT_RIGHT:           Literal["^1;7C"] = "^1;7C"
        CTRL_ALT_LEFT:            Literal["^1;7D"] = "^1;7D"
        CTRL_ALT_NUM_PAD_5:       Literal["^1;7E"] = "^1;7E"
        CTRL_ALT_END:             Literal["^1;7F"] = "^1;7F"
        CTRL_ALT_HOME:            Literal["^1;7H"] = "^1;7H"
        CTRL_ALT_F1:              Literal["^1;7P"] = "^1;7P"
        CTRL_ALT_F2:              Literal["^1;7Q"] = "^1;7Q"
        CTRL_ALT_F3:              Literal["^1;7R"] = "^1;7R"
        CTRL_ALT_F4:              Literal["^1;7S"] = "^1;7S"
        CTRL_ALT_SHIFT_UP:        Literal["^1;8A"] = "^1;8A"
        CTRL_ALT_SHIFT_DOWN:      Literal["^1;8B"] = "^1;8B"
        CTRL_ALT_SHIFT_RIGHT:     Literal["^1;8C"] = "^1;8C"
        CTRL_ALT_SHIFT_LEFT:      Literal["^1;8D"] = "^1;8D"
        CTRL_ALT_SHIFT_NUM_PAD_5: Literal["^1;8E"] = "^1;8E"
        CTRL_ALT_SHIFT_END:       Literal["^1;8F"] = "^1;8F"
        CTRL_ALT_SHIFT_HOME:      Literal["^1;8H"] = "^1;8H"
        CTRL_ALT_SHIFT_F1:        Literal["^1;8P"] = "^1;8P"
        CTRL_ALT_SHIFT_F2:        Literal["^1;8Q"] = "^1;8Q"
        CTRL_ALT_SHIFT_F3:        Literal["^1;8R"] = "^1;8R"
        CTRL_ALT_SHIFT_F4:        Literal["^1;8S"] = "^1;8S"
        INSERT:                   Literal["^2~"] = "^2~"
        SHIFT_INSERT:             Literal["^2;2~"] = "^2;2~"
        ALT_INSERT:               Literal["^2;3~"] = "^2;3~"
        ALT_SHIFT_INSERT:         Literal["^2;4~"] = "^2;4~"
        CTRL_INSERT:              Literal["^2;5~"] = "^2;5~"
        CTRL_SHIFT_INSERT:        Literal["^2;6~"] = "^2;6~"
        CTRL_ALT_INSERT:          Literal["^2;7~"] = "^2;7~"
        CTRL_ALT_SHIFT_INSERT:    Literal["^2;8~"] = "^2;8~"
        DEL:                      Literal["^3~"] = "^3~"
        SHIFT_DEL:                Literal["^3;2~"] = "^3;2~"
        ALT_DEL:                  Literal["^3;3~"] = "^3;3~"
        ALT_SHIFT_DEL:            Literal["^3;4~"] = "^3;4~"
        CTRL_DEL:                 Literal["^3;5~"] = "^3;5~"
        CTRL_SHIFT_DEL:           Literal["^3;6~"] = "^3;6~"
        CTRL_ALT_DEL:             Literal["^3;7~"] = "^3;7~"
        CTRL_ALT_SHIFT_DEL:       Literal["^3;8~"] = "^3;8~"
        PG_UP:                    Literal["^5~"] = "^5~"
        SHIFT_PAGE_UP:            Literal["^5;2~"] = "^5;2~"
        ALT_PAGE_UP:              Literal["^5;3~"] = "^5;3~"
        ALT_SHIFT_PAGE_UP:        Literal["^5;4~"] = "^5;4~"
        CTRL_PAGE_UP:             Literal["^5;5~"] = "^5;5~"
        CTRL_SHIFT_PAGE_UP:       Literal["^5;6~"] = "^5;6~"
        CTRL_ALT_PAGE_UP:         Literal["^5;7~"] = "^5;7~"
        CTRL_ALT_SHIFT_PAGE_UP:   Literal["^5;8~"] = "^5;8~"
        PG_DOWN:                  Literal["^6~"] = "^6~"
        SHIFT_PAGE_DOWN:          Literal["^6;2~"] = "^6;2~"
        ALT_PAGE_DOWN:            Literal["^6;3~"] = "^6;3~"
        ALT_SHIFT_PAGE_DOWN:      Literal["^6;4~"] = "^6;4~"
        CTRL_PAGE_DOWN:           Literal["^6;5~"] = "^6;5~"
        CTRL_SHIFT_PAGE_DOWN:     Literal["^6;6~"] = "^6;6~"
        CTRL_ALT_PAGE_DOWN:       Literal["^6;7~"] = "^6;7~"
        CTRL_ALT_SHIFT_PAGE_DOWN: Literal["^6;8~"] = "^6;8~"
        F5:                       Literal["^15~"] = "^15~"
        SHIFT_F5:                 Literal["^15;2~"] = "^15;2~"
        ALT_F5:                   Literal["^15;3~"] = "^15;3~"
        ALT_SHIFT_F5:             Literal["^15;4~"] = "^15;4~"
        CTRL_F5:                  Literal["^15;5~"] = "^15;5~"
        CTRL_SHIFT_F5:            Literal["^15;6~"] = "^15;6~"
        CTRL_ALT_F5:              Literal["^15;7~"] = "^15;7~"
        CTRL_ALT_SHIFT_F5:        Literal["^15;8~"] = "^15;8~"
        SHIFT_F6:                 Literal["^17;2~"] = "^17;2~"
        F6:                       Literal["^17~"] = "^17~"
        ALT_F6:                   Literal["^17;3~"] = "^17;3~"
        ALT_SHIFT_F6:             Literal["^17;4~"] = "^17;4~"
        CTRL_F6:                  Literal["^17;5~"] = "^17;5~"
        CTRL_SHIFT_F6:            Literal["^17;6~"] = "^17;6~"
        CTRL_ALT_F6:              Literal["^17;7~"] = "^17;7~"
        CTRL_ALT_SHIFT_F6:        Literal["^17;8~"] = "^17;8~"
        F7:                       Literal["^18~"] = "^18~"
        SHIFT_F7:                 Literal["^18;2~"] = "^18;2~"
        ALT_F7:                   Literal["^18;3~"] = "^18;3~"
        ALT_SHIFT_F7:             Literal["^18;4~"] = "^18;4~"
        CTRL_F7:                  Literal["^18;5~"] = "^18;5~"
        CTRL_SHIFT_F7:            Literal["^18;6~"] = "^18;6~"
        CTRL_ALT_F7:              Literal["^18;7~"] = "^18;7~"
        CTRL_ALT_SHIFT_F7:        Literal["^18;8~"] = "^18;8~"
        F8:                       Literal["^19~"] = "^19~"
        SHIFT_F8:                 Literal["^19;2~"] = "^19;2~"
        ALT_F8:                   Literal["^19;3~"] = "^19;3~"
        ALT_SHIFT_F8:             Literal["^19;4~"] = "^19;4~"
        CTRL_F8:                  Literal["^19;5~"] = "^19;5~"
        CTRL_SHIFT_F8:            Literal["^19;6~"] = "^19;6~"
        CTRL_ALT_F8:              Literal["^19;7~"] = "^19;7~"
        CTRL_ALT_SHIFT_F8:        Literal["^19;8~"] = "^19;8~"
        F9:                       Literal["^20~"] = "^20~"
        SHIFT_F9:                 Literal["^20;2~"] = "^20;2~"
        ALT_F9:                   Literal["^20;3~"] = "^20;3~"
        ALT_SHIFT_F9:             Literal["^20;4~"] = "^20;4~"
        CTRL_F9:                  Literal["^20;5~"] = "^20;5~"
        CTRL_SHIFT_F9:            Literal["^20;6~"] = "^20;6~"
        CTRL_ALT_F9:              Literal["^20;7~"] = "^20;7~"
        CTRL_ALT_SHIFT_F9:        Literal["^20;8~"] = "^20;8~"
        F10:                      Literal["^21~"] = "^21~"
        SHIFT_F10:                Literal["^21;2~"] = "^21;2~"
        ALT_F10:                  Literal["^21;3~"] = "^21;3~"
        ALT_SHIFT_F10:            Literal["^21;4~"] = "^21;4~"
        CTRL_F10:                 Literal["^21;5~"] = "^21;5~"
        CTRL_SHIFT_F10:           Literal["^21;6~"] = "^21;6~"
        CTRL_ALT_F10:             Literal["^21;7~"] = "^21;7~"
        CTRL_ALT_SHIFT_F10:       Literal["^21;8~"] = "^21;8~"
        F11:                      Literal["^23~"] = "^23~"
        SHIFT_F11:                Literal["^23;2~"] = "^23;2~"
        ALT_F11:                  Literal["^23;3~"] = "^23;3~"
        ALT_SHIFT_F11:            Literal["^23;4~"] = "^23;4~"
        CTRL_F11:                 Literal["^23;5~"] = "^23;5~"
        CTRL_SHIFT_F11:           Literal["^23;6~"] = "^23;6~"
        CTRL_ALT_F11:             Literal["^23;7~"] = "^23;7~"
        CTRL_ALT_SHIFT_F11:       Literal["^23;8~"] = "^23;8~"
        F12:                      Literal["^24~"] = "^24~"
        SHIFT_F12:                Literal["^24;2~"] = "^24;2~"
        ALT_F12:                  Literal["^24;3~"] = "^24;3~"
        ALT_SHIFT_F12:            Literal["^24;4~"] = "^24;4~"
        CTRL_F12:                 Literal["^24;5~"] = "^24;5~"
        CTRL_SHIFT_F12:           Literal["^24;6~"] = "^24;6~"
        CTRL_ALT_F12:             Literal["^24;7~"] = "^24;7~"
        CTRL_ALT_SHIFT_F12:       Literal["^24;8~"] = "^24;8~"

        CTRL_0: Literal["Undefined"] = "Undefined"
        CTRL_1: Literal["Undefined"] = "Undefined"
        CTRL_2: Literal["Undefined"] = "Undefined"
        CTRL_3: Literal["Undefined"] = "Undefined"
        CTRL_4: Literal["Undefined"] = "Undefined"
        CTRL_5: Literal["Undefined"] = "Undefined"
        CTRL_6: Literal["Undefined"] = "Undefined"
        CTRL_7: Literal["Undefined"] = "Undefined"
        CTRL_8: Literal["Undefined"] = "Undefined"
        CTRL_9: Literal["Undefined"] = "Undefined"

        __key_names: dict[str, str] = {
            NUM_PAD_5: "NUMERIC PAD 5",
            SHIFT_NUM_PAD_5: "SHIFT NUMERIC PAD 5",
            ALT_NUM_PAD_5: "ALT NUMERIC PAD 5",
            ALT_SHIFT_NUM_PAD_5: "ALT_SHIFT NUMERIC PAD 5",
            CTRL_NUM_PAD_5: "CTRL NUMERIC PAD 5",
            CTRL_SHIFT_NUM_PAD_5: "CTRL SHIFT NUMERIC PAD 5",
            CTRL_ALT_NUM_PAD_5: "CTRL ALT NUMERIC PAD 5",
            CTRL_ALT_SHIFT_NUM_PAD_5: "CTRL ALT SHIFT NUMERIC PAD 5",

            UP: "UP",
            SHIFT_UP: "SHIFT UP",
            ALT_UP: "ALT UP",
            ALT_SHIFT_UP: "ALT SHIFT UP",
            CTRL_UP: "CTRL UP",
            CTRL_SHIFT_UP: "CTRL SHIFT UP",
            CTRL_ALT_UP: "CTRL ALT UP",
            CTRL_ALT_SHIFT_UP: "CTRL ALT SHIFT UP",

            DOWN: "DOWN",
            SHIFT_DOWN: "SHIFT DOWN",
            ALT_DOWN: "ALT DOWN",
            ALT_SHIFT_DOWN: "ALT SHIFT DOWN",
            CTRL_DOWN: "CTRL DOWN",
            CTRL_SHIFT_DOWN: "CTRL SHIFT DOWN",
            CTRL_ALT_DOWN: "CTRL ALT DOWN",
            CTRL_ALT_SHIFT_DOWN: "CTRL ALT SHIFT DOWN",

            RIGHT: "RIGHT",
            SHIFT_RIGHT: "SHIFT RIGHT",
            ALT_RIGHT: "ALT RIGHT",
            ALT_SHIFT_RIGHT: "ALT SHIFT RIGHT",
            CTRL_RIGHT: "CTRL RIGHT",
            CTRL_SHIFT_RIGHT: "CTRL SHIFT RIGHT",
            CTRL_ALT_RIGHT: "CTRL ALT RIGHT",
            CTRL_ALT_SHIFT_RIGHT: "CTRL ALT SHIFT RIGHT",

            LEFT: "LEFT",
            SHIFT_LEFT: "SHIFT LEFT",
            ALT_LEFT: "ALT LEFT",
            ALT_SHIFT_LEFT: "ALT SHIFT LEFT",
            CTRL_LEFT: "CTRL LEFT",
            CTRL_SHIFT_LEFT: "CTRL SHIFT LEFT",
            CTRL_ALT_LEFT: "CTRL ALT LEFT",
            CTRL_ALT_SHIFT_LEFT: "CTRL ALT SHIFT LEFT",

            END: "END",
            SHIFT_END: "SHIFT END",
            ALT_END: "ALT END",
            ALT_SHIFT_END: "ALT SHIFT END",
            CTRL_END: "CTRL END",
            CTRL_SHIFT_END: "CTRL SHIFT END",
            CTRL_ALT_END: "CTRL ALT END",
            CTRL_ALT_SHIFT_END: "CTRL ALT SHIFT END",

            HOME: "HOME",
            SHIFT_HOME: "SHIFT HOME",
            ALT_HOME: "ALT HOME",
            ALT_SHIFT_HOME: "ALT SHIFT HOME",
            CTRL_HOME: "CTRL HOME",
            CTRL_SHIFT_HOME: "CTRL SHIFT HOME",
            CTRL_ALT_HOME: "CTRL ALT HOME",
            CTRL_ALT_SHIFT_HOME: "CTRL ALT SHIFT HOME",

            INSERT: "INSERT",
            SHIFT_INSERT: "SHIFT INSERT",
            ALT_INSERT: "ALT INSERT",
            ALT_SHIFT_INSERT: "ALT SHIFT INSERT",
            CTRL_INSERT: "CTRL INSERT",
            CTRL_SHIFT_INSERT: "CTRL SHIFT INSERT",
            CTRL_ALT_INSERT: "CTRL ALT INSERT",
            CTRL_ALT_SHIFT_INSERT: "CTRL ALT SHIFT INSERT",

            DEL: "DEL",
            SHIFT_DEL: "SHIFT DEL",
            ALT_DEL: "ALT DEL",
            ALT_SHIFT_DEL: "ALT SHIFT DEL",
            CTRL_DEL: "CTRL DEL",
            CTRL_SHIFT_DEL: "CTRL SHIFT DEL",
            CTRL_ALT_DEL: "CTRL ALT DEL",
            CTRL_ALT_SHIFT_DEL: "CTRL ALT SHIFT DEL",

            PG_UP: "PAGE UP",
            SHIFT_PAGE_UP: "SHIFT PAGE UP",
            ALT_PAGE_UP: "ALT UP",
            ALT_SHIFT_PAGE_UP: "ALT SHIFT PAGE UP",
            CTRL_PAGE_UP: "CTRL PAGE UP",
            CTRL_SHIFT_PAGE_UP: "CTRL SHIFT PAGE UP",
            CTRL_ALT_PAGE_UP: "CTRL ALT UP",
            CTRL_ALT_SHIFT_PAGE_UP: "CTRL ALT SHIFT PAGE UP",

            PG_DOWN: "PAGE DOWN",
            SHIFT_PAGE_DOWN: "SHIFT PAGE DOWN",
            ALT_PAGE_DOWN: "ALT PAGE DOWN",
            ALT_SHIFT_PAGE_DOWN: "ALT SHIFT PAGE DOWN",
            CTRL_PAGE_DOWN: "CTRL PAGE DOWN",
            CTRL_SHIFT_PAGE_DOWN: "CTRL SHIFT PAGE DOWN",
            CTRL_ALT_PAGE_DOWN: "CTRL ALT PAGE DOWN",
            CTRL_ALT_SHIFT_PAGE_DOWN: "CTRL ALT SHIFT PAGE DOWN",

            F1: "F1",
            SHIFT_F1: "SHIFT F1",
            ALT_F1: "ALT F1",
            ALT_SHIFT_F1: "ALT SHIFT F1",
            CTRL_F1: "CTRL F1",
            CTRL_SHIFT_F1: "CTRL SHIFT F1",
            CTRL_ALT_F1: "CTRL ALT F1",
            CTRL_ALT_SHIFT_F1: "CTRL ALT SHIFT F1",

            F2: "F2",
            SHIFT_F2: "SHIFT F2",
            ALT_F2: "ALT F2",
            ALT_SHIFT_F2: "ALT SHIFT F2",
            CTRL_F2: "CTRL F2",
            CTRL_SHIFT_F2: "CTRL SHIFT F2",
            CTRL_ALT_F2: "CTRL ALT F2",
            CTRL_ALT_SHIFT_F2: "CTRL ALT SHIFT F2",

            F3: "F3",
            SHIFT_F3: "SHIFT F3",
            ALT_F3: "ALT F3",
            ALT_SHIFT_F3: "ALT SHIFT F3",
            CTRL_F3: "CTRL F3",
            CTRL_SHIFT_F3: "CTRL SHIFT F3",
            CTRL_ALT_F3: "CTRL ALT F3",
            CTRL_ALT_SHIFT_F3: "CTRL ALT SHIFT F3",

            F4: "F4",
            SHIFT_F4: "SHIFT F4",
            ALT_F4: "ALT F4",
            ALT_SHIFT_F4: "ALT SHIFT F4",
            CTRL_F4: "CTRL F4",
            CTRL_SHIFT_F4: "CTRL SHIFT F4",
            CTRL_ALT_F4: "CTRL ALT F4",
            CTRL_ALT_SHIFT_F4: "CTRL ALT SHIFT F4",

            F5: "F5",
            SHIFT_F5: "SHIFT F5",
            ALT_F5: "ALT F5",
            ALT_SHIFT_F5: "ALT SHIFT F5",
            CTRL_F5: "CTRL F5",
            CTRL_SHIFT_F5: "CTRL SHIFT F5",
            CTRL_ALT_F5: "CTRL ALT F5",
            CTRL_ALT_SHIFT_F5: "CTRL ALT SHIFT F5",

            F6: "F6",
            SHIFT_F6: "SHIFT F6",
            ALT_F6: "ALT F6",
            ALT_SHIFT_F6: "ALT SHIFT F6",
            CTRL_F6: "CTRL F6",
            CTRL_SHIFT_F6: "CTRL SHIFT F6",
            CTRL_ALT_F6: "CTRL ALT F6",
            CTRL_ALT_SHIFT_F6: "CTRL ALT SHIFT F6",

            F7: "F7",
            SHIFT_F7: "SHIFT F7",
            ALT_F7: "ALT F7",
            ALT_SHIFT_F7: "ALT SHIFT F7",
            CTRL_F7: "CTRL F7",
            CTRL_SHIFT_F7: "CTRL SHIFT F7",
            CTRL_ALT_F7: "CTRL ALT F7",
            CTRL_ALT_SHIFT_F7: "CTRL ALT SHIFT F7",

            F8: "F8",
            SHIFT_F8: "SHIFT F8",
            ALT_F8: "ALT F8",
            ALT_SHIFT_F8: "ALT SHIFT F8",
            CTRL_F8: "CTRL F8",
            CTRL_SHIFT_F8: "CTRL SHIFT F8",
            CTRL_ALT_F8: "CTRL ALT F8",
            CTRL_ALT_SHIFT_F8: "CTRL ALT SHIFT F8",

            F9: "F9",
            SHIFT_F9: "SHIFT F9",
            ALT_F9: "ALT F9",
            ALT_SHIFT_F9: "ALT SHIFT F9",
            CTRL_F9: "CTRL F9",
            CTRL_SHIFT_F9: "CTRL SHIFT F9",
            CTRL_ALT_F9: "CTRL ALT F9",
            CTRL_ALT_SHIFT_F9: "CTRL ALT SHIFT F9",

            F10: "F10",
            SHIFT_F10: "SHIFT F10",
            ALT_F10: "ALT F10",
            ALT_SHIFT_F10: "ALT SHIFT F10",
            CTRL_F10: "CTRL F10",
            CTRL_SHIFT_F10: "CTRL SHIFT F10",
            CTRL_ALT_F10: "CTRL ALT F10",
            CTRL_ALT_SHIFT_F10: "CTRL ALT SHIFT F10",

            F11: "F11",
            SHIFT_F11: "SHIFT F11",
            ALT_F11: "ALT F11",
            ALT_SHIFT_F11: "ALT SHIFT F11",
            CTRL_F11: "CTRL F11",
            CTRL_SHIFT_F11: "CTRL SHIFT F11",
            CTRL_ALT_F11: "CTRL ALT F11",
            CTRL_ALT_SHIFT_F11: "CTRL ALT SHIFT F11",

            F12: "F12",
            SHIFT_F12: "SHIFT F12",
            ALT_F12: "ALT F12",
            ALT_SHIFT_F12: "ALT SHIFT F12",
            CTRL_F12: "CTRL F12",
            CTRL_SHIFT_F12: "CTRL SHIFT F12",
            CTRL_ALT_F12: "CTRL ALT F12",
            CTRL_ALT_SHIFT_F12: "CTRL ALT SHIFT F12",

            BACKSPACE: "BACKSPACE",
            TAB: "TAB",
            ENTER: "ENTER",
            ESC: "ESC",
            CTRL_BKSLASH: "CTRL BACKSLASH",
            CTRL_SLASH: "CTRL SLASH",
            CTRL_BACKSPACE: "CTRL BACKSPACE",
            CTRL_TAB: "CTRL TAB",
            SHIFT_TAB: "SHIFT TAB",
            CTRL_ENTER: "CTRL ENTER",

            CTRL_A: "CTRL A",
            CTRL_B: "CTRL B",
            CTRL_C: "CTRL C",
            CTRL_D: "CTRL D",
            CTRL_E: "CTRL E",
            CTRL_F: "CTRL F",
            CTRL_G: "CTRL G",
            CTRL_H: "CTRL BACKSPACE",
            CTRL_I: "TAB",
            CTRL_J: "CTRL ENTER",
            CTRL_K: "CTRL K",
            CTRL_L: "CTRL L",
            CTRL_M: "ENTER",
            CTRL_N: "CTRL N",
            CTRL_O: "CTRL O",
            CTRL_P: "CTRL P",
            CTRL_Q: "CTRL Q",
            CTRL_R: "CTRL R",
            CTRL_S: "CTRL S",
            CTRL_T: "CTRL T",
            CTRL_U: "CTRL U",
            CTRL_V: "CTRL V",
            CTRL_W: "CTRL W",
            CTRL_X: "CTRL X",
            CTRL_Y: "CTRL Y",
            CTRL_Z: "CTRL Z",

            CTRL_0: "CTRL 0",
            CTRL_1: "CTRL 1",
            CTRL_2: "CTRL 2",
            CTRL_3: "CTRL 3",
            CTRL_4: "CTRL 4",
            CTRL_5: "CTRL 5",
            CTRL_6: "CTRL 6",
            CTRL_7: "CTRL 7",
            CTRL_8: "CTRL 8",
            CTRL_9: "CTRL 9",
        }

        @staticmethod
        def nameof(char: str) -> str:
            """
            Converts a control character or special character to its corresponding representation.

            Args:
                char (str): The character to be converted.

            Returns:
                str: The converted character or its representation.

            Raises:
                AssertionError: If the input `char` is not a string.

            Examples:
                >>> Key.nameof("\x01")
                "CTRL A"
                >>> Key.nameof(Key.CTRL_A)
                "CTRL A"
                >>> Key.nameof"\r")
                "ENTER"
                >>> Key.nameof("A")
                "A"
            """

            key = Key.__key_names.get(char)
            result = key if key else char
            return result

    def readlines(allow_ctrl_c: bool = False) -> list[str]:
        """
        Read multiple lines of input from the user.

        Returns:
            A list of strings, where each string represents a line of input entered by the user.
        """
        fd, old_settings = __start_read()
        multiline = list[str]()
        line = ""
        try:
            key = __read_key(allow_ctrl_c)
            while key not in (Key.CTRL_D, Key.CTRL_ENTER):
                # TODO: Handle special keys
                if key in (Key.ENTER):
                    multiline.append(line)
                    line = ""
                else:
                    line += key
                print(key, end="", flush=True)
                key = __read_key(allow_ctrl_c)
        finally:
            __end_read(fd, old_settings)
        return multiline

    def readline(allow_ctrl_c: bool = False) -> str:
        """
        Reads a line of input from the user.

        Returns:
            str: The line of input entered by the user.
        """
        fd, old_settings = __start_read()
        line = ""
        try:
            key = __read_key(allow_ctrl_c)
            while key not in (Key.CTRL_D, Key.ENTER, Key.CTRL_ENTER):
                # TODO: Handle arrow keys (left and right only)
                line += key
                print(key, end="", flush=True)
                key = __read_key(allow_ctrl_c)
        finally:
            __end_read(fd, old_settings)
        return line

    def readchar(allow_ctrl_c: bool = False) -> str:
        """
        Reads a single key press from the user.

        Returns:
            str: The key pressed by the user.
        """
        fd, old_settings = __start_read()
        try :
            return __read_key(allow_ctrl_c)
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

    def __read_key(allow_ctrl_c: bool) -> str:
        ch = sys.stdin.read(1)
        if ord(ch) == 27:
            ch = "^"
            code = sys.stdin.read(1)
            if code == "[" :
                code = ""
            ch += code

            code = sys.stdin.read(1)
            ch += code
            while code.isnumeric() or code == ";":
                code = sys.stdin.read(1)
                ch += code
        if ch in Key.CTRL_C and not allow_ctrl_c:
            raise KeyboardInterrupt
        return ch

    def get_key_name() -> str:
        """
        Reads a single key press from the user.

        Returns:
            str: The name of key pressed by the user.
        """
        return Key.nameof(readchar())
