"""Entry point."""

import sys

import utils
if "--dev" in sys.argv:
    text = utils.read_lines()
    print()
    print()
    print(text)
    sys.exit()

from langgraph.graph.graph import CompiledGraph
import workflow

is_debugging = "--debug" in sys.argv or "-d" in sys.argv
wkf: CompiledGraph = workflow.build(is_debugging)

if "--graph" in sys.argv or "-g" in sys.argv:
    with open("../docs/graph.png","wb") as image_file:
        image_file.write(wkf.get_graph().draw_mermaid_png())
        sys.exit()

wkf.validate()
wkf.invoke({}, debug=is_debugging)
