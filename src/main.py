"""Entry point."""

print("Starting...")

# pylint: disable=wrong-import-position
import sys
# pylint: enable=wrong-import-position

if len(sys.argv) > 1:
    if any(arg in sys.argv for arg in ["--text", "-t"]):
        from utils import terminal
        print("Add a text input:")
        text: str = terminal.read_text()
        print()
        print("Result:")
        print(text)
        sys.exit()

    if any(arg in sys.argv for arg in ["--list", "-f"]):
        from utils import terminal
        keys = terminal.Key.list()
        keys.sort(key=lambda x: x[1])
        for key in keys:
            print(f"{key[1]}: {key[0]}")
        sys.exit()


    if any(arg in sys.argv for arg in ["--key_press", "-k"]):
        from utils import terminal
        print("Press a key to display its code and name (press 'q' to finish):")
        key = terminal.read_key()
        while key != "q":
            print(f"{terminal.Key.code_of(key)}")
            key = terminal.read_key()
        sys.exit()

    if any(arg in sys.argv for arg in ["--sandbox", "-s"]):
        print("Sandbox")
        sys.exit()

    if any(arg in sys.argv for arg in ["--graph", "-g"]):
        import os
        import workflow
        print("Generating graph...")
        temp = workflow.build()
        absolute_path = os.path.abspath("../docs/graph.png")
        temp.get_graph().draw_mermaid_png(output_file_path=absolute_path)
        print(f"Graph generated at '{absolute_path}'.")
        sys.exit()

if __name__ == "__main__":
    import workflow

    is_debugging = any(arg in sys.argv for arg in ["--debug", "-d"])
    wkf = workflow.build(is_debugging)
    wkf.validate()
    wkf.invoke({}, debug=is_debugging)
