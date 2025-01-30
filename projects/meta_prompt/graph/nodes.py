import yaml
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.types import StreamWriter
from pydantic import BaseModel
from typing import List

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")
TEMPERATURE = os.getenv("TEMPERATURE")

# * information gather

with open("./prompts/gather.yaml", "r") as f:
    gather_template = yaml.safe_load(f)

gather_prompt = ChatPromptTemplate.from_messages(
    [
        (gather_template["role"], gather_template["template"]),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


class PromptInstructions(BaseModel):
    """Instructions on how to prompt the LLM."""

    objective: str
    variables: List[str]
    constraints: List[str]
    requirements: List[str]


llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)
llm_with_tool = llm.bind_tools([PromptInstructions])

gather_chain = gather_prompt | llm_with_tool


async def information_gather(state, writer: StreamWriter):
    """사용자와 상호작용하며 필요한 요구 사항을 수집하는 노드"""
    print("--- [Information_gather] ---")
    messages = state["messages"]
    print(messages)
    response = []
    tool_calls = None

    first = True
    async for chunk in gather_chain.astream({"messages": messages}):
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
        return {"messages": [response]}
    else:
        return {"messages": [tool_calls]}


# * generate prompt
with open("./prompts/generate_prompt.yaml", "r") as f:
    generate_template = yaml.safe_load(f)


def get_prompt_messages(messages: list):
    tool_call = None
    other_messages = []

    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            tool_call = msg.tool_calls[0]["args"]
        elif isinstance(msg, ToolMessage):
            continue
        # tool call 이후의 메세지 추가 (추가적인 대화 내용)
        elif tool_call is not None:
            other_messages.append(msg)
    return [
        SystemMessage(
            content=generate_template["template"].format(requirements=tool_call)
        )
    ] + other_messages


async def generate_prompt(state, writer: StreamWriter):
    print("--- [GENERATE PROMPT] ---")
    messages = get_prompt_messages(state["messages"])
    print(messages)
    response = []
    async for chunk in llm.astream(messages):
        response.append(chunk.content)
        # print(chunk)
        # print("---")
        writer(chunk.content)

    return {"messages": [AIMessage(content="".join(response))]}


# * add_tool_message 노드 정의
def add_tool_message(state):
    return {
        "messages": [
            ToolMessage(
                content="prompt 생성 완료!",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"],
            )
        ]
    }


if __name__ == "__main__":
    print(
        gather_chain.invoke(
            {"messages": [("user", "안녕하세요, 프롬프트 만들어주세요.")]}
        ).content
    )
