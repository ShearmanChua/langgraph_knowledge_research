from typing import TypedDict, List

class ResearchState(TypedDict):
    query: str
    plan: str
    converstation: int
    notes: List[str]
    sources: List[str]
    draft: str
    final: str
    token_count: int