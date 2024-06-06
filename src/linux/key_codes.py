# """
# Tools that helps reading the console input from the user in LINUX.
# """

# import os
# if os.name != "nt":
#     import sys
#     import tty
#     import termios
#     from enum import IntEnum
#     from typing import Any, Literal, Iterable

#     class IndentationMode(IntEnum):
#         """
#         Enumeration class representing different indentation modes.

#         Attributes:
#             Keep (int): Keep the original indentation.
#             RemoveAll (int): Remove all indentation.
#             Dedent (int): Dedent the code.
#             Normalize (int): Normalize the indentation.
#         """
#         KEEP = 0
#         REMOVE_ALL = 1
#         DEDENT = 2
#         NORMALIZE = 3

#     class Key:
#         """
#         Represents a collection of key constants used for keyboard input handling.
#         Each key is represented as a string literal.
#         """

#         CTRL_A                     = "\x01"
#         CTRL_B                     = "\x02"
#         CTRL_C                     = "\x03"
#         CTRL_D                     = "\x04"
#         CTRL_E                     = "\x05"
#         CTRL_F                     = "\x06"
#         CTRL_G                     = "\x07"
#         CTRL_BACKSPACE             = "\x08"
#         CTRL_H                     = "\x08"
#         TAB                        = "\x09"
#         CTRL_I                     = "\x09"
#         CTRL_ENTER                 = "\x0a"
#         CTRL_J                     = "\x0a"
#         CTRL_K                     = "\x0b"
#         CTRL_L                     = "\x0c"
#         ENTER                      = "\x0d"
#         CTRL_M                     = "\x0d"
#         CTRL_N                     = "\x0e"
#         CTRL_O                     = "\x0f"
#         CTRL_P                     = "\x10"
#         CTRL_Q                     = "\x11"
#         CTRL_R                     = "\x12"
#         CTRL_S                     = "\x13"
#         CTRL_T                     = "\x14"
#         CTRL_U                     = "\x15"
#         CTRL_V                     = "\x16"
#         CTRL_W                     = "\x17"
#         CTRL_X                     = "\x18"
#         CTRL_Y                     = "\x19"
#         CTRL_Z                     = "\x1a"
#         ESC                        = "\x1b"
#         CTRL_BKSLASH               = "\x1c"
#         CTRL_SLASH                 = "\x1f"
#         BACKSPACE                  = "\x7f"

#         UP                         = "\x1b[A"
#         DOWN                       = "\x1b[B"
#         RIGHT                      = "\x1b[C"
#         LEFT                       = "\x1b[D"
#         BEGIN                      = "\x1b[E"
#         END                        = "\x1b[F"
#         HOME                       = "\x1b[H"
#         CLEAR_EOS                  = "\x1b[J"
#         CLEAR_EOL                  = "\x1b[K"
#         CLEAR_BOL                  = "\x1b[1K"
#         INS_LINE                   = "\x1b[L"
#         DEL_LINE                   = "\x1b[M"
#         DEL_CHAR                   = "\x1b[P"
#         F1                         = "\x1b[P"
#         F2                         = "\x1b[Q"
#         F3                         = "\x1b[R"
#         F4                         = "\x1b[S"

#         ENTER_INSERT_MODE          = "\x1b[4h"
#         EXIT_INSERT_MODE           = "\x1b[4l"
#         ENTER_UNDERLINE_MODE       = "\x1b[4m"
#         EXIT_UNDERLINE_MODE        = "\x1b[24m"

#         SHIFT_TAB                  = "\x1b[Z"

#         CTRL_TAB                   = "Undefined" # Need to find out the value

