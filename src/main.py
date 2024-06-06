"""Entry point."""

import sys
from langgraph.graph.graph import CompiledGraph
import workflow

import utils
if "--dev" in sys.argv:
    print("Start:")
    TEXT: str = utils.read_text()
    print()
    print("Result:")
    print(TEXT)
    sys.exit()

is_debugging = "--debug" in sys.argv or "-d" in sys.argv
wkf: CompiledGraph = workflow.build(is_debugging)

if "--graph" in sys.argv or "-g" in sys.argv:
    with open("../docs/graph.png","wb") as image_file:
        image_file.write(wkf.get_graph().draw_mermaid_png())
        sys.exit()

wkf.validate()
wkf.invoke({}, debug=is_debugging)
