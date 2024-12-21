from langgraph.graph import StateGraph, END
from app.supervisor.supervisor import supervisor_chain, members
from app.agents.agents import research_node, review_node, test_node, code_node
from app.agents.state import AgentState

# Create the workflow
workflow = StateGraph(AgentState)
workflow.add_node("Reviewer", review_node)
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", code_node)
workflow.add_node("supervisor", supervisor_chain)

# Ensure that all workers report back to the supervisor.
for member in members:
    workflow.add_edge(member, "supervisor")

# Define conditional edges
conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)

# Set the entry point
workflow.set_entry_point("supervisor")

# Compile the workflow
graph = workflow.compile()
