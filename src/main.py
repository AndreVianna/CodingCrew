"""Entry point."""

from ctypes import util
import sys
from langgraph.graph.graph import CompiledGraph
import workflow
import utils

if sys.argv and ["--debug"] != sys.argv and ["-d"] != sys.argv:
    print("Start:")

if "--text" in sys.argv or "-t" in sys.argv:
    TEXT: str = utils.read_text()
    print()
    print("Result:")
    print(TEXT)
    sys.exit()

if "--list" in sys.argv or "-l" in sys.argv:
    keys = utils.KeyMapping.list()
    keys.sort(key=lambda x: x[1])
    for key in keys:
        print(f"{key[1]}: {key[0]}")
    sys.exit()


if "--key" in sys.argv or "-k" in sys.argv:
    key = utils.read_key()
    while key != "q":
        print(f"{utils.Key.code_of(key)}")
        key = utils.read_key()
    sys.exit()

if "--simulate" in sys.argv or "-s" in sys.argv:
    utils.write_raw("dsdfdskfsdkfsdl" + utils.Key.CTRL_ENTER)
    utils.write_raw("fjhknvn" + utils.Key.CTRL_ENTER)
    utils.write_raw("jshdfghg")
    utils.read_key()
    utils.write_raw(utils.Key.CURSOR_LEFT.replace("#n", "5"))
    utils.read_key()
    pos = utils.get_cursor_position()
    print()
    print(pos)
    utils.read_key()
    sys.exit()

is_debugging = "--debug" in sys.argv or "-d" in sys.argv
wkf: CompiledGraph = workflow.build(is_debugging)

if "--graph" in sys.argv or "-g" in sys.argv:
    with open("../docs/graph.png","wb") as image_file:
        image_file.write(wkf.get_graph().draw_mermaid_png())
        sys.exit()

wkf.validate()
wkf.invoke({}, debug=is_debugging)
