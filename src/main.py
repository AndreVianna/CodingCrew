"""Entry point."""

import sys
from workflows.workflow import PlaningWorkflow

app = PlaningWorkflow().app

if '--graph' in sys.argv or '-g' in sys.argv:
    with open("../docs/graph.png","wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
        sys.exit()

if '--debug' in sys.argv or '-d' in sys.argv:
    app.invoke({}, debug=True)
    sys.exit()

app.invoke({})
