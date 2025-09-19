import sys
import asyncio
from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langchain_core.messages import HumanMessage

from src.graph.edges import (
    select_workflow,
    should_summarize_conversation,
)
from src.graph.nodes import (
    audio_node,
    context_injection_node,
    conversation_node,
    image_node,
    memory_extraction_node,
    memory_injection_node,
    router_node,
    summarize_conversation_node,
)
from src.graph.state import AgentState


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(AgentState)

    # Add all nodes
    graph_builder.add_node("memory_extraction_node", memory_extraction_node)
    graph_builder.add_node("router_node", router_node)
    graph_builder.add_node("context_injection_node", context_injection_node)
    graph_builder.add_node("memory_injection_node", memory_injection_node)
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("image_node", image_node)
    graph_builder.add_node("audio_node", audio_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)

    graph_builder.add_edge(START, "memory_extraction_node")

    graph_builder.add_edge("memory_extraction_node", "router_node")

    graph_builder.add_edge("router_node", "context_injection_node")
    graph_builder.add_edge("context_injection_node", "memory_injection_node")

    graph_builder.add_conditional_edges("memory_injection_node", select_workflow)

    graph_builder.add_conditional_edges("conversation_node", should_summarize_conversation)
    graph_builder.add_conditional_edges("image_node", should_summarize_conversation)
    graph_builder.add_conditional_edges("audio_node", should_summarize_conversation)
    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder


input_data = {"messages": [HumanMessage(content="who are you")]}

async def main():
    graph = create_workflow_graph().compile()
    result = await graph.ainvoke(input_data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())