import functools
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from app.tools.tools import tavily_tool, python_repl_tool
from .state import AgentState

# Function to create an agent
def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

# Function to create an agent node
def agent_node(state: AgentState, agent, name: str):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

# Initialize a base LLM
llm = ChatOpenAI(model="gpt-4o")

# Create specific agents
research_agent = create_agent(llm, [tavily_tool], "You are a web researcher.")
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

review_agent = create_agent(llm, [tavily_tool],
    """You are an senior developer. You excel at code reviews.
    You give detailed and specific actionable feedback.
    You aren't rude, but you don't worry about being polite either.
    Instead you just communicate directly about technical matters.
    """)
review_node = functools.partial(agent_node, agent=review_agent, name="Reviewer")

test_agent = create_agent(
    llm,
    [python_repl_tool],
    "You may generate safe python code to test functions and classes using unittest or pytest.",
)
test_node = functools.partial(agent_node, agent=test_agent, name="QA Tester")

code_agent = create_agent(
    llm,
    [python_repl_tool],
    "You may generate safe python code to analyze data with pandas and generate charts using matplotlib.",
)
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")