#         SHIFT_UP                   = "\x1b[1;2A"
#         SHIFT_DOWN                 = "\x1b[1;2B"
#         SHIFT_RIGHT                = "\x1b[1;2C"
#         SHIFT_LEFT                 = "\x1b[1;2D"
#         SHIFT_BEGIN                = "\x1b[1;2E"
#         SHIFT_END                  = "\x1b[1;2F"
#         SHIFT_HOME                 = "\x1b[1;2H"
#         SHIFT_F1                   = "\x1b[1;2P"
#         SHIFT_F2                   = "\x1b[1;2Q"
#         SHIFT_F3                   = "\x1b[1;2R"
#         SHIFT_F4                   = "\x1b[1;2S"
#         ALT_UP                     = "\x1b[1;3A"
#         ALT_DOWN                   = "\x1b[1;3B"
#         ALT_RIGHT                  = "\x1b[1;3C"
#         ALT_LEFT                   = "\x1b[1;3D"
#         ALT_BEGIN                  = "\x1b[1;3E"
#         ALT_END                    = "\x1b[1;3F"
#         ALT_HOME                   = "\x1b[1;3H"
#         ALT_F1                     = "\x1b[1;3P"
#         ALT_F2                     = "\x1b[1;3Q"
#         ALT_F3                     = "\x1b[1;3R"
#         ALT_F4                     = "\x1b[1;3S"
#         ALT_SHIFT_UP               = "\x1b[1;4A"
#         ALT_SHIFT_DOWN             = "\x1b[1;4B"
#         ALT_SHIFT_RIGHT            = "\x1b[1;4C"
#         ALT_SHIFT_LEFT             = "\x1b[1;4D"
#         ALT_SHIFT_BEGIN            = "\x1b[1;4E"
#         ALT_SHIFT_END              = "\x1b[1;4F"
#         ALT_SHIFT_HOME             = "\x1b[1;4H"
#         ALT_SHIFT_F1               = "\x1b[1;4P"
#         ALT_SHIFT_F2               = "\x1b[1;4Q"
#         ALT_SHIFT_F3               = "\x1b[1;4R"
#         ALT_SHIFT_F4               = "\x1b[1;4S"
#         CTRL_UP                    = "\x1b[1;5A"
#         CTRL_DOWN                  = "\x1b[1;5B"
#         CTRL_RIGHT                 = "\x1b[1;5C"
#         CTRL_LEFT                  = "\x1b[1;5D"
#         CTRL_BEGIN                 = "\x1b[1;5E"
#         CTRL_END                   = "\x1b[1;5F"
#         CTRL_HOME                  = "\x1b[1;5H"
#         CTRL_F1                    = "\x1b[1;5P"
#         CTRL_F2                    = "\x1b[1;5Q"
#         CTRL_F3                    = "\x1b[1;5R"
#         CTRL_F4                    = "\x1b[1;5S"
#         CTRL_SHIFT_UP              = "\x1b[1;6A"
#         CTRL_SHIFT_DOWN            = "\x1b[1;6B"
#         CTRL_SHIFT_RIGHT           = "\x1b[1;6C"
#         CTRL_SHIFT_LEFT            = "\x1b[1;6D"
#         CTRL_SHIFT_BEGIN           = "\x1b[1;6E"
#         CTRL_SHIFT_END             = "\x1b[1;6F"
#         CTRL_SHIFT_HOME            = "\x1b[1;6H"
#         CTRL_SHIFT_F1              = "\x1b[1;6P"
#         CTRL_SHIFT_F2              = "\x1b[1;6Q"
#         CTRL_SHIFT_F3              = "\x1b[1;6R"
#         CTRL_SHIFT_F4              = "\x1b[1;6S"
#         CTRL_ALT_UP                = "\x1b[1;7A"
#         CTRL_ALT_DOWN              = "\x1b[1;7B"
#         CTRL_ALT_RIGHT             = "\x1b[1;7C"
#         CTRL_ALT_LEFT              = "\x1b[1;7D"
#         CTRL_ALT_BEGIN             = "\x1b[1;7E"
#         CTRL_ALT_END               = "\x1b[1;7F"
#         CTRL_ALT_HOME              = "\x1b[1;7H"
#         CTRL_ALT_F1                = "\x1b[1;7P"
#         CTRL_ALT_F2                = "\x1b[1;7Q"
#         CTRL_ALT_F3                = "\x1b[1;7R"
#         CTRL_ALT_F4                = "\x1b[1;7S"
#         CTRL_ALT_SHIFT_UP          = "\x1b[1;8A"
#         CTRL_ALT_SHIFT_DOWN        = "\x1b[1;8B"
#         CTRL_ALT_SHIFT_RIGHT       = "\x1b[1;8C"
#         CTRL_ALT_SHIFT_LEFT        = "\x1b[1;8D"
#         CTRL_ALT_SHIFT_BEGIN       = "\x1b[1;8E"
#         CTRL_ALT_SHIFT_END         = "\x1b[1;8F"
#         CTRL_ALT_SHIFT_HOME        = "\x1b[1;8H"
#         CTRL_ALT_SHIFT_F1          = "\x1b[1;8P"
#         CTRL_ALT_SHIFT_F2          = "\x1b[1;8Q"
#         CTRL_ALT_SHIFT_F3          = "\x1b[1;8R"
#         CTRL_ALT_SHIFT_F4          = "\x1b[1;8S"
#         INSERT                     = "\x1b[2~"
#         SHIFT_INSERT               = "\x1b[2;2~"
#         ALT_INSERT                 = "\x1b[2;3~"
#         ALT_SHIFT_INSERT           = "\x1b[2;4~"
#         CTRL_INSERT                = "\x1b[2;5~"
#         CTRL_SHIFT_INSERT          = "\x1b[2;6~"
#         CTRL_ALT_INSERT            = "\x1b[2;7~"
#         CTRL_ALT_SHIFT_INSERT      = "\x1b[2;8~"
#         DEL                        = "\x1b[3~"
#         SHIFT_DEL                  = "\x1b[3;2~"
#         ALT_DEL                    = "\x1b[3;3~"
#         ALT_SHIFT_DEL              = "\x1b[3;4~"
#         CTRL_DEL                   = "\x1b[3;5~"
#         CTRL_SHIFT_DEL             = "\x1b[3;6~"
#         CTRL_ALT_DEL               = "\x1b[3;7~"
#         CTRL_ALT_SHIFT_DEL         = "\x1b[3;8~"
#         PG_UP                      = "\x1b[5~"
#         SHIFT_PAGE_UP              = "\x1b[5;2~"
#         ALT_PAGE_UP                = "\x1b[5;3~"
#         ALT_SHIFT_PAGE_UP          = "\x1b[5;4~"
#         CTRL_PAGE_UP               = "\x1b[5;5~"
#         CTRL_SHIFT_PAGE_UP         = "\x1b[5;6~"
#         CTRL_ALT_PAGE_UP           = "\x1b[5;7~"
#         CTRL_ALT_SHIFT_PAGE_UP     = "\x1b[5;8~"
#         PG_DOWN                    = "\x1b[6~"
#         SHIFT_PAGE_DOWN            = "\x1b[6;2~"
#         ALT_PAGE_DOWN              = "\x1b[6;3~"
#         ALT_SHIFT_PAGE_DOWN        = "\x1b[6;4~"
#         CTRL_PAGE_DOWN             = "\x1b[6;5~"
#         CTRL_SHIFT_PAGE_DOWN       = "\x1b[6;6~"
#         CTRL_ALT_PAGE_DOWN         = "\x1b[6;7~"
#         CTRL_ALT_SHIFT_PAGE_DOWN   = "\x1b[6;8~"
#         F5                         = "\x1b[15~"
#         SHIFT_F5                   = "\x1b[15;2~"
#         ALT_F5                     = "\x1b[15;3~"
#         ALT_SHIFT_F5               = "\x1b[15;4~"
#         CTRL_F5                    = "\x1b[15;5~"
#         CTRL_SHIFT_F5              = "\x1b[15;6~"
#         CTRL_ALT_F5                = "\x1b[15;7~"
#         CTRL_ALT_SHIFT_F5          = "\x1b[15;8~"
#         SHIFT_F6                   = "\x1b[17;2~"
#         F6                         = "\x1b[17~"
#         ALT_F6                     = "\x1b[17;3~"
#         ALT_SHIFT_F6               = "\x1b[17;4~"
#         CTRL_F6                    = "\x1b[17;5~"
#         CTRL_SHIFT_F6              = "\x1b[17;6~"
#         CTRL_ALT_F6                = "\x1b[17;7~"
#         CTRL_ALT_SHIFT_F6          = "\x1b[17;8~"
#         F7                         = "\x1b[18~"
#         SHIFT_F7                   = "\x1b[18;2~"
#         ALT_F7                     = "\x1b[18;3~"
#         ALT_SHIFT_F7               = "\x1b[18;4~"
#         CTRL_F7                    = "\x1b[18;5~"
#         CTRL_SHIFT_F7              = "\x1b[18;6~"
#         CTRL_ALT_F7                = "\x1b[18;7~"
#         CTRL_ALT_SHIFT_F7          = "\x1b[18;8~"
#         F8                         = "\x1b[19~"
#         SHIFT_F8                   = "\x1b[19;2~"
#         ALT_F8                     = "\x1b[19;3~"
#         ALT_SHIFT_F8               = "\x1b[19;4~"
#         CTRL_F8                    = "\x1b[19;5~"
#         CTRL_SHIFT_F8              = "\x1b[19;6~"
#         CTRL_ALT_F8                = "\x1b[19;7~"
#         CTRL_ALT_SHIFT_F8          = "\x1b[19;8~"
#         F9                         = "\x1b[20~"
#         SHIFT_F9                   = "\x1b[20;2~"
#         ALT_F9                     = "\x1b[20;3~"
#         ALT_SHIFT_F9               = "\x1b[20;4~"
#         CTRL_F9                    = "\x1b[20;5~"
#         CTRL_SHIFT_F9              = "\x1b[20;6~"
#         CTRL_ALT_F9                = "\x1b[20;7~"
#         CTRL_ALT_SHIFT_F9          = "\x1b[20;8~"
#         F10                        = "\x1b[21~"
#         SHIFT_F10                  = "\x1b[21;2~"
#         ALT_F10                    = "\x1b[21;3~"
#         ALT_SHIFT_F10              = "\x1b[21;4~"
#         CTRL_F10                   = "\x1b[21;5~"
#         CTRL_SHIFT_F10             = "\x1b[21;6~"
#         CTRL_ALT_F10               = "\x1b[21;7~"
#         CTRL_ALT_SHIFT_F10         = "\x1b[21;8~"
#         F11                        = "\x1b[23~"
#         SHIFT_F11                  = "\x1b[23;2~"
#         ALT_F11                    = "\x1b[23;3~"
#         ALT_SHIFT_F11              = "\x1b[23;4~"
#         CTRL_F11                   = "\x1b[23;5~"
#         CTRL_SHIFT_F11             = "\x1b[23;6~"
#         CTRL_ALT_F11               = "\x1b[23;7~"
#         CTRL_ALT_SHIFT_F11         = "\x1b[23;8~"
#         F12                        = "\x1b[24~"
#         SHIFT_F12                  = "\x1b[24;2~"
#         ALT_F12                    = "\x1b[24;3~"
#         ALT_SHIFT_F12              = "\x1b[24;4~"
#         CTRL_F12                   = "\x1b[24;5~"
#         CTRL_SHIFT_F12             = "\x1b[24;6~"
#         CTRL_ALT_F12               = "\x1b[24;7~"
#         CTRL_ALT_SHIFT_F12         = "\x1b[24;8~"


