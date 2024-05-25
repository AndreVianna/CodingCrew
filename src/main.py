"""Entry point."""

import sys
from workflows.email_workflow import WorkFlow

app = WorkFlow().app

if '--graph' in sys.argv or '-g' in sys.argv:
    with open("../docs/graph.png","wb") as f:
        f.write(app.get_graph().draw_png())
        sys.exit()

app.invoke({})
