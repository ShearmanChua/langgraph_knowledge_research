from langchain.messages import AnyMessage
from typing import TypedDict, List
from typing_extensions import Annotated
import operator

class ResearchState(TypedDict):
    query: str
    plan: str
    current_thought: str
    converstation:  Annotated[list[AnyMessage], operator.add]
    compressed_observations: str
    sources: List[str]
    output: str
