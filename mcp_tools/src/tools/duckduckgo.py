from ddgs import DDGS

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

logger = logging.getLogger("mcp-search")


def search_duckduckgo(query, max_results=5):
    results = DDGS().text(query, region='us-en', backend="google", max_results=max_results)
    logger.info(f"Search google results for {query}: {results}")
    
    return results
