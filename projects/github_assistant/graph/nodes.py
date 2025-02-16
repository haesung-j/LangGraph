from abc import ABC, abstractmethod
from langgraph.prebuilt import ToolNode
from langgraph.types import StreamWriter
from langchain_core.messages import AIMessage

from graph.chains import create_summary_chain
from graph.state import State
from graph.tools import get_directory_structure, get_file_contents


class BaseNode(ABC):
    def __init__(self, **kwargs):
        self.name = "BaseNode"
        self.verbose = False
        if "verbose" in kwargs:
            self.verbose = kwargs["verbose"]

    @abstractmethod
    def run(self, state: State):
        pass

    def logging(self, method_name, **kwargs):
        if self.verbose:
            print(f"[{self.name}] {method_name}")
            for k, v in kwargs.items():
                print(f"    {k}: {v}")

    def __call__(self, state: State):
        return self.run(state)


class SummaryNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "SummaryNode"
        self.chain = create_summary_chain()

    def run(self, state: State):

        messages = state["messages"]
        response = self.chain.invoke({"messages": messages})
        return {"messages": [response]}


def summary_node(state: State, writer: StreamWriter):
    chain = create_summary_chain()
    messages = state["messages"]

    response = []
    tool_calls = None

    first = True
    for chunk in chain.stream({"messages": messages}):
        if chunk.tool_call_chunks:
            if first:
                tool_calls = chunk
                first = False
            else:
                tool_calls += chunk
        elif chunk.content:
            response.append(chunk.content)
            writer(chunk.content)
        else:
            continue
    if response:
        response = AIMessage(content="".join(response))
        if tool_calls:
            response.tool_calls = tool_calls.tool_calls
        return {"messages": [response]}
    else:
        return {"messages": [tool_calls]}


class SummaryToolNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "SummaryToolNode"
        self.tools = [get_directory_structure, get_file_contents]

    def run(self, state: State):
        return ToolNode(tools=self.tools)
