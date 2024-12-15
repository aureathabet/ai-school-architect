from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_openai import ChatOpenAI

# Define the members and system prompt for the supervisor
members = ["Researcher", "Coder", "Reviewer", "QA Tester"]
system_prompt = (
    f"You are a supervisor tasked with managing a conversation between the"
    f" following workers:  {members}. Given the following user request,"
    f" respond with the worker to act next. Each worker will perform a"
    f" task and respond with their results and status. When finished,"
    f" respond with FINISH."
)

# Define options
options = members + ["FINISH"]

# Define the function for OpenAI function calling
function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {
            "next": {
                "title": "Next",
                "anyOf": [
                    {"enum": options},
                ],
            }
        },
        "required": ["next"],
    },
}

# Create a prompt for the supervisor
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            f"Given the conversation above, who should act next?"
            f" Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# Create the supervisor chain
supervisor_chain = (
    prompt
    | llm.bind_functions(functions=[function_def], function_call="route")
    | JsonOutputFunctionsParser()
)
