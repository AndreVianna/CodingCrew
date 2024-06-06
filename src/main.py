"""Entry point."""

import sys
from langgraph.graph.graph import CompiledGraph
import workflow
import utils

if sys.argv and ["--debug"] != sys.argv and ["-d"] != sys.argv:
    print("Start:")

if "--txt" in sys.argv or "-t" in sys.argv:
    TEXT: str = utils.read_text()
    print()
    print("Result:")
    print(TEXT)
    sys.exit()

if "--keys" in sys.argv or "-k" in sys.argv:
    keys = utils.KeyMapping.list()
    keys.sort(key=lambda x: x[1])
    for key in keys:
        print(f"{key[1]}: {key[0]}")
    sys.exit()

is_debugging = "--debug" in sys.argv or "-d" in sys.argv
wkf: CompiledGraph = workflow.build(is_debugging)

if "--graph" in sys.argv or "-g" in sys.argv:
    with open("../docs/graph.png","wb") as image_file:
        image_file.write(wkf.get_graph().draw_mermaid_png())
        sys.exit()

wkf.validate()
wkf.invoke({}, debug=is_debugging)
