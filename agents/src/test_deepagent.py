import asyncio
import os
from typing import Literal
from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents.middleware import wrap_tool_call

from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register

os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://research-phoenix-1:6006/v1/traces"

tracer_provider = register(endpoint="http://research-phoenix-1:6006/v1/traces", project_name="mcp-test")
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

async def main():
    system_prompt = "You are a helpful assistant that performs web search and summarize the search results to answer the user."

    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "http",
                "url": "http://research-mcp-server-1:8000/mcp",
            }
        }
    )
    tools = await client.get_tools()

    agent = create_deep_agent(
        model="openai:gpt-4.1",
        tools= tools,
        system_prompt=system_prompt
    )

    result = await agent.ainvoke({"messages": [{"role": "user", "content": "Find out what are the top 10 AI companies and also do a survey on them to find out which company offers on-prem AI services"}]})

    # Print the agent's response
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())