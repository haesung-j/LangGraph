from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict

from graph.nodes import information_gather, generate_prompt, add_tool_message
from graph.edges import get_state


class State(TypedDict):
    messages: Annotated[list, add_messages]


memory = MemorySaver()

flow = StateGraph(State)
flow.add_node("information_gather", information_gather)
flow.add_node("generate_prompt", generate_prompt)
flow.add_node("add_tool_message", add_tool_message)

flow.add_edge(START, "information_gather")
flow.add_conditional_edges(
    "information_gather",
    get_state,
    {
        "add_tool_message": "add_tool_message",
        END: END,
    },
)
flow.add_edge("add_tool_message", "generate_prompt")
flow.add_edge("generate_prompt", END)


graph = flow.compile(checkpointer=memory)


graph.get_graph().draw_mermaid_png(output_file_path="./graph.png")
