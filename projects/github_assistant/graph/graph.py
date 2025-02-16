from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver

from graph.nodes import summary_node, SummaryToolNode

# from graph.nodes import SummaryNode, SummaryToolNode
from graph.state import State


def create_summary_agent():
    flow = StateGraph(State)
    flow.add_node("agent", summary_node)
    # flow.add_node("agent", SummaryNode())
    flow.add_node("tool_node", SummaryToolNode())

    flow.add_edge(START, "agent")
    flow.add_edge("tool_node", "agent")
    flow.add_conditional_edges(
        "agent",
        tools_condition,
        {"tools": "tool_node", "__end__": END},
    )

    memory = MemorySaver()
    graph = flow.compile(checkpointer=memory)
    return graph


if __name__ == "__main__":
    graph = create_summary_agent()
    config = {"recursion_limit": 10, "configurable": {"thread_id": "abc"}}

    inputs = {
        "messages": [
            (
                "user",
                "/home/sean/PythonProject/langgraph/langgraph/projects/meta_prompt 입니다",
            )
        ]
    }

    # stream_graph(graph, inputs, config)

    # for event in graph.stream(
    #     input=inputs,
    #     config=config,
    #     stream_mode="values",  # 각 노드의 출력 상태
    #     # interrupt_before=["tool_node"],  # tool_node로 가기 전에 멈추기!
    # ):
    #     for key, value in event.items():
    #         print(f"\n[ {key} ]\n")

    #         print(value[-1].pretty_print())

    for chunk, metadata in graph.stream(
        input=inputs,
        config=config,
        stream_mode="messages",  # 각 노드의 출력 상태
        # interrupt_before=["tool_node"],  # tool_node로 가기 전에 멈추기!
    ):
        if chunk.content:
            print(chunk.content, end="", flush=True)
