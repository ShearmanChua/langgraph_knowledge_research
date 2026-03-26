from typing import Callable, Dict
from langgraph.graph import StateGraph, END

from prompts.planning import PLANNING_SYSTEM_PROMPT, PLANNING_PROMPT

# -----------------------------
# 2. Deep Research Agent Class
# -----------------------------

class DeepResearchAgent:
    def __init__(
        self,
        name: str,
        tools: Dict[str, Callable],
        system_prompt: str,
        llm,  # pass in a model object (e.g., ChatOpenAI(...))
        steps_before_reflection: int = 3,
        max_tokens: int = 3000,
    ):
        self.name = name
        self.tools = tools
        self.system_prompt = system_prompt
        self.steps_before_reflection = steps_before_reflection
        self.max_tokens = max_tokens
        self.llm = llm
        self.graph = self._build_graph()
    # -----------------------------
    # Node: Planner
    # -----------------------------
    def planner(self, state: ResearchState):
        prompt = PLANNING_PROMPT.format(query=state["query"])
        
        response = self.llm.predict(prompt)
        steps = [s.strip() for s in response.split("\n") if s.strip()]

        return {
            "plan": steps,
            "step_index": 0
        }

    # -----------------------------
    # Node: Tool Executor
    # -----------------------------
    def executor(self, state: ResearchState):
        step = state["plan"][state["step_index"]]

        results = []
        for tool_name, tool_fn in self.tools.items():
            try:
                output = tool_fn(step)
                results.append(f"[{tool_name}] {output}")
            except Exception as e:
                results.append(f"[{tool_name} ERROR] {e}")

        new_notes = state.get("notes", []) + results
        token_estimate = sum(len(n) for n in new_notes)

        return {
            "notes": new_notes,
            "step_index": state["step_index"] + 1,
            "token_count": token_estimate
        }

    # -----------------------------
    # Node: Reflection
    # -----------------------------
    def reflector(self, state: ResearchState):
        prompt = f"""
        Review the research progress and improve the plan if needed.

        Current Plan: {state['plan']}
        Notes: {state['notes']}
        """
        response = self.llm.predict(prompt)
        updated_plan = state["plan"] + [response]

        return {"plan": updated_plan}

    # -----------------------------
    # Node: Context Compression
    # -----------------------------
    def compressor(self, state: ResearchState):
        prompt = f"""
        Compress the following research notes while preserving key facts:

        {state['notes']}
        """
        compressed = self.llm.predict(prompt)

        return {
            "notes": [compressed],
            "token_count": len(compressed)
        }

    # -----------------------------
    # Node: Final Writer
    # -----------------------------
    def writer(self, state: ResearchState):
        prompt = f"""
        {self.system_prompt}

        Generate a final comprehensive answer:
        Query: {state['query']}
        Notes: {state['notes']}
        """
        final = self.llm.predict(prompt)

        return {"final": final}

    # -----------------------------
    # Routing Logic
    # -----------------------------
    def router(self, state: ResearchState):
        # 1. Check if done
        if state["step_index"] >= len(state["plan"]):
            return "writer"

        # 2. Reflection condition
        if state["step_index"] > 0 and state["step_index"] % self.steps_before_reflection == 0:
            return "reflector"

        # 3. Context compression condition
        if state.get("token_count", 0) > self.max_tokens:
            return "compressor"

        return "executor"

    # -----------------------------
    # Build Graph
    # -----------------------------
    def _build_graph(self):
        graph = StateGraph(ResearchState)

        graph.add_node("planner", self.planner)
        graph.add_node("executor", self.executor)
        graph.add_node("reflector", self.reflector)
        graph.add_node("compressor", self.compressor)
        graph.add_node("writer", self.writer)

        graph.set_entry_point("planner")
        graph.add_edge("planner", "executor")

        graph.add_conditional_edges("executor", self.router)
        graph.add_edge("reflector", "executor")
        graph.add_edge("compressor", "executor")
        graph.add_edge("writer", END)

        return graph.compile()

    # -----------------------------
    # Run Agent
    # -----------------------------
    def run(self, query: str):
        return self.graph.invoke({"query": query})