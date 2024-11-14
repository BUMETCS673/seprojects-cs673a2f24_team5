from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph.message import add_messages

TAVILY_API_KEY = ''
OPENAI_KEY = ''


class State(TypedDict):
    messages: Annotated[list, add_messages]


def create_graph(api_key_openai=OPENAI_KEY, api_key_tavily=TAVILY_API_KEY):
    memory = MemorySaver()

    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key_openai)
    tool = TavilySearchResults(max_results=2, tavily_api_key=api_key_tavily)
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