#         CTRL_0 = "Undefined" # Need to find out the value
#         CTRL_1 = "Undefined" # Need to find out the value
#         CTRL_2 = "Undefined" # Need to find out the value
#         CTRL_3 = "Undefined" # Need to find out the value
#         CTRL_4 = "Undefined" # Need to find out the value
#         CTRL_5 = "Undefined" # Need to find out the value
#         CTRL_6 = "Undefined" # Need to find out the value
#         CTRL_7 = "Undefined" # Need to find out the value
#         CTRL_8 = "Undefined" # Need to find out the value
#         CTRL_9 = "Undefined" # Need to find out the value

#         __key_names: dict[str, str] = {
#             CLEAR_EOS: "CLEAR_EOS",
#             CLEAR_EOL: "CLEAR_EOL",
#             CLEAR_BOL: "CLEAR_BOL",
#             INS_LINE: "INS_LINE",
#             DEL_LINE: "DEL_LINE",
#             DEL_CHAR: "DEL_CHAR",

#             BEGIN: "NEW LINE",
#             SHIFT_BEGIN: "SHIFT NUMERIC PAD 5",
#             ALT_BEGIN: "ALT NUMERIC PAD 5",
#             ALT_SHIFT_BEGIN: "ALT_SHIFT NUMERIC PAD 5",
#             CTRL_BEGIN: "CTRL NUMERIC PAD 5",
#             CTRL_SHIFT_BEGIN: "CTRL SHIFT NUMERIC PAD 5",
#             CTRL_ALT_BEGIN: "CTRL ALT NUMERIC PAD 5",
#             CTRL_ALT_SHIFT_BEGIN: "CTRL ALT SHIFT NUMERIC PAD 5",

