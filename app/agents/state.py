from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage

# Define a typed dictionary for agent state
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str
