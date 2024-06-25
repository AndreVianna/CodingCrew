print("Starting...")

import sys                                      # pylint: disable=wrong-import-position
from utils.terminal import terminal             # pylint: disable=wrong-import-position

# pylint: disable-next=missing-function-docstring
# async def main():
if sys.platform not in ["linux", "win32"]:
    print(f"The '{sys.platform}' is not supported.")
    sys.exit(1)
if sys.version_info < (3, 11) or sys.version_info > (3, 12):
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
        import os        # pylint: disable=import-outside-toplevel
        import workflow  # pylint: disable=import-outside-toplevel

        print("Generating graph...")
        temp = workflow.build()
        absolute_path = os.path.abspath("../docs/graph.png")
        temp.get_graph().draw_mermaid_png(output_file_path=absolute_path)
        print(f"Graph generated at '{absolute_path}'.")
        sys.exit()

if __name__ == "__main__":
    from models.project_state import ProjectState   # pylint: disable=import-outside-toplevel
    from utils.common import is_verbose            # pylint: disable=import-outside-toplevel, ungrouped-imports
    import workflow                                 # pylint: disable=import-outside-toplevel, ungrouped-imports

    terminal.write_line("Building workflow...")
    wkf = workflow.build(is_verbose)
    terminal.write_line("Validating workflow...")
    wkf.validate()
    terminal.write_line("Executing workflow...")
    state=ProjectState()
    result = wkf.invoke(input=state, debug=is_verbose)
    terminal.write_line("Workflow completed.")
    terminal.write_line("Result:")
    terminal.write_line(result)


# asyncio.run(main(), debug=is_verbose)
