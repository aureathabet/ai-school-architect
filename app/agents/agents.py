import functools
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from app.tools.tools import *
from .state import AgentState
from app.prompts import *

# Function to create an agent
def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    if tools is None:
        tools = []
    # Ensure tools are correctly formatted and passed
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools)
    return executor

# Function to create an agent node
def agent_node(state: AgentState, agent, name: str):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

# Initialize a base LLM
llm = ChatOpenAI(model="gpt-4o")

# Create specific agents
research_agent = create_agent(
    llm, 
    [tavily_tool], 
    RESEARCHER_PROMPT
)
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

code_agent = create_agent(
    llm,
    [python_repl_tool, read_file_tool, write_file_tool, list_files_tool],
    MATHS_WRITER_PROMPT,
)
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")

review_agent = create_agent(
    llm, 
    [tavily_tool, list_files_tool, read_file_tool, write_file_tool], 
    MATHS_REVIEWER_PROMPT
)
review_node = functools.partial(agent_node, agent=review_agent, name="Reviewer")

test_agent = create_agent(
    llm,
    [python_repl_tool, read_file_tool, list_files_tool, write_file_tool],
    TEST_AGENT_PROMPT,
)
test_node = functools.partial(agent_node, agent=test_agent, name="Tester")