#             UP: "UP",
#             SHIFT_UP: "SHIFT UP",
#             ALT_UP: "ALT UP",
#             ALT_SHIFT_UP: "ALT SHIFT UP",
#             CTRL_UP: "CTRL UP",
#             CTRL_SHIFT_UP: "CTRL SHIFT UP",
#             CTRL_ALT_UP: "CTRL ALT UP",
#             CTRL_ALT_SHIFT_UP: "CTRL ALT SHIFT UP",

#             DOWN: "DOWN",
#             SHIFT_DOWN: "SHIFT DOWN",
#             ALT_DOWN: "ALT DOWN",
#             ALT_SHIFT_DOWN: "ALT SHIFT DOWN",
#             CTRL_DOWN: "CTRL DOWN",
#             CTRL_SHIFT_DOWN: "CTRL SHIFT DOWN",
#             CTRL_ALT_DOWN: "CTRL ALT DOWN",
#             CTRL_ALT_SHIFT_DOWN: "CTRL ALT SHIFT DOWN",

#             RIGHT: "RIGHT",
#             SHIFT_RIGHT: "SHIFT RIGHT",
#             ALT_RIGHT: "ALT RIGHT",
#             ALT_SHIFT_RIGHT: "ALT SHIFT RIGHT",
#             CTRL_RIGHT: "CTRL RIGHT",
#             CTRL_SHIFT_RIGHT: "CTRL SHIFT RIGHT",
#             CTRL_ALT_RIGHT: "CTRL ALT RIGHT",
#             CTRL_ALT_SHIFT_RIGHT: "CTRL ALT SHIFT RIGHT",

