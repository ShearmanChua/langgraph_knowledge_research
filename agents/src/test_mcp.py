from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

import json

import asyncio
import os
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register

from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import ToolNode

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://research-phoenix-1:6006/v1/traces"

tracer_provider = register(endpoint="http://research-phoenix-1:6006/v1/traces", project_name="mcp-test")
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

base_model = ChatOpenAI(model="gpt-4.1")

async def get_mcp_tools():
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "http",
                "url": "http://research-mcp-server-1:8000/mcp",
            }
        }
    )
    tools = await client.get_tools()
    return tools

async def call_model(state: MessagesState):
    tools = await get_mcp_tools()
    model = base_model.bind_tools(tools)
    system_message = SystemMessage(
        content="You are a helpful assistant that performs web search and summarize the search results to answer the user."
    )
    response = model.invoke([system_message] + state["messages"])
    return {"messages": response}

async def main():
    tools = await get_mcp_tools()

    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    response = await graph.ainvoke({"messages": "Search for what are the top 10 AI companies?"})

    
    print(response)

if __name__ == "__main__":
    asyncio.run(main())