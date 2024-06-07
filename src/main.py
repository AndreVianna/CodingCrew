"""Entry point."""

import sys
from langgraph.graph.graph import CompiledGraph
import workflow
import utils.terminal as terminal

if sys.argv and ["--debug"] != sys.argv and ["-d"] != sys.argv:
    print("Start:")

if "--text" in sys.argv or "-t" in sys.argv:
    TEXT: str = terminal.read_text()
    print()
    print("Result:")
    print(TEXT)
    sys.exit()

if "--list" in sys.argv or "-l" in sys.argv:
    keys = terminal.Key.list()
    keys.sort(key=lambda x: x[1])
    for key in keys:
        print(f"{key[1]}: {key[0]}")
    sys.exit()


if "--key" in sys.argv or "-k" in sys.argv:
    key = terminal.read_key()
    while key != "q":
        print(f"{terminal.Key.code_of(key)}")
        key = terminal.read_key()
    sys.exit()

if "--simulate" in sys.argv or "-s" in sys.argv:
    terminal.read_text()
    sys.exit()

is_debugging = "--debug" in sys.argv or "-d" in sys.argv
wkf: CompiledGraph = workflow.build(is_debugging)

if "--graph" in sys.argv or "-g" in sys.argv:
    with open("../docs/graph.png", "wb") as image_file:
        image_file.write(wkf.get_graph().draw_mermaid_png())
        sys.exit()

wkf.validate()
wkf.invoke({}, debug=is_debugging)
