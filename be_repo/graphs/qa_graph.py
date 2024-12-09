from configs.database import get_key_database
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph.message import add_messages

import os

keys_db = get_key_database()
keys_collection = keys_db["keys"]
TAVILY_API_KEY = keys_collection.find_one({"_id": "tavily_key"})["api_key"]
LANGSMITH_KEY = keys_collection.find_one({"_id": "langsmith_key"})["api_key"]
OPENAI_KEY = keys_collection.find_one({"_id": "chatgpt_api"})["api_key"]
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "CS673"


class State(TypedDict):
    messages: Annotated[list, add_messages]


def create_graph():
    memory = MemorySaver()

    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_KEY)
    tool = TavilySearchResults(max_results=2)
    tools = [tool]
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    tool_node = ToolNode(tools=[tool])
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")

    return graph_builder.compile(checkpointer=memory)