#             LEFT: "LEFT",
#             SHIFT_LEFT: "SHIFT LEFT",
#             ALT_LEFT: "ALT LEFT",
#             ALT_SHIFT_LEFT: "ALT SHIFT LEFT",
#             CTRL_LEFT: "CTRL LEFT",
#             CTRL_SHIFT_LEFT: "CTRL SHIFT LEFT",
#             CTRL_ALT_LEFT: "CTRL ALT LEFT",
#             CTRL_ALT_SHIFT_LEFT: "CTRL ALT SHIFT LEFT",

#             END: "END",
#             SHIFT_END: "SHIFT END",
#             ALT_END: "ALT END",
#             ALT_SHIFT_END: "ALT SHIFT END",
#             CTRL_END: "CTRL END",
#             CTRL_SHIFT_END: "CTRL SHIFT END",
#             CTRL_ALT_END: "CTRL ALT END",
#             CTRL_ALT_SHIFT_END: "CTRL ALT SHIFT END",

#             HOME: "HOME",
#             SHIFT_HOME: "SHIFT HOME",
#             ALT_HOME: "ALT HOME",
#             ALT_SHIFT_HOME: "ALT SHIFT HOME",
#             CTRL_HOME: "CTRL HOME",
#             CTRL_SHIFT_HOME: "CTRL SHIFT HOME",
#             CTRL_ALT_HOME: "CTRL ALT HOME",
#             CTRL_ALT_SHIFT_HOME: "CTRL ALT SHIFT HOME",

#             INSERT: "INSERT",
#             SHIFT_INSERT: "SHIFT INSERT",
#             ALT_INSERT: "ALT INSERT",
#             ALT_SHIFT_INSERT: "ALT SHIFT INSERT",
#             CTRL_INSERT: "CTRL INSERT",
#             CTRL_SHIFT_INSERT: "CTRL SHIFT INSERT",
#             CTRL_ALT_INSERT: "CTRL ALT INSERT",
#             CTRL_ALT_SHIFT_INSERT: "CTRL ALT SHIFT INSERT",

#             DEL: "DEL",
#             SHIFT_DEL: "SHIFT DEL",
#             ALT_DEL: "ALT DEL",
#             ALT_SHIFT_DEL: "ALT SHIFT DEL",
#             CTRL_DEL: "CTRL DEL",
#             CTRL_SHIFT_DEL: "CTRL SHIFT DEL",
#             CTRL_ALT_DEL: "CTRL ALT DEL",
#             CTRL_ALT_SHIFT_DEL: "CTRL ALT SHIFT DEL",

#             PG_UP: "PAGE UP",
#             SHIFT_PAGE_UP: "SHIFT PAGE UP",
#             ALT_PAGE_UP: "ALT UP",
#             ALT_SHIFT_PAGE_UP: "ALT SHIFT PAGE UP",
#             CTRL_PAGE_UP: "CTRL PAGE UP",
#             CTRL_SHIFT_PAGE_UP: "CTRL SHIFT PAGE UP",
#             CTRL_ALT_PAGE_UP: "CTRL ALT UP",
#             CTRL_ALT_SHIFT_PAGE_UP: "CTRL ALT SHIFT PAGE UP",

#             PG_DOWN: "PAGE DOWN",
#             SHIFT_PAGE_DOWN: "SHIFT PAGE DOWN",
#             ALT_PAGE_DOWN: "ALT PAGE DOWN",
#             ALT_SHIFT_PAGE_DOWN: "ALT SHIFT PAGE DOWN",
#             CTRL_PAGE_DOWN: "CTRL PAGE DOWN",
#             CTRL_SHIFT_PAGE_DOWN: "CTRL SHIFT PAGE DOWN",
#             CTRL_ALT_PAGE_DOWN: "CTRL ALT PAGE DOWN",
#             CTRL_ALT_SHIFT_PAGE_DOWN: "CTRL ALT SHIFT PAGE DOWN",

#             F1: "F1",
#             SHIFT_F1: "SHIFT F1",
#             ALT_F1: "ALT F1",
#             ALT_SHIFT_F1: "ALT SHIFT F1",
#             CTRL_F1: "CTRL F1",
#             CTRL_SHIFT_F1: "CTRL SHIFT F1",
#             CTRL_ALT_F1: "CTRL ALT F1",
#             CTRL_ALT_SHIFT_F1: "CTRL ALT SHIFT F1",

#             F2: "F2",
#             SHIFT_F2: "SHIFT F2",
#             ALT_F2: "ALT F2",
#             ALT_SHIFT_F2: "ALT SHIFT F2",
#             CTRL_F2: "CTRL F2",
#             CTRL_SHIFT_F2: "CTRL SHIFT F2",
#             CTRL_ALT_F2: "CTRL ALT F2",
#             CTRL_ALT_SHIFT_F2: "CTRL ALT SHIFT F2",

