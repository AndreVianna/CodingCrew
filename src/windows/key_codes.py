# """
# Tools that helps reading the console input from the user in Windows.
# """

# import os
# if os.name == "nt":
#     import msvcrt
#     import sys
#     from enum import IntEnum
#     from typing import Literal, Iterable

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

#         CTRL_A:         Literal["\x01"] = "\x01"
#         CTRL_B:         Literal["\x02"] = "\x02"
#         CTRL_C:         Literal["\x03"] = "\x03"
#         CTRL_D:         Literal["\x04"] = "\x04"
#         CTRL_E:         Literal["\x05"] = "\x05"
#         CTRL_F:         Literal["\x06"] = "\x06"
#         CTRL_G:         Literal["\x07"] = "\x07"
#         CTRL_H:         Literal["\x08"] = "\x08"
#         BACKSPACE:      Literal["\x08"] = "\x08"
#         CTRL_I:         Literal["\x09"] = "\x09"
#         TAB:            Literal["\x09"] = "\x09"
#         CTRL_J:         Literal["\x0a"] = "\x0a"
#         CTRL_ENTER:     Literal["\x0a"] = "\x0a"
#         CTRL_K:         Literal["\x0b"] = "\x0b"
#         CTRL_L:         Literal["\x0c"] = "\x0c"
#         CTRL_M:         Literal["\x0d"] = "\x0d"
#         ENTER:          Literal["\x0d"] = "\x0d"
#         CTRL_N:         Literal["\x0e"] = "\x0e"
#         CTRL_O:         Literal["\x0f"] = "\x0f"
#         CTRL_P:         Literal["\x10"] = "\x10"
#         CTRL_Q:         Literal["\x11"] = "\x11"
#         CTRL_R:         Literal["\x12"] = "\x12"
#         CTRL_S:         Literal["\x13"] = "\x13"
#         CTRL_T:         Literal["\x14"] = "\x14"
#         CTRL_U:         Literal["\x15"] = "\x15"
#         CTRL_V:         Literal["\x16"] = "\x16"
#         CTRL_W:         Literal["\x17"] = "\x17"
#         CTRL_X:         Literal["\x18"] = "\x18"
#         CTRL_Y:         Literal["\x19"] = "\x19"
#         CTRL_Z:         Literal["\x1a"] = "\x1a"
#         ESC:            Literal["\x1b"] = "\x1b"

#         CTRL_0:         Literal["Undefined"] = "Undefined"
#         CTRL_1:         Literal["Undefined"] = "Undefined"
#         CTRL_2:         Literal["^\x03"] = "^\x03"
#         CTRL_3:         Literal["Undefined"] = "Undefined"
#         CTRL_4:         Literal["Undefined"] = "Undefined"
#         CTRL_5:         Literal["Undefined"] = "Undefined"
#         CTRL_6:         Literal["Undefined"] = "Undefined"
#         CTRL_7:         Literal["Undefined"] = "Undefined"
#         CTRL_8:         Literal["Undefined"] = "Undefined"
#         CTRL_9:         Literal["Undefined"] = "Undefined"

#         CTRL_BACKSPACE: Literal["\x7f"] = "\x7f"

