import os
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from app.tools.filetools import ReadFileTool, WriteFileTool, ListFilesTool


# Define tools
tavily_tool = TavilySearchResults(max_results=5)

# This tool executes code locally, which can be unsafe. Use with caution:
python_repl_tool = PythonREPLTool()

# Ensure the output directory exists
output_dir = "/code/app/projects"
os.makedirs(output_dir, exist_ok=True)
BASE_PATH = output_dir

# Instantiate the tools
read_file_tool_instance = ReadFileTool(base_path=BASE_PATH)
list_files_tool_instance = ListFilesTool(base_path=BASE_PATH)
write_file_tool_instance = WriteFileTool(base_path=BASE_PATH)

# Wrap them in functions so they have __name__ and can be recognized properly
def read_file(file_path: str):
    """Read the contents of a file."""
    return read_file_tool_instance(file_path)

def list_files(directory_path: str = ""):
    """List files in the specified directory."""
    return list_files_tool_instance(directory_path)

def write_file(file_path: str, content: str, render_as_pdf=False):
    """Write content to a specified file."""
    return write_file_tool_instance(file_path, content, render_as_pdf)

# Optional: Wrap these functions using LangChain's Tool if desired
read_file_tool = Tool(
    name="read_file",
    func=read_file,
    description="Reads a file from the base path."
)

list_files_tool = Tool(
    name="list_files",
    func=list_files,
    description="Lists files in the specified directory."
)

class WriteFileArgs(BaseModel):
    file_path: str
    content: str
    render_as_pdf: bool
   
write_file_tool = StructuredTool(
    name="write_file",
    func=write_file,
    description="""
        Writes content to a file. If render_as_pdf is True, the content is treated as LaTeX formatted text and saved as a PDF.
        :param file_path: The relative path to the file from the base directory.
        :param content: The content to write to the file. If render_as_pdf is True, this should include LaTeX formatted mathematical expressions.
        :param render_as_pdf: A boolean indicating whether to render the content as a PDF. Defaults to false.
        :return: A success message if the file is written successfully, or an error message if an error occurs.
        """,
    args_schema=WriteFileArgs
)