#             F3: "F3",
#             SHIFT_F3: "SHIFT F3",
#             ALT_F3: "ALT F3",
#             ALT_SHIFT_F3: "ALT SHIFT F3",
#             CTRL_F3: "CTRL F3",
#             CTRL_SHIFT_F3: "CTRL SHIFT F3",
#             CTRL_ALT_F3: "CTRL ALT F3",
#             CTRL_ALT_SHIFT_F3: "CTRL ALT SHIFT F3",

#             F4: "F4",
#             SHIFT_F4: "SHIFT F4",
#             ALT_F4: "ALT F4",
#             ALT_SHIFT_F4: "ALT SHIFT F4",
#             CTRL_F4: "CTRL F4",
#             CTRL_SHIFT_F4: "CTRL SHIFT F4",
#             CTRL_ALT_F4: "CTRL ALT F4",
#             CTRL_ALT_SHIFT_F4: "CTRL ALT SHIFT F4",

#             F5: "F5",
#             SHIFT_F5: "SHIFT F5",
#             ALT_F5: "ALT F5",
#             ALT_SHIFT_F5: "ALT SHIFT F5",
#             CTRL_F5: "CTRL F5",
#             CTRL_SHIFT_F5: "CTRL SHIFT F5",
#             CTRL_ALT_F5: "CTRL ALT F5",
#             CTRL_ALT_SHIFT_F5: "CTRL ALT SHIFT F5",

#             F6: "F6",
#             SHIFT_F6: "SHIFT F6",
#             ALT_F6: "ALT F6",
#             ALT_SHIFT_F6: "ALT SHIFT F6",
#             CTRL_F6: "CTRL F6",
#             CTRL_SHIFT_F6: "CTRL SHIFT F6",
#             CTRL_ALT_F6: "CTRL ALT F6",
#             CTRL_ALT_SHIFT_F6: "CTRL ALT SHIFT F6",

#             F7: "F7",
#             SHIFT_F7: "SHIFT F7",
#             ALT_F7: "ALT F7",
#             ALT_SHIFT_F7: "ALT SHIFT F7",
#             CTRL_F7: "CTRL F7",
#             CTRL_SHIFT_F7: "CTRL SHIFT F7",
#             CTRL_ALT_F7: "CTRL ALT F7",
#             CTRL_ALT_SHIFT_F7: "CTRL ALT SHIFT F7",

#             F8: "F8",
#             SHIFT_F8: "SHIFT F8",
#             ALT_F8: "ALT F8",
#             ALT_SHIFT_F8: "ALT SHIFT F8",
#             CTRL_F8: "CTRL F8",
#             CTRL_SHIFT_F8: "CTRL SHIFT F8",
#             CTRL_ALT_F8: "CTRL ALT F8",
#             CTRL_ALT_SHIFT_F8: "CTRL ALT SHIFT F8",

#             F9: "F9",
#             SHIFT_F9: "SHIFT F9",
#             ALT_F9: "ALT F9",
#             ALT_SHIFT_F9: "ALT SHIFT F9",
#             CTRL_F9: "CTRL F9",
#             CTRL_SHIFT_F9: "CTRL SHIFT F9",
#             CTRL_ALT_F9: "CTRL ALT F9",
#             CTRL_ALT_SHIFT_F9: "CTRL ALT SHIFT F9",

#             F10: "F10",
#             SHIFT_F10: "SHIFT F10",
#             ALT_F10: "ALT F10",
#             ALT_SHIFT_F10: "ALT SHIFT F10",
#             CTRL_F10: "CTRL F10",
#             CTRL_SHIFT_F10: "CTRL SHIFT F10",
#             CTRL_ALT_F10: "CTRL ALT F10",
#             CTRL_ALT_SHIFT_F10: "CTRL ALT SHIFT F10",

#             F11: "F11",
#             SHIFT_F11: "SHIFT F11",
#             ALT_F11: "ALT F11",
#             ALT_SHIFT_F11: "ALT SHIFT F11",
#             CTRL_F11: "CTRL F11",
#             CTRL_SHIFT_F11: "CTRL SHIFT F11",
#             CTRL_ALT_F11: "CTRL ALT F11",
#             CTRL_ALT_SHIFT_F11: "CTRL ALT SHIFT F11",

#             F12: "F12",
#             SHIFT_F12: "SHIFT F12",
#             ALT_F12: "ALT F12",
#             ALT_SHIFT_F12: "ALT SHIFT F12",
#             CTRL_F12: "CTRL F12",
#             CTRL_SHIFT_F12: "CTRL SHIFT F12",
#             CTRL_ALT_F12: "CTRL ALT F12",
#             CTRL_ALT_SHIFT_F12: "CTRL ALT SHIFT F12",