#         PRNT_SCR:       Literal["^\x37"] = "^\x37"
#         F1:             Literal["^\x3b"] = "^\x3b"
#         F2:             Literal["^\x3c"] = "^\x3c"
#         F3:             Literal["^\x3d"] = "^\x3d"
#         F4:             Literal["^\x3e"] = "^\x3e"
#         F5:             Literal["^\x3f"] = "^\x3f"
#         F6:             Literal["^\x40"] = "^\x40"
#         F7:             Literal["^\x41"] = "^\x41"
#         F8:             Literal["^\x42"] = "^\x42"
#         F9:             Literal["^\x43"] = "^\x43"
#         F10:            Literal["^\x44"] = "^\x44"
#         HOME:           Literal["^\x47"] = "^\x47"
#         UP:             Literal["^\x48"] = "^\x48"
#         PAGE_UP:        Literal["^\x49"] = "^\x49"
#         LEFT:           Literal["^\x4b"] = "^\x4b"
#         NUM_PAD_5:      Literal["^\x4c"] = "^\x4c"
#         RIGHT:          Literal["^\x4d"] = "^\x4d"
#         END:            Literal["^\x4f"] = "^\x4f"
#         DOWN:           Literal["^\x50"] = "^\x50"
#         PAGE_DOWN:      Literal["^\x51"] = "^\x51"
#         INS:            Literal["^\x52"] = "^\x52"
#         DEL:            Literal["^\x53"] = "^\x53"
#         SHIFT_F1:       Literal["^\x54"] = "^\x54"
#         SHIFT_F2:       Literal["^\x55"] = "^\x55"
#         SHIFT_F3:       Literal["^\x56"] = "^\x56"
#         SHIFT_F4:       Literal["^\x57"] = "^\x57"
#         SHIFT_F5:       Literal["^\x58"] = "^\x58"
#         SHIFT_F6:       Literal["^\x59"] = "^\x59"
#         SHIFT_F7:       Literal["^\x5a"] = "^\x5a"
#         SHIFT_F8:       Literal["^\x5b"] = "^\x5b"
#         SHIFT_F9:       Literal["^\x5c"] = "^\x5c"
#         SHIFT_F10:      Literal["^\x5d"] = "^\x5d"
#         CTRL_F1:        Literal["^\x5e"] = "^\x5e"
#         CTRL_F2:        Literal["^\x5f"] = "^\x5f"
#         CTRL_F3:        Literal["^\x60"] = "^\x60"
#         CTRL_F4:        Literal["^\x61"] = "^\x61"
#         CTRL_F5:        Literal["^\x62"] = "^\x62"
#         CTRL_F6:        Literal["^\x63"] = "^\x63"
#         CTRL_F7:        Literal["^\x64"] = "^\x64"
#         CTRL_F8:        Literal["^\x65"] = "^\x65"
#         CTRL_F9:        Literal["^\x66"] = "^\x66"
#         CTRL_F10:       Literal["^\x67"] = "^\x67"
#         ALT_F1:         Literal["^\x68"] = "^\x68"
#         ALT_F2:         Literal["^\x69"] = "^\x69"
#         ALT_F3:         Literal["^\x6a"] = "^\x6a"
#         ALT_F4:         Literal["^\x6b"] = "^\x6b"
#         ALT_F5:         Literal["^\x6c"] = "^\x6c"
#         ALT_F6:         Literal["^\x6d"] = "^\x6d"
#         ALT_F7:         Literal["^\x6e"] = "^\x6e"
#         ALT_F8:         Literal["^\x6f"] = "^\x6f"
#         ALT_F9:         Literal["^\x70"] = "^\x70"
#         ALT_F10:        Literal["^\x71"] = "^\x71"
#         CTRL_PRNT_SCR:  Literal["^\x72"] = "^\x72"
#         CTRL_LEFT:      Literal["^\x73"] = "^\x73"
#         CTRL_RIGHT:     Literal["^\x74"] = "^\x74"
#         CTRL_END:       Literal["^\x75"] = "^\x75"
#         CTRL_PAGE_DOWN: Literal["^\x76"] = "^\x76"
#         CTRL_HOME:      Literal["^\x77"] = "^\x77"

#         ALT_1:          Literal["^\x78"] = "^\x78"
#         ALT_2:          Literal["^\x79"] = "^\x79"
#         ALT_3:          Literal["^\x7a"] = "^\x7a"
#         ALT_4:          Literal["^\x7b"] = "^\x7b"
#         ALT_5:          Literal["^\x7c"] = "^\x7c"
#         ALT_6:          Literal["^\x7d"] = "^\x7d"
#         ALT_7:          Literal["^\x7e"] = "^\x7e"
#         ALT_8:          Literal["^\x7f"] = "^\x7f"
#         ALT_9:          Literal["^\x80"] = "^\x80"
#         ALT_0:          Literal["^\x81"] = "^\x81"
#         ALT_MINUS:      Literal["^\x82"] = "^\x82"
#         ALT_EQUALS:     Literal["^\x83"] = "^\x83"

