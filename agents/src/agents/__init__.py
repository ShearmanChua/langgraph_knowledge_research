"""
LangGraph Research Agent Classes

This module provides agent classes that can be composed into
multi-agent systems using the orchestrator graph.

Available Agents:
- ResearchAgent: Web and academic research
- DataAgent: Database queries and analysis
- GraphAgent: Relationship graph management
"""

from .base import BaseAgent, AgentState
from .research_agent import ResearchAgent
from .data_agent import DataAgent
from .graph_agent import GraphAgent


__all__ = [
    "BaseAgent",
    "AgentState",
    "ResearchAgent",
    "DataAgent",
    "GraphAgent",
]