#             BACKSPACE: "BACKSPACE",
#             TAB: "TAB",
#             ENTER: "ENTER",
#             ESC: "ESC",
#             CTRL_BKSLASH: "CTRL BACKSLASH",
#             CTRL_SLASH: "CTRL SLASH",
#             CTRL_BACKSPACE: "CTRL BACKSPACE",
#             CTRL_TAB: "CTRL TAB",
#             SHIFT_TAB: "SHIFT TAB",
#             CTRL_ENTER: "CTRL ENTER",
#             CLEAR_EOL: "CLEAR EOL",

#             CTRL_A: "CTRL A",
#             CTRL_B: "CTRL B",
#             CTRL_C: "CTRL C",
#             CTRL_D: "CTRL D",
#             CTRL_E: "CTRL E",
#             CTRL_F: "CTRL F",
#             CTRL_G: "CTRL G",
#             CTRL_H: "CTRL BACKSPACE",
#             CTRL_I: "TAB",
#             CTRL_J: "CTRL ENTER",
#             CTRL_K: "CTRL K",
#             CTRL_L: "CTRL L",
#             CTRL_M: "ENTER",
#             CTRL_N: "CTRL N",
#             CTRL_O: "CTRL O",
#             CTRL_P: "CTRL P",
#             CTRL_Q: "CTRL Q",
#             CTRL_R: "CTRL R",
#             CTRL_S: "CTRL S",
#             CTRL_T: "CTRL T",
#             CTRL_U: "CTRL U",
#             CTRL_V: "CTRL V",
#             CTRL_W: "CTRL W",
#             CTRL_X: "CTRL X",
#             CTRL_Y: "CTRL Y",
#             CTRL_Z: "CTRL Z",

#             CTRL_0: "CTRL 0",
#             CTRL_1: "CTRL 1",
#             CTRL_2: "CTRL 2",
#             CTRL_3: "CTRL 3",
#             CTRL_4: "CTRL 4",
#             CTRL_5: "CTRL 5",
#             CTRL_6: "CTRL 6",
#             CTRL_7: "CTRL 7",
#             CTRL_8: "CTRL 8",
#             CTRL_9: "CTRL 9",
#         }

#         @staticmethod
#         def nameof(char: str) -> str:
#             """
#             Converts a control character or special character to its corresponding representation.

#             Args:
#                 char (str): The character to be converted.

#             Returns:
#                 str: The converted character or its representation.

#             Raises:
#                 AssertionError: If the input `char` is not a string.

#             Examples:
#                 >>> Key.nameof("\x01")
#                 "CTRL A"
#                 >>> Key.nameof(Key.CTRL_A)
#                 "CTRL A"
#                 >>> Key.nameof"\r")
#                 "ENTER"
#                 >>> Key.nameof("A")
#                 "A"
#             """

#             key = Key.__key_names.get(char)
#             result = key if key else char
#             return result

#     def read_text(interrupt: bool = True,
#                   linebreak_keys: Iterable[str] = None,
#                   exit_keys: Iterable[str] = None,
#                   remove_empty_lines: bool = False,
#                   trim_line_ends: bool = False,
#                   indentation_mode: IndentationMode = IndentationMode.KEEP,
#                   indent_size: int = 4,
#                   indent_str: str = " ") -> str:
#         """
#         Reads a text from the user's input.
#         If one of the linebreak keys is pressed it ends a line (default: [ ENTER ]).
#         If one of the exit keys is pressed it finishes the input (default: [ CTRL+ENTER ]).

#         Args:
#             interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
#             linebreak_keys (Iterable[str]): The keys that will end a line.
#             exit_keys (Iterable[str]): The keys that will finish the input.

#         Returns:
#             str: The text entered by the user.
#         """
#         return "\n".join(read_lines(interrupt, linebreak_keys, exit_keys, remove_empty_lines, trim_line_ends, indentation_mode, indent_size, indent_str))+"\n"

#     def read_lines(interrupt: bool = True,
#                    linebreak_keys: Iterable[str] = None,
#                    exit_keys: Iterable[str] = None,
#                    remove_empty_lines: bool = False,
#                    trim_line_ends: bool = False,
#                    indentation_mode: IndentationMode = IndentationMode.KEEP,
#                    indent_size: int = 4,
#                    indent_str: str = " ") -> list[str]:
#         """
#         Reads a multipe lines from the user's input.
#         If one of the linebreak keys is pressed it ends a line (default: [ ENTER ]).
#         If one of the exit keys is pressed it ends a line AND finishes the input (default: [ CTRL+ENTER, CTRL+D ]).