#         CTRL_PAGE_UP:   Literal["^\x84"] = "^\x84"
#         F11:            Literal["^\x85"] = "^\x85"
#         F12:            Literal["^\x86"] = "^\x86"
#         SHIFT_F11:      Literal["^\x87"] = "^\x87"
#         SHIFT_F12:      Literal["^\x88"] = "^\x88"
#         CTRL_F11:       Literal["^\x89"] = "^\x89"
#         CTRL_F12:       Literal["^\x8a"] = "^\x8a"
#         ALT_F11:        Literal["^\x8b"] = "^\x8b"
#         ALT_F12:        Literal["^\x8c"] = "^\x8c"
#         CTRL_UP:        Literal["^\x8d"] = "^\x8d"
#         CTRL_MINUS:     Literal["^\x8e"] = "^\x8e"
#         CTRL_5:         Literal["^\x8f"] = "^\x8f"
#         CTRL_PLUS:      Literal["^\x90"] = "^\x90"
#         CTRL_DOWN:      Literal["^\x91"] = "^\x91"
#         CTRL_INS:       Literal["^\x92"] = "^\x92"
#         CTRL_DEL:       Literal["^\x93"] = "^\x93"
#         CTRL_TAB:       Literal["^\x94"] = "^\x94"
#         CTRL_SLASH:     Literal["^\x95"] = "^\x95"
#         CTRL_START:     Literal["^\x96"] = "^\x96"
#         ALT_HOME:       Literal["^\x97"] = "^\x97"
#         ALT_UP:         Literal["^\x98"] = "^\x98"
#         ALT_PAGE_UP:    Literal["^\x99"] = "^\x99"
#         ALT_LEFT:       Literal["^\x9b"] = "^\x9b"
#         ALT_RIGHT:      Literal["^\x9d"] = "^\x9d"
#         ALT_END:        Literal["^\x9f"] = "^\x9f"
#         ALT_DOWN:       Literal["^\xa0"] = "^\xa0"
#         ALT_PAGE_DOWN:  Literal["^\xa1"] = "^\xa1"
#         ALT_INS:        Literal["^\xa2"] = "^\xa2"
#         ALT_DEL:        Literal["^\xa3"] = "^\xa3"
#         ALT_SLASH:      Literal["^\xa4"] = "^\xa4"
#         ALT_TAB:        Literal["^\xa5"] = "^\xa5"
#         ALT_ENTER:      Literal["^\xa6"] = "^\xa6"

#         __key_names: dict[str, str] = {
#             NUM_PAD_5: "NUMERIC PAD 5",
#             UP: "UP",
#             ALT_UP: "ALT UP",
#             CTRL_UP: "CTRL UP",
#             DOWN: "DOWN",
#             ALT_DOWN: "ALT DOWN",
#             CTRL_DOWN: "CTRL DOWN",
#             RIGHT: "RIGHT",
#             ALT_RIGHT: "ALT RIGHT",
#             CTRL_RIGHT: "CTRL RIGHT",
#             LEFT: "LEFT",
#             ALT_LEFT: "ALT LEFT",
#             CTRL_LEFT: "CTRL LEFT",
#             END: "END",
#             ALT_END: "ALT END",
#             CTRL_END: "CTRL END",
#             HOME: "HOME",
#             ALT_HOME: "ALT HOME",
#             CTRL_HOME: "CTRL HOME",
#             INS: "INSERT",
#             ALT_INS: "ALT INSERT",
#             CTRL_INS: "CTRL INSERT",
#             DEL: "DEL",
#             ALT_DEL: "ALT DEL",
#             CTRL_DEL: "CTRL DEL",
#             PAGE_UP: "PAGE UP",
#             ALT_PAGE_UP: "ALT PAGE UP",
#             CTRL_PAGE_UP: "CTRL PAGE UP",
#             PAGE_DOWN: "PAGE DOWN",
#             ALT_PAGE_DOWN: "ALT PAGE DOWN",
#             CTRL_PAGE_DOWN: "CTRL PAGE DOWN",
#             F1: "F1",
#             SHIFT_F1: "SHIFT F1",
#             ALT_F1: "ALT F1",
#             CTRL_F1: "CTRL F1",
#             F2: "F2",
#             SHIFT_F2: "SHIFT F2",
#             ALT_F2: "ALT F2",
#             CTRL_F2: "CTRL F2",
#             F3: "F3",
#             SHIFT_F3: "SHIFT F3",
#             ALT_F3: "ALT F3",
#             CTRL_F3: "CTRL F3",
#             F4: "F4",
#             SHIFT_F4: "SHIFT F4",
#             ALT_F4: "ALT F4",
#             CTRL_F4: "CTRL F4",
#             F5: "F5",
#             SHIFT_F5: "SHIFT F5",
#             ALT_F5: "ALT F5",
#             CTRL_F5: "CTRL F5",
#             F6: "F6",
#             SHIFT_F6: "SHIFT F6",
#             ALT_F6: "ALT F6",
#             CTRL_F6: "CTRL F6",
#             F7: "F7",
#             SHIFT_F7: "SHIFT F7",
#             ALT_F7: "ALT F7",
#             CTRL_F7: "CTRL F7",
#             F8: "F8",
#             SHIFT_F8: "SHIFT F8",
#             ALT_F8: "ALT F8",
#             CTRL_F8: "CTRL F8",
#             F9: "F9",
#             SHIFT_F9: "SHIFT F9",
#             ALT_F9: "ALT F9",
#             CTRL_F9: "CTRL F9",
#             F10: "F10",
#             SHIFT_F10: "SHIFT F10",
#             ALT_F10: "ALT F10",
#             CTRL_F10: "CTRL F10",
#             F11: "F11",
#             SHIFT_F11: "SHIFT F11",
#             ALT_F11: "ALT F11",
#             CTRL_F11: "CTRL F11",
#             F12: "F12",
#             SHIFT_F12: "SHIFT F12",
#             ALT_F12: "ALT F12",
#             CTRL_F12: "CTRL F12",
#             BACKSPACE: "BACKSPACE",
#             TAB: "TAB",
#             ENTER: "ENTER",
#             ESC: "ESC",
#             CTRL_PLUS: "CTRL +",
#             CTRL_MINUS: "CTRL -",
#             CTRL_SLASH: "CTRL /",
#             CTRL_START: "CTRL *",
#             ALT_MINUS: "ALT -",
#             ALT_EQUALS: "ALT =",
#             ALT_SLASH: "ALT /",
#             ALT_TAB: "ALT TAB",
#             ALT_ENTER: "ALT ENTER",
#             PRNT_SCR: "PRINT SCREEN",
#             CTRL_PRNT_SCR: "CTRL PRINT SCREEN",
#             CTRL_BACKSPACE: "CTRL BACKSPACE",
#             CTRL_TAB: "CTRL TAB",
#             CTRL_ENTER: "CTRL ENTER",
#             CTRL_A: "CTRL A",
#             CTRL_B: "CTRL B",
#             CTRL_C: "CTRL C",
#             CTRL_D: "CTRL D",
#             CTRL_E: "CTRL E",
#             CTRL_F: "CTRL F",
#             CTRL_G: "CTRL G",
#             CTRL_H: "BACKSPACE",
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
#             ALT_0: "ALT 0",
#             ALT_1: "ALT 1",
#             ALT_2: "ALT 2",
#             ALT_3: "ALT 3",
#             ALT_4: "ALT 4",
#             ALT_5: "ALT 5",
#             ALT_6: "ALT 6",
#             ALT_7: "ALT 7",
#             ALT_8: "ALT 8",
#             ALT_9: "ALT 9",
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
#         If one of the exit keys is pressed it ends a line AND finishes the input (default: [ CTRL+ENTER ]).

