print("Starting...")

# pylint: disable=wrong-import-position
import sys
import pretty_errors

from utils import terminal
# pylint: enable=wrong-import-position

pretty_errors.configure(
    name = "coding-crew",
    #always_display_bottom     = True,
    #arrow_head_character      = '^',
    #arrow_tail_character      = '-',
    #display_arrow             = True,
    display_link              = True,
    display_locals            = True,
    #display_timestamp         = False,
    display_trace_locals      = True,
    #exception_above           = False,
    #exception_below           = True,
    #filename_display          = pretty_errors.FILENAME_COMPACT,  # FILENAME_EXTENDED | FILENAME_FULL,
    #full_line_newline         = False,
    #infix                     = None,
    #inner_exception_message   = None,
    #inner_exception_separator = False,
    #line_length               = 0,
    #line_number_first         = True,
    lines_after               = 2,
    lines_before              = 5,
    #postfix                   = None,
    #prefix                    = None,
    #reset_stdout              = False,
    #separator_character       = '-',
    #show_suppressed           = False,
    #stack_depth               = 0,
    #timestamp_function        = time.perf_counter,
    #top_first                 = False,
    trace_lines_after         = 2,
    trace_lines_before        = 1,
    #truncate_code             = False,
    #truncate_locals           = True,
    #arrow_head_color          = '\x1b[1;32m',
    #arrow_tail_color          = '\x1b[1;32m',
    #code_color                = '\x1b[1;30m',
    #exception_arg_color       = '\x1b[1;33m',
    #exception_color           = '\x1b[1;31m',
    #exception_file_color      = '\x1b[1;35m',
    #filename_color            = '\x1b[1;36m',
    #function_color            = '\x1b[1;34m',
    #header_color              = '\x1b[1;30m',
    #line_color                = '\x1b[1;37m',
    #line_number_color         = '\x1b[1;32m',
    #link_color                = '\x1b[1;30m',
    #local_len_color           = '\x1b[1;30m',
    #local_name_color          = '\x1b[1;35m',
    #local_value_color         = '\x1b[m',
    #syntax_error_color        = '\x1b[1;32m',
    #timestamp_color           = '\x1b[1;30m',
)

if sys.platform not in ["linux", "win32"]:
    print(f"The '{sys.platform}' is not supported.")
    sys.exit(1)
if sys.version_info < (3, 12) or sys.version_info >= (3, 13):
    print(f"This applicaiton requires Python 3.11+. Found: {sys.version}.")
    sys.exit(1)

if len(sys.argv) > 1:
    if any(arg in sys.argv for arg in ["-t"]):
        print("Add a text input:")
        text: str = terminal.read_text()
        print()
        print("Result:")
        print(text)
        sys.exit()

    if any(arg in sys.argv for arg in ["-l"]):
        keys = terminal.Key.list()
        keys.sort(key=lambda x: x[1])
        for key in keys:
            print(f"{key[1]}: {key[0]}")
        sys.exit()

    if any(arg in sys.argv for arg in ["-k"]):
        print("Press a key to display its code and name (press 'q' to finish):")
        key = terminal.read_key()
        while key != "q":
            print(f"{terminal.Key.code_of(key)}")
            key = terminal.read_key()
        sys.exit()

    if any(arg in sys.argv for arg in ["-s"]):
        sys.exit()

    if any(arg in sys.argv for arg in ["-g"]):
        # pylint: disable=import-outside-toplevel, ungrouped-imports
        import os
        import workflow
        # pylint: enable=import-outside-toplevel, ungrouped-imports

        print("Generating graph...")
        temp = workflow.build()
        absolute_path = os.path.abspath("../docs/graph.png")
        temp.get_graph().draw_mermaid_png(output_file_path=absolute_path)
        print(f"Graph generated at '{absolute_path}'.")
        sys.exit()

if __name__ == "__main__":
    # pylint: disable=import-outside-toplevel, ungrouped-imports
    import os
    import workflow
    from utils.common import is_win32, is_verbose
    from states import BaseState
    from langchain.globals import set_debug
    # pylint: enable=import-outside-toplevel, ungrouped-imports
    set_debug(is_verbose)
    terminal.write_line("Building workflow...")
    wkf = workflow.build(is_verbose)
    terminal.write_line("Validating workflow...")
    wkf.validate()
    terminal.write_line("Executing workflow...")
    workspace: str = os.path.expanduser( os.environ["WORKSPACE_FOLDER"].replace("~", "$HOMEPATH").replace("/", "\\")) if is_win32 else \
                     os.path.expanduser( os.environ["WORKSPACE_FOLDER"].replace("$HOMEPATH", "~").replace("\\", "/"))
    state=BaseState(workspace=workspace)
    result = wkf.invoke(input=state, debug=is_verbose)
    terminal.write_line()
    terminal.write_line("Workflow completed.", "green")
