from typing_extensions import TypedDict, Literal, Optional
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

class State(TypedDict):
    graph_state: str
    number: int

def node_1(state):
    print("--node_1--")
    return {"graph_state": state["graph_state"] + "I"}

def node_2(state):
    print("--node_1--")
    return {"graph_state": state["graph_state"] + "love"}

def node_3(state):
    print("--node_1--")
    return {"graph_state": state["graph_state"] + "Python!"}

def node_change(state: State) -> Literal["node_2", "node_3"]:

    user_input = state["number"]

    if user_input % 2:
        "node_2"
    else:
        "node_3"


builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", node_change)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()

#display(Image(graph.get_graph().draw_mermaid_png()))

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

from PIL import Image
img = Image.open('graph.png')
img.show()