#         Args:
#             interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
#             linebreak_keys (Iterable[str]): The keys that will end a line.
#             exit_keys (Iterable[str]): The keys that will finish the input.

#         Returns:
#             list[str]: The lines entered by the user.
#         """
#         linebreak_keys = linebreak_keys if linebreak_keys else [Key.ENTER]
#         exit_keys = exit_keys if exit_keys else [Key.CTRL_ENTER]
#         multiline = list[str]()
#         line = ""
#         key = read_key(interrupt)
#         while key not in exit_keys:
#             # TODO: Handle special keys
#             if key in linebreak_keys:
#                 multiline.append(line)
#                 line = ""
#             else:
#                 line += key
#             print(key, end="", flush=True)
#             key = read_key(interrupt)
#         multiline.append(line)
#         print(flush=True)

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
#         If one of the exit keys is pressed it finishes the input (default: [ ENTER, CTRL+ENTER ]).

#         Args:
#             interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).
#             exit_keys (Iterable[str]): The keys that will finish the input.

#         Returns:
#             str: The line entered by the user.
#         """
#         exit_keys = exit_keys if exit_keys else [Key.ENTER, Key.CTRL_ENTER]
#         line = ""
#         key = read_key(interrupt)
#         while key not in exit_keys:
#             # TODO: Handle speacil keys (left and right only)
#             line += key
#             print(key, end="", flush=True)
#             key = read_key(interrupt)

#         return line.strip() if trim_line else line

#     def read_key(interrupt: bool = True) -> str:
#         """
#         Reads a single key press from the user.

#         Args:
#             interrupt (bool): If set to True raises a KeyboardInterrupt when CTRL+C is presses (default: True).

#         Returns:
#             str: The key pressed by the user.
#         """
#         ch = msvcrt.getwch()
#         if ord(ch) in (0, 224) :
#             code = msvcrt.getwch()
#             ch = f"^{code}"
#         if ch == Key.CTRL_C and interrupt:
#             raise KeyboardInterrupt
#         return ch