#         Args:
#             interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
#             linebreak_keys (Iterable[str]): The keys that will end a line.
#             exit_keys (Iterable[str]): The keys that will finish the input.

#         Returns:
#             list[str]: The lines entered by the user.
#         """
#         indentation_mode = IndentationMode(indentation_mode)
#         linebreak_keys = linebreak_keys if linebreak_keys else [Key.ENTER]
#         exit_keys = exit_keys if exit_keys else [Key.CTRL_ENTER, Key.CTRL_D]
#         multiline = list[str]()
#         line = ""

#         fd, old_settings = __start_read()
#         try:
#             key = __read_key(interrupt)
#             while key not in exit_keys:
#                 # TODO: Handle special keys
#                 if key == Key.BACKSPACE:
#                     if line:
#                         line = line[:-1]
#                         __write("\b \b")
#                     elif multiline:
#                         line = multiline.pop()
#                         __write(Key.UP)
#                         __write(Key.END)
#                 elif key in linebreak_keys or key in exit_keys:
#                     multiline.append(line)
#                     line = ""
#                     __write("\n")
#                 else:
#                     line += key
#                 __write(key)
#                 key = __read_key(interrupt)
#         finally:
#             __end_read(fd, old_settings)

#         multiline.append(line)
#         __write("\n")
#         if indentation_mode == IndentationMode.REMOVE_ALL:
#             multiline = [line.lstrip() for line in multiline]
#         elif indentation_mode in (IndentationMode.DEDENT, IndentationMode.NORMALIZE) and len(multiline) > 0:
#             offset = min([len(line) - len(line.lstrip()) for line in multiline])
#             result = list[str]()
#             for line in multiline:
#                 offset_line = line[offset:]
#                 if indentation_mode == IndentationMode.NORMALIZE:
#                     extra_spaces = len(offset_line) - len(offset_line.lstrip())
#                     indent_level = (extra_spaces // indent_size) + (extra_spaces % indent_size >= indent_size // 2)
#                     indent = indent_str * (indent_size * indent_level)
#                     offset_line = indent + offset_line.lstrip()
#                 result.append(offset_line)
#             multiline = result
#         if trim_line_ends:
#             multiline = [line.rstrip() for line in multiline]
#         if remove_empty_lines:
#             multiline = [line for line in multiline if line.strip()]
#         return multiline

#     def read_line(interrupt: bool = True,
#                   exit_keys: Iterable[str] = None,
#                   trim_line: bool = False) -> str:
#         """
#         Reads a line from the from the user's input.
#         If one of the exit keys is pressed it finishes the input (default: [ ENTER, CTRL+ENTER, CTRL+D ]).

#         Args:
#             interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
#             exit_keys (Iterable[str]): The keys that will finish the input.

#         Returns:
#             str: The line entered by the user.
#         """
#         exit_keys = exit_keys if exit_keys else [Key.ENTER, Key.CTRL_ENTER, Key.CTRL_D]
#         line = ""

#         fd, old_settings = __start_read()
#         try:
#             key = __read_key(interrupt)
#             while key not in exit_keys:
#                 # TODO: Handle arrow keys (left and right only)
#                 if key == Key.BACKSPACE:
#                     if line:
#                         line = line[:-1]
#                         __write("\b \b")
#                 else:
#                     line += key
#                     __write(key)
#                 key = __read_key(interrupt)
#         finally:
#             __end_read(fd, old_settings)

#         return line.strip() if trim_line else line

#     def read_key(interrupt: bool = True) -> str:
#         """
#         Reads a single key press from the user.

#         Args:
#             interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).

#         Returns:
#             str: The key pressed by the user.
#         """
#         fd, old_settings = __start_read()
#         try :
#             return __read_key(interrupt)
#         finally :
#             __end_read(fd, old_settings)

#     def __start_read() -> tuple[int, list[Any]]:
#         sys.stdout.flush()
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         tty.setraw(fd)
#         return fd, old_settings

#     def __end_read(fd: int, old_settings: list[Any]) -> None:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

#     def __write(char: str) -> None:
#         sys.stdout.write(char)
#         sys.stdout.flush()

#     def __read_key(interrupt: bool) -> str:
#         ch = sys.stdin.read(1)
#         if ord(ch) == 27:
#             ch = "\x1b"
#             ch += sys.stdin.read(1)
#             code = sys.stdin.read(1)
#             ch += code
#             while code.isnumeric() or code == ";":
#                 code = sys.stdin.read(1)
#                 ch += code
#         if ch in Key.CTRL_C and interrupt:
#             raise KeyboardInterrupt
#         return ch
