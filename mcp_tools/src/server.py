from fastmcp import FastMCP
from tools.duckduckgo import search_duckduckgo

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

logger = logging.getLogger("mcp-search")

# Create MCP server
mcp = FastMCP("search-server")

@mcp.tool(
    name="duckduckgo_search",
    description="Search DuckDuckGo and return max results.",
)
def duckduckgo_search(query: str, max_results: int = 5):
    """
    Search DuckDuckGo and return results.
    """
    results = search_duckduckgo(query, max_results)
    logger.info(f"Search results for {query}: {results}")

    return results


if __name__ == "__main__":
    # Start MCP server
    mcp.run(transport="http",host="0.0.0.0", port=8000)
