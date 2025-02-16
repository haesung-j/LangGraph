from langchain_openai import ChatOpenAI
from langchain_core.prompts import load_prompt, ChatPromptTemplate, MessagesPlaceholder

from graph.tools import get_directory_structure, get_file_contents


def create_summary_chain():
    system_prompt = load_prompt("prompts/summary_prompt.yaml")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt.template),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    tools = [get_directory_structure, get_file_contents]

    llm = llm.bind_tools(tools)

    chain = prompt | llm
    return chain
