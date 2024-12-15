from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool

# Define tools
tavily_tool = TavilySearchResults(max_results=5)

# This tool executes code locally, which can be unsafe. Use with caution:
python_repl_tool = PythonREPLTool()
