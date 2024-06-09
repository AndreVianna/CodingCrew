"""Entry point."""

import sys
from langgraph.graph.graph import CompiledGraph
import workflow
import os
import utils.terminal as terminal

if len(sys.argv) > 1:
    print("Start:")

    if any(arg in sys.argv for arg in ["--text", "-t"]):
        print("Add a text input:")
        text: str = terminal.read_text()
        print()
        print("Result:")
        print(text)
        sys.exit()

    if any(arg in sys.argv for arg in ["--list", "-f"]):
        keys = terminal.Key.list()
        keys.sort(key=lambda x: x[1])
        for key in keys:
            print(f"{key[1]}: {key[0]}")
        sys.exit()


    if any(arg in sys.argv for arg in ["--key_press", "-k"]):
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
        print("Generating graph...")
        temp: CompiledGraph = workflow.build()
        absolute_path = os.path.abspath("../docs/graph.png")
        temp.get_graph().draw_mermaid_png(output_file_path=absolute_path)
        print(f"Graph generated at '{absolute_path}'.")
        sys.exit()

is_debugging = any(arg in sys.argv for arg in ["--debug", "-d"])
wkf: CompiledGraph = workflow.build(is_debugging)
wkf.validate()
wkf.invoke({}, debug=is_debugging